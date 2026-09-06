# firefox_gnome_theme.py
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

from pathlib import Path
from configparser import ConfigParser
from .css_templates import DEFAULT_TEMPLATE, FFG_TEMPLATE, COLORED_TEMPLATE, MACOS_TEMPLATE, HIDDEN_TEMPLATE, MINT_TEMPLATE, BREEZE_TEMPLATE

window_control_map = {
    "default": "",
    "colored": COLORED_TEMPLATE,
    "macos": MACOS_TEMPLATE,
    "breeze": BREEZE_TEMPLATE,
    "hidden": HIDDEN_TEMPLATE,
    "mint": MINT_TEMPLATE
}

# This code is taken from the Gradience Project, with adjustments for Rewaita
# Specifically: https://github.com/GradienceTeam/Plugins/blob/main/firefox_gnome_theme.py
class FirefoxGnomeThemePlugin():
    template = ""
    variables = []
    window_controls = ""

    def validate(self):
        return False, None

    def open_settings(self):
        return False

    def reset(self):
        for path in [
            "~/.mozilla/firefox",
            "~/.librewolf",
            "~/.waterfox",
            "~/.var/app/org.mozilla.firefox/.mozilla/firefox",
            "~/.var/app/io.gitlab.librewolf-community/.librewolf",
            "~/.var/app/net.waterfox.waterfox/.waterfox",
            "~/.config/mozilla/firefox"
        ]:
            try:
                directory = Path(path).expanduser()
                cp = ConfigParser()
                cp.read(str(directory / "profiles.ini"))
                results = []
                for section in cp.sections():
                    if not section.startswith("Profile"):
                        continue
                    if cp[section]["IsRelative"] == 0:
                        results.append(Path(cp[section]["Path"]))
                    else:
                        results.append(directory / Path(cp[section]["Path"]))
                for result in results:
                    try:
                        if(Path(f"{result}/chrome/firefox-gnome-theme").exists()):
                            if result.resolve().is_dir():
                                Path(f"{result}/chrome/firefox-gnome-theme/customChrome.css").unlink()
                        else:
                            Path(f"{result}/chrome/rewaitaChrome.css").unlink()
                    except OSError:
                        pass
            except OSError:
                pass
            except StopIteration:
                pass
            except FileExistsError:
                pass

    def apply(self):
        from .utils import Preferences
        prefs = Preferences()
        for path in [
            "~/.mozilla/firefox",
            "~/.librewolf",
            "~/.waterfox",
            "~/.var/app/org.mozilla.firefox/.mozilla/firefox",
            "~/.var/app/io.gitlab.librewolf-community/.librewolf",
            "~/.var/app/net.waterfox.waterfox/.waterfox",
            "~/.config/mozilla/firefox"
        ]:
            try:
                directory = Path(path).expanduser()
                cp = ConfigParser()
                cp.read(str(directory / "profiles.ini"))
                results = []
                for section in cp.sections():
                    if not section.startswith("Profile"):
                        continue
                    if cp[section]["IsRelative"] == 0:
                        results.append(Path(cp[section]["Path"]))
                    else:
                        results.append(directory / Path(cp[section]["Path"]))
                for result in results:
                    try:
                        if result.resolve().is_dir():
                            extra_css = ""
                            if(prefs.get("sharp")):
                                extra_css += "* { border-radius: 0px !important; }"
                            if(prefs.get("transparency")):
                                extra_css += "* { opacity: 96% !important; }"

                            if(Path(f"{result}/chrome/firefox-gnome-theme").exists()):
                                Path(f"{result}/chrome/firefox-gnome-theme").mkdir(mode=0o755, parents=True, exist_ok=True)
                                with open(f"{result}/chrome/firefox-gnome-theme/customChrome.css", "w") as f:
                                    f.write(FFG_TEMPLATE.format(**self.variables) + f"\n{extra_css}")
                                if(Path(f"{result}/chrome/rewaitaChrome.css").exists()):
                                    Path(f"{result}/chrome/rewaitaChrome.css").unlink()
                            else:
                                Path(f"{result}/chrome").mkdir(mode=0o755, parents=True, exist_ok=True)
                                Path(f"{result}/chrome/userChrome.css").touch()
                                Path(f"{result}/user.js").touch()
                                pref_text = "\nuser_pref(\"toolkit.legacyUserProfileCustomizations.stylesheets\", true);\nuser_pref(\"widget.gtk.rounded-bottom-corners.enabled\", true);"
                                with open(f"{result}/user.js", "r") as rf:
                                    if(pref_text not in rf.read()):
                                        with open(f"{result}/user.js", "a") as f:
                                            f.write(pref_text)

                                with open(f"{result}/chrome/rewaitaChrome.css", "w") as f:
                                    f.write(DEFAULT_TEMPLATE.format(**self.variables) + f"\n{window_control_map[self.window_controls].format(**self.variables)}\n{extra_css}")

                                with open(f"{result}/chrome/userChrome.css", "r") as rf:
                                    if("@import \"rewaitaChrome.css\";" not in rf.read()):
                                        with open(f"{result}/chrome/userChrome.css", "a") as f:
                                            f.write("@import \"rewaitaChrome.css\";")
                    except OSError:
                        pass
            except OSError:
                pass
            except StopIteration:
                pass
            except FileExistsError:
                pass
