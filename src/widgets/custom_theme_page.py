# custom_theme_page.py
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

import gi, shutil, os
gi.require_version("Gtk", "4.0")
gi.require_version('GtkSource', '5')
from gi.repository import Gtk, Gdk, Adw, GLib, GtkSource, Gio
from .theme_page import load_colors_from_css, create_color_thumbnail_button
from .utils import add_new_theme_button, rgb_to_hex
from .css_templates import gnome_colors, titles

class ColorRow(Adw.ActionRow):
    def __init__(self, title: str, variable: str, default_color: str, registry: dict):
        super().__init__(selectable=False)
        self.set_title(title)
        self.set_subtitle(variable)

        rgba = Gdk.RGBA()
        rgba.parse(default_color)
        self.color_button = Gtk.ColorButton()
        self.color_button.set_rgba(rgba)
        self.color_button.variable = variable
        registry[variable] = self.color_button

        end_box = Gtk.Box(spacing=6)
        end_box.append(self.color_button)

        self.add_suffix(end_box)

class CustomBundle(Gtk.Box):
    def __init__(self, label, bundle, registry: dict):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_start=12, margin_end=12)
        label.add_css_class("title-4")
        self.prepend(label)
        colors = gnome_colors[label.title]
        description_label = Gtk.Label(label=colors["description"], wrap=True)
        description_label.add_css_class("dimmed")
        self.append(description_label)
        listbox = Gtk.ListBox(valign=Gtk.Align.CENTER)
        listbox.add_css_class("boxed-list")
        for color in colors.keys():
            if(color == 'description'): continue
            row = ColorRow(titles[color], color, colors[color], registry)
            listbox.append(row)
        self.append(listbox)

EXTRA_CSS_MARKER = "/* --- custom css below (do not remove this line) --- */"

class CustomPage(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20, margin_top=20)

        self.parent = parent
        self.color_buttons = {}
        self.editing_theme = None

        # The label.title is so the value is consistent through translations
        main_label = Gtk.Label(label=_("Main Colors")); main_label.title = "Main Colors"
        success_label = Gtk.Label(label=_("Success Colors")); success_label.title = "Success Colors"
        destructive_label = Gtk.Label(label=_("Destructive Colors")); destructive_label.title = "Destructive Colors"
        warning_label = Gtk.Label(label=_("Warning Colors")); warning_label.title = "Warning Colors"
        interface_label = Gtk.Label(label=_("Interface Colors")); interface_label.title = "Interface Colors"
        colors_label = Gtk.Label(label=_("Named Colors")); colors_label.title = "Named Colors"

        for bundle, label in zip(gnome_colors.keys(), [main_label, success_label, destructive_label, warning_label, interface_label, colors_label]):
            self.append(CustomBundle(label, bundle, self.color_buttons))

        name_box = Gtk.Box(halign=Gtk.Align.CENTER, spacing=12)
        self.name_entry = Gtk.Entry(placeholder_text=_("Name (required)"), hexpand=True)
        self.name_entry.connect("changed", self.entry_changed)
        self.name_entry.add_css_class("error")
        name_box.append(self.name_entry)

        light_radio = Adw.Toggle(label=_("Light"))
        dark_radio = Adw.Toggle(label=_("Dark"))
        self.toggle_group = Adw.ToggleGroup(halign=Gtk.Align.START)
        self.toggle_group.add(light_radio)
        self.toggle_group.add(dark_radio)
        self.toggle_group.add_css_class("round")
        name_box.append(self.toggle_group)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        label = Gtk.Label(label=_("Save Folder"))
        icon = Gtk.Image.new_from_icon_name("folder-symbolic")
        box.append(label); box.append(icon)
        open_folder_button = Gtk.Button(child=box, halign=Gtk.Align.CENTER)
        open_folder_button.set_css_classes(["suggested-action", "pill"])
        folder = Gio.File.new_for_path(GLib.get_user_data_dir())
        open_folder_button.connect("clicked", lambda d : Gio.AppInfo.launch_default_for_uri(folder.get_uri(), None))
        self.save_button = Gtk.Button(label=_("Save"), sensitive=False, margin_bottom=12, margin_start=12, margin_end=12)
        self.save_button.connect("clicked", self.save_theme, parent, self.name_entry, self.toggle_group)

        GtkSource.init()
        css_entry = GtkSource.View(auto_indent=True, indent_width=2, show_line_numbers=True)
        self.buffer = GtkSource.Buffer(text=_("/* Enter any extra CSS here */"))

        scheme_manager = GtkSource.StyleSchemeManager.get_default()
        scheme = scheme_manager.get_scheme("Adwaita")
        if(scheme):
            self.buffer.set_style_scheme(scheme)

        language_manager = GtkSource.LanguageManager.get_default()
        language = language_manager.get_language("css")
        self.buffer.set_language(language)
        css_entry.set_buffer(self.buffer)

        self.append(name_box)
        self.append(Gtk.ScrolledWindow(child=css_entry, height_request=240))
        self.append(open_folder_button)
        self.append(self.save_button)

    def entry_changed(self, entry):
        if(entry.get_text() == ''):
            self.save_button.set_sensitive(False)
            entry.add_css_class("error")
        else:
            self.save_button.set_sensitive(True)
            entry.remove_css_class("error")

    def edit_theme(self, button, theme_path, theme_name, theme_type, stack, edit_button):
        self.name_entry.set_text(theme_name.replace(".css", ""))
        self.toggle_group.set_active(0 if theme_type == "light" else 1)
        stack.set_visible_child_name("custom")
        edit_button.emit("clicked")

        colors = load_colors_from_css(theme_path)
        for variable, hex_color in colors.items():
            button_widget = self.color_buttons.get(f"--{variable}")
            if(button_widget is None):
                continue
            rgba = Gdk.RGBA()
            rgba.parse(hex_color)
            button_widget.set_rgba(rgba)

        with open(theme_path) as f:
            existing_text = f.read()
        if(EXTRA_CSS_MARKER in existing_text):
            extra_css = existing_text.split(EXTRA_CSS_MARKER, 1)[1].lstrip("\n")
            self.buffer.set_text(extra_css)
        else:
            self.buffer.set_text("")

        self.editing_theme = (theme_name, theme_type, theme_path, button)

    def save_theme(self, button, parent, entry, radio_group):
        theme_type = ["light", "dark"][radio_group.get_active()]
        new_name = entry.get_text()

        if(self.editing_theme):
            old_name, old_type, old_path, old_button = self.editing_theme
            if(old_name != new_name or old_type != theme_type):
                if(os.path.exists(old_path)):
                    os.remove(old_path)
                old_flowbox = parent.light_flowbox if old_type == "light" else parent.dark_flowbox
                self.remove_button_for(old_flowbox, old_name)
            else:
                flowbox = parent.light_flowbox if theme_type == "light" else parent.dark_flowbox
                self.remove_button_for(flowbox, old_name)

        parent.toast_overlay.add_toast(Adw.Toast(timeout=3, title=new_name + _(" has been saved")))

        src_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom-template.css")
        src_file_text = open(src_file).read()
        for variable, color_button in self.color_buttons.items():
            rgb = color_button.get_rgba()
            hex_color = rgb_to_hex((rgb.red * 255, rgb.green * 255, rgb.blue * 255))
            src_file_text = src_file_text.replace(f"var({variable})", hex_color)

        extra_css = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(), True)
        src_file_text += "\n" + EXTRA_CSS_MARKER + "\n" + extra_css

        os.makedirs(os.path.join(parent.data_dir, theme_type), exist_ok=True)
        theme_file = os.path.join(parent.data_dir, theme_type, new_name + ".css")
        shutil.copyfile(src_file, theme_file)
        with open(theme_file, "w") as file:
            file.write(src_file_text)

        if(theme_type == "light"):
            flowbox = parent.light_flowbox
        else:
            flowbox = parent.dark_flowbox
        
        add_new_theme_button(theme_file, flowbox, parent.on_theme_button_clicked, theme_type)
        self.editing_theme = None

    def remove_button_for(self, flowbox, theme_name):
        for existing in flowbox:
            child = existing.get_first_child()
            if(child is not None and getattr(child, "theme", None) == theme_name):
                flowbox.remove(existing)
                break
