import re, gi, os, shutil
from collections import defaultdict
from gi.repository import Gtk, Gdk, GLib

def parse_gtk_theme(gtk_css, gnome_shell_css, theme_file):
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(f"""
        {gtk_css}
    """.encode())
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )
    color_pattern = r'@define-color\s+([a-z0-9_]+)\s+(#[a-fA-F0-9]+|@[a-z0-9_]+);'
    colors = dict()
    references = defaultdict(list)

    for match in re.finditer(color_pattern, gtk_css):
        name, value = match.groups()
        if(value.startswith('@')):
            ref_name = value[1:]
            references[ref_name].append(name)
        else:
            colors[name] = value

    for ref_name, dependent_names in references.items():
        if(ref_name in colors):
            for name in dependent_names:
                colors[name] = colors[ref_name]

    items_to_replace = ["window_bg_color", "window_fg_color", "card_bg_color", "headerbar_bg_color", "blue_1", "red_1"]
    for item in items_to_replace:
        gnome_shell_css = gnome_shell_css.replace(item, colors[item])

    if(GLib.getenv("HOST_XDG_DATA_HOME") == None):
        GLib.setenv("HOST_XDG_DATA_HOME", os.path.join(GLib.getenv("HOME"), ".local", "share"), True)

    gnome_shell_theme_dir = os.path.join(GLib.getenv("HOST_XDG_DATA_HOME"), "themes")
    os.makedirs(os.path.join(gnome_shell_theme_dir, "rewaita/gnome-shell"), exist_ok=True)
    rewaita_theme_dir = os.path.join(gnome_shell_theme_dir, "rewaita/gnome-shell")
    file = shutil.copyfile(theme_file, os.path.join(rewaita_theme_dir, "gnome-shell.css"))
    with open(file, "w") as f:
        f.write(gnome_shell_css)



