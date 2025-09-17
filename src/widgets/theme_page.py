import gi, os, re, random, json
from gi.repository import Gtk, Adw, Gdk

def flowbox_sort_func(child1: Gtk.FlowBoxChild, child2: Gtk.FlowBoxChild, _):
    button1 = child1.get_first_child()
    button2 = child2.get_first_child()

    theme1 = button1.theme.lower()
    theme2 = button2.theme.lower()

    if(theme1 < theme2):
        return -1
    elif(theme1 > theme2):
        return 1
    return 0

def load_colors_from_css(file_path):
    colors = {}
    define_re = re.compile(r"@define-color\s+(\S+)\s+([^;]+);")

    with open(file_path, "r") as f:
        for line in f:
            match = define_re.search(line)
            if(match):
                name, color = match.groups()
                colors[name] = color.strip()
    return colors

def create_color_thumbnail_button(colors, name):
    button = Gtk.Button(valign=Gtk.Align.START)
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    frame = Gtk.Frame()
    box.append(frame)
    color_box = Gtk.Box()

    keys_to_show = ["window_bg_color", "window_fg_color", "card_bg_color", "headerbar_bg_color", "dark_1", "light_1", "red_1", "green_1", "blue_1"]
    for key in keys_to_show:
        color = colors.get(key)
        rand = random.randint(0, 10000000)
        if(color):
            color_widget = Gtk.Box(hexpand=True, height_request=40)
            color_widget.add_css_class(f"color-{rand}")
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(f"""
                .color-{rand} {{
                    background-color: {color};
                }}
            """.encode())
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            color_box.append(color_widget)

    box.append(Gtk.Label(margin_bottom=12, margin_top=12, label=name))
    button.set_child(box)
    frame.set_child(color_box)
    return button

class ThemePage(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        help_button = Gtk.Button(label=_("User Guide"), halign=Gtk.Align.CENTER)
        help_button.add_css_class("pill")
        help_button.set_action_name("app.guide")
        self.prepend(help_button)
        for theme_type in ["light", "dark"]:
            self.append(Adw.Clamp(maximum_size=1200, child=Gtk.Separator(margin_start=20, margin_end=20, margin_top=25)))
            reset_button = Gtk.Button(icon_name="reload-symbolic", tooltip_text=_("Reset to default"))
            reset_button.add_css_class("circular")
            reset_button.connect("clicked", parent.on_theme_button_clicked, "Default", theme_type)
            themes = os.listdir(os.path.join(parent.data_dir, theme_type))

            if(theme_type == "light"):
                parent.light_flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
                flowbox = parent.light_flowbox
                parent.light_button = reset_button
            else:
                parent.dark_flowbox = Gtk.FlowBox(column_spacing=12, row_spacing=12, max_children_per_line=3, homogeneous=True, margin_start=12, margin_end=12, selection_mode=Gtk.SelectionMode.NONE)
                flowbox = parent.dark_flowbox
                parent.dark_button = reset_button

            title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.CENTER)
            title = Gtk.Label(label=_(theme_type.capitalize()), margin_end=25)
            title.add_css_class("title-2")
            title_box.append(title); title_box.append(reset_button)
            self.append(title_box)

            for theme in themes:
                colors = load_colors_from_css(os.path.join(parent.data_dir, theme_type, theme))
                btn = create_color_thumbnail_button(colors, theme.replace(".css", ""))
                btn.add_css_class("monospace")
                if(theme == parent.dark_theme and theme_type == "dark"): btn.add_css_class("suggested-action")
                elif(theme == parent.light_theme and theme_type == "light"): btn.add_css_class("suggested-action")
                btn.connect("clicked", parent.on_theme_button_clicked, theme, theme_type)

                #Attributes
                btn.path = os.path.join(parent.data_dir, theme_type, theme)
                btn.func = parent.on_theme_button_clicked
                btn.theme = theme
                btn.theme_type = theme_type

                flowbox.append(btn)

            flowbox.set_sort_func(flowbox_sort_func, None)
            self.append(Adw.Clamp(maximum_size=850, child=flowbox))


