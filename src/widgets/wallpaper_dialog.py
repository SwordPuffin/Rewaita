# wallpaper_dialog.py
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

import os
from gi.repository import Adw, Gtk, Gio, Gdk, GLib
from .image_modifier import on_image_opened, make_new_image

picture_path = os.path.join(GLib.get_user_data_dir(), "wallpapers")

class WallpaperDialog(Adw.Dialog):
    def __init__(self, parent):
        super().__init__()
        page = Gtk.Box(hexpand=True, vexpand=True, orientation=Gtk.Orientation.VERTICAL)
        message_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_bottom=24, margin_start=24, margin_end=24, valign=Gtk.Align.CENTER, halign=Gtk.Align.CENTER)
        page.append(Adw.HeaderBar())
        page.append(message_area)

        def on_drop_file(target, value, x, y):
            file_path = value.get_path() or value.get_uri()
            make_new_image(parent, file_path)
            return True

        def on_open_image(button):
            file_filter_image = Gtk.FileFilter()
            file_filter_image.set_name("Image files")
            file_filter_image.add_mime_type("image/svg+xml")
            file_filter_image.add_mime_type("image/png")
            file_filter_image.add_mime_type("image/jpeg")
            file_filter_image.add_mime_type("image/webp")
            file_dialog = Gtk.FileDialog(default_filter=file_filter_image)
            file_dialog.open(parent, None, on_image_opened, parent)

        warning_label = Gtk.Label(wrap=True, margin_top=24, justify=Gtk.Justification.CENTER, halign=Gtk.Align.CENTER, label=_("This feature is still under development. Under 4k resolution is recommended."))
        warning_label.set_css_classes(["warning", "bold"])
        message_area.append(warning_label)

        file_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8, hexpand=True, halign=Gtk.Align.CENTER, margin_top=20)

        open_file_button = Gtk.Button(label=_("Open File"), halign=Gtk.Align.CENTER)
        open_file_button.connect("clicked", on_open_image)
        file_box.append(open_file_button)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        label = Gtk.Label(label=_("Save Folder"))
        icon = Gtk.Image.new_from_icon_name("folder-open-symbolic")
        box.append(label); box.append(icon)
        dir_button = Gtk.Button(child=box)
        os.makedirs(picture_path, exist_ok=True)
        folder = Gio.File.new_for_path(picture_path)
        dir_button.connect("clicked", lambda d : Gio.AppInfo.launch_default_for_uri(folder.get_uri(), None))
        file_box.append(dir_button)

        message_area.append(file_box)
        open_file_button.set_css_classes(["suggested-action", "pill"])
        dir_button.set_css_classes(["suggested-action", "pill"])

        drop_target = Gtk.DropTarget.new(Gio.File, Gdk.DragAction.COPY)
        drop_target.connect("drop", on_drop_file)
        drop_area = Gtk.Box(margin_start=12, margin_end=12, margin_top=12, margin_bottom=12, height_request=80, hexpand=True)
        hint = Gtk.Label(label=_("Drop Image Here"), hexpand=True, vexpand=True, xalign=0.5, yalign=0.5)
        hint.set_css_classes(["dimmed", "title-4"])
        drop_area.append(hint)
        drop_area.add_css_class("drop-area")
        drop_area.add_controller(drop_target)

        message_area.append(drop_area)
        self.set_child(page)
