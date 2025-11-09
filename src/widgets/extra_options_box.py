# extra_options_box.py
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

import gi
from gi.repository import Gtk, Gdk, Adw

transparency_css = """
.background {
	opacity: 92%;
}
"""

border_css = """
window {
  border: none;
}

window.csd.maximized, window.csd.fullscreen, window.csd.tiled, window.csd.tiled-top, window.csd.tiled-right, window.csd.tiled-bottom, window.csd.tiled-left {
  border-radius: 0;
  border: none;
  transition: none;
}

window.csd:backdrop {
  transition: box-shadow 75ms cubic-bezier(0, 0, 0.2, 1);
  box-shadow: 0 8px 6px -5px rgba(0, 0, 0, 0.2), 0 16px 15px 2px rgba(0, 0, 0, 0.14), 0 6px 18px 5px rgba(0, 0, 0, 0.12), 0 0 0 2px @accent_bg_color, 0 0 36px transparent;
}

window.csd, window.solid-csd, popover contents, dialog .background {
  transition: none;
  box-shadow: 0 8px 6px -5px rgba(0, 0, 0, 0.2), 0 16px 15px 2px rgba(0, 0, 0, 0.14), 0 6px 18px 5px rgba(0, 0, 0, 0.12), 0 0 0 2px @accent_bg_color, 0 0 36px transparent;
}
"""

sharp_corners_css = """
* {
   border-radius: 0px;
}
"""

class OptionsBox(Gtk.FlowBox):
    def __init__(self, parent):
        super().__init__(halign=Gtk.Align.CENTER, selection_mode=Gtk.SelectionMode.NONE)
        for option, css in zip(["Transparency", "Window borders", "Sharp corners"], [transparency_css, border_css, sharp_corners_css]):
            row = Gtk.Box(height_request=48)
            row.prepend(Gtk.Label(margin_start=12, label=_(option)))
            row.add_css_class("card")

            option = option.split()[0].lower()
            toggle = Gtk.Switch(active=parent.app_settings.get_boolean(option), valign=Gtk.Align.CENTER, hexpand=True, halign=Gtk.Align.END, margin_start=36, margin_end=12)
            toggle.connect("notify::active", self.on_row_toggled, parent, css, option)
            row.append(toggle)
            self.append(row)

            if(parent.app_settings.get_boolean(option)):
                self.set_active_extra_options(parent, css)

    def set_active_extra_options(self, parent, css):
        parent.extra_css.add(css)

    def on_row_toggled(self, switch, args, parent, css, key):
        if(switch.get_active()):
            parent.extra_css.add(css)
        else:
            parent.extra_css.remove(css)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data("""
            .background {
	            opacity: 100%;
            }

            window {
                box-shadow: none;
            }
        """.encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        parent.app_settings.set_boolean(key, switch.get_active())
        parent.on_theme_selected()





