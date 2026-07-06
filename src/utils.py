# utils.py
#
# Copyright 2026 Nathan Perlman
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
from .image_modifier import hex_to_rgb
from .firefox_gnome_theme import FirefoxGnomeThemePlugin

settings = Xdp.Portal().get_settings()
css_provider = Gtk.CssProvider()
firefox_theme_plugin = FirefoxGnomeThemePlugin()

no_pill_css = """
#panel .panel-button, .search-entry, .clock {
  border-radius: 12px;
}

.quick-toggle, .quick-toggle-has-menu {
  border-radius: 12px;
}

.quick-toggle-has-menu .quick-toggle {
  min-width: auto;
  max-width: auto;
}

.quick-toggle-has-menu .quick-toggle:ltr {
  border-radius: 12px 0 0 12px;
}

.quick-toggle-has-menu .quick-toggle:rtl {
  border-radius: 0 12px 12px 0;
}

.quick-toggle-has-menu .quick-toggle:ltr:last-child {
  border-radius: 12px;
}

.quick-toggle-has-menu .quick-toggle:rtl:last-child {
  border-radius: 12px;
}

.quick-toggle-has-menu .quick-toggle-menu-button:ltr {
  border-radius: 0 12px 12px 0;
}

.quick-toggle-has-menu .quick-toggle-menu-button:rtl {
  border-radius: 12px 0 0 12px;
}
"""

accent_tab_css_gs = """
#panel .panel-button:hover, .clock:hover,
#panel .panel-button:active, .clock:active{
  color: @accent-color !important;
}
"""

class Preferences:
    DEFAULTS = {
        "light-theme": "default",
        "dark-theme": "default",
        "window-controls": "default",
        "modify-gtk3-theme": True,
        "modify-gnome-shell": True,
        "run-in-background": True,
        "transparency": False,
        "window": False,
        "sharp": False,
        "firefox-theme": False,
        "accent-fg": False,
        "accent-tabs": False,
        "light-text": False,
        "dark-panel": False,
        "trans-panel": False,
        "no-pills": False,
        "accent": "'blue'"
    }

    def __init__(self):
        self.pref_dir = GLib.get_user_data_dir()
        self.pref_file = os.path.join(self.pref_dir, "prefs.json")
        self.make_file()

    def make_file(self):
        if(not os.path.exists(self.pref_file)):
            self.save(self.DEFAULTS)

    def get(self, key):
        try:
            with open(self.pref_file, "r") as f:
                prefs = json.load(f)
                return prefs.get(key, self.DEFAULTS.get(key))
        except:
            self.make_file()
            return self.DEFAULTS.get(key)

    def set(self, key, value):
        try:
            with open(self.pref_file, "r") as f:
                prefs = json.load(f)
        except:
            prefs = dict(self.DEFAULTS)

        prefs[key] = value
        self.save(prefs)

    def save(self, data):
        os.makedirs(self.pref_dir, exist_ok=True)
        with open(self.pref_file, "w") as f:
            json.dump(data, f, indent=4)

    def get_all(self):
        try:
            with open(self.pref_file, "r") as f:
                return json.load(f)
        except:
            self.make_file()
            return dict(self.DEFAULTS)

def get_accent_color(palette, win):
    accent_map = {
        "'blue'": "blue-1", "'teal'": "blue-2", "'green'": "green-1", "'yellow'": "yellow-1",
        "'orange'": "orange-1", "'red'": "red-1", "'pink'": "purple-1", "'purple'": "purple-2", "'slate'": "dark-1"
    }

    if(win.accent_fg):
        accent_fg = "#EEEEEE"
    else:
        accent_fg = "#222222"

    if("GNOME" in GLib.getenv("XDG_CURRENT_DESKTOP") or ""):
        accent = settings.read_value("org.gnome.desktop.interface", "accent-color")
        return (palette[accent_map[str(accent)]], accent_fg)
    else:
        return (palette[accent_map[win.accent]], accent_fg)

def add_css_provider(css, accent_colors):
    Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(), css_provider)
    if(accent_colors is not None):
        css += f"\n:root {{ --accent-bg-color: {accent_colors[0]};\n--accent-fg-color: {accent_colors[1]};\n}}"
    css_provider.load_from_data(f"""
        {css}
    """.encode())
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )

def add_gtk3_window_controls(window_controls, gtk_css):
    if(window_controls != "default"):
        window_control_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "window-controls", "gtk3", window_controls + ".css")
        with open(window_control_file, "r") as wcf:
            css = wcf.read()
    else:
        css = ""
    with open(os.path.join(os.path.expanduser("~/.config"), "gtk-3.0", "gtk.css"), "a") as file:
        file.write(gtk_css + css)

def parse_gtk_theme(colors, gnome_shell_css, theme_file, gtk3_file, reset_func):
    prefs = Preferences()
    all_prefs = prefs.get_all()

    if(all_prefs["window"]):
        colors["border-color"] = colors["accent-color"]
    else:
        colors["border-color"] = 'transparent'

    colors["overview-bg-color"] = colors["window-bg-color"] # overview_bg_color must be opaque
    if(all_prefs["transparency"]):
        for color_to_replace in ["window-bg-color", "headerbar-bg-color", "card-bg-color"]:
            rgb = hex_to_rgb(colors[color_to_replace])
            colors[color_to_replace] = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.82)"
        gtk3_file += ".background:not(.nautilus-desktop):not(.desktopwindow) { opacity: 0.95; }"

    if(all_prefs["light-text"]):
        colors["search-fg-color"] = "white"
    else:
        colors["search-fg-color"] = colors["window-fg-color"]

    if(all_prefs["accent-tabs"]):
        gnome_shell_css += accent_tab_css_gs

    if(not all_prefs["dark-panel"] and not all_prefs["trans-panel"]):
        colors["panel-bg-color"] = colors["window-bg-color"]
        colors["panel-fg-color"] = colors["window-fg-color"]

    if(all_prefs["trans-panel"]):
        colors["panel-bg-color"] = "transparent"
        colors["panel-fg-color"] = "white"

    if(all_prefs["dark-panel"]):
        colors["panel-bg-color"] = "black"
        colors["panel-fg-color"] = "white"

    rgb = hex_to_rgb(colors["accent-color"])
    colors["accent-transparent"] = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.5)"

    if(all_prefs["firefox-theme"]):
        firefox_theme_plugin.variables = colors
        firefox_theme_plugin.window_controls = all_prefs["window-controls"]
        firefox_theme_plugin.apply()
    else:
        firefox_theme_plugin.reset()

    items_to_replace = ["window-bg-color", "window-fg-color", "card-bg-color", "headerbar-bg-color",
                        "accent-color", "border-color", "red-1", "panel-bg-color", "panel-fg-color",
                        "overview-bg-color", "search-fg-color", "accent-transparent", "accent-fg-color"]

    if(all_prefs["modify-gtk3-theme"]):
        for color in colors.keys():
            gtk3_file = gtk3_file.replace(f"@{color}", colors[color])

        if(all_prefs["sharp"]):
            gtk3_file += f"\n\n* {{border-radius: 0px;}}\n\n"

        gtk3_theme_file = os.path.join(GLib.getenv("HOME"), ".config", "gtk-3.0", "gtk.css")
        with open(gtk3_theme_file, "w") as file:
            file.write(gtk3_file)

    if(all_prefs["modify-gnome-shell"] and "GNOME" in GLib.getenv("XDG_CURRENT_DESKTOP") or ""):
        for item in items_to_replace:
            gnome_shell_css = gnome_shell_css.replace(f"@{item}", colors[item])

        gnome_shell_theme_dir = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
        os.makedirs(gnome_shell_theme_dir, exist_ok=True)
        file = shutil.copyfile(theme_file, os.path.join(gnome_shell_theme_dir, "gnome-shell.css"))

        if(all_prefs["sharp"]):
            gnome_shell_css += f"\n\n* {{border-radius: 0px !important;}}"

        if(all_prefs["no-pills"]):
            gnome_shell_css += no_pill_css

        with open(file, "w") as f:
            f.write(gnome_shell_css)

        reset_func()

def set_to_default(gtk4_config_dir, theme_type, reset_func, extras, modify_gtk3_theme):
    with open(os.path.join(gtk4_config_dir, "gtk.css"), "w") as file:
        file.write(extras[0])

    gnome_shell_path = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
    if(os.path.exists(os.path.join(gnome_shell_path, "gnome-shell.css"))):
        os.remove(os.path.join(gnome_shell_path, "gnome-shell.css"))

    gtk_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"default-{theme_type}.css")
    gtk_css = open(gtk_file).read()
    add_css_provider(gtk_css + extras[0], None)
    firefox_theme_plugin.reset()

    if(modify_gtk3_theme):
        add_gtk3_window_controls(extras[1], gtk_css)
        
    if("GNOME" in GLib.getenv("XDG_CURRENT_DESKTOP") or ""):
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
    dialog.set_heading(_("Delete") + f" {button.theme}?")
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

def change_autostart(state):
    if(state == False):
        path = os.path.join(GLib.getenv("HOME"), ".config", "autostart", "rewaita.desktop")
        if(os.path.exists(path)):
            os.remove(path)
    else:
        with open(os.path.join(GLib.getenv("HOME"), ".config", "autostart", "rewaita.desktop"), "w") as file:
            if(Xdp.Portal().running_under_flatpak()):
                command = "flatpak run io.github.swordpuffin.rewaita --background"
            else:
                command = "rewaita --background"
            file.write(f"""
[Desktop Entry]
Type=Application
Name=io.github.swordpuffin.rewaita
X-XDP-Autostart=io.github.swordpuffin.rewaita
Exec={command}
DBusActivatable=true
X-Flatpak=io.github.swordpuffin.rewaita
                """)
