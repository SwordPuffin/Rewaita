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

from gi.repository import Adw, Gtk, Gio, Gdk
from .image_modifier import on_image_opened, make_new_image

class WallpaperDialog(Adw.Dialog):
    def __init__(self, parent):
        super().__init__()

        message_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_top=24, margin_bottom=24, margin_start=24, margin_end=24, valign=Gtk.Align.CENTER, halign=Gtk.Align.CENTER)

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

        warning_label = Gtk.Label(wrap=True, margin_top=24, justify=Gtk.Justification.CENTER, halign=Gtk.Align.CENTER, label=_("This feature is still under development, and results can be hit or miss. Under 4k resolution is recommended."))
        warning_label.set_css_classes(["warning", "bold"])
        message_area.append(warning_label)

        open_file_button = Gtk.Button(label=_("Open Image"), halign=Gtk.Align.CENTER, margin_top=20)
        open_file_button.connect("clicked", on_open_image)
        open_file_button.set_css_classes(["suggested-action", "pill"])

        message_area.append(open_file_button)

        drop_target = Gtk.DropTarget.new(Gio.File, Gdk.DragAction.COPY)
        drop_target.connect("drop", on_drop_file)
        drop_area = Gtk.Box(margin_start=12, margin_end=12, margin_top=12, margin_bottom=12, height_request=80, hexpand=True)
        hint = Gtk.Label(label=_("Drop Image Here"), hexpand=True, vexpand=True, xalign=0.5, yalign=0.5)
        hint.set_css_classes(["dimmed", "title-4"])
        drop_area.append(hint)
        drop_area.add_css_class("drop-area")
        drop_area.add_controller(drop_target)

        message_area.append(drop_area)
        self.set_child(message_area)
