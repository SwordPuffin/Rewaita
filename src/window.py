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

import os, random, re, shutil, json, gi, subprocess
gi.require_version('Xdp', '1.0')
from gi.repository import Adw, Gdk, Gio, GLib, Gtk, Xdp
from .utils import parse_gtk_theme, set_to_default, delete_items, css
from .custom_theme import CustomPage

on_gnome = True

try:
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
except Exception:
    print("Desktop environment is not Gnome, skip shell integration")
    on_gnome = False

def reset_shell():
    proxy.call_sync("DisableExtension",
        GLib.Variant("(s)", ("user-theme@gnome-shell-extensions.gcampax.github.com",)),
        Gio.DBusCallFlags.NONE, -1, None)

    proxy.call_sync("EnableExtension",
        GLib.Variant("(s)", ("user-theme@gnome-shell-extensions.gcampax.github.com",)),
        Gio.DBusCallFlags.NONE, -1, None)

@Gtk.Template(resource_path='/io/github/swordpuffin/rewaita/window.ui')
class RewaitaWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'RewaitaWindow'

    main_box = Gtk.Template.Child()
    switcher = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    delete_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        #Moves the themes in the app sources to Rewaita's data directory
        if(not os.path.exists(os.path.join(GLib.get_user_data_dir(), "prefs.json"))):
            print("Refreshing themes")
            if(not os.path.exists(os.path.join(GLib.get_user_data_dir(), "light"))):
                shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "light"), os.path.join(GLib.get_user_data_dir(), "light"))
            if(not os.path.exists(os.path.join(GLib.get_user_data_dir(), "dark"))):
                shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dark"), os.path.join(GLib.get_user_data_dir(), "dark"))

        delete = Gio.SimpleAction.new(name="trash")
        delete.connect("activate", delete_items, self.delete_button, self)
        self.add_action(delete)

        self.grab_prefs()
        scroll_box = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.main_box.append(scroll_box)

        self.theme_page = self.create_theme_page()
        self.custom_page = CustomPage(self)

        stack = Gtk.Stack(transition_type=Gtk.StackTransitionType.SLIDE_LEFT_RIGHT, transition_duration=200)
        stack.connect("notify::visible-child", self.on_page_changed)
        self.switcher.set_stack(stack)
        stack.add_titled(self.theme_page, "settings", _("Theming"))
        stack.add_titled(Adw.Clamp(child=self.custom_page, maximum_size=850), "custom", _("Custom"))
        for titled in self.switcher:
            titled.add_css_class("circular")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.append(stack)
        scroll_box.set_child(box)

    light_theme = ""
    dark_theme = ""
    pref = 0
    data_dir = GLib.get_user_data_dir()

    def on_page_changed(self, stack, _):
        if(stack.get_visible_child_name() == "custom"):
            self.delete_button.set_visible(False)
        else:
            self.delete_button.set_visible(True)

    def load_colors_from_css(self, file_path, theme_type):
        colors = {}
        define_re = re.compile(r"@define-color\s+(\S+)\s+([^;]+);")

        with open(file_path, "r") as f:
            for line in f:
                match = define_re.search(line)
                if(match):
                    name, color = match.groups()
                    colors[name] = color.strip()
        return colors

    def create_color_thumbnail_button(self, colors, name):
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

        box.append(Gtk.Label(margin_bottom=12, margin_top=12, label=name.replace(".css", "")))
        button.set_child(box)
        flowbox.set_child(color_box)
        return button

    def grab_prefs(self):
        if(not os.path.exists(f"{self.data_dir}/prefs.json")):
            with open(f"{self.data_dir}/prefs.json", "w") as file:
                json.dump({"light_theme": "default", "dark_theme": "default"}, file, indent=4)

        with open(f"{self.data_dir}/prefs.json", "r") as file:
            data = json.load(file)
            self.light_theme = data["light_theme"]
            self.dark_theme = data["dark_theme"]
        
        self.portal = Xdp.Portal()
        self.settings = self.portal.get_settings()
        self.pref = self.settings.read_uint("org.freedesktop.appearance", "color-scheme")
        if(on_gnome):
            self.accent = self.settings.read_string("org.gnome.desktop.interface", "accent-color")
        self.request_background()

    def request_background(self):
        self.portal.request_background(
            None,
            "Automatic transitions between light/dark mode",
            None,
            Xdp.BackgroundFlags.AUTOSTART | Xdp.BackgroundFlags.ACTIVATABLE,
            None,
            self.on_background_response
        )

    def on_background_response(self, portal, result):
        success = portal.request_background_finish(result)
        if(success):
            print("Background permission granted")
        else:
            print("Background permission denied")

    def background_service(self):
        check_accent_color = False
        
        if(on_gnome): #Will break on non-gnome systems
            check_accent_color = bool(self.settings.read_string("org.gnome.desktop.interface", "accent-color") != self.accent)
            
        if(self.settings.read_uint("org.freedesktop.appearance", "color-scheme") != self.pref or check_accent_color):
            print("background")
            self.pref = self.settings.read_uint("org.freedesktop.appearance", "color-scheme")
            self.accent = self.settings.read_string("org.gnome.desktop.interface", "accent-color")
            if(self.pref == 1):
                self.on_theme_selected(self.dark_theme, "dark")
            elif(self.pref in [0, 2]):
                self.on_theme_selected(self.light_theme, "light")
        print(self.pref)

    def on_readme_clicked(self, button, args):
        dialog = Gtk.MessageDialog(modal=True, buttons=Gtk.ButtonsType.CLOSE, transient_for=self, title=(_("User Guide")))
        dialog.set_default_size(480, 300)
        info_box = Gtk.Label(margin_start=12, margin_end=12, justify=Gtk.Justification.CENTER, selectable=True, wrap=True, label=_("After setting a color scheme, go to Gnome-Tweaks (or similar) and set 'Rewaita' as your Shell theme. It contains the same colors as the active scheme for continuity\n\nRewaita will also run in the background to save the light/dark mode configuration, and will change styles automatically when the color preference is altered. Rewaita also does not style parts of applications like Gnome Builder and BlackBox which have their own syntax highlighting system\n\nIf you find a problem with any theme, would like to suggest another be added, or want to submit your own to be included, please make an issue or a pull request @ https://github.com/SwordPuffin/Rewaita"))
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

        button.add_css_class("suggested-action")
        def remove_success():
            button.remove_css_class("suggested-action")
        GLib.timeout_add(1000, remove_success)

    template_file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gnome-shell-template.css"))
    template_file_content = template_file.read()

    def create_theme_page(self):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        help_button = Gtk.Button(label=_("User Guide"), halign=Gtk.Align.CENTER)
        help_button.add_css_class("pill")
        help_button.connect("clicked", self.on_readme_clicked, None)
        page.prepend(help_button)

        for theme_type in ["light", "dark"]:
            page.append(Adw.Clamp(maximum_size=1200, child=Gtk.Separator(margin_start=20, margin_end=20, margin_top=25)))
            reset_button = Gtk.Button(icon_name="reload-symbolic", tooltip_text=_("Reset to default"))
            reset_button.add_css_class("circular")
            reset_button.connect("clicked", self.on_theme_button_clicked, "Default", theme_type)
            if(theme_type == "light"):
                themes = os.listdir(os.path.join(self.data_dir, "light"))
                self.light_flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
                flowbox = self.light_flowbox
                self.light_button = reset_button
            else:
                themes = os.listdir(os.path.join(self.data_dir, "dark"))
                self.dark_flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
                flowbox = self.dark_flowbox
                self.dark_button = reset_button

            title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER)
            title = Gtk.Label(label=_(theme_type.capitalize()), margin_end=25)
            title.add_css_class("title-2")
            title_box.append(title); title_box.append(reset_button)
            page.append(title_box)

            for theme in sorted(themes):
                colors = self.load_colors_from_css(os.path.join(self.data_dir, theme_type, theme), theme_type)
                btn = self.create_color_thumbnail_button(colors, theme)
                btn.add_css_class("monospace")
                if(theme == self.dark_theme and theme_type == "dark"): btn.add_css_class("suggested-action")
                elif(theme == self.light_theme and theme_type == "light"): btn.add_css_class("suggested-action")
                btn.connect("clicked", self.on_theme_button_clicked, theme, theme_type)

                #Attributes
                btn.path = os.path.join(self.data_dir, theme_type, theme)
                btn.func = self.on_theme_button_clicked
                btn.theme = theme
                btn.theme_type = theme_type

                flowbox.append(btn)
            page.append(Adw.Clamp(maximum_size=850, child=flowbox))
        return page

    def on_theme_button_clicked(self, button, theme_name, theme_type):
        if(theme_type == "dark" and theme_name != "Default"):
            self.dark_theme = theme_name
        elif(theme_type == "light" and theme_name != "Default"):
            self.light_theme = theme_name
        elif(theme_type == "dark" and theme_name == "Default"):
            self.dark_theme = "default"
        elif(theme_type == "light" and theme_name == "Default"):
            self.light_theme = "default"

        with open(f"{self.data_dir}/prefs.json", "w") as file:
            json.dump({"light_theme": self.light_theme, "dark_theme": self.dark_theme}, file, indent=4)

        if(theme_type == "light" and self.pref in [0, 2] or theme_type == "dark" and self.pref == 1):
            self.on_theme_selected(theme_name, theme_type)
        else:
            self.toast_overlay.dismiss_all()
            self.toast_overlay.add_toast(Adw.Toast(timeout=3, title=(_(f"{theme_type.capitalize()} theme set to: {theme_name.replace('.css', '')}"))))

        if(theme_type == "dark"):
            flowbox_type = self.dark_flowbox
        else:
            flowbox_type = self.light_flowbox

        for flowbox in flowbox_type:
            for theme in flowbox:
                theme.remove_css_class("suggested-action")

        if(button.get_icon_name() != "reload-symbolic"): button.add_css_class("suggested-action")

    def on_theme_selected(self, theme_name, theme_type):
        config_dir = os.path.join(os.path.expanduser("~/.config"), "gtk-4.0")
        print(theme_name)

        if(theme_name.lower() == "default"):
            set_to_default(config_dir, theme_type, reset_shell)
            return
        theme_file = os.path.join(self.data_dir, theme_type, theme_name)
        try:
            shutil.copy(theme_file, os.path.join(config_dir, "gtk.css"))
        except Exception as e:
            print(f"Error moving file: {e}")
        gtk_file = open(theme_file)
        self.toast_overlay.dismiss_all()
        self.toast_overlay.add_toast(Adw.Toast(timeout=3, title=(_("Change GNOME shell theme to 'Rewaita' and reboot for full changes"))))
        parse_gtk_theme(gtk_file.read(), self.template_file_content, os.path.join(os.path.dirname(os.path.abspath(__file__)), "gnome-shell-template.css"))
        if(on_gnome):
            reset_shell()

