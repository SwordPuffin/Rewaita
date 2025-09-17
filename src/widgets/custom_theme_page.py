import gi, shutil, os
gi.require_version("Gtk", "4.0")
gi.require_version('GtkSource', '5')
from gi.repository import Gtk, Gdk, Adw, GLib, GtkSource
from .theme_page import load_colors_from_css, create_color_thumbnail_button

#Stripped down colors for the time being
gnome_colors = {
    "Accent Colors": {
        "description": "Used on a variety of widgets to indicate importance or activity",
        "accent_color": "#3584e4",
        "accent_bg_color": "#3584e4",
        "accent_fg_color": "#ffffff",
    },
    "Main Colors": {
        "description": "Used as the main window colors",
        "window_bg_color": "#222226",
        "window_fg_color": "#ffffff",
    },
    "Success Colors": {
        "description": "Used to indicate successful actions or high levels",
        "success_color": "#78e9ab",
        "success_bg_color": "#26a269",
        "success_fg_color": "#ffffff",
    },
    "Destructive Colors": {
        "description": "Used on buttons to indicate destruction or dangerous actions like deleting files",
        "destructive_color": "#ff938c",
        "destructive_bg_color": "#c01c28",
        "destructive_fg_color": "#ffffff",
    },
    "Warning Colors": {
        "description": "Used on a variety of widgets to indicate warnings or caution",
        "warning_color": "#ffc252",
        "warning_bg_color": "#cd9309",
        "warning_fg_color": "#000000",
    },
    "Interface Colors": {
        "description": "Used on most background UI elements like text-views, buttons, and headerbars",
        "view_bg_color": "#1d1d20",
        "view_fg_color": "#ffffff",
        "headerbar_bg_color": "#2e2e32",
        "headerbar_fg_color": "#ffffff",
        "card_bg_color": "#252525",
        "card_fg_color": "#ffffff",
    },
    "Named Colors": {
        "description": "Array of palette colors, used to separate UI elements and to give your theme some character",
        "blue_1": "#99c1f1",
        "blue_2": "#62a0ea",
        "green_1": "#8ff0a4",
        "yellow_1": "#f9f06b",
        "orange_1": "#ffbe6f",
        "red_1": "#f66151",
        "purple_1": "#dc8add",
        "purple_2": "#c061cb",
        "brown_1": "#cdab8f",
        "light_1": "#ffffff",
        "light_5": "#9a9996",
        "dark_1": "#77767b",
    }
}

titles = {
    "accent_color": "Standalone Color",
    "accent_bg_color": "Background Color",
    "accent_fg_color": "Text Color",
    "window_bg_color": "Window Background Color",
    "window_fg_color": "Window Text Color",
    "success_color": "Standalone Color",
    "success_bg_color": "Background Color",
    "success_fg_color": "Text Color",
    "destructive_color": "Standalone Color",
    "destructive_bg_color": "Background Color",
    "destructive_fg_color": "Text Color",
    "warning_color": "Standalone",
    "warning_bg_color": "Background Color",
    "warning_fg_color": "Text Color",
    "view_bg_color": "Text View Background Color",
    "view_fg_color": "Text Color",
    "headerbar_bg_color": "Headerbar Background Color",
    "headerbar_fg_color": "Text Color",
    "card_bg_color": "Button/Frame Background Color",
    "card_fg_color": "Text Color",
    "blue_1": "Blue",
    "blue_2": "Teal",
    "green_1": "Green",
    "yellow_1": "Yellow",
    "orange_1": "Orange",
    "red_1": "Red",
    "purple_1": "Pink",
    "purple_2": "Purple",
    "brown_1": "Brown",
    "light_1": "Light",
    "light_5": "Slate",
    "dark_1": "Dark",
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
    def __init__(self, title: Gtk.Label, bundle: str):
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

        accent_label = Gtk.Label(label=_("Accent Colors"))
        main_label = Gtk.Label(label=_("Main Colors"))
        success_label = Gtk.Label(label=_("Success Colors"))
        destructive_label = Gtk.Label(label=_("Destructive Colors"))
        warning_label = Gtk.Label(label=_("Warning Colors"))
        interface_label = Gtk.Label(label=_("Interface Colors"))
        colors_label = Gtk.Label(label=_("Named Colors"))

        for bundle, title in zip(gnome_colors.keys(), [accent_label, main_label, success_label, destructive_label, warning_label, interface_label, colors_label]):
            self.append(CustomBundle(title, bundle))

        name_entry = Gtk.Entry(placeholder_text=_("Theme name (required)"), width_request=171)
        name_entry.connect("changed", self.entry_changed)
        name_entry.add_css_class("error")
        emoji_chooser = Gtk.EmojiChooser()
        emoji_entry = Gtk.MenuButton(label=_("Emoji (optional)"), popover=emoji_chooser)
        emoji_chooser.connect("emoji-picked", self.on_emoji_picked, emoji_entry)
        entry_box = Gtk.Box(spacing=12, halign=Gtk.Align.CENTER, orientation=Gtk.Orientation.HORIZONTAL); entry_box.append(name_entry); entry_box.append(emoji_entry)

        mode_label = Gtk.Label(label=_("Theme Type"), xalign=0.5); mode_label.add_css_class("title-4")
        light_radio = Gtk.CheckButton(label=_("Light"), group=None, active=True)
        dark_radio = Gtk.CheckButton(label=_("Dark"), group=light_radio)

        mode_box = Gtk.Box(spacing=6, halign=Gtk.Align.CENTER)
        mode_box.append(light_radio)
        mode_box.append(dark_radio)

        self.append(mode_label)
        self.append(mode_box)
        self.append(entry_box)

        self.append(Gtk.Label(wrap=True, label=_(f"*Themes will be saved to: ") + GLib.get_user_data_dir()))
        self.save_button = Gtk.Button(label=_("Save"), sensitive=False, margin_bottom=12, margin_start=12, margin_end=12)
        self.save_button.connect("clicked", self.save_theme, parent, name_entry, light_radio, emoji_entry)

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

        self.append(Gtk.ScrolledWindow(child=css_entry, height_request=240))
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

    def save_theme(self, button, parent, entry, light_radio, emoji_entry):
        parent.toast_overlay.add_toast(Adw.Toast(timeout=3, title=entry.get_text() + _(" has been saved")))

        if(light_radio.get_active()):
            theme_type = "light"
        else:
            theme_type = "dark"

        src_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom-template.css")
        src_file_text = open(src_file).read()
        for color in rgba_pickers:
            rgb = color.get_rgba()
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb.red * 255),
                int(rgb.green * 255),
                int(rgb.blue * 255)
            )
            src_file_text = src_file_text.replace("@" + color.variable, hex_color)
        src_file_text += self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(), True)
        os.makedirs(os.path.join(parent.data_dir, theme_type), exist_ok=True)
        if(emoji_entry.get_label() == "Emoji (optional)"):
            emoji = ""
        else:
            emoji = emoji_entry.get_label()
        theme_file = os.path.join(parent.data_dir, theme_type, (entry.get_text() + " " + emoji + ".css"))
        shutil.copyfile(src_file, theme_file)
        with open(theme_file, "w") as file:
            file.write(src_file_text)

        colors = load_colors_from_css(theme_file)
        new_button = create_color_thumbnail_button(colors, (entry.get_text() + " " + emoji))
        new_button.connect("clicked", parent.on_theme_button_clicked, (entry.get_text() + " " + emoji + ".css"), theme_type)

        #Attributes
        new_button.func = parent.on_theme_button_clicked
        new_button.path = os.path.join(parent.data_dir, theme_type, (entry.get_text() + " " + emoji + ".css"))
        new_button.theme_type = theme_type
        new_button.theme = entry.get_text()

        match(theme_type):
            case("light"):
                flowbox = parent.light_flowbox
            case("dark"):
                flowbox = parent.dark_flowbox

        flowbox.insert(new_button, -1)
        flowbox.invalidate_sort()

