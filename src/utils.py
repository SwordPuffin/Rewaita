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

import gi, os,  shutil, json
from gi.repository import Gtk, Gdk, Gio, GLib, Xdp, Adw
from pathlib import Path
from .css_templates import no_pill_css, accent_tab_css_gs
from .firefox_gnome_theme import FirefoxGnomeThemePlugin
from .loading_dialog import LoadingDialog

settings = Xdp.Portal().get_settings()
css_provider = Gtk.CssProvider()
firefox_theme_plugin = FirefoxGnomeThemePlugin()
dir = os.path.dirname(os.path.abspath(__file__))

class Preferences:
    DEFAULTS = {
        "light-theme": "default",
        "dark-theme": "default",
        "window-controls": "default",
        "modify-gtk3-theme": True,
        "modify-gnome-shell": True,
        "modify-cinnamon-shell": True,
        "run-in-background": True,
        "transparency": False,
        "window": False,
        "sharp": False,
        "firefox-theme": False,
        "accent-fg": 0,
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

def create_companion_file(companion, main_file, companion_content):
    with open(companion, "w") as file:
        file.write(companion_content)
    companion_name = os.path.basename(companion)
    with open(main_file, "a+") as rf:
        rf.seek(0) # Not really sure why I need this, it doesn't read correctly otherwise
        if(f"@import \"{companion_name}\";" not in rf.read()):
            with open(main_file, "a") as f:
                f.write(f"\n@import \"{companion_name}\";")

def get_accent_color(palette, win):
    accent_map = {
        "'blue'": "blue-1", "'teal'": "blue-2", "'green'": "green-1", "'yellow'": "yellow-1",
        "'orange'": "orange-1", "'red'": "red-1", "'pink'": "purple-1", "'purple'": "purple-2", "'slate'": "dark-1"
    }

    if(win.accent_fg == 3 or win.pref == 1 and win.accent_fg == 1 or win.pref in [0, 2] and win.accent_fg == 2):
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
        window_control_file = os.path.join(dir, "window-controls", "gtk3", window_controls + ".css")
        with open(window_control_file, "r") as wcf:
            css = wcf.read()
    else:
        css = ""
    with open(os.path.join(os.path.expanduser("~/.config"), "gtk-3.0", "rewaita.css"), "a") as file:
        file.write(gtk_css + css)

def rgb_to_hex(rgb):
    r, g, b = (int(round(max(0, min(255, c)))) for c in rgb)
    return f"#{r:02x}{g:02x}{b:02x}"
    
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
def parse_gtk_theme(colors, reset_gnome, reset_cinnamon):
    gnome_theme_file = os.path.join(dir, "gnome-shell-template.css")
    cinnamon_theme_file = os.path.join(dir, "cinnamon-template.css")
    gnome_shell_css = open(gnome_theme_file).read()
    cinnamon_css = open(cinnamon_theme_file).read()
    gtk3_template_file = open(os.path.join(dir, "gtk3-template", "gtk.css")).read()
    gedit_template_file = open(os.path.join(dir, "gedit-template.xml")).read()

    prefs = Preferences()
    all_prefs = prefs.get_all()

    gtksourceview_path = os.path.join(GLib.getenv("HOME"), ".local", "share", "gtksourceview-5", "styles")
    os.makedirs(gtksourceview_path, exist_ok=True)
    with open(os.path.join(gtksourceview_path, "rewaita.xml"), "w") as f:
        f.write(gedit_template_file.format(**colors))

    if(all_prefs["window"]):
        colors["border-color"] = colors["accent-color"]
    else:
        colors["border-color"] = 'transparent'

    colors["overview-bg-color"] = colors["window-bg-color"] # overview_bg_color must be opaque
    if(all_prefs["transparency"]):
        for color_to_replace in ["window-bg-color", "headerbar-bg-color", "card-bg-color"]:
            rgb = hex_to_rgb(colors[color_to_replace])
            colors[color_to_replace] = f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.82)"
        gtk3_template_file += ".background:not(.nautilus-desktop):not(.desktopwindow) { opacity: 0.95; }"

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
            gtk3_template_file = gtk3_template_file.replace(f"@{color}", colors[color])

        if(all_prefs["sharp"]):
            gtk3_template_file += f"\n\n* {{border-radius: 0px;}}\n\n"

        gtk3_theme_file = os.path.join(GLib.getenv("HOME"), ".config", "gtk-3.0", "gtk.css")
        companion_file = os.path.join(GLib.getenv("HOME"), ".config", "gtk-3.0", "rewaita.css")
        create_companion_file(companion_file, gtk3_theme_file, gtk3_template_file)

        main_file_text = Path(gtk3_theme_file).read_text()
        new_text = main_file_text.replace(".titlebutton:", ".break-this-class:")
        Path(gtk3_theme_file).write_text(new_text)

    if(all_prefs["modify-gnome-shell"] and "GNOME" in GLib.getenv("XDG_CURRENT_DESKTOP") or ""):
        for item in items_to_replace:
            gnome_shell_css = gnome_shell_css.replace(f"@{item}", colors[item])

        gnome_shell_theme_dir = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
        os.makedirs(gnome_shell_theme_dir, exist_ok=True)
        g_file = shutil.copyfile(gnome_theme_file, os.path.join(gnome_shell_theme_dir, "gnome-shell.css"))

        if(all_prefs["sharp"]):
            gnome_shell_css += f"\n\n* {{border-radius: 0px !important;}}"

        if(all_prefs["no-pills"]):
            gnome_shell_css += no_pill_css

        with open(g_file, "w") as f:
            f.write(gnome_shell_css)

        reset_gnome()

    if(all_prefs["modify-cinnamon-shell"] and "Cinnamon" in GLib.getenv("XDG_CURRENT_DESKTOP") or ""):
        cinnamon_theme_dir = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "cinnamon")
        os.makedirs(cinnamon_theme_dir, exist_ok=True)
        c_file = shutil.copyfile(cinnamon_theme_file, os.path.join(cinnamon_theme_dir, "cinnamon.css"))
        for item in items_to_replace:
            color = colors[item]
            try:
                if(color.startswith("#")):
                    r, g, b = hex_to_rgb(color)
                elif(color == "transparent"):
                    r, g, b = (0, 0, 0)
                else:
                    r, g, b = color
            except:
                continue

            cinnamon_css = cinnamon_css.replace(f"@{item}-rgb", f"{r}, {g}, {b}")
            cinnamon_css = cinnamon_css.replace(f"@{item}", color)

        if(all_prefs["sharp"]):
            cinnamon_css += f"\n\n* {{border-radius: 0px !important;}}"

        with open(c_file, "w") as f:
            f.write(cinnamon_css)

        reset_cinnamon()

def set_to_default(gtk4_config_dir, theme_type, reset_gnome, reset_cinnamon, extras, modify_gtk3_theme):
    with open(os.path.join(gtk4_config_dir, "gtk.css"), "w") as file:
        file.write(extras[0])

    gnome_shell_path = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
    if(os.path.exists(os.path.join(gnome_shell_path, "gnome-shell.css"))):
        os.remove(os.path.join(gnome_shell_path, "gnome-shell.css"))

    cinnamon_shell_path = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "cinnamon")
    if(os.path.exists(os.path.join(cinnamon_shell_path, "cinnamon.css"))):
        os.remove(os.path.join(cinnamon_shell_path, "cinnamon.css"))

    gtk_file = os.path.join(dir, f"default-{theme_type}.css")
    gtk_css = open(gtk_file).read()
    add_css_provider(gtk_css + extras[0], None)
    firefox_theme_plugin.reset()

    if(modify_gtk3_theme):
        add_gtk3_window_controls(extras[1], gtk_css)
        
    if("GNOME" in GLib.getenv("XDG_CURRENT_DESKTOP") or ""):
        reset_gnome()

    if("Cinnamon" in GLib.getenv("XDG_CURRENT_DESKTOP") or ""):
        reset_cinnamon()

def open_toast(window, message):
    window.toast_overlay.dismiss_all()
    window.toast_overlay.add_toast(Adw.Toast(timeout=3, title=message))
    
def confirm_delete(dialog, response, button, window):
    if(response == "confirm"):
        open_toast(window, button.theme + _(" Has Been Deleted"))
        # Bear with me through this
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
    
def edit_items(action, _, button, window, stack):
    if(button.has_css_class("success")):
        button.remove_css_class("success")
        for flowbox in [window.light_flowbox, window.dark_flowbox]:
            for theme in flowbox:
                child = theme.get_first_child()
                if(not child.has_css_class("success")):
                    child.set_sensitive(True)
                    window.light_button.set_sensitive(True); window.dark_button.set_sensitive(True);
                    continue
                child.remove_css_class("success"); child.remove_css_class("edit-button")
                child.disconnect_by_func(window.custom_page.edit_theme)
                child.connect("clicked", window.on_theme_button_clicked, child.theme, child.theme_type)
    else:
        button.add_css_class("success")
        for flowbox in [window.light_flowbox, window.dark_flowbox]:
            for theme in flowbox:
                child = theme.get_first_child()
                if(child.has_css_class("active-scheme")):
                    child.set_sensitive(False)
                    window.light_button.set_sensitive(False); window.dark_button.set_sensitive(False);
                    continue
                child.add_css_class("success")
                child.add_css_class("edit-button")
                child.disconnect_by_func(child.func)
                child.connect("clicked", window.custom_page.edit_theme, child.path, child.theme, child.theme_type, stack, button)

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

def add_new_theme_button(theme_file, flowbox, on_theme_button_clicked, theme_type):
    from .theme_page import load_colors_from_css, create_color_thumbnail_button
    
    colors = load_colors_from_css(theme_file)
    new_name = os.path.basename(theme_file).replace(".css", "")
    new_button = create_color_thumbnail_button(colors, new_name, flowbox.snippet)
    new_button.connect("clicked", on_theme_button_clicked, new_name + ".css", theme_type)

    # Attributes
    new_button.func = on_theme_button_clicked
    new_button.path = os.path.join(GLib.get_user_data_dir(), theme_type, new_name + ".css")
    new_button.theme_type = theme_type
    new_button.theme = new_name
    new_button.default = False

    already_exists = False
    for existing in flowbox:
        if(existing.get_first_child().theme == new_button.theme):
            already_exists = True

    if(not already_exists):
        flowbox.insert(new_button, -1)
        flowbox.invalidate_sort()

def run_loading_task(parent, task_function, on_success=None):
    spinner = LoadingDialog()
    spinner.present(parent)

    def task_func(task, source_object, task_data, cancellable):
        success_val = task_function()
        if(on_success):
            on_success(success_val)
        task.return_value(success_val)
        
    def on_done(task, _):
        spinner.close()

    task = Gio.Task.new(None, None, on_done)
    task.run_in_thread(task_func)
    
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
