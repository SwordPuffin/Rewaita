# item_carousel.py
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
from gi.repository import Gtk, Adw

class ItemCarousel(Gtk.Overlay):
    signal_ids = []
    
    def __init__(self, connect_button):
        super().__init__()
        
        carousel = Adw.Carousel(allow_scroll_wheel=False, spacing=12)
        self.signal_ids.append((carousel, connect_button(carousel,  "page-changed", self.reorder)))
        carousel.add_css_class("carousel-view")
        self.carousel = carousel
        self.set_child(carousel)
        
        left_button = Gtk.Button(icon_name="go-previous-symbolic", valign=Gtk.Align.CENTER, halign=Gtk.Align.START, margin_start=12)
        left_button.set_css_classes(["circular", "osd"])
        right_button = Gtk.Button(icon_name="go-next-symbolic", valign=Gtk.Align.CENTER, halign=Gtk.Align.END, margin_end=12)
        right_button.set_css_classes(["circular", "osd"])
        self.add_overlay(left_button)
        self.add_overlay(right_button)

        def scroll_to(button, direction):
            n = carousel.get_n_pages()
            pos = carousel.get_position()
            if(abs(pos - round(pos)) > 0.0):
                return
            target = round(pos) + direction
            if(target < 0 or target >= n):
                return
            carousel.scroll_to(carousel.get_nth_page(target), True)

        self.signal_ids.append((left_button, connect_button(left_button,  "clicked", scroll_to, -1)))
        self.signal_ids.append((right_button, connect_button(right_button, "clicked", scroll_to,  1)))
    
    def connect_button(self, widget, signal, callback, *args):
        return widget.connect(signal, callback, *args) 
    
    def reorder(self, carousel, index):
        n = carousel.get_n_pages()
        if(n < 3):
            return
        mid = n // 2
        if(index > mid):
            first = carousel.get_nth_page(0)
            carousel.remove(first)
            carousel.append(first)
        elif(index < mid):
            last = carousel.get_nth_page(n - 1)
            carousel.reorder(last, 0)

    def clean(self):
        for widget, handler_id in self.signal_ids:
            if handler_id is not None and widget.handler_is_connected(handler_id):
                widget.disconnect(handler_id)
        self.signal_ids.clear()
        
