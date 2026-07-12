# main.py
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

import sys, gi, os, re

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Xdp', '1.0')

from gi.repository import Gtk, Gdk, Gio, Adw, GLib, Xdp, GObject
from .utils import Preferences, change_autostart
from .window import RewaitaWindow

class RewaitaApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id='io.github.swordpuffin.rewaita',
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         resource_base_path='/io/github/swordpuffin/rewaita')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('guide', self.on_guide_clicked)

        self.add_main_option(
            "background",
            ord("b"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Checks for when the accent color or light/dark mode changes",
            None,
        )

        self.add_main_option(
            "theme",
            ord("t"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Sets the theme through CLI",
            None,
        )

        self.add_main_option(
            "list",
            ord("l"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.NONE,
            "Lists all available themes",
            None,
        )

        self.grab_prefs()

    def grab_prefs(self):
        win = RewaitaWindow
        prefs = Preferences()
        all_prefs = prefs.get_all()

        try:
            win.light_theme = all_prefs["light-theme"]
            win.dark_theme = all_prefs["dark-theme"]
            win.window_control = all_prefs["window-controls"]
            win.modify_gtk3_theme = all_prefs["modify-gtk3-theme"]
            win.modify_gnome_shell = all_prefs["modify-gnome-shell"]
            win.run_in_background = all_prefs["run-in-background"]
            win.transparency = all_prefs["transparency"]
            win.borders = all_prefs["window"]
            win.sharp = all_prefs["sharp"]
            win.accent_fg = all_prefs["accent-fg"]
            win.accent_tabs = all_prefs["accent-tabs"]
            win.firefox_theme = all_prefs["firefox-theme"]
            win.light_text = all_prefs["light-text"]
            win.dark_panel = all_prefs["dark-panel"]
            win.trans_panel = all_prefs["trans-panel"]
            win.no_pills = all_prefs["no-pills"]
            win.accent = all_prefs["accent"]
        except:
            prefs.make_file()
            self.grab_prefs()

    def on_close_request(self, window, *args):
        if(window.run_in_background):
            window.hide()
            return True

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = RewaitaWindow(application=self)

        win.connect("close-request", self.on_close_request)
        if(win.run_in_background):
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

    def on_guide_clicked(self, action, _):
        builder = Gtk.Builder().new_from_resource('/io/github/swordpuffin/rewaita/widgets/guide_dialog.ui')
        guide_dialog = builder.get_object("GuideDialog")
        guide_dialog.present(parent=self.props.active_window)
        self.clipboard = Gdk.Display.get_default().get_clipboard()

        def on_copy(button, entry):
            text = entry.get_text()
            self.clipboard.set(text)

            button.add_css_class("suggested-action")
            def remove_success():
                button.remove_css_class("suggested-action")
            GLib.timeout_add(1000, remove_success)

        builder.get_object("copy_button_gtk3").connect("clicked", on_copy, builder.get_object("gtk3_entry"))
        builder.get_object("copy_button_gtk4").connect("clicked", on_copy, builder.get_object("gtk4_entry"))
        builder.get_object("copy_button_fp").connect("clicked", on_copy, builder.get_object("fp_entry"))
        builder.get_object("copy_button_ln").connect("clicked", on_copy, builder.get_object("ln_entry"))

    def on_background_response(self, portal, result):
        success = portal.request_background_finish(result)
        if(success):
            print("Background permission granted")
        else:
            print("Background permission denied")
        change_autostart(success)

    def do_command_line(self, args):
        options = args.get_options_dict().end().unpack()
        win = self.props.active_window
        if not win:
            win = RewaitaWindow(application=self)

        self.activate()

        if("background" in options):
            win.emit("close-request")

        theme_type = "light" if win.pref in [0, 2] else "dark"

        if("theme" in options):
            for arg in sys.argv: # For whatever reason, options doesn't include the value of --theme=, just that it is a flag'
                if("--theme=" in arg):
                    theme = arg.split("=")[1]
                    self.set_theme(win, theme, theme_type)
                    sys.exit(0)

        if("list" in options):
            print(list(map(self.adjust_theme_name, os.listdir(os.path.join(win.data_dir, theme_type)))))
            sys.exit(0)

    def adjust_theme_name(self, theme_name):
        emoji_pattern = re.compile(r"[\s\u200d\ufe0f]*[\U00010000-\U0010FFFF\u2600-\u2B55]+[\s\u200d\ufe0f]*", flags=re.UNICODE)
        new_theme_name = emoji_pattern.sub('', theme_name).replace(" ", "-").replace(".css", "").lower()
        return new_theme_name

    def set_theme(self, win, theme_name, theme_type):
        theme_files = os.listdir(os.path.join(win.data_dir, theme_type))
        comparison_name = theme_name

        for theme in theme_files:
            adjusted_name = self.adjust_theme_name(theme)
            if(adjusted_name == comparison_name):
                win.on_theme_button_clicked(None, theme, theme_type)
                return
        print(f"Theme: {theme_name}, was not found\nUse --list to get all available themes")

    def on_about_action(self, *args):
        about = Adw.AboutDialog(application_name='Rewaita',
                                application_icon='io.github.swordpuffin.rewaita',
                                developer_name='Nathan Perlman',
                                version='1.1.2',
                                developers=['Nathan Perlman'],
                                copyright='© 2026 Nathan Perlman')
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
