import gi, os, shutil
from gi.repository import Gtk, Adw, GLib, Xdp
from .extra_options_box import OptionsBox
from .accent_box import AccentBox
from .utils import change_autostart

class PrefPage(Gtk.Box):
    def __init__(self, win):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.CENTER, spacing=32, margin_start=12, margin_end=12)

        if(not "GNOME" in GLib.getenv("XDG_CURRENT_DESKTOP") or ""):
            self.append(Adw.Clamp(maximum_size=800, child=AccentBox(win)))
        self.append(OptionsBox(win))
        prefs_page = Adw.PreferencesGroup()
        prefs_page.set_title(_("Preferences"))

        toggle_group = Adw.PreferencesGroup()
        prefs_page.add(toggle_group)

        for title in [
            ("Generate GTK-3.0 Theme", "Highly recommended for all users"),
            ("Generate GNOME Shell Theme", "For GNOME users"),
            ("Generate Firefox CSS Theme", "May conflict with existing theme"),
            ("Run in background", "For users who swap between light/dark mode")
        ]:
            if(title[0] == "Generate GTK-3.0 Theme"):
                state = win.modify_gtk3_theme
                def state_function(value): win.modify_gtk3_theme = value
            elif(title[0] == "Generate GNOME Shell Theme"):
                state = win.modify_gnome_shell
                def state_function(value): win.modify_gnome_shell = value
            elif(title[0] == "Generate Firefox CSS Theme"):
                state = win.firefox_theme
                def state_function(value): win.firefox_theme = value
            else:
                state = win.run_in_background
                def state_function(value): win.run_in_background = value
            row = Adw.SwitchRow(title=_(title[0]), subtitle=_(title[1]), active=state)
            row.connect("notify::active", self.on_pref_toggle_switched, title[0], win, state_function)
            toggle_group.add(row)

        self.append(prefs_page)

    def on_pref_toggle_switched(self, switch, _pspec, title, win, state_function):
        state = switch.get_active()
        state_function(state)
        win.save_prefs()
        if(title == "Generate GTK-3.0 Theme"):
            if(not state):
                self.clear_theme(None, "gtk-3.0", win)
            else:
                win.on_theme_selected()
        elif(title == "Generate GNOME Shell Theme"):
            self.clear_gnome_shell(state, win)
        elif(title == "Run in background"):
            change_autostart(state)
        else:
            win.on_theme_selected()

    def clear_theme(self, button, folder, win):
        folder_path = os.path.join(GLib.getenv("HOME"), ".config", folder)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if(os.path.isfile(file_path) or os.path.islink(file_path)):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to clear folder: ' + e)

    def clear_gnome_shell(self, state, win):
        from .window import reset_shell
        if(not state):
            folder_path = os.path.join(GLib.getenv("HOME"), ".local", "share", "themes", "rewaita", "gnome-shell")
            if(os.path.exists(folder_path)):
                shutil.rmtree(folder_path)
                reset_shell()
        else:
            win.on_theme_selected()
