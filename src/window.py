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

import os, shutil, gi, re
gi.require_version('Xdp', '1.0')
from gi.repository import Adw, Gdk, Gio, GLib, Gtk, Xdp
from collections import defaultdict
from .utils import parse_gtk_theme, set_to_default, delete_items, set_gtk3_theme, get_accent_color, add_css_provider
from .custom_theme_page import CustomPage
from .theme_page import ThemePage
from .window_control_box import WindowControlBox

if(GLib.getenv("XDG_CURRENT_DESKTOP") == "GNOME"):
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

@Gtk.Template(resource_path='/io/github/swordpuffin/rewaita/window.ui')
class RewaitaWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'RewaitaWindow'

    main_box = Gtk.Template.Child()
    switcher = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()
    delete_button = Gtk.Template.Child()
    endbox = Gtk.Template.Child()
    extra_css = set()
    window_control_css = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.css")).read())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        if(os.path.exists(os.path.join(GLib.get_user_data_dir(), "prefs.json"))):
            os.remove(os.path.join(GLib.get_user_data_dir(), "prefs.json"))

        if(not os.path.exists(os.path.join(GLib.getenv("HOME"), ".local", "share", "themes"))):
            print("Making gnome shell theme directory")
            os.mkdir(os.path.join(GLib.getenv("HOME"), ".local", "share", "themes"))

        delete = Gio.SimpleAction.new(name="trash")
        delete.connect("activate", delete_items, self.delete_button, self)
        self.add_action(delete)

        if(self.window_control != "default"):
            self.window_control_css = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "window-controls", f"{self.window_control}.css")).read()
        self.portal = Xdp.Portal()
        self.settings = self.portal.get_settings()
        self.pref = self.settings.read_uint("org.freedesktop.appearance", "color-scheme")

        scroll_box = Gtk.ScrolledWindow(hexpand=True)
        self.main_box.append(scroll_box)

        self.controls = self.endbox.get_parent().get_last_child() #Gets the window controls

        self.theme_page = ThemePage(self)
        self.theme_page.append(WindowControlBox(self, self.window_control))
        self.custom_page = CustomPage(self)

        stack = Adw.ViewStack(transition_duration=200, vhomogeneous=False)
        stack.connect("notify::visible-child", self.on_page_changed)
        self.switcher.set_stack(stack)
        stack.add_titled_with_icon(self.theme_page, "settings", _("Theming"), "brush-symbolic")
        stack.add_titled_with_icon(Adw.Clamp(child=self.custom_page, maximum_size=850), "custom", _("Custom"), "hammer-symbolic")

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

    template_file_content = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gnome-shell-template.css")).read()
    gtk3_template_file_content = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gtk3-template", "gtk.css")).read()

    def on_theme_selected(self):
        self.pref = self.settings.read_uint("org.freedesktop.appearance", "color-scheme")
        gtk3_config_dir = os.path.join(os.path.expanduser("~/.config"), "gtk-3.0")
        gtk4_config_dir = os.path.join(os.path.expanduser("~/.config"), "gtk-4.0")
        if(self.pref == 1):
            theme_name = self.dark_theme
            theme_type = "dark"
        else:
            theme_name = self.light_theme
            theme_type = "light"

        self.save_prefs()

        extra_css_string = ""
        for item in self.extra_css:
            extra_css_string += item
        extras = self.window_control_css + extra_css_string

        if(theme_name.lower() == "default"):
            set_to_default([gtk3_config_dir, gtk4_config_dir], theme_type, reset_shell, extras)
            return

        theme_file = os.path.join(self.data_dir, theme_type, theme_name)
        self.controls.set_css_classes([self.window_control])
        gtk_css = open(theme_file).read()
        self.toast_overlay.dismiss_all()
        self.toast_overlay.add_toast(Adw.Toast(timeout=3, title=(_("Change GNOME shell theme to 'Rewaita' and reboot for full changes"))))

        color_pattern = r'@define-color\s+([a-z0-9_]+)\s+(#[a-fA-F0-9]+|@[a-z0-9_]+);'
        references = defaultdict(list)
        colors = dict()

        for match in re.finditer(color_pattern, gtk_css):
            name, value = match.groups()
            if(value.startswith('@')):
                ref_name = value[1:]
                references[ref_name].append(name)
            else:
                colors[name] = value

        for ref_name, dependent_names in references.items():
            if(ref_name in colors):
                for name in dependent_names:
                    colors[name] = colors[ref_name]

        accent_color = get_accent_color(colors.values())
        colors["accent_color"] = accent_color
        extras = "\n" + extras + f"\n@define-color accent_bg_color {accent_color};\n@define-color accent_fg_color @window_bg_color;"

        try:
            shutil.copy(theme_file, os.path.join(gtk4_config_dir, "gtk.css"))
            with open(os.path.join(gtk4_config_dir, "gtk.css"), "a") as file:
                file.write(extras)
        except Exception as e:
            print(f"Error moving file: {e}")

        add_css_provider(open(theme_file).read() + extras, accent_color)
        parse_gtk_theme(
            colors,
            self.template_file_content,
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "gnome-shell-template.css"),
            self.gtk3_template_file_content,
            self.modify_gtk3_theme,
            self.modify_gnome_shell,
            self.app_settings,
            reset_shell
        )

        if(self.modify_gtk3_theme):
            set_gtk3_theme(gtk3_config_dir, self.window_control)

    def on_window_control_clicked(self, button, control_file, window, flowbox):
        if(control_file != "default"):
            self.window_control_css = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "window-controls", f"{control_file}.css")).read()
        else:
            self.window_control_css = ""
        for control in flowbox:
            control_button = control.get_first_child()
            control_button.remove_css_class("active-scheme")

        self.window_control = control_file
        button.add_css_class("active-scheme")
        self.on_theme_selected()

    def on_theme_button_clicked(self, button, theme_name, theme_type):
        if(theme_type == "dark" and theme_name != "Default"):
            self.dark_theme = theme_name
        elif(theme_type == "light" and theme_name != "Default"):
            self.light_theme = theme_name
        elif(theme_type == "dark" and theme_name == "Default"):
            self.dark_theme = "default"
        elif(theme_type == "light" and theme_name == "Default"):
            self.light_theme = "default"

        if(theme_type == "light" and self.pref in [0, 2] or theme_type == "dark" and self.pref == 1):
            self.on_theme_selected()
        else:
            self.save_prefs()
            self.toast_overlay.dismiss_all()
            self.toast_overlay.add_toast(Adw.Toast(timeout=3, title=(_(f"{theme_type.capitalize()} theme set to: {theme_name.replace('.css', '')}"))))

        if(theme_type == "dark"):
            flowbox_type = self.dark_flowbox
        elif(theme_type == "light"):
            flowbox_type = self.light_flowbox

        for flowbox in flowbox_type:
            for theme in flowbox:
                theme.remove_css_class("active-scheme")

        if(button.get_icon_name() != "reload-symbolic"): button.add_css_class("active-scheme")

    def save_prefs(self):
        self.app_settings.set_string("light-theme", self.light_theme)
        self.app_settings.set_string("dark-theme", self.dark_theme)
        self.app_settings.set_string("window-controls", self.window_control)
        self.app_settings.set_boolean("modify-gtk3-theme", self.modify_gtk3_theme)
        self.app_settings.set_boolean("modify-gnome-shell", self.modify_gnome_shell)
        self.app_settings.set_boolean("run-in-background", self.run_in_background)
