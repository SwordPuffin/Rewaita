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

import re, gi, os, shutil
from collections import defaultdict
from gi.repository import Gtk, Gdk, GLib, Xdp, Adw, Gio

def get_accent_color():
    settings = Xdp.Portal().get_settings()

    try:
        accent = settings.read_string("org.gnome.desktop.interface", "accent-color")
    except:
        accent = "blue" #Pass through for the time being
    match(accent):
        case("blue"):
            accent_color = "blue_1"
        case("teal"):
            accent_color = "blue_2"
        case("green"):
            accent_color = "green_1"
        case("yellow"):
            accent_color = "yellow_1"
        case("orange"):
            accent_color = "orange_1"
        case("red"):
            accent_color = "red_1"
        case("pink"):
            accent_color = "purple_1"
        case("purple"):
            accent_color = "purple_2"
        case("slate"):
            accent_color = "light_5"

    return accent_color

def add_css_provider(css):
    accent_color = get_accent_color()
    css_provider = Gtk.CssProvider()

    css_provider.load_from_data(f"""
        {css}
        @define-color accent_bg_color @{accent_color};
        @define-color accent_fg_color @window_bg_color;
    """.encode())
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )

    return accent_color

def parse_gtk_theme(gtk_css, gnome_shell_css, theme_file, gtk3_file, modify_gtk3_theme, modify_gnome_shell, reset_func):
    color_pattern = r'@define-color\s+([a-z0-9_]+)\s+(#[a-fA-F0-9]+|@[a-z0-9_]+);'
    colors = dict()
    references = defaultdict(list)
    accent_color = add_css_provider(gtk_css)

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
    colors["accent_color"] = colors[accent_color]
    items_to_replace = ["window_bg_color", "window_fg_color", "card_bg_color", "headerbar_bg_color", "accent_color", "red_1"]

    if(modify_gtk3_theme):
        for color in colors.keys():
            gtk3_file = gtk3_file.replace(f"@{color}", colors[color])

        gtk3_theme_file = os.path.join(GLib.getenv("HOME"), ".config", "gtk-3.0", "gtk.css")
        with open(gtk3_theme_file, "w") as file:
            file.write(gtk3_file)

    if(modify_gnome_shell and GLib.getenv("XDG_CURRENT_DESKTOP") == "GNOME"):
        for item in items_to_replace:
            gnome_shell_css = gnome_shell_css.replace(item, colors[item])

        gnome_shell_theme_dir = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
        os.makedirs(gnome_shell_theme_dir, exist_ok=True)
        file = shutil.copyfile(theme_file, os.path.join(gnome_shell_theme_dir, "gnome-shell.css"))
        with open(file, "w") as f:
            f.write(gnome_shell_css)

        reset_func()


def set_to_default(config_dirs, theme_type, reset_func, window_control_css):
    for config_dir in config_dirs:
        with open(os.path.join(config_dir, "gtk.css"), "w") as file:
            file.write(window_control_css)

    gnome_shell_path = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
    if(os.path.exists(os.path.join(gnome_shell_path, "gnome-shell.css"))):
        os.remove(os.path.join(gnome_shell_path, "gnome-shell.css"))

    gtk_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"default-{theme_type}.css")
    gtk_css = open(gtk_file).read()
    add_css_provider(gtk_css)
    reset_func()

def confirm_delete(dialog, response, button, window):
    #Bear with me through the get_first_childs, get_last_childs, and get_parents
    if(response == "confirm"):
        window.toast_overlay.dismiss_all()
        window.toast_overlay.add_toast(Adw.Toast(timeout=3, title=button.get_first_child().get_last_child().get_label() + _(" has been deleted")))
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
                if(child.has_css_class("suggested-action")):
                    child.set_sensitive(True)
                    window.light_button.set_sensitive(True); window.dark_button.set_sensitive(True);
                    continue
                child.remove_css_class("destructive-action"); child.remove_css_class("shake")
                child.disconnect_by_func(delete_theme)
                child.connect("clicked", window.on_theme_button_clicked, child.theme, child.theme_type)
    else:
        button.add_css_class("destructive-action")
        for flowbox in [window.light_flowbox, window.dark_flowbox]:
            for theme in flowbox:
                child = theme.get_first_child()
                if(child.has_css_class("suggested-action")):
                    child.set_sensitive(False)
                    window.light_button.set_sensitive(False); window.dark_button.set_sensitive(False);
                    continue
                child.add_css_class("destructive-action")
                child.add_css_class("shake")
                child.add_css_class("monospace")
                child.disconnect_by_func(child.func)
                child.connect("clicked", delete_theme, window)

def set_gtk3_theme(gtk3_config_dir, window_control):
    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gtk3-template")
    for item in os.listdir(dir):
        if(os.path.isdir(os.path.join(dir, item))):
            shutil.copytree(os.path.join(dir, item), os.path.join(gtk3_config_dir, item), copy_function=shutil.copyfile, dirs_exist_ok=True)

    with open(os.path.join(gtk3_config_dir, "gtk.css"), "a") as file:
        if(window_control == "colored"):
            file.write("""
                button.minimize.titlebutton:not(.suggested-action):not(.destructive-action) {
                  background: alpha(@yellow_1,0.1);
                  color: @yellow_1;
                }

                button.minimize.titlebutton:backdrop:not(.suggested-action):not(.destructive-action) {
                  color: shade(@yellow_1,0.5);
                }

                button.maximize.titlebutton:not(.suggested-action):not(.destructive-action) {
                  background: alpha(@green_1,0.1);
                  color: @green_1;
                }

                button.maximize.titlebutton:backdrop:not(.suggested-action):not(.destructive-action) {
                  color: shade(@green_1,0.5);
                }

                button.close.titlebutton:not(.suggested-action):not(.destructive-action) {
                  background: alpha(@red_1,0.1);
                  color: @red_1;
                }

                button.close.titlebutton:backdrop:not(.suggested-action):not(.destructive-action) {
                  color: shade(@red_1,0.5);
                }
            """)
        elif(window_control == "macos"):
            file.write("""
                button.minimize.titlebutton:not(.suggested-action):not(.destructive-action) {
                  background-color: @yellow_1;
                  min-width: 16px;
                  min-height: 16px;
                  color: transparent;
                }

                button.minimize.titlebutton:active:not(.suggested-action):not(.destructive-action) {
                  background-color: shade(@yellow_1, 0.8);
                }

                button.maximize.titlebutton:not(.suggested-action):not(.destructive-action) {
                  background-color: @green_1;
                  min-width: 16px;
                  min-height: 16px;
                  color: transparent;
                }

                button.maximize.titlebutton:active:not(.suggested-action):not(.destructive-action) {
                  background-color: shade(@green_1, 0.8);
                }

                button.close.titlebutton:not(.suggested-action):not(.destructive-action) {
                  background-color: @red_1;
                  min-width: 16px;
                  min-height: 16px;
                  color: transparent;
                }

                button.close.titlebutton:active:not(.suggested-action):not(.destructive-action) {
                  background-color: shade(@red_1, 0.8);
                }

                button.minimize.titlebutton:backdrop:not(.suggested-action):not(.destructive-action), button.maximize.titlebutton:backdrop:not(.suggested-action):not(.destructive-action), button.close.titlebutton:backdrop:not(.suggested-action):not(.destructive-action) {
                  color: transparent;
                }

                button.minimize.titlebutton:backdrop:hover:not(.suggested-action):not(.destructive-action), button.minimize.titlebutton:backdrop:active:not(.suggested-action):not(.destructive-action), button.maximize.titlebutton:backdrop:hover:not(.suggested-action):not(.destructive-action), button.maximize.titlebutton:backdrop:active:not(.suggested-action):not(.destructive-action), button.close.titlebutton:backdrop:hover:not(.suggested-action):not(.destructive-action), button.close.titlebutton:backdrop:active:not(.suggested-action):not(.destructive-action),
                button.maximize.titlebutton:hover:not(.suggested-action):not(.destructive-action), button.close.titlebutton:hover:not(.suggested-action):not(.destructive-action),
                button.minimize.titlebutton:hover:not(.suggested-action):not(.destructive-action) {
                  color: @window_bg_color;
                }
            """
            )

css = """
    .shake {
        animation: shake_animation 0.4s ease-in-out infinite;
    }

    textview {
        background-color: @card_bg_color;
        color: @window_fg_color;
        border-radius: 6px;
        font-family: "Fira Code", monospace;
        font-size: 12pt;
    }

    gutter {
        background-color: @headerbar_bg_color;
        color: @window_fg_color;
    }

    @keyframes shake_animation {
      0%   { transform: rotate(-0.75deg); }
      25%  { transform: rotate(0.75deg); }
      50%  { transform: rotate(-0.75deg); }
      75%  { transform: rotate(0.75deg); }
      100% { transform: rotate(-0.75deg); }
    }

    windowcontrols.colored > button.minimize > image {
        color: @yellow_1;
    }

    windowcontrols.colored > button.maximize > image {
        color: @green_1;
    }

    windowcontrols.colored > button.close > image {
        color: @red_1;
    }

    windowcontrols.macos > button:not(.suggested-action):not(.destructive-action) {
      margin-left: 0px;
      margin-right: 0px;
      margin-top: 6px;
      margin-bottom: 2px;
    }

    windowcontrols.macos > button.minimize:not(.suggested-action):not(.destructive-action), windowcontrols.macos > button.maximize:not(.suggested-action):not(.destructive-action), windowcontrols.macos> button.close:not(.suggested-action):not(.destructive-action) {
      color: transparent;
      background: none;
    }

    windowcontrols.macos > button.minimize:hover:not(.suggested-action):not(.destructive-action), windowcontrols.macos > button.minimize:active:not(.suggested-action):not(.destructive-action), windowcontrols.macos> button.maximize:hover:not(.suggested-action):not(.destructive-action), windowcontrols.macos> button.maximize:active:not(.suggested-action):not(.destructive-action), windowcontrols.macos> button.close:hover:not(.suggested-action):not(.destructive-action), windowcontrols.macos > button.close:active:not(.suggested-action):not(.destructive-action) {
      box-shadow: none;
    }

    windowcontrols.macos > button.minimize:active:not(.suggested-action):not(.destructive-action) > image, windowcontrols.macos > button.maximize:active:not(.suggested-action):not(.destructive-action) > image, windowcontrols.macos> button.close:active:not(.suggested-action):not(.destructive-action) > image {
      box-shadow: inset 0 0 100px 100px rgba(0, 0, 0, 0.6);
      transition-duration: 350ms;
      transition-timing-function: ease;
    }

    windowcontrols.macos > button.minimize:hover:not(.suggested-action):not(.destructive-action), windowcontrols.macos> button.minimize:active:not(.suggested-action):not(.destructive-action), windowcontrols.macos> button.maximize:hover:not(.suggested-action):not(.destructive-action), windowcontrols.macos> button.maximize:active:not(.suggested-action):not(.destructive-action), windowcontrols.macos> button.close:hover:not(.suggested-action):not(.destructive-action), windowcontrols.macos> button.close:active:not(.suggested-action):not(.destructive-action) {
      color: @window_bg_color;
    }

    windowcontrols.macos > button.minimize:not(.suggested-action):not(.destructive-action) > image {
      background-color: @yellow_1;
    }

    windowcontrols.macos > button.minimize:active:not(.suggested-action):not(.destructive-action) > image {
      background-color: @yellow_1;
    }

    windowcontrols.macos > button.maximize:not(.suggested-action):not(.destructive-action) > image {
      background-color: @green_1;
    }

    windowcontrols.macos > button.maximize:active:not(.suggested-action):not(.destructive-action) > image {
      background-color: @green_1;
    }

    windowcontrols.macos > button.close:not(.suggested-action):not(.destructive-action) > image {
      background-color: @red_1;
    }

    windowcontrols.macos > button.close:active:not(.suggested-action):not(.destructive-action) > image {
      background-color: @red_1;
    }

    windowcontrols.macos {
      border-spacing: 6px;
    }

    windowcontrols.macos:not(.empty).start:dir(ltr), windowcontrols.macos:not(.empty).end:dir(rtl) {
      margin-right: 6px;
      margin-left: 6px;
    }

    windowcontrols.macos:not(.empty).start:dir(rtl), windowcontrols.macos:not(.empty).end:dir(ltr) {
      margin-left: 6px;
      margin-right: 6px;
    }

    windowcontrols.macos > button:not(.suggested-action):not(.destructive-action) > image {
      border-radius: 100%;
      min-width: 17px;
      min-height: 17px;
      padding: 0;
    }

    windowcontrols.macos > button.minimize:backdrop:not(.suggested-action):not(.destructive-action) > image, windowcontrols.macos > button.maximize:backdrop:not(.suggested-action):not(.destructive-action) > image, windowcontrols.macos > button.close:backdrop:not(.suggested-action):not(.destructive-action) > image, windowcontrols.macos > button.minimize:backdrop:hover:not(.suggested-action):not(.destructive-action), windowcontrols.macos > button.minimize:backdrop:active:not(.suggested-action):not(.destructive-action), windowcontrols.macos > button.maximize:backdrop:hover:not(.suggested-action):not(.destructive-action), windowcontrols.macos > button.maximize:backdrop:active:not(.suggested-action):not(.destructive-action), windowcontrols.macos > button.close:backdrop:hover:not(.suggested-action):not(.destructive-action), windowcontrols.macos > button.close:backdrop:active:not(.suggested-action):not(.destructive-action) {
        opacity: 0.7;
    }

    windowcontrols.macos > button {
      min-height: 17px;
      min-width: 17px;
      padding: 2px;
    }
"""

