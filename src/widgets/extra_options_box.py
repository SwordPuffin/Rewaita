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
from .css_templates import transparency_css, border_css, sharp_corners_css, accent_tab_css_gtk4, window_blur, dialog_blur

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
        _("Only applies to GTK4 application and GNOME Shell"),
        accent_tab_css_gtk4,
    ),
    (
        "blur",
        _("Application Blur"),
        _("Only works on GTK-4.24.1 or newer applications"),
        ""
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
    "blur": "blur",
    "light-text": "light_text",
    "dark-panel": "dark_panel",
    "trans-panel": "trans_panel",
    "no-pills": "no_pills"
}

accent_fg_options = Gtk.StringList()
accent_fg_options.append(_("In Neither"))
accent_fg_options.append(_("In Dark Mode"))
accent_fg_options.append(_("In Light Mode"))
accent_fg_options.append(_("In Both"))

blur_options = Gtk.StringList()
blur_options.append(_("No Blur"))
blur_options.append(_("Full window"))
blur_options.append(_("Dialogs/popovers"))

list_options = {
    "accent-fg": accent_fg_options,
    "blur": blur_options,
}

blur_css = {
    1: window_blur,
    2: dialog_blur,
}

class OptionsBox(Adw.PreferencesGroup):
    def __init__(self, parent):
        super().__init__(
            title=_("Extra Options"),
        )
        self.parent = parent

        pref = Preferences()
        for key, label, subtitle, css in options:
            if(key == "blur" and not "GNOME" in GLib.getenv("XDG_CURRENT_DESKTOP") or ""):
                continue

            active = pref.get(key)

            if(key in list_options):
                model = list_options[key]
                selected = int(active or 0)
                if(selected >= model.get_n_items()):
                    selected = 0

                row = Adw.ComboRow(title=label, subtitle=subtitle, model=model, selected=selected)
                row.connect("notify::selected", self.on_row_selected, css, key)

                if(key == "blur" and selected in blur_css):
                    self.parent.extra_css.add(blur_css[selected])
            else:
                row = Adw.SwitchRow(title=label, subtitle=subtitle, active=bool(active))
                row.connect("notify::active", self.on_row_selected, css, key)

                if(active and css):
                    self.parent.extra_css.add(css)

            self.add(row)

    def on_row_selected(self, row, _pspec, css, key):
        if(isinstance(row, Adw.ComboRow)):
            value = row.get_selected()
        else:
            value = row.get_active()

        attr = keys.get(key)
        if(attr):
            setattr(self.parent, attr, value)

        if(key == "blur"):
            for c in blur_css.values():
                self.parent.extra_css.discard(c)
            if(value in blur_css):
                self.parent.extra_css.add(blur_css[value])
        elif(css):
            if(value):
                self.parent.extra_css.add(css)
            else:
                self.parent.extra_css.discard(css)

        self.parent.on_theme_selected()

