# utils.py
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

import gi, os, shutil, json
from gi.repository import Gtk, Gdk, GLib, Xdp, Adw
from .image_modifier import hex_to_rgb, find_closest_color
from .firefox_gnome_theme import FirefoxGnomeThemePlugin

settings = Xdp.Portal().get_settings()
css_provider = Gtk.CssProvider()
firefox_theme_plugin = FirefoxGnomeThemePlugin()

def read_accent_color():
    try:
        accent = settings.read_value("org.freedesktop.appearance", "accent-color")
        converted = tuple(int(x * 255) for x in accent)
        if(any(value < 0 for value in converted) or any(value > 255 for value in converted)):
            converted = (53, 132, 228) # Default Gnome blue
    except Exception:
        converted = (53, 132, 228) # Default Gnome blue
    return converted

def get_accent_color(palette):
    return find_closest_color(read_accent_color(), palette)

def add_css_provider(css, accent_color):
    Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(), css_provider)
    css_provider.load_from_data(f"""
        {css}
        @define-color accent_bg_color {accent_color};
        @define-color accent_fg_color @window_bg_color;
    """.encode())
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )

def parse_gtk_theme(colors, gnome_shell_css, theme_file, gtk3_file, modify_gtk3_theme, modify_gnome_shell, reset_func):
    if(preferences("window", _, "get")):
        colors["border_color"] = colors["accent_color"]
    else:
        colors["border_color"] = 'transparent'

    colors["overview_bg_color"] = colors["window_bg_color"] # overview_bg_color must be opaque
    if(preferences("transparency", _, "get")):
        for color_to_replace in ["window_bg_color", "headerbar_bg_color", "card_bg_color"]:
            rgb = hex_to_rgb(colors[color_to_replace])
            colors[color_to_replace] = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.82)"
        gtk3_file += ".background:not(.nautilus-desktop):not(.desktopwindow) { opacity: 0.95; }"

    if(preferences("light-text", _, "get")):
        colors["search_fg_color"] = "white"
    else:
        colors["search_fg_color"] = colors["window_fg_color"]

    # Panel colors
    colors["panel_bg_color"] = colors["window_bg_color"]
    colors["panel_fg_color"] = colors["window_fg_color"]
    colors["panel_button_bg_color"] = "transparent"
    colors["panel_hover_bg_color"] = colors["card_bg_color"]

    firefox_theme_plugin.variables = colors
    firefox_theme_plugin.window_controls = preferences("window-controls", _, "get")
    firefox_theme_plugin.apply()

    items_to_replace = ["window_bg_color", "window_fg_color", "card_bg_color", "headerbar_bg_color", "accent_color", "border_color", "red_1", "panel_bg_color", "panel_fg_color", "panel_button_bg_color", "panel_hover_bg_color", "overview_bg_color", "search_fg_color"]

    if(modify_gtk3_theme):
        for color in colors.keys():
            gtk3_file = gtk3_file.replace(f"@{color}", colors[color])

        gtk3_theme_file = os.path.join(GLib.getenv("HOME"), ".config", "gtk-3.0", "gtk.css")
        with open(gtk3_theme_file, "w") as file:
            file.write(gtk3_file)

    if(modify_gnome_shell and "GNOME" in GLib.getenv("XDG_CURRENT_DESKTOP")):
        for item in items_to_replace:
            gnome_shell_css = gnome_shell_css.replace(f"@{item}", colors[item])

        gnome_shell_theme_dir = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
        os.makedirs(gnome_shell_theme_dir, exist_ok=True)
        file = shutil.copyfile(theme_file, os.path.join(gnome_shell_theme_dir, "gnome-shell.css"))

        if(preferences("sharp", _, "get")):
            gnome_shell_css += f"\n\n* {{border-radius: 0px;}}"
        with open(file, "w") as f:
            f.write(gnome_shell_css)

        reset_func()

def set_to_default(config_dirs, theme_type, reset_func, extras):
    for config_dir in config_dirs:
        with open(os.path.join(config_dir, "gtk.css"), "w") as file:
            file.write(extras)

    gnome_shell_path = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
    if(os.path.exists(os.path.join(gnome_shell_path, "gnome-shell.css"))):
        os.remove(os.path.join(gnome_shell_path, "gnome-shell.css"))

    gtk_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"default-{theme_type}.css")
    gtk_css = open(gtk_file).read()
    add_css_provider(gtk_css + extras, f"rgb{read_accent_color()}")
    firefox_theme_plugin.reset()
        
    if("GNOME" in GLib.getenv("XDG_CURRENT_DESKTOP")):
        reset_func()

def confirm_delete(dialog, response, button, window):
    if(response == "confirm"):
        window.toast_overlay.dismiss_all()
        # Bear with me through this
        window.toast_overlay.add_toast(Adw.Toast(timeout=3, title=button.theme + _(" has been deleted")))
        button.get_parent().get_parent().remove(button.get_parent())
        os.remove(button.path)

def delete_theme(button, window):
    dialog = Adw.AlertDialog()
    button.theme = button.theme.replace('.css', '')
    dialog.set_heading(_("Delete ") + f"{button.theme}?")
    dialog.set_body(_("Are you sure you want to delete that theme?\nThis cannot be undone."))
    
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("confirm", _("Delete"))
    dialog.set_response_appearance("confirm", Adw.ResponseAppearance.DESTRUCTIVE)

    dialog.connect("response", confirm_delete, button, window)
    dialog.present(window)
    
def delete_items(action, _, button, window):
    if(button.has_css_class("destructive-action")):
        button.remove_css_class("destructive-action")
        for flowbox in [window.light_flowbox, window.dark_flowbox]:
            for theme in flowbox:
                child = theme.get_first_child()
                if(not child.has_css_class("delete-action")):
                    child.set_sensitive(True)
                    window.light_button.set_sensitive(True); window.dark_button.set_sensitive(True);
                    continue
                child.remove_css_class("delete-action"); child.remove_css_class("shake")
                child.disconnect_by_func(delete_theme)
                child.connect("clicked", window.on_theme_button_clicked, child.theme, child.theme_type)
    else:
        button.add_css_class("destructive-action")
        for flowbox in [window.light_flowbox, window.dark_flowbox]:
            for theme in flowbox:
                child = theme.get_first_child()
                if(child.has_css_class("active-scheme") or child.default):
                    child.set_sensitive(False)
                    window.light_button.set_sensitive(False); window.dark_button.set_sensitive(False);
                    continue
                child.add_css_class("delete-action")
                child.add_css_class("shake")
                child.disconnect_by_func(child.func)
                child.connect("clicked", delete_theme, window)

def set_gtk3_theme(gtk3_config_dir, window_control):
    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gtk3-template")
    assets = os.path.join(dir, "assets.tar.xz")
    shutil.unpack_archive(assets, extract_dir=gtk3_config_dir, format="tar")
    if(window_control != "default"):
        window_control_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "window-controls", "gtk3", window_control + ".css")
        with open(os.path.join(gtk3_config_dir, "gtk.css"), "a") as file:
            with open(window_control_file, "r") as css:
                file.write(css.read())


pref_dir = GLib.get_user_data_dir()
pref_file = os.path.join(pref_dir, "prefs.json")

def preferences(key, value, action):
    try:
        def get_value():
            with open(pref_file, "r") as f:
                prefs = json.load(f)
                return prefs[key]

        def save_values():
            with open(pref_file, "w") as f:
                json.dump(value, f, indent=4)

        if(action == "get"):
            return get_value()
        elif(action == "set"):
            change_value()
        elif(action == "save"):
            save_values()
    except:
        defaults = {
            "light-theme": "default",
            "dark-theme": "default",
            "window-controls": "default",
            "modify-gtk3-theme": True,
            "modify-gnome-shell": True,
            "run-in-background": True,
            "transparency": False,
            "window": False,
            "sharp": False,
            "light-text": False,
        }

        with open(pref_file, "w") as f:
            json.dump(defaults, f, indent=4)




