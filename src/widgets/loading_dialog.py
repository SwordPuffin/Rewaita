# loading_dialog.py
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

from gi.repository import Adw, Gtk

class LoadingDialog(Adw.Dialog):
    def __init__(self, parent):
        super().__init__(can_close=False)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin_top=24, margin_bottom=24, margin_start=24, margin_end=24, valign=Gtk.Align.CENTER, halign=Gtk.Align.CENTER)

        spinner = Gtk.Spinner(spinning=True)
        spinner.set_size_request(40, 40)

        label = Gtk.Label(label=_("This may take a moment"))
        label.add_css_class("title-4")

        box.append(label)
        box.append(spinner)

        self.set_child(box)
