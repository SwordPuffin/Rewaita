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

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, GLib
from .window import RewaitaWindow

class RewaitaApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id='io.github.swordpuffin.rewaita',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/io/github/swordpuffin/rewaita')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = RewaitaWindow(application=self)
        win.present()
        GLib.timeout_add_seconds(1, self.background_tick, win)
        loop = GLib.MainLoop()
        loop.run()

    def background_tick(self, win):
        win.background_service()
        return True

    # def do_command_line(self, command_line):
    #     args = command_line.get_arguments()
    #     win = self.props.active_window
    #     if(not win):
    #         win = RewaitaWindow(application=self)
    #     if("--background" not in args):
    #         self.activate()
    #     return 0

    def on_about_action(self, *args):
        about = Adw.AboutDialog(application_name='Rewaita',
                                application_icon='io.github.swordpuffin.rewaita',
                                developer_name='Nathan Perlman',
                                version='1.0.1',
                                developers=['Nathan Perlman'],
                                copyright='© 2025 Nathan Perlman')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = RewaitaApplication()
    return app.run(sys.argv)
