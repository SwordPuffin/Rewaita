# theme_cell.py
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
from gi.repository import Gtk, Adw, Soup, GLib, Gdk
from .install_page import InstallPage

class ThemeCell(Gtk.Box):
    session = Soup.Session()
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, width_request=350, height_request=400)
        self.add_css_class("card")
    
    def set_thumbnail_image(self, session, result, background):
        bytes = self.session.send_and_read_finish(result)
        texture = Gdk.Texture.new_from_bytes(bytes)
        
        background.unparent()
        background = Gtk.Picture.new_for_paintable(texture)
        background.set_content_fit(Gtk.ContentFit.COVER)
        background.add_css_class("rounded")
        background.set_vexpand(True)
        
        self.append(background)
        self.append(self.make_bottom_box())

    def make_bottom_box(self):
        def on_get_button_clicked(button):
            install_page = InstallPage(self)
            self.page.add(install_page)
            self.page.push(install_page)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        bottom_box = Gtk.Box(margin_start=12, margin_end=12, margin_top=8, margin_bottom=10, spacing=4)

        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER, spacing=2)
        title_label = Gtk.Label(label=self.title, xalign=0.0, wrap=True, hexpand=True)
        title_label.add_css_class("bold")

        download_label = Gtk.Label(label=f"↓ {self.downloads}, ★ {self.rating}", xalign=0.0, valign=Gtk.Align.CENTER)
        download_label.add_css_class("dimmed")

        dev_label = Gtk.Label(label=_("By: ") + self.dev, xalign=0.0, hexpand=True, valign=Gtk.Align.CENTER)
        dev_label.add_css_class("dimmed")

        text_box.append(title_label)
        text_box.append(dev_label)
        text_box.append(download_label)

        self.get_button = Gtk.Button(icon_name="download-symbolic", valign=Gtk.Align.CENTER)
        self.get_button.set_css_classes(["circular", "suggested-action"])
        self.button_id = self.get_button.connect("clicked", on_get_button_clicked)

        bottom_box.append(text_box)
        bottom_box.append(self.get_button)

        wrapper = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        wrapper.append(separator)
        wrapper.append(bottom_box)
        
        return wrapper
    
    def destroy_cell(self):
        try:
            self.get_button.disconnect(self.button_id)
        except:
            # Errors might arise in testing, something like: gdk-pixbuf-error-quark: Loader process exited early with status '1'
            # I do not believe this happens in production
            print("Unable to disconnect function")
        
    def build_cell(self):
        url = self.image_urls[0]
        background = Gtk.Spinner(spinning=True, vexpand=True, valign=Gtk.Align.CENTER, width_request=40, height_request=40)
        self.append(background)
        message = Soup.Message(method="GET", uri=GLib.Uri.parse(url, GLib.UriFlags.NONE))
        self.session.send_and_read_async(message, GLib.PRIORITY_DEFAULT, None, self.set_thumbnail_image, background)


