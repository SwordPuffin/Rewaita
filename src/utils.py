import re, gi, os, shutil
from collections import defaultdict
gi.require_version('Xdp', '1.0')
from gi.repository import Gtk, Gdk, GLib, Xdp, Adw

def add_css_provider(css):
    from .window import on_gnome
    if(on_gnome): #Would break on non-gnome system
        settings = Xdp.Portal().get_settings()
        accent = settings.read_string("org.gnome.desktop.interface", "accent-color")
    else:
        accent = "blue" 

    match(accent):
        case("blue"):
            accent_color = "blue_1"
        case("teal"):
            accent_color = "blue_2"
        case("green"):
            accent_color = "green_1"
        case("yellow"):
            accent_color = "yellow_1"
        case("orange"):
            accent_color = "orange_1"
        case("red"):
            accent_color = "red_1"
        case("pink"):
            accent_color = "purple_1"
        case("purple"):
            accent_color = "purple_2"
        case("slate"):
            accent_color = "light_5"

    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(f"""
        {css}
        @define-color accent_bg_color @{accent_color};
        @define-color accent_fg_color @window_bg_color;
    """.encode())
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )

    return accent_color

def parse_gtk_theme(gtk_css, gnome_shell_css, theme_file):
    color_pattern = r'@define-color\s+([a-z0-9_]+)\s+(#[a-fA-F0-9]+|@[a-z0-9_]+);'
    colors = dict()
    references = defaultdict(list)
    accent_color = add_css_provider(gtk_css)

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
    colors["accent_color"] = colors[accent_color]
    items_to_replace = ["window_bg_color", "window_fg_color", "card_bg_color", "headerbar_bg_color", "accent_color", "red_1"]
    for item in items_to_replace:
        gnome_shell_css = gnome_shell_css.replace(item, colors[item])

    gnome_shell_theme_dir = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
    os.makedirs(gnome_shell_theme_dir, exist_ok=True)
    file = shutil.copy2(theme_file, os.path.join(gnome_shell_theme_dir, "gnome-shell.css"))
    with open(file, "w") as f:
        f.write(gnome_shell_css)

def set_to_default(config_dir, theme_type, reset_func):
    if(os.path.exists(os.path.join(config_dir, "gtk.css"))):
        os.remove(os.path.join(config_dir, "gtk.css"))

    gnome_shell_path = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
    if(os.path.exists(os.path.join(gnome_shell_path, "gnome-shell.css"))):
        os.remove(os.path.join(gnome_shell_path, "gnome-shell.css"))

    gtk_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"default-{theme_type}.css")
    gtk_css = open(gtk_file).read()
    add_css_provider(gtk_css)
    reset_func()

def confirm_delete(dialog, response, button, window):
    #Bear with me through the get_first_childs, get_last_childs, and get_parents
    if(response == "confirm"):
        window.toast_overlay.dismiss_all()
        window.toast_overlay.add_toast(Adw.Toast(timeout=3, title=button.get_first_child().get_last_child().get_label() + _(" has been deleted")))
        button.get_parent().get_parent().remove(button.get_parent())
        os.remove(button.path)

def delete_theme(button, window):
    dialog = Adw.AlertDialog()
    button.theme = button.theme.replace('.css', '')
    dialog.set_heading(_("Delete ") + f"{button.theme}?")
    dialog.set_body(_("Are you sure you want to delete that theme?\nThis cannot be undone."))
    
    dialog.add_response("cancel", _("Cancel"))
    dialog.add_response("confirm", _("Delete"))
    dialog.set_response_appearance("confirm", Adw.ResponseAppearance.DESTRUCTIVE)

    dialog.connect("response", confirm_delete, button, window)
    dialog.present(window)
    
def delete_items(action, _, button, window):
    if(button.has_css_class("destructive-action")):
        button.remove_css_class("destructive-action")
        for flowbox in [window.light_flowbox, window.dark_flowbox]:
            for theme in flowbox:
                child = theme.get_first_child()
                if(child.has_css_class("suggested-action")):
                    child.set_sensitive(True)
                    window.light_button.set_sensitive(True); window.dark_button.set_sensitive(True);
                    continue
                child.remove_css_class("destructive-action"); child.remove_css_class("shake")
                child.disconnect_by_func(delete_theme)
                child.connect("clicked", window.on_theme_button_clicked, child.theme, child.theme_type)
    else:
        button.add_css_class("destructive-action")
        for flowbox in [window.light_flowbox, window.dark_flowbox]:
            for theme in flowbox:
                child = theme.get_first_child()
                if(child.has_css_class("suggested-action")):
                    child.set_sensitive(False)
                    window.light_button.set_sensitive(False); window.dark_button.set_sensitive(False);
                    continue
                child.add_css_class("destructive-action")
                child.add_css_class("shake")
                child.add_css_class("monospace")
                child.disconnect_by_func(child.func)
                child.connect("clicked", delete_theme, window)

css = """
    .shake {
        animation: shake_animation 0.4s ease-in-out infinite;
    }

    @keyframes shake_animation {
      0%   { transform: rotate(-0.75deg); }
      25%  { transform: rotate(0.75deg); }
      50%  { transform: rotate(-0.75deg); }
      75%  { transform: rotate(0.75deg); }
      100% { transform: rotate(-0.75deg); }
    }
"""
