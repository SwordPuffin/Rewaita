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

import sys, gi, os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Xdp', '1.0')

from gi.repository import Gtk, Gio, Adw, GLib, Xdp
from .window import RewaitaWindow

class RewaitaApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id='io.github.swordpuffin.rewaita',
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         resource_base_path='/io/github/swordpuffin/rewaita')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)

        self.add_main_option(
            "background",
            ord("b"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Checks for when the accent color or light/dark mode changes",
            None,
        )
        
    def on_close_request(self, window, *args):
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
        if(not hasattr(self, "_background_tick_id")):
            self._background_tick_id = GLib.timeout_add_seconds(1, self.background_tick)

    def on_background_response(self, portal, result):
        success = portal.request_background_finish(result)
        if(success):
            print("Background permission granted")
            with open(os.path.join(GLib.getenv("HOME"), ".config", "autostart", "rewaita.desktop"), "w") as file:
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

    def background_tick(self):
        win = self.props.active_window
        if not win:
            win = RewaitaWindow(application=self)
        win.background_service()
        return True

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
                                version='1.0.6',
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


