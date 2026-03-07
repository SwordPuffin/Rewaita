# window_control_box.py
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

TEMPLATE = """
* {{
  color: {window_fg_color};
}}

:root {{
    --gnome-browser-before-load-background:        {window_bg_color};
    --gnome-accent-bg:                             {accent_color};
    --gnome-accent:                                {accent_color};
    --gnome-window-background:                     {window_bg_color};
    --gnome-window-color:                          {window_fg_color};
    --gnome-tabbar-tab-color:                      {window_fg_color};
    --gnome-tabbar-tab-active-color:               {window_fg_color};
    --gnome-toolbar-background:                    {window_bg_color};
    --gnome-toolbar-color:                         {window_fg_color};
    --gnome-toolbar-icon-fill:                     {window_fg_color};
    --gnome-inactive-window-background:            {window_bg_color};
    --gnome-inactive-toolbar-color:                {window_bg_color};
    --gnome-inactive-toolbar-border-color:         {headerbar_bg_color};
    --gnome-inactive-toolbar-icon-fill:            {window_fg_color};
    --gnome-menu-background:                       {dialog_bg_color};
    --gnome-headerbar-background:                  {headerbar_bg_color};
    --gnome-button-destructive-action-background:  {red_1};
    --gnome-entry-color:                           {view_fg_color};
    --gnome-inactive-entry-color:                  {view_fg_color};
    --gnome-switch-slider-background:              {view_bg_color};
    --gnome-switch-active-slider-background:       {accent_color};
    --gnome-inactive-tabbar-tab-background:        {window_bg_color};
    --gnome-inactive-tabbar-tab-active-background: rgba(255,255,255,0.025);
    --gnome-tabbar-tab-background:                 {card_bg_color};
    --gnome-tabbar-tab-hover-background:           rgba(255,255,255,0.025);
    --gnome-tabbar-tab-active-background:          rgba(255,255,255,0.075);
    --gnome-tabbar-tab-active-hover-background:    rgba(255,255,255,0.100);
    --gnome-tabbar-tab-active-background-contrast: rgba(255,255,255,0.125);

	&:-moz-window-inactive {{
        --gnome-window-color:                      {window_fg_color};
	}}
}}

@-moz-document url-prefix(about:home), url-prefix(about:newtab) {{
 body{{
  --newtab-background-color: #2A2A2E!important;
  --newtab-border-primary-color: rgba(249, 249, 250, 0.8)!important;
  --newtab-border-secondary-color: rgba(249, 249, 250, 0.1)!important;
  --newtab-button-primary-color: #0060DF!important;
  --newtab-button-secondary-color: #38383D!important;
  --newtab-element-active-color: rgba(249, 249, 250, 0.2)!important;
  --newtab-element-hover-color: rgba(249, 249, 250, 0.1)!important;
  --newtab-icon-primary-color: rgba(249, 249, 250, 0.8)!important;
  --newtab-icon-secondary-color: rgba(249, 249, 250, 0.4)!important;
  --newtab-icon-tertiary-color: rgba(249, 249, 250, 0.4)!important;
  --newtab-inner-box-shadow-color: rgba(249, 249, 250, 0.2)!important;
  --newtab-link-primary-color: var(--gnome-accent)!important;
  --newtab-link-secondary-color: #50BCB6!important;
  --newtab-text-conditional-color: #F9F9FA!important;
  --newtab-text-primary-color: var(--gnome-accent)!important;
  --newtab-text-secondary-color: rgba(249, 249, 250, 0.8)!important;
  --newtab-textbox-background-color: var(--gnome-toolbar-background)!important;
  --newtab-textbox-border: var(--gnome-inactive-toolbar-border-color)!important;
  --newtab-textbox-focus-color: #45A1FF!important;
  --newtab-textbox-focus-boxshadow: 0 0 0 1px #45A1FF, 0 0 0 4px rgba(69, 161, 255, 0.3)!important;
  --newtab-feed-button-background: #38383D!important;
  --newtab-feed-button-text: #F9F9FA!important;
  --newtab-feed-button-background-faded: rgba(56, 56, 61, 0.6)!important;
  --newtab-feed-button-text-faded: rgba(249, 249, 250, 0)!important;
  --newtab-feed-button-spinner: #D7D7DB!important;
  --newtab-contextmenu-background-color: #4A4A4F!important;
  --newtab-contextmenu-button-color: #2A2A2E!important;
  --newtab-modal-color: #2A2A2E!important;
  --newtab-overlay-color: rgba(12, 12, 13, 0.8)!important;
  --newtab-section-header-text-color: rgba(249, 249, 250, 0.8)!important;
  --newtab-section-navigation-text-color: rgba(249, 249, 250, 0.8)!important;
  --newtab-section-active-contextmenu-color: #FFF!important;
  --newtab-search-border-color: rgba(249, 249, 250, 0.2)!important;
  --newtab-search-dropdown-color: #38383D!important;
  --newtab-search-dropdown-header-color: #4A4A4F!important;
  --newtab-search-header-background-color: rgba(42, 42, 46, 0.95)!important;
  --newtab-search-icon-color: rgba(249, 249, 250, 0.6)!important;
  --newtab-search-wordmark-color: #FFF!important;
  --newtab-topsites-background-color: #38383D!important;
  --newtab-topsites-icon-shadow: none!important;
  --newtab-topsites-label-color: rgba(249, 249, 250, 0.8)!important;
  --newtab-card-active-outline-color: var(--gnome-toolbar-icon-fill)!important;
  --newtab-card-background-color: var(--gnome-toolbar-background)!important;
  --newtab-card-hairline-color: rgba(249, 249, 250, 0.1)!important;
  --newtab-card-placeholder-color: #4A4A4F!important;
  --newtab-card-shadow: 0 1px 8px 0 rgba(12, 12, 13, 0.2)!important;
  --newtab-snippets-background-color: #38383D!important;
  --newtab-snippets-hairline-color: rgba(255, 255, 255, 0.1)!important;
  --trailhead-header-text-color: rgba(255, 255, 255, 0.6)!important;
  --trailhead-cards-background-color: rgba(12, 12, 13, 0.1)!important;
  --trailhead-card-button-background-color: rgba(12, 12, 13, 0.3)!important;
  --trailhead-card-button-background-hover-color: rgba(12, 12, 13, 0.5)!important;
  --trailhead-card-button-background-active-color: rgba(12, 12, 13, 0.7)!important;
 }}
}}
"""

# This code is taken from the Gradience Project, with adjustments for Rewaita
# Specifically: https://github.com/GradienceTeam/Plugins/blob/main/firefox_gnome_theme.py
class FirefoxGnomeThemePlugin():
    template = TEMPLATE
    variables = []

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
            "~/.var/app/net.waterfox.waterfox/.waterfox"
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
                            Path(f"{result}/chrome/firefox-gnome-theme/customChrome.css").unlink()
                    except OSError:
                        pass
            except OSError:
                pass
            except StopIteration:
                pass
            except FileExistsError:
                pass

    def apply(self):
        for path in [
            "~/.mozilla/firefox",
            "~/.librewolf",
            "~/.waterfox",
            "~/.var/app/org.mozilla.firefox/.mozilla/firefox",
            "~/.var/app/io.gitlab.librewolf-community/.librewolf",
            "~/.var/app/net.waterfox.waterfox/.waterfox"
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
                            Path(f"{result}/chrome/firefox-gnome-theme").mkdir(mode=0o755, parents=True, exist_ok=True)
                            with open(
                                f"{result}/chrome/firefox-gnome-theme/customChrome.css",
                                "w",
                            ) as f:
                                f.write(self.template.format(**self.variables))
                    except OSError:
                        pass
            except OSError:
                pass
            except StopIteration:
                pass
            except FileExistsError:
                pass
