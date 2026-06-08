# main_page.py
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

import gi, random
from gi.repository import Gtk, Adw
from .utils import soup_get, parse_json
from .search_page import SearchPage
from .theme_page import ThemePage
from .main_page_banner import FeaturedBanner
from .item_carousel import ItemCarousel

class CategoryBox(Gtk.FlowBox):
    def __init__(self, view):
        super().__init__(margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE, max_children_per_line=3, row_spacing=3, column_spacing=3, valign=Gtk.Align.START, homogeneous=True)
        self.view = view
        self.theme_page = ThemePage(view)
    
        icons = [
            "shell-symbolic",
            "icon-symbolic",
            "interface-symbolic",
            "cursor-symbolic",
            "wallpaper-symbolic",
            "search-symbolic",
        ]

        categories = [
            "GNOME Shell",
            "Icons",
            "GTK3/4",
            "Cursors",
            "Wallpapers",
            "Search",
        ]

        for category, icon_name in zip(categories, icons):
            self.insert(self.make_category(category, icon_name), -1)

    def make_category(self, label_text, icon_name):
        box = Gtk.Box(
            spacing=10,
            margin_top=12,
            margin_bottom=12,
            margin_start=12,
            margin_end=12,
            halign=Gtk.Align.CENTER
        )

        icon = Gtk.Image(icon_name=icon_name, pixel_size=20)

        label = Gtk.Label(label=_(label_text), wrap=True, justify=Gtk.Justification.CENTER)
        label.add_css_class("title-4")

        box.append(icon)
        box.append(label)

        button = Gtk.Button(child=box, hexpand=True, vexpand=True)
        button.connect("clicked", self.on_category_clicked, label_text)
        button.add_css_class(icon_name)
        return button

    def on_category_clicked(self, button, category):
        if(category == "Search"):
            search_page = SearchPage(self.view)
            self.view.add(search_page)
            self.view.push(search_page)
        else:
            self.theme_page.category = category
            self.theme_page.make_new_page()
            self.view.push(self.theme_page)

class MainPage(Adw.NavigationPage):
    def __init__(self, view):
        super().__init__(tag="main_page")
        content_box = Gtk.Box(vexpand=True, hexpand=True, orientation=Gtk.Orientation.VERTICAL, spacing=18, margin_bottom=25)
        curated_ids = random.sample(["2299211", "1681315", "1477945", "1166289", "1359276", "1598493", "1197198", "1366182", "1499429", "1209330", "1267246", "1203425"], 8)
        featured_banner = FeaturedBanner()
        featured_banner.page = view
        featured_banner.build_banner(self.get_url(curated_ids[0]))
        curated_ids.pop(0)
        content_box.append(Adw.Clamp(maximum_size=880, child=featured_banner))
        content_box.append(Adw.Clamp(maximum_size=840, child=CategoryBox(view)))
        
        content_box.append(Gtk.Separator())
        carousel_box = Gtk.Box()
        content_box.append(carousel_box)
        carousel_configs = [
            ("Curated", None),
            ("Most Downloaded", "https://api.opendesktop.org/ocs/v1/content/data/?format=json&page=0&&categories=134x386x366x107x261&sortmode=down"),
            ("New & Updated", "https://api.opendesktop.org/ocs/v1/content/data/?format=json&page=0&categories=134x386x366x107x261&sortmode=new"),
        ]

        for topic, url, in carousel_configs:
            title = Gtk.Label(label=_(topic), halign=Gtk.Align.START, margin_start=25, margin_top=25)
            title.add_css_class("title-2")

            carousel = ItemCarousel(self.connect_button)
            carousel.carousel.page = view

            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            box.append(title)
            box.append(carousel)
            content_box.append(Adw.Clamp(maximum_size=1350, child=box))

            if(topic == "Curated"):
                self.curated_carousel = carousel
                for item in curated_ids:
                    soup_get(self.get_url(item), self.make_curated)
            else:
                attr = "down_carousel" if topic == "Most Downloaded" else "new_carousel"
                setattr(self, attr, carousel)
                callback = self.make_new if topic == "New & Updated" else lambda r, c=carousel.carousel: parse_json(r, c)
                soup_get(url, callback)
       
        scroller = Gtk.ScrolledWindow(child=content_box, vexpand=True, hexpand=True)
        self.set_child(scroller)
    
    def connect_button(self, widget, signal, handler, *args):
        widget.connect(signal, handler, *args)
        
    def make_curated(self, response):
        parse_json(response, self.curated_carousel.carousel)

    def make_new(self, response):
        parse_json(response, self.new_carousel.carousel)

    def get_url(self, id):
        return f"https://api.opendesktop.org/ocs/v1/content/data/{id}?format=json"




