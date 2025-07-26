# window.py
#
# Copyright 2025 Nathan Perlman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gtk, Gdk, Gio, GLib
from gettext import gettext as _
import os, shutil, re, random
from .interface_to_shell_theme import parse_gtk_theme

bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
proxy = Gio.DBusProxy.new_sync(
    bus,
    Gio.DBusProxyFlags.NONE,
    None,
    'org.gnome.Shell.Extensions',
    '/org/gnome/Shell/Extensions',
    'org.gnome.Shell.Extensions',
    None
)

def reset_shell():
    proxy.call_sync("DisableExtension",
        GLib.Variant("(s)", ("user-theme@gnome-shell-extensions.gcampax.github.com",)),
        Gio.DBusCallFlags.NONE, -1, None)

    proxy.call_sync("EnableExtension",
        GLib.Variant("(s)", ("user-theme@gnome-shell-extensions.gcampax.github.com",)),
        Gio.DBusCallFlags.NONE, -1, None)

def load_colors_from_css(file_path):
    colors = {}
    define_re = re.compile(r"@define-color\s+(\S+)\s+([^;]+);")
    with open(file_path, "r") as f:
        for line in f:
            match = define_re.search(line)
            if(match):
                name, color = match.groups()
                colors[name] = color.strip()
    return colors

def create_color_thumbnail_button(colors):
    button = Gtk.Button(valign=Gtk.Align.START)
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    flowbox = Gtk.Frame()
    box.append(flowbox)
    color_box = Gtk.Box()

    keys_to_show = ["window_bg_color", "window_fg_color", "card_bg_color", "headerbar_bg_color", "dark_1", "light_1", "red_1", "green_1", "blue_1"]
    for key in keys_to_show:
        color = colors.get(key)
        rand = random.randint(1, 100000)

        if(color):
            color_widget = Gtk.Box(hexpand=True, height_request=40)
            color_widget.add_css_class(f"thumbnail-swatch-{rand}")
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(f"""
                .thumbnail-swatch-{rand} {{
                    background-color: {color};
                }}
            """.encode())
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            color_box.append(color_widget)

    button.set_child(box)
    flowbox.set_child(color_box)
    return button

@Gtk.Template(resource_path='/io/github/swordpuffin/rewaita/window.ui')
class RewaitaWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'RewaitaWindow'

    main_box = Gtk.Template.Child()
    switcher = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        help = Gio.SimpleAction.new(name="help")
        help.connect("activate", self.on_readme_clicked)
        self.add_action(help)

        scroll_box = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.main_box.append(scroll_box)

        self.light_page = self._create_theme_page(_("Light"))
        self.dark_page = self._create_theme_page(_("Dark"))

        stack = Gtk.Stack(transition_type=Gtk.StackTransitionType.SLIDE_LEFT_RIGHT, transition_duration=200)
        self.switcher.set_stack(stack)
        stack.add_titled(self.light_page, "light", _("Light"))
        stack.add_titled(self.dark_page, "dark", _("Dark"))
        for titled in self.switcher: titled.add_css_class("circular")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.append(stack)
        scroll_box.set_child(box)

    def on_readme_clicked(self, button, args):
        dialog = Gtk.MessageDialog(modal=True, buttons=Gtk.ButtonsType.CLOSE, transient_for=self, title=(_("Help")))
        dialog.set_default_size(480, 300)
        info_box = Gtk.Label(margin_start=12, margin_end=12, justify=Gtk.Justification.CENTER, selectable=True, wrap=True, label=_("After setting a color scheme, go to Gnome-Tweaks (or similar) and set 'Rewaita' as your Shell theme. It contains the same colors as the active scheme for continuity\n\nRewaita also does not style parts of apps like Gnome Builder and BlackBox which have their own syntax highlighting system\n\nIf you find a problem with any theme, would like to suggest another be added, or want to submit your own to be included, please make an issue or a pull request @ https://github.com/SwordPuffin/Rewaita"))
        warning_box = Gtk.Button(halign=Gtk.Align.CENTER, child=Gtk.Label(wrap=True, label=_("**Rewaita will only style GTK4 applications; GTK3 support may come later, but any other UI libraries are altogether NOT supported**")))
        warning_box.add_css_class("warning")
        dialog.get_content_area().append(info_box)
        dialog.get_content_area().append(warning_box)
        dialog.connect("response", lambda d, r: dialog.destroy())
        dialog.present()

        command_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER, spacing=8)
        command_label = Gtk.Label(justify=Gtk.Justification.CENTER, label=_("For Flatpak application support, run:"))
        self.entry = Gtk.Entry(halign=Gtk.Align.CENTER, hexpand=True, editable=False, can_focus=True, width_request=390)
        self.entry.set_text("sudo flatpak override --filesystem=xdg-config/gtk-4.0:rw")

        self.copy_button = Gtk.Button.new_from_icon_name("edit-copy-symbolic")
        self.copy_button.set_halign(Gtk.Align.START)
        self.copy_button.set_hexpand(True)
        self.copy_button.set_tooltip_text("Copy to clipboard")
        self.copy_button.connect("clicked", self.on_copy_clicked)
        command_box.append(self.entry)
        command_box.append(self.copy_button)
        dialog.get_content_area().append(command_label)
        dialog.get_content_area().append(command_box)
        self.clipboard = Gdk.Display.get_default().get_clipboard()

    def on_copy_clicked(self, button):
        text = self.entry.get_text()
        self.clipboard.set(text)

        button.add_css_class("success")
        def remove_success():
            button.remove_css_class("success")
        GLib.timeout_add(1000, remove_success)

    template_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gnome-shell-template.css"))
    template_file_content = template_file.read()

    def _create_theme_page(self, theme_type):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        reset_button = Gtk.Button(label=_("Reset"), halign=Gtk.Align.CENTER, margin_top=16)
        reset_button.add_css_class("pill")
        reset_button.connect("clicked", self.on_theme_selected, None, "light")
        page.prepend(reset_button)
        if(theme_type == "Light"):
            themes = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "light"))
            self.light_flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
            flowbox = self.light_flowbox
        else:
            themes = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dark"))
            self.dark_flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
            flowbox = self.dark_flowbox
        theme_type = theme_type.lower()
        emojis = { "Catppuccin-latte": " 🌻", "Catppuccin-frappe": " 🪴", "Catppuccin-mocha": " 🌿", "Dawnfox": " 🦊", "Dracula": " 🧛🏻‍♂️", "Everforest": " 🌲",
                   "Gruvbox-medium": " 🌴", "Gruvbox-soft": " 🌱", "Kanagawa": " 🌊", "Nord": " 🏔️", "Rosepine": " 🌹", "Nightfox": " 🦊",
                   "Solarized": " ☀️", "Tokyonight": " 🗼", "Tokyonight-storm": " 🌪️", "Material-deepocean": " 🐚", "Material-palenight": " 🌙"
        }
        for theme in themes:
            colors = load_colors_from_css(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), theme_type, theme)))
            btn = create_color_thumbnail_button(colors)
            btn.connect("clicked", self.on_theme_selected, theme, theme_type)
            btn.set_css_classes(["title-4", "monospace"])
            text = theme.replace(".css", "").capitalize()
            btn.get_first_child().append(Gtk.Label(margin_bottom=12, margin_top=12, label=text + emojis[text]))
            flowbox.append(btn)

        page.append(Adw.Clamp(maximum_size=850, child=flowbox))
        return page

    def on_theme_selected(self, button, theme_name, theme_type):
        print(f"Theme selected: {theme_name}")
        for flowbox in [self.light_flowbox, self.dark_flowbox]:
            for theme in flowbox: theme.remove_css_class("success")
        config_dir = os.path.join(os.path.expanduser("~/.config"), "gtk-4.0")
        try:
            if(theme_name == None):
                os.remove(os.path.join(config_dir, "gtk.css"))
                return
        except:
            print("File already deleted")
            return

        button.get_parent().add_css_class("success")
        theme_file = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), theme_type), theme_name)
        try:
            shutil.copy(theme_file, os.path.join(config_dir, "gtk.css"))
        except Exception as e:
            print(f"Error moving file: {e}")
        gtk_file = open(theme_file)
        self.toast_overlay.dismiss_all()
        self.toast_overlay.add_toast(Adw.Toast(timeout=3, title=(_("Set Rewaita as shell theme and reboot for full changes"))))
        parse_gtk_theme(gtk_file.read(), self.template_file_content, os.path.join(os.path.dirname(os.path.abspath(__file__)), "gnome-shell-template.css"))
        reset_shell()



