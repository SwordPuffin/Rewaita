# main.py
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

import sys, gi, os, json

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Xdp', '1.0')

from gi.repository import Gtk, Gdk, Gio, Adw, GLib, Xdp, GObject
from .window import RewaitaWindow
from .pref_dialog import PrefDialog

class RewaitaApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id='io.github.swordpuffin.rewaita',
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         resource_base_path='/io/github/swordpuffin/rewaita')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('pref', self.on_pref_clicked)
        self.create_action('guide', self.on_guide_clicked)

        self.add_main_option(
            "background",
            ord("b"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Checks for when the accent color or light/dark mode changes",
            None,
        )

        self.grab_prefs()

    def grab_prefs(self):
        win = RewaitaWindow
        win.app_settings = Gio.Settings.new("io.github.swordpuffin.rewaita")

        win.light_theme = win.app_settings.get_string("light-theme")
        win.dark_theme = win.app_settings.get_string("dark-theme")
        win.window_control = win.app_settings.get_string("window-controls")
        win.modify_gtk3_theme = win.app_settings.get_boolean("modify-gtk3-theme")
        win.modify_gnome_shell = win.app_settings.get_boolean("modify-gnome-shell")
        win.run_in_background = win.app_settings.get_boolean("run-in-background")
        win.transparency = win.app_settings.get_boolean("transparency")
        win.borders = win.app_settings.get_boolean("window")
        win.sharp = win.app_settings.get_boolean("sharp")

    def on_close_request(self, window, *args):
        if(window.run_in_background):
            window.hide()
            return True

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = RewaitaWindow(application=self)

        win.connect("close-request", self.on_close_request)
        win.portal.request_background(
            None,
            "Automatic transitions between light/dark mode",
            None,
            Xdp.BackgroundFlags.ACTIVATABLE,
            None,
            self.on_background_response
        )

        win.present()
        self.settings = Xdp.Portal().get_settings()
        self.settings.connect("changed", self.on_settings_changed, win)

    def on_settings_changed(self, settings, namespace, key, value, win):
        if(namespace == "org.freedesktop.appearance" and key == "color-scheme" or namespace == "org.gnome.desktop.interface" and key == "accent-color"):
            win.on_theme_selected()

    def on_pref_clicked(self, action, _):
        win = self.props.active_window
        if not win:
            win = RewaitaWindow(application=self)
        dialog = PrefDialog(win)
        dialog.present(win)

    def on_guide_clicked(self, action, _):
        builder = Gtk.Builder().new_from_resource('/io/github/swordpuffin/rewaita/widgets/guide_dialog.ui')
        guide_dialog = builder.get_object("GuideDialog")
        guide_dialog.present(parent=self.props.active_window)
        gtk3_entry = builder.get_object("gtk3_entry")
        gtk4_entry = builder.get_object("gtk4_entry")
        self.clipboard = Gdk.Display.get_default().get_clipboard()

        def on_copy(button, entry):
            text = entry.get_text()
            self.clipboard.set(text)

            button.add_css_class("suggested-action")
            def remove_success():
                button.remove_css_class("suggested-action")
            GLib.timeout_add(1000, remove_success)

        builder.get_object("copy_button_gtk3").connect("clicked", on_copy, gtk3_entry)
        builder.get_object("copy_button_gtk4").connect("clicked", on_copy, gtk4_entry)

    def on_background_response(self, portal, result):
        success = portal.request_background_finish(result)
        if(success):
            print("Background permission granted")
            path = os.path.join(GLib.getenv("HOME"), ".config", "autostart")
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, "rewaita.desktop"), "w") as file:
                file.write("""
[Desktop Entry]
Type=Application
Name=io.github.swordpuffin.rewaita
X-XDP-Autostart=io.github.swordpuffin.rewaita
Exec=flatpak run io.github.swordpuffin.rewaita --background
DBusActivatable=true
X-Flatpak=io.github.swordpuffin.rewaita
                """
                )
        else:
            print("Background permission denied")

    def do_command_line(self, args):
        options = args.get_options_dict().end().unpack()
        win = self.props.active_window
        if not win:
            win = RewaitaWindow(application=self)

        self.activate()
        if("background" in options):
            win.emit("close-request")

    def on_about_action(self, *args):
        about = Adw.AboutDialog(application_name='Rewaita',
                                application_icon='io.github.swordpuffin.rewaita',
                                developer_name='Nathan Perlman',
                                version='1.1.0',
                                developers=['Nathan Perlman'],
                                copyright='© 2025 Nathan Perlman')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def main(version):
    app = RewaitaApplication()
    return app.run(sys.argv)

