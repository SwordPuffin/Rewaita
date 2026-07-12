import gi, shutil, os
gi.require_version("Gtk", "4.0")
gi.require_version('GtkSource', '5')
from gi.repository import Gtk, Gdk, Adw, GLib, GtkSource, Gio
from .theme_page import load_colors_from_css, create_color_thumbnail_button

gnome_colors = {
    "Main Colors": {
        "description": "Used as the main window colors",
        "--window-bg-color": "#222226",
        "--window-fg-color": "#ffffff",
    },
    "Success Colors": {
        "description": "Used to indicate successful actions or high levels",
        "--success-color": "#78e9ab",
        "--success-bg-color": "#26a269",
        "--success-fg-color": "#ffffff",
    },
    "Destructive Colors": {
        "description": "Used on buttons to indicate destruction or dangerous actions like deleting files",
        "--destructive-color": "#ff938c",
        "--destructive-bg-color": "#c01c28",
        "--destructive-fg-color": "#ffffff",
    },
    "Warning Colors": {
        "description": "Used on a variety of widgets to indicate warnings or caution",
        "--warning-color": "#ffc252",
        "--warning-bg-color": "#cd9309",
        "--warning-fg-color": "#000000",
    },
    "Interface Colors": {
        "description": "Used on most background UI elements like text-views, buttons, and headerbars",
        "--view-bg-color": "#1d1d20",
        "--view-fg-color": "#ffffff",
        "--headerbar-bg-color": "#2e2e32",
        "--headerbar-fg-color": "#ffffff",
        "--card-bg-color": "#252525",
        "--card-fg-color": "#ffffff",
    },
    "Named Colors": {
        "description": "Array of palette colors, used to separate UI elements and to give your theme some character",
        "--blue-1": "#99c1f1",
        "--blue-2": "#62a0ea",
        "--green-1": "#8ff0a4",
        "--yellow-1": "#f9f06b",
        "--orange-1": "#ffbe6f",
        "--red-1": "#f66151",
        "--purple-1": "#dc8add",
        "--purple-2": "#c061cb",
        "--brown-1": "#cdab8f",
        "--light-1": "#ffffff",
        "--light-5": "#9a9996",
        "--dark-1": "#77767b",
    }
}
titles = {
    "--window-bg-color": "Window Background Color",
    "--window-fg-color": "Window Text Color",
    "--success-color": "Standalone Color",
    "--success-bg-color": "Background Color",
    "--success-fg-color": "Text Color",
    "--destructive-color": "Standalone Color",
    "--destructive-bg-color": "Background Color",
    "--destructive-fg-color": "Text Color",
    "--warning-color": "Standalone",
    "--warning-bg-color": "Background Color",
    "--warning-fg-color": "Text Color",
    "--view-bg-color": "Text View Background Color",
    "--view-fg-color": "Text Color",
    "--headerbar-bg-color": "Headerbar Background Color",
    "--headerbar-fg-color": "Text Color",
    "--card-bg-color": "Button/Frame Background Color",
    "--card-fg-color": "Text Color",
    "--blue-1": "Blue",
    "--blue-2": "Teal",
    "--green-1": "Green",
    "--yellow-1": "Yellow",
    "--orange-1": "Orange",
    "--red-1": "Red",
    "--purple-1": "Pink",
    "--purple-2": "Purple",
    "--brown-1": "Brown",
    "--light-1": "Light",
    "--light-5": "Slate",
    "--dark-1": "Dark",
}
rgba_pickers = []

class ColorRow(Adw.ActionRow):
    def __init__(self, title: str, variable: str, default_color: str):
        super().__init__(selectable=False)
        self.set_title(title)
        self.set_subtitle(variable)

        rgba = Gdk.RGBA()
        rgba.parse(default_color)
        self.color_button = Gtk.ColorButton()
        self.color_button.set_rgba(rgba)
        self.color_button.variable = variable
        rgba_pickers.append(self.color_button)

        end_box = Gtk.Box(spacing=6)
        end_box.append(self.color_button)

        self.add_suffix(end_box)

class CustomBundle(Gtk.Box):
    def __init__(self, title, bundle):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_start=12, margin_end=12)
        self.prepend(title)
        title.add_css_class("title-4")
        colors = gnome_colors[title.get_label()]
        description_label = Gtk.Label(label=colors["description"], wrap=True)
        description_label.add_css_class("dimmed")
        self.append(description_label)
        listbox = Gtk.ListBox(valign=Gtk.Align.CENTER)
        listbox.add_css_class("boxed-list")
        for color in colors.keys():
            if(color == 'description'): continue
            row = ColorRow(titles[color], color, colors[color])
            listbox.append(row)
        self.append(listbox)

class CustomPage(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20, margin_top=20)

        main_label = Gtk.Label(label=_("Main Colors"))
        success_label = Gtk.Label(label=_("Success Colors"))
        destructive_label = Gtk.Label(label=_("Destructive Colors"))
        warning_label = Gtk.Label(label=_("Warning Colors"))
        interface_label = Gtk.Label(label=_("Interface Colors"))
        colors_label = Gtk.Label(label=_("Named Colors"))

        for bundle, title in zip(gnome_colors.keys(), [main_label, success_label, destructive_label, warning_label, interface_label, colors_label]):
            self.append(CustomBundle(title, bundle))

        name_box = Gtk.Box(halign=Gtk.Align.CENTER, spacing=12)
        name_entry = Gtk.Entry(placeholder_text=_("Name (required)"), hexpand=True)
        name_entry.connect("changed", self.entry_changed)
        name_entry.add_css_class("error")
        name_box.append(name_entry)

        light_radio = Adw.Toggle(label=_("Light"))
        dark_radio = Adw.Toggle(label=_("Dark"))
        group = Adw.ToggleGroup(halign=Gtk.Align.START)
        group.add(light_radio)
        group.add(dark_radio)
        group.add_css_class("round")
        name_box.append(group)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        label = Gtk.Label(label=_("Save Folder"))
        icon = Gtk.Image.new_from_icon_name("folder-symbolic")
        box.append(label); box.append(icon)
        open_folder_button = Gtk.Button(child=box, halign=Gtk.Align.CENTER)
        open_folder_button.set_css_classes(["suggested-action", "pill"])
        folder = Gio.File.new_for_path(GLib.get_user_data_dir())
        open_folder_button.connect("clicked", lambda d : Gio.AppInfo.launch_default_for_uri(folder.get_uri(), None))
        self.save_button = Gtk.Button(label=_("Save"), sensitive=False, margin_bottom=12, margin_start=12, margin_end=12)
        self.save_button.connect("clicked", self.save_theme, parent, name_entry, group)

        GtkSource.init()
        css_entry = GtkSource.View(auto_indent=True, indent_width=2, show_line_numbers=True)
        self.buffer = GtkSource.Buffer(text=_("/* Enter any extra CSS here */"))

        scheme_manager = GtkSource.StyleSchemeManager.get_default()
        scheme = scheme_manager.get_scheme("Adwaita")
        if(scheme):
            self.buffer.set_style_scheme(scheme)

        language_manager = GtkSource.LanguageManager.get_default()
        language = language_manager.get_language("css")
        self.buffer.set_language(language)
        css_entry.set_buffer(self.buffer)

        self.append(name_box)
        self.append(Gtk.ScrolledWindow(child=css_entry, height_request=240))
        self.append(open_folder_button)
        self.append(self.save_button)

    def entry_changed(self, entry):
        if(entry.get_text() == ''):
            self.save_button.set_sensitive(False)
            entry.add_css_class("error")
        else:
            self.save_button.set_sensitive(True)
            entry.remove_css_class("error")

    def on_emoji_picked(self, emojipicker, emoji, entry):
        entry.set_label(emoji)

    def save_theme(self, button, parent, entry, radio_group):
        parent.toast_overlay.add_toast(Adw.Toast(timeout=3, title=entry.get_text() + _(" has been saved")))

        theme_type = ["light", "dark"][radio_group.get_active()]

        src_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom-template.css")
        src_file_text = open(src_file).read()
        for color in rgba_pickers:
            rgb = color.get_rgba()
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb.red * 255),
                int(rgb.green * 255),
                int(rgb.blue * 255)
            )
            src_file_text = src_file_text.replace(f"var({color.variable})", hex_color)
        src_file_text += self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(), True)
        os.makedirs(os.path.join(parent.data_dir, theme_type), exist_ok=True)
        theme_file = os.path.join(parent.data_dir, theme_type, entry.get_text() + ".css")
        shutil.copyfile(src_file, theme_file)
        with open(theme_file, "w") as file:
            file.write(src_file_text)

        match(theme_type):
            case("light"):
                flowbox = parent.light_flowbox
            case("dark"):
                flowbox = parent.dark_flowbox

        colors = load_colors_from_css(theme_file)
        new_button = create_color_thumbnail_button(colors, entry.get_text(), flowbox.snippet)
        new_button.connect("clicked", parent.on_theme_button_clicked, entry.get_text() + ".css", theme_type)

        #Attributes
        new_button.func = parent.on_theme_button_clicked
        new_button.path = os.path.join(parent.data_dir, theme_type, entry.get_text() + ".css")
        new_button.theme_type = theme_type
        new_button.theme = entry.get_text()
        new_button.default = False

        already_exists = False
        for button in flowbox:
            if(button.get_first_child().theme == new_button.theme):
                already_exists = True

        if(not already_exists):
            flowbox.insert(new_button, -1)
            flowbox.invalidate_sort()
