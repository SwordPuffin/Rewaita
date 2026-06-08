import gi, json
from gi.repository import Gtk, Adw, Soup, GLib, Gdk
from .install_page import InstallPage
from .utils import soup_get

class FeaturedBanner(Gtk.Overlay):
    session = Soup.Session()

    def __init__(self):
        super().__init__(height_request=260)
        self.add_css_class("card")
        
        self.background = Gtk.Picture()
        self.background.set_content_fit(Gtk.ContentFit.COVER)
        self.background.add_css_class("rounded")
        self.set_child(self.background)

        self.scrim = Gtk.Box()
        self.add_overlay(self.scrim)

        self.spinner = Gtk.Spinner(spinning=True, halign=Gtk.Align.CENTER, valign=Gtk.Align.CENTER, height_request=40, width_request=40)
        self.add_overlay(self.spinner)

        self.content_row = self.make_content_row()
        self.content_row.set_visible(False)
        self.add_overlay(self.content_row)

        self.add_css_class("featured-banner")

    def make_content_row(self):
        def on_get_clicked(button):
            install_page = InstallPage(self)
            self.page.add(install_page)
            self.page.push(install_page)

        self.title_label = Gtk.Label(label="", xalign=0.0, wrap=True, hexpand=True, max_width_chars=48)
        self.title_label.add_css_class("featured-title")

        self.meta_label = Gtk.Label(label="", xalign=0.0)
        self.meta_label.add_css_class("featured-meta")

        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4, valign=Gtk.Align.END, hexpand=True)
        left_box.append(self.title_label)
        left_box.append(self.meta_label)

        get_button = Gtk.Button(label=_("Get"), valign=Gtk.Align.END)
        get_button.set_css_classes(["pill", "suggested-action", "featured-get-button"])
        get_button.connect("clicked", on_get_clicked)

        row = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
            margin_start=18,
            margin_end=18,
            margin_bottom=16,
            valign=Gtk.Align.END,
            vexpand=True,
        )
        row.append(left_box)
        row.append(get_button)
        return row

    def on_image_loaded(self, session, result):
        data = self.session.send_and_read_finish(result)
        texture = Gdk.Texture.new_from_bytes(data)
        del data
        self.background.set_paintable(texture)
        self.scrim.add_css_class("featured-banner-scrim")

        self.spinner.set_spinning(False)
        self.spinner.set_visible(False)
        self.content_row.set_visible(True)

    def build_banner(self, url):
        def make_ui():
            self.title_label.set_label(self.title)
            self.meta_label.set_label(_("By: ") + self.dev + f"   ↓ {self.downloads}   ★ {self.rating}")

            image_url = self.image_urls[0]
            message = Soup.Message(method="GET", uri=GLib.Uri.parse(image_url, GLib.UriFlags.NONE))
            self.session.send_and_read_async(message, GLib.PRIORITY_DEFAULT, None, self.on_image_loaded)

        def get_params(response):
            if(isinstance(response, str)):
                data = json.loads(response)
            else:
                data = response

            content = data.get("data", [])[0]

            self.title = content.get("name", "Unknown")
            self.home_page = content.get("detailpage", "")
            self.dev = content.get("personid", "Unknown")
            self.rating = int(content.get("score", 0)) / 10 if content.get("score") else 0
            self.last_update = content.get("changed", "")
            self.description = content.get("description", "")
            self.downloads = content.get("downloads", "0") if content.get("downloads") else 0
            self.theme_type = content.get("typeid", 0)

            self.download_links = []
            self.download_names = []

            i = 1
            while(True):
                download_link = content.get(f"downloadlink{i}")
                download_name = content.get(f"downloadname{i}")
                if(download_link is None or download_name is None):
                    break
                if(download_link):
                    if("." not in download_name):
                        i += 1
                        continue
                    self.download_links.append(download_link)
                    self.download_names.append(download_name)
                i += 1

            self.image_urls = []
            z = 1
            while(True):
                preview = content.get(f"previewpic{z}")
                if(preview is None):
                    break
                self.image_urls.append(preview)
                z += 1

            make_ui()

        soup_get(url, get_params)
