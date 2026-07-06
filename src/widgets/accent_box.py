# accent_box.py
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
# import colorsys

# def hex_to_rgb(hex_color):
#     hex_color = hex_color.lstrip("#")
#     return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

# def rgb_to_hex(r, g, b):
#     return "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))

# def mix(hex_a, hex_b, t=0.3):
#     r1, g1, b1 = hex_to_rgb(hex_a)
#     r2, g2, b2 = hex_to_rgb(hex_b)
#     return rgb_to_hex(
#         r1 + (r2 - r1) * t,
#         g1 + (g2 - g1) * t,
#         b1 + (b2 - b1) * t,
#     )

# def palette_to_css(palette):
#     return "\n".join(f"@define-color {k} {v};" for k, v in palette.items())

# def generate_tint_palette(hex_color):
#     r, g, b = hex_to_rgb(hex_color)
#     h, s, v = colorsys.rgb_to_hsv(r, g, b)
#     bg_r, bg_g, bg_b = colorsys.hsv_to_rgb(h, 0.06, 0.97)
#     return palette_to_css({
#         "accent_color": hex_color,
#         "accent_bg_color": hex_color,
#         "accent_fg_color": mix("#ffffff", hex_color),
#         "window_bg_color": mix("#222226", hex_color, 0.1),
#         "window_fg_color": mix("#ffffff", hex_color),
#         "headerbar_bg_color": mix("#2e2e32", hex_color, 0.4),
#         "headerbar_fg_color": mix("#ffffff", hex_color),
#         "sidebar_bg_color": rgb_to_hex(bg_r*0.8, bg_g*0.8, bg_b*0.8),
#     })

class AccentBox(Gtk.Box):
    accents = [
        ("'blue'", "#3584e4"),
        ("'teal'", "#2190a4"),
        ("'green'", "#3a944a"),
        ("'yellow'", "#c88800"),
        ("'orange'", "#ed5b00"),
        ("'red'", "#e62d42"),
        ("'pink'", "#d56199"),
        ("'purple'", "#9141ac"),
        ("'slate'", "#6f8396"),
    ]

    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12, halign=Gtk.Align.CENTER)
        prefs = Preferences()
        accent = prefs.get("accent")

        title = Gtk.Label(label=_("Accent Color"), xalign=0.0)
        title.add_css_class("heading")
        self.append(title)

        buttons = Gtk.Box()
        buttons.add_css_class("card")

        for css_class, color in self.accents:
            button = Gtk.Button(width_request=24, height_request=24, margin_start=7, margin_end=7, margin_top=12, margin_bottom=12)
            button.add_css_class("circular")

            if(css_class == accent):
                button.add_css_class("active-scheme")
                self.last_button = button

            provider = Gtk.CssProvider()
            provider.load_from_data(f"button {{ min-width: 0; min-height: 0; background-color: {color}; }}".encode())
            button.get_style_context().add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

            button.connect("clicked", self.on_clicked, css_class, color, parent)
            buttons.append(button)

        self.append(buttons)

    def on_clicked(self, button, color, hex_color, parent):
        prefs = Preferences()
        prefs.set("accent", color)
        setattr(parent, "accent", color)

        if(hasattr(self, "last_button")):
            self.last_button.remove_css_class("active-scheme")
        self.last_button = button
        button.add_css_class("active-scheme")
        parent.on_theme_selected()

        # palette = generate_tint_palette(hex_color)

        # if(parent.pref == 1):
        #     parent.dark_theme = "accent"
        #     flowbox_type = parent.dark_flowbox
        # else:
        #     parent.light_theme = "accent"
        #     flowbox_type = parent.light_flowbox

        # for flowbox in flowbox_type:
        #     for theme in flowbox:
        #         theme.remove_css_class("active-scheme")

        # parent.on_theme_selected()
