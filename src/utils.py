# utils.py
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

import gi, os, random, json
from gi.repository import GnomeAutoar, Soup, GLib, Gtk, Gdk, Gio, Adw
from html.parser import HTMLParser
from pathlib import Path

def soup_get(url, response_func):
    def on_response(session, result):
        response_bytes = session.send_and_read_finish(result)
        try:
            response_text = response_bytes.get_data().decode()
        except:
            response_text = response_bytes.get_data()
        response_func(response_text)
    session = Soup.Session()
    message = Soup.Message.new("GET", url)
    session.send_and_read_async(message, GLib.PRIORITY_DEFAULT, None, on_response)

def match_theme_type(typeid):
    category_map = {
        134: 0, 386: 1, 199: 1, 132: 1, 366: 2, 135: 2, 136: 2,
        107: 3, 300: 4, 286: 4, 312: 4, 261: 4, 299: 4, 283: 4, 360: 4,
        287: 4
    }
    return category_map.get(int(typeid), int(typeid))

def is_picture(file):
    if(any(ext in file for ext in [".png", ".jpg", ".svg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".tif", ".jxl"])):
        return True
    else:
        return False

def search_for_images(folders):
    return_val = []
    for folder in folders:
        if(os.path.isdir(folder)):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if(is_picture(file)):
                        return_val.append(os.path.join(root, file))
        else:
            return_val.append(folder)
    return return_val

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, data):
        self.result.append(data)

    def handle_starttag(self, tag, attrs):
        if(tag in ("p", "div", "br", "li")):
            self.result.append("\n")

    def handle_endtag(self, tag):
        if(tag in ("p", "div", "li")):
            self.result.append("\n")

    def get_data(self):
        return ''.join(self.result)

def strip_html(source):
    parser = HTMLStripper()
    parser.feed(source)
    return parser.get_data()

def resolve_issues(archive_path, typeid, change_func):
    archive_file = Gio.File.new_for_path(archive_path)
    output = os.path.dirname(archive_file)
    from .install_page import folders as theme_dirs
    theme_dir = os.path.dirname(theme_dirs[typeid])
    gio_output = Gio.File.new_for_path(output)
    before = set(os.listdir(output))
    def arrange_folders(extractor):
        print("Extraction Complete")
        folders = {
            0: ["gnome-shell"],
            1: ["index.theme"],
            2: ["gtk-2.0", "gnome-shell", "gtk-3.0", "gtk-4.0", "cinnamon", "xfwm4", "index.theme"],
            3: ["cursors", "cursors_scalable", "index.theme"]
        }

        after = set(os.listdir(output))
        added = set()
        for item in after - before:
            item_path = os.path.join(output, item)
            if(os.path.isdir(item_path)):
                added.add(item_path)

        if(typeid == 4):
            change_func(added, search_for_images(added))
            return
        else:
            important_items = folders.get(typeid)

        # I can't tell if this code is very good or very bad
        important_paths = set()
        linked_paths = set()
        for folder in added:
            for root, dirs, files in os.walk(folder, topdown=False):
                for folder_name in important_items:
                    if(folder_name == "index.theme"):
                        search = files
                    else:
                        search = dirs
                    for item in search:
                        if(item == folder_name):
                            important_paths.add(os.path.dirname(os.path.join(root, item)))
        if(typeid != 1):
            for path in important_paths:
                try:
                    os.symlink(path, os.path.join(theme_dir, os.path.basename(path)))
                except:
                    continue
            linked_paths = important_paths
        else:
            for path in important_paths:
                extension = ""
                folder = os.path.basename(path)
                if('dark' in folder.lower()):
                    extension = '-dark'
                elif('light' in folder.lower()):
                    extension = '-light'

                parent_name = os.path.basename(os.path.dirname(path)).lower()
                correct_folder_name = folder.lower().replace(extension, '')

                if(parent_name in correct_folder_name):
                    new_folder_name = correct_folder_name + extension
                elif(correct_folder_name in parent_name):
                    new_folder_name = parent_name + extension
                else:
                    new_folder_name = folder.lower() + '-' + str(random.randint(1, 1000))

                new_path = os.path.join(theme_dir, os.path.basename(new_folder_name))
                os.symlink(path, new_path)
                
                linked_paths.add(new_path)
        change_func(added, linked_paths)

    if(is_picture(archive_path)):
        change_func([archive_path], [archive_path])
    extractor = GnomeAutoar.Extractor.new(archive_file, gio_output)
    extractor.set_delete_after_extraction(True)

    extractor.start_async()
    extractor.connect("completed", arrange_folders)

def parse_json(response, flowbox):
    from .theme_cell import ThemeCell
    
    if(isinstance(response, str)):
        data = json.loads(response)
    else:
        data = response
            
    content = data.get("data", [])
            
    for item in content:
        cell = ThemeCell()
        cell.page = flowbox.page

        cell.title = item.get("name", "Unknown")
        cell.home_page = item.get("detailpage", "")
        cell.dev = item.get("personid", "Unknown")
        cell.rating = int(item.get("score", 0)) / 10 if item.get("score") else 0
        cell.last_update = item.get("changed", "")
        cell.description = item.get("description", "")
        cell.downloads = item.get("downloads", "0") if item.get("downloads") else 0
        cell.theme_type = item.get("typeid", 0)

        # Get download links
        cell.download_links = []
        cell.download_names = []

        i = 1
        while(True):
            download_link = item.get(f"downloadlink{i}")
            download_name = item.get(f"downloadname{i}")

            if(download_link is None or download_name is None):
                break

            if(download_link):
                if("." not in download_name):
                    i += 1
                    continue
                cell.download_links.append(download_link)
                cell.download_names.append(download_name)

            i += 1

        # Get image links
        cell.image_urls = []
        z = 1
        while(True):
            preview = item.get(f"previewpic{z}")
            if(preview is None):
                break
            cell.image_urls.append(preview)
            z += 1
        cell.build_cell()
        flowbox.append(Adw.Clamp(child=cell, maximum_size=375))
                
        if(hasattr(flowbox, "get_n_pages")):
            if(flowbox.get_n_pages() == 7):
                mid = flowbox.get_n_pages() // 2
                def scroll(attempts=0):
                    page = flowbox.get_nth_page(mid)
                    if(page is None or attempts > 20):
                        return False
                    flowbox.scroll_to(page, False)
                    if(round(flowbox.get_position()) != mid):
                        GLib.timeout_add(20, scroll, attempts + 1)
                    return False
                GLib.idle_add(scroll)
                break
        
    if(hasattr(flowbox, "group")):
        flowbox.group.set_sensitive(True)
    
    
