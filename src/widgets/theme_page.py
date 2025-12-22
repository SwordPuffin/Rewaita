# theme_page.py
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

import gi, os, re
from gi.repository import Gtk, Adw, Gdk, GLib
from fortune import fortune
from .wallpaper_dialog import WallpaperDialog
from .extra_options_box import OptionsBox

def flowbox_sort_func(child1: Gtk.FlowBoxChild, child2: Gtk.FlowBoxChild, _):
    button1 = child1.get_first_child()
    button2 = child2.get_first_child()

    theme1 = button1.theme.lower()
    theme2 = button2.theme.lower()

    if(theme1 < theme2):
        return -1
    elif(theme1 > theme2):
        return 1
    return 0

def load_colors_from_css(file_path):
    colors = {}
    define_re = re.compile(r"@define-color\s+(\S+)\s+([^;]+);")

    with open(file_path, "r") as f:
        for line in f:
            match = define_re.search(line)
            if(match):
                name, color = match.groups()
                colors[name] = color.strip()
    return colors

def create_color_thumbnail_button(colors, name, example_text):
    button = Gtk.Button()
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    dots = Gtk.Label(vexpand=True, valign=Gtk.Align.END, use_markup=True)
    dot_txt = ""

    keys_to_show = ["red_1", "orange_1", "yellow_1", "green_1", "blue_1", "dark_1", "light_1"]
    for key in keys_to_show:
        color = colors.get(key)
        if(color):
            dot_txt += f"<span font_size='20pt' foreground='{color}'> ● </span>"

    dots.set_label(dot_txt)
    rand = os.urandom(15).hex()
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(f"""
        .background-{rand} {{
            border-radius: 18px;
            background-color: {colors.get("window_bg_color")};
            color: {colors.get("window_fg_color")};
        }}
    """.encode())
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    button.add_css_class(f'background-{rand}')

    example = Gtk.Label(wrap=True, margin_top=12, margin_bottom=12, hexpand=True, vexpand=True, valign=Gtk.Align.CENTER, halign=Gtk.Align.CENTER, max_width_chars=12)
    example.set_markup(f"<i><b>{example_text}</b></i>")
    box.prepend(example)
    title = Gtk.Label(margin_bottom=12, margin_top=12, label=name)
    title.set_css_classes(["monospace", "title-2"])
    box.prepend(title)
    box.append(dots)
    button.set_child(box)
    return button

def symlink_all_in_dir(src, out):
    os.makedirs(out, exist_ok=True)

    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        out_path = os.path.join(out, name)

        if(os.path.isfile(src_path)):
            if(os.path.exists(out_path)):
                os.remove(out_path)

            os.symlink(src_path, out_path)

class ThemePage(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        top_box = Gtk.Box(hexpand=True, halign=Gtk.Align.CENTER, margin_top=12, spacing=8)
        help_button = Gtk.Button(label=_("User Guide"), valign=Gtk.Align.CENTER, vexpand=True)
        help_button.set_css_classes(["pill", "suggested-action"])
        help_button.set_action_name("app.guide")
        top_box.append(help_button)

        wallpaper_dialog = WallpaperDialog(parent)
        image_button = Gtk.Button(label=_("Tint Wallpaper"), valign=Gtk.Align.CENTER, vexpand=True)
        image_button.connect("clicked", lambda d : wallpaper_dialog.present(parent))
        image_button.set_css_classes(["pill", "suggested-action"])
        top_box.append(image_button)

        options_listbox = OptionsBox(parent)
        self.append(top_box)
        self.append(options_listbox)

        snippet = self.get_example_text()
        for theme_type in ["light", "dark"]:
            self.append(Adw.Clamp(maximum_size=1200, child=Gtk.Separator(margin_start=20, margin_end=20, margin_top=25)))
            reset_button = Gtk.Button(icon_name="reload-symbolic", tooltip_text=_("Reset to default"))
            reset_button.add_css_class("circular")
            reset_button.connect("clicked", parent.on_theme_button_clicked, "Default", theme_type)

            default_theme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), theme_type)
            default_themes = os.listdir(default_theme_path)
            symlink_all_in_dir(default_theme_path, os.path.join(GLib.get_user_data_dir(), theme_type))
            themes = os.listdir(os.path.join(parent.data_dir, theme_type))

            if(theme_type == "light"):
                parent.light_flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
                flowbox = parent.light_flowbox
                parent.light_button = reset_button
            else:
                parent.dark_flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
                flowbox = parent.dark_flowbox
                parent.dark_button = reset_button

            title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER)
            title = Gtk.Label(label=_(theme_type.capitalize()), margin_end=25)
            title.add_css_class("title-2")
            title_box.append(title); title_box.append(reset_button)
            self.append(title_box)

            flowbox.snippet = snippet
            for theme in sorted(themes):
                colors = load_colors_from_css(os.path.join(parent.data_dir, theme_type, theme))
                btn = create_color_thumbnail_button(colors, theme.replace(".css", ""), flowbox.snippet)
                btn.connect("clicked", parent.on_theme_button_clicked, theme, theme_type)

                if(theme == parent.dark_theme and theme_type == "dark" or theme == parent.light_theme and theme_type == "light"):
                    btn.add_css_class("active-scheme")
                if(theme in default_themes):
                    btn.default = True
                else:
                    btn.default = False

                #Attributes
                btn.path = os.path.join(parent.data_dir, theme_type, theme)
                btn.func = parent.on_theme_button_clicked
                btn.theme = theme
                btn.theme_type = theme_type

                flowbox.append(btn)

            flowbox.set_sort_func(flowbox_sort_func, None)
            self.append(Adw.Clamp(maximum_size=900, child=flowbox))

    def get_example_text(self):
        while(True):
            example = fortune()
            if(len(example) < 70 and not "<" in example and ">" not in example):
                return example
