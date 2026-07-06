# extra_options_box.py
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

import gi
from gi.repository import Gtk, Adw, GLib
from .utils import Preferences

transparency_css = """
.background {
	opacity: 0.92;
}
"""

border_css = """
window {
  border: none;
}

window.csd.maximized, window.csd.fullscreen, window.csd.tiled,
window.csd.tiled-top, window.csd.tiled-right, window.csd.tiled-bottom,
window.csd.tiled-left {
  border-radius: 0;
  border: none;
  transition: none;
}

window.csd:backdrop {
  transition: box-shadow 75ms cubic-bezier(0, 0, 0.2, 1);
  box-shadow: 0 8px 6px -5px rgba(0,0,0,0.2), 0 16px 15px 2px rgba(0,0,0,0.14),
              0 6px 18px 5px rgba(0,0,0,0.12), 0 0 0 2px @accent-bg-color,
              0 0 36px transparent;
}

window.csd, window.solid-csd, popover contents, dialog .background {
  transition: none;
  box-shadow: 0 8px 6px -5px rgba(0,0,0,0.2), 0 16px 15px 2px rgba(0,0,0,0.14),
              0 6px 18px 5px rgba(0,0,0,0.12), 0 0 0 2px @accent-bg-color,
              0 0 36px transparent;
}
"""

sharp_corners_css = """
* {
   border-radius: 0px;
}
"""

accent_tab_css_gtk4 = """
*:selected {
    color: var(--accent-bg-color);
}

*:checked:not(expander) {
    color: var(--accent-fg-color);
    background-color: var(--accent-bg-color);
}
"""

options = [
    (
        "transparency",
        _("Transparency"),
        _("Adds a transparency effect to all window backdrops"),
        transparency_css,
    ),
    (
        "window",
        _("Window Borders"),
        _("Draws an accented border around the window"),
        border_css,
    ),
    (
        "sharp",
        _("Sharp Corners"),
        _("Gives all elements square borders"),
        sharp_corners_css,
    ),
    (
        "accent-fg",
        _("Use Light Accent Foreground Color"),
        _("May work better for some themes or accents"),
        "",
    ),
    (
        "accent-tabs",
        _("Use Accent Color for Selected Tabs"),
        _("Only applies to GTK3/4 application"),
        accent_tab_css_gtk4,
    ),
    (
        "light-text",
        _("Force Light Text in Overview"),
        _("Might be useful for Blur my Shell users"),
        "",
    ),
    (
        "dark-panel",
        _("Keep Top Panel Dark"),
        _("The bar will stay dark regardless of theme"),
        "",
    ),
    (
        "trans-panel",
        _("Transparent Top Panel"),
        _("Makes the Top Panel Background Transparent"),
        "",
    ),
    (
        "no-pills",
        _("Reduce Rounding on Pill Buttons"),
        _("Smoothens all pill button on the top panel"),
        "",
    ),
]

keys = {
    "transparency": "transparency",
    "window": "borders",
    "sharp": "sharp",
    "accent-fg": "accent_fg",
    "accent-tabs": "accent_tabs",
    "light-text": "light_text",
    "dark-panel": "dark_panel",
    "trans-panel": "trans_panel",
    "no-pills": "no_pills"
}

class OptionsBox(Adw.PreferencesGroup):
    def __init__(self, parent):
        super().__init__(
            title=_("Extra Options"),
        )
        self.parent = parent

        pref = Preferences()
        for key, label, subtitle, css in options:
            if(key == "light-text" and not "GNOME" in GLib.getenv("XDG_CURRENT_DESKTOP") or ""):
                break

            active = pref.get(key)
            row = Adw.SwitchRow(title=label, subtitle=subtitle, active=active)
            row.connect("notify::active", self.on_row_toggled, css, key)
            self.add(row)

            if(active):
                self.parent.extra_css.add(css)

    def on_row_toggled(self, row, _pspec, css, key):
        is_active = row.get_active()

        attr = keys.get(key)
        if(attr):
            setattr(self.parent, attr, is_active)

        if(is_active):
            self.parent.extra_css.add(css)
        else:
            self.parent.extra_css.discard(css)

        self.parent.on_theme_selected()
