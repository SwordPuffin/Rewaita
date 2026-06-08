# search_page.py
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
from .utils import soup_get, parse_json
from .theme_cell_flowbox import ThemeCellFlowbox

category_map = {
        134: 0, 386: 1, 199: 1, 132: 1, 366: 2, 135: 2, 136: 2,
        107: 3, 300: 4, 312: 4, 261: 4, 299: 4, 283: 4, 360: 4
    }

class SearchPage(Adw.NavigationPage):
    def __init__(self, view):
        super().__init__(tag="search_page")
        content_box = Gtk.Box(vexpand=True, hexpand=True, orientation=Gtk.Orientation.VERTICAL, spacing=18)
        search_box = Gtk.Box()
        self.search_bar = Gtk.SearchEntry(placeholder_text=_("Search Themes"), hexpand=True, margin_start=5, margin_end=5)
        self.search_bar.connect("activate", self.search, "new_page")
        filter_button = Gtk.Button(icon_name="view-more-symbolic", valign=Gtk.Align.CENTER)
        filter_button.add_css_class("circular")
        
        self.current_page = 0
        self.filter_popover = Gtk.Popover()
        self.filter_popover.set_has_arrow(True)
        self.filter_popover.set_autohide(True)
        self.filter_popover.set_parent(filter_button)
        self.make_filter()
        filter_button.connect("clicked", self.toggle_filter_popover)

        search_box.append(self.search_bar); search_box.append(filter_button)
        content_box.append(Adw.Clamp(maximum_size=520, child=search_box))
        content_box.append(Gtk.Separator())

        self.search_flowbox = ThemeCellFlowbox()
        self.search_flowbox.is_search_flowbox = True
        self.search_flowbox.page = view
        self.search_icon = Gtk.Image(icon_name="search-symbolic", pixel_size=160, valign=Gtk.Align.START, vexpand=True, margin_bottom=12)
        self.search_icon.add_css_class("dimmed")
        self.search_flowbox.search_icon = self.search_icon
        self.next_page_button = Gtk.Button(label=_("Next Page"), hexpand=True, halign=Gtk.Align.CENTER, width_request=350, margin_top=24, margin_bottom=24, visible=False)
        self.next_page_button.connect("clicked", self.next_page)
        self.search_flowbox.next_page_button = self.next_page_button
        scroll_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scroll_box.append(self.search_flowbox); scroll_box.append(self.next_page_button); scroll_box.append(self.search_icon)
        scroller = Gtk.ScrolledWindow(child=scroll_box, vexpand=True, hexpand=True)
        content_box.append(scroller)
        self.set_child(content_box)
    
    def next_page(self, button):
        button.set_child(Gtk.Spinner(spinning=True))
        button.set_sensitive(False)
        self.current_page += 1
        self.search(self.search_bar, "add_page");
        
    def toggle_filter_popover(self, button):
        if(self.filter_popover.get_visible()):
            self.filter_popover.popdown()
        else:
            self.filter_popover.popup()

    def make_filter(self):
        self.active_filters = {134, 386, 366, 107, 261}
        def on_filter_changed(button):
            if(button.id in self.active_filters):
                if(len(self.active_filters) == 1): return
                self.active_filters.remove(button.id)
                button.remove_css_class("accent")
                button.set_label(button.get_label().replace(" ✔", ""))
            else:
                self.active_filters.add(button.id)
                button.add_css_class("accent")
                button.set_label(button.get_label() + " ✔")

        filters = Gtk.FlowBox(selection_mode=Gtk.SelectionMode.NONE, min_children_per_line=1, max_children_per_line=2)

        for category, id in [("GNOME Shell", 134), ("Icons", 386), ("GTK3/4", 366), ("Cursors", 107), ("Wallpapers", 261)]:
            button = Gtk.Button(label=_(category) + " ✔")
            button.id = id
            button.add_css_class("accent")
            button.connect("clicked", on_filter_changed)
            filters.append(button)

        self.filter_popover.set_child(filters)

    def search(self, entry, action):
        if(action == "new_page"):
            self.search_icon.set_visible(False)
            self.next_page_button.set_visible(False)
            self.search_flowbox.remove_all()
            self.current_page = 0
        cats = "x".join(str(i) for i in self.active_filters)
        url = f"https://api.opendesktop.org/ocs/v1/content/data/?format=json&search={entry.get_text()}&page={self.current_page}&pagesize=10&categories={cats}"
        self.search_flowbox.build_cells(url)
    
    def clean(self):
        self.search_flowbox.remove_all()


