import gi, os, shutil
from gi.repository import Gtk, Adw, GLib
from .window import reset_shell

class ToggleRow(Adw.ActionRow):
    def __init__(self, title, win, parent):
        super().__init__()
        self.set_title(_(title[0]))
        self.set_subtitle(_(title[1]))

        if(title[0] == "Generate GTK-3.0 Theme"):
            state = win.modify_gtk3_theme
        elif(title[0] == "Generate Gnome Shell Theme"):
            state = win.modify_gnome_shell
        else:
            state = win.run_in_background

        toggle = Gtk.Switch(valign=Gtk.Align.CENTER)
        toggle.set_active(state)
        toggle.connect("state_set", parent.on_pref_toggle_switched, title[0], win)
        self.add_suffix(toggle)

class PrefDialog(Adw.PreferencesDialog):
    def __init__(self, win):
        super().__init__()
        toggle_group = Adw.PreferencesGroup()
        page = Adw.PreferencesPage()
        page.add(toggle_group)

        # clear_box = Gtk.Box(hexpand=True, halign=Gtk.Align.CENTER, spacing=10, margin_top=8)
        # clear_box.add_css_class("error")

        # clear_gtk3_button = Gtk.Button(label=_("Clear GTK-3.0 theme"))
        # clear_gtk3_button.connect("clicked", self.clear_theme, "gtk-3.0", win)
        # clear_box.append(clear_gtk3_button)

        # clear_gtk4_button = Gtk.Button(label=_("Clear GTK-4.0 theme"))
        # clear_gtk4_button.connect("clicked", self.clear_theme, "gtk-4.0", win)
        # clear_box.append(clear_gtk4_button)

        # toggle_group.add(clear_box)

        for title in [("Generate GTK-3.0 Theme", "Highly recommended for all users"), ("Generate Gnome Shell Theme", "For Gnome users"), ("Run in background", "For users who swap between light/dark mode")]:
            toggle_group.add(ToggleRow(title, win, self))
        self.add(page)

    def on_pref_toggle_switched(self, switch, state, title, win):
        if(title == "Generate GTK-3.0 Theme"):
            win.modify_gtk3_theme = bool(state)
            if(not state):
                self.clear_theme(None, "gtk-3.0", win)
            else:
                win.on_theme_selected()
        elif(title == "Generate Gnome Shell Theme"):
            win.modify_gnome_shell = bool(state)
            self.clear_gnome_shell(bool(state), win)
        elif(title == "Run in background"):
            win.run_in_background = bool(state)
            self.change_autostart(bool(state))

        win.save_prefs()

    def clear_theme(self, button, folder, win):
        folder_path = os.path.join(GLib.getenv("HOME"), ".config", folder)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to clear folder: ' + e)

    def clear_gnome_shell(self, state, win):
        if(not state):
            folder_path = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
            if(os.path.exists(folder_path)):
                shutil.rmtree(folder_path)
                reset_shell()
        else:
            win.on_theme_selected()

    def change_autostart(self, state):
        if(state == False):
            path = os.path.join(GLib.getenv("HOME"), ".config", "autostart", "rewaita.desktop")
            if(os.path.exists(path)):
                os.remove(os.path.join(GLib.getenv("HOME"), ".config", "autostart", "rewaita.desktop"))
        else:
            with open(os.path.join(GLib.getenv("HOME"), ".config", "autostart", "rewaita.desktop"), "w") as file:
                file.write("""
[Desktop Entry]
Type=Application
Name=io.github.swordpuffin.rewaita
X-XDP-Autostart=io.github.swordpuffin.rewaita
Exec=flatpak run io.github.swordpuffin.rewaita --background
DBusActivatable=true
X-Flatpak=io.github.swordpuffin.rewaita
                """
                )
