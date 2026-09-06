# wallpaper_dialog.py
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

import os
from gi.repository import Adw, Gtk, Gio, Gdk, GLib

from .image_modifier import make_new_image
from .image_to_css import make_new_theme

class WallpaperDialog(Adw.Dialog):
    folder_path = os.path.join(GLib.get_user_data_dir(), "wallpapers")
    
    def __init__(self, parent, run_function):
        super().__init__()
        page = Gtk.Box(hexpand=True, vexpand=True, orientation=Gtk.Orientation.VERTICAL)
        message_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_bottom=24, margin_start=24, margin_end=24, valign=Gtk.Align.CENTER, halign=Gtk.Align.CENTER)
        page.append(Adw.HeaderBar())
        page.append(message_area)

        # These are used later, but needed here
        open_file_button = Gtk.Button(label=_("Open File"), halign=Gtk.Align.CENTER)
        drop_area = Gtk.Box(margin_start=12, margin_end=12, margin_top=12, margin_bottom=12, height_request=80, hexpand=True)

        def entry_changed(entry):
            open_file_button.set_sensitive(entry.get_text() != '')
            drop_area.set_sensitive(entry.get_text() != '')

            if(entry.get_text() == ''):
                entry.add_css_class("error")
            else:
                entry.remove_css_class("error")

        if(run_function == "make_new_theme"):
            open_file_button.set_sensitive(False)
            drop_area.set_sensitive(False)
            self.folder_path = GLib.get_user_data_dir()

            extras_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, margin_top=12, spacing=4)
            self.name_entry = Gtk.Entry(placeholder_text=_("Name (required)"), hexpand=True)
            self.name_entry.connect("changed", entry_changed)
            self.name_entry.add_css_class("error")
            light_radio = Adw.Toggle(label=_("Light"))
            dark_radio = Adw.Toggle(label=_("Dark"))
            self.toggle_group = Adw.ToggleGroup(halign=Gtk.Align.START)
            self.toggle_group.add(light_radio)
            self.toggle_group.add(dark_radio)
            self.toggle_group.add_css_class("round")
            extras_box.append(self.name_entry)
            extras_box.append(self.toggle_group)
            message_area.append(extras_box)

        def exec_function(file_path, key):
            if(key == "make_new_image"):
                make_new_image(parent, file_path)
            else:
                make_new_theme(parent, file_path, self.name_entry.get_text(), self.toggle_group.get_active() == 0)
            self.close()

        def on_drop_file(target, value, x, y):
            file_path = value.get_path() or value.get_uri()
            exec_function(file_path, run_function)
            return True

        def on_image_opened(file_dialog, result):
            file = file_dialog.open_finish(result)
            file_path = file.get_path()
            exec_function(file_path, run_function)

        def on_open_image(button):
            file_filter_image = Gtk.FileFilter()
            file_filter_image.set_name("Image files")
            file_filter_image.add_mime_type("image/svg+xml")
            file_filter_image.add_mime_type("image/png")
            file_filter_image.add_mime_type("image/jpeg")
            file_filter_image.add_mime_type("image/webp")
            file_dialog = Gtk.FileDialog(default_filter=file_filter_image)
            file_dialog.open(parent, None, on_image_opened)

        file_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8, hexpand=True, halign=Gtk.Align.CENTER, margin_top=20)

        open_file_button.connect("clicked", on_open_image)
        file_box.append(open_file_button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        label = Gtk.Label(label=_("Save Folder"))
        icon = Gtk.Image.new_from_icon_name("folder-symbolic")
        box.append(label); box.append(icon)
        dir_button = Gtk.Button(child=box)
        os.makedirs(self.folder_path, exist_ok=True)
        folder = Gio.File.new_for_path(self.folder_path)
        dir_button.connect("clicked", lambda d : Gio.AppInfo.launch_default_for_uri(folder.get_uri(), None))
        file_box.append(dir_button)

        message_area.append(file_box)
        open_file_button.set_css_classes(["suggested-action", "pill"])
        dir_button.set_css_classes(["suggested-action", "pill"])
        drop_target = Gtk.DropTarget.new(Gio.File, Gdk.DragAction.COPY)
        drop_target.connect("drop", on_drop_file)

        hint = Gtk.Label(label=_("Drop Image Here"), hexpand=True, vexpand=True, xalign=0.5, yalign=0.5)
        hint.set_css_classes(["dimmed", "title-4"])
        drop_area.append(hint)
        drop_area.add_css_class("drop-area")
        drop_area.add_controller(drop_target)

        message_area.append(drop_area)
        self.set_child(page)
