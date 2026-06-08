# window.py
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

import gi, os
gi.require_version('Xdp', '1.0')
gi.require_version('XdpGtk4', '1.0')
gi.require_version('Soup', '3.0')
gi.require_version('GnomeAutoar', '0.1')
from gi.repository import Gtk, Gdk, Adw, Gio, Xdp, XdpGtk4
from .main_page import MainPage

@Gtk.Template(resource_path='/io/github/swordpuffin/wardrobe/window.ui')
class WardrobeWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'WardrobeWindow'

    page = Gtk.Template.Child()
    back_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.css")).read())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        self.main_page = MainPage(self.page)
        self.page.connect("pushed", self.on_page_pushed)
        self.page.connect("popped", self.on_page_popped)

        self.page.add(self.main_page)
        self.back_button.connect("clicked", self.back_to_menu)
        self.back_button.set_visible(False)
        
    def back_to_menu(self, button):
        if(self.page.get_visible_page_tag() != "main_page"):
            self.page.get_visible_page().clean()
            self.page.remove(self.page.get_visible_page())
            self.page.pop()

    def on_page_pushed(self, page):
        self.back_button.set_visible(True)

    def on_page_popped(self, page, _):
        if(self.page.get_visible_page_tag() == "main_page"):
            self.back_button.set_visible(False)
        if(self.page.find_page("search_page") != None):
            self.page.remove(self.page.find_page("search_page"))
        if(self.page.find_page("install_page") != None):
            self.page.remove(self.page.find_page("install_page"))
                
        
