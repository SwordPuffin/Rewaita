# theme_page.py
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

import gi, os, re
from gi.repository import Gtk, Adw, Gdk, Gio, GLib, Pango
from fortune import fortune
from .wallpaper_dialog import WallpaperDialog

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
    color_pattern = re.compile(r'--([a-z0-9-]+)\s*:\s*(#[a-fA-F0-9]+|(?!var\()[a-z0-9_-]+(?:\([^)]*\))?)\s*;')

    with open(file_path, "r") as f:
        for line in f:
            match = color_pattern.search(line)
            if(match):
                name, color = match.groups()
                if(color.startswith('var')):
                    continue
                colors[name] = color.strip()
    return colors

SWATCH_KEYS = ["red-1", "orange-1", "yellow-1", "green-1", "blue-1", "dark-1", "light-1"]

def add_css(css):
    provider = Gtk.CssProvider()
    provider.load_from_data(css.encode())
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

def add_box(css_class, width=-1, height=-1):
    b = Gtk.Box(halign=Gtk.Align.START, valign=Gtk.Align.CENTER)
    b.add_css_class(css_class)
    b.set_size_request(width, height)
    return b


def theme_button_css(key, colors):
    bg = colors.get("window-bg-color", "#ffffff")
    fg = colors.get("window-fg-color", "#000000")
    mock = colors.get("card-bg-color", bg)
    # accent = colors.get("accent-bg-color") or colors.get("blue-1") or fg
    c = f"button.card-{key}"

    css = f"""
    {c}, {c}:hover, {c}:active {{ background-color: {bg}; color: {fg}; }}
    {c} .preview {{
        background-color: {mock};
        border-radius: 12px;
    }}
    """
    for i, k in enumerate(SWATCH_KEYS):
        color = colors.get(k)
        if color:
            css += f"{c} .s{i} {{ background-color: {color}; }}\n"
    return css

def create_color_thumbnail_button(colors, name, example_text):
    registered = set()
    key = os.urandom(15).hex()
    if(key not in registered):
        add_css(theme_button_css(key, colors))
        registered.add(key)

    button = Gtk.Button()
    button.add_css_class("theme-card")
    button.add_css_class(f"card-{key}")

    root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    for side in ("top", "bottom", "start", "end"):
        getattr(root, f"set_margin_{side}")(14)

    preview = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    preview.add_css_class("preview")
    preview.set_overflow(Gtk.Overflow.HIDDEN)

    body = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=9, margin_top=11, margin_bottom=11, margin_start=12, margin_end=12)
    quote = Gtk.Label(label=example_text, wrap=True, halign=Gtk.Align.START, max_width_chars=18)
    body.append(quote)
    preview.append(body)
    root.append(preview)

    title = Gtk.Label(label=name, halign=Gtk.Align.START, ellipsize=Pango.EllipsizeMode.END)
    root.append(title)

    dots = Gtk.Label(use_markup=True, halign=Gtk.Align.START)
    dots_text = ""
    for i, k in enumerate(SWATCH_KEYS):
        if(colors.get(k)):
            if(k != "red-1"):
                dots_text += " "
            dots_text += f"<span font_size='12pt' foreground='{colors.get(k)}'>● </span>"

    dots.set_label(dots_text)
    # bar = Gtk.Separator(height_request=4)
    # bar.add_css_class("bar")
    root.append(dots)
    # root.append(bar)

    button.set_child(root)

    def set_selected(selected):
        if(selected):
            button.add_css_class("selected")
        else:
            button.remove_css_class("selected")
        indicator.set_visible_child_name("picked" if selected else "idle")

    button.set_selected = set_selected
    return button

def symlink_all_in_dir(src, out):
    os.makedirs(out, exist_ok=True)

    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        out_path = os.path.join(out, name)

        if(os.path.isfile(src_path)):
            if(os.path.exists(out_path) and not os.path.islink(out_path)):
                continue
            if(os.path.islink(out_path)):
                os.remove(out_path)

            os.symlink(src_path, out_path)

def open_wallpaper_dialog(button, window, run_function):
    wallpaper_dialog = WallpaperDialog(window, run_function)
    wallpaper_dialog.present(window)

class ThemePage(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        topadd_box = Gtk.Box(hexpand=True, halign=Gtk.Align.CENTER, margin_top=12, spacing=8)
        help_button = Gtk.Button(label=_("Wiki"), valign=Gtk.Align.CENTER, vexpand=True, css_classes=["pill", "suggested-action"])
        help_button.connect("clicked", lambda d: Gio.AppInfo.launch_default_for_uri("https://github.com/SwordPuffin/Rewaita/wiki", None))
        topadd_box.append(help_button)

        image_button = Gtk.Button(label=_("Tint Wallpaper"), valign=Gtk.Align.CENTER, vexpand=True, css_classes=["pill", "suggested-action"])
        image_button.connect("clicked", open_wallpaper_dialog, parent, "make_new_image")
        topadd_box.append(image_button)

        image_button = Gtk.Button(label=_("Generate Theme From Image"), halign=Gtk.Align.CENTER, css_classes=["pill", "suggested-action"])
        image_button.connect("clicked", open_wallpaper_dialog, parent, "make_new_theme")

        self.append(topadd_box)
        self.append(image_button)

        snippet = self.get_example_text()
        for theme_type in ["light", "dark"]:
            self.append(Adw.Clamp(maximum_size=600, child=Gtk.Separator(margin_start=20, margin_end=20, margin_top=25)))

            default_theme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), theme_type)
            symlink_all_in_dir(default_theme_path, os.path.join(GLib.get_user_data_dir(), theme_type))
            themes = os.listdir(os.path.join(parent.data_dir, theme_type))

            reset_button = Gtk.Button(icon_name="reload-symbolic", tooltip_text=_("Reset to default"))
            reset_button.add_css_class("circular")
            reset_button.connect("clicked", parent.on_theme_button_clicked, "Default", theme_type)

            if(theme_type == "light"):
                parent.light_flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
                flowbox = parent.light_flowbox
                parent.light_button = reset_button
            else:
                parent.dark_flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
                flowbox = parent.dark_flowbox
                parent.dark_button = reset_button

            toggle_button = Gtk.ToggleButton(active=True, tooltip_text=_("Show More"), icon_name="pan-down-symbolic")
            toggle_button.add_css_class("flat")
            toggle_button.add_css_class("circular")

            titleadd_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER, spacing=25)
            title = Gtk.Label(label=_(theme_type.capitalize()))
            title.add_css_class("title-2")
            titleadd_box.append(title); titleadd_box.append(reset_button); titleadd_box.append(toggle_button)
            self.append(titleadd_box)

            revealer = Gtk.Revealer(transition_type=Gtk.RevealerTransitionType.SLIDE_DOWN, transition_duration=200)
            revealer.set_reveal_child(True)

            def on_toggle_clicked(button, revealer=revealer, reset_button=reset_button):
                expanded = button.get_active()
                revealer.set_reveal_child(expanded)
                button.set_icon_name("pan-down-symbolic" if expanded else "pan-end-symbolic")
                reset_button.set_visible(expanded)

            toggle_button.connect("toggled", on_toggle_clicked)

            if(theme_type == "light"):
                parent.light_revealer = revealer
            else:
                parent.dark_revealer = revealer

            flowbox.snippet = snippet
            for theme in sorted(themes):
                file_path = os.path.join(parent.data_dir, theme_type, theme)

                if(not os.path.exists(file_path)):
                    continue

                colors = load_colors_from_css(file_path)
                btn = create_color_thumbnail_button(colors, theme.replace(".css", ""), flowbox.snippet)
                btn.connect("clicked", parent.on_theme_button_clicked, theme, theme_type)

                if(theme == parent.dark_theme and theme_type == "dark" or theme == parent.light_theme and theme_type == "light"):
                    btn.add_css_class("active-scheme")
                if(os.path.islink(file_path)):
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
            revealer.set_child(Adw.Clamp(maximum_size=900, child=flowbox))
            self.append(revealer)

    def get_example_text(self):
        while(True):
            example = fortune()
            if(len(example) < 70 and not "<" in example and ">" not in example):
                return example
