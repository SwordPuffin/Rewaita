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
DEFAULT_TEMPLATE = """
:root {{
  --window_bg_color:   {window_bg_color};
  --window_fg_color:   {window_fg_color};
  --view_bg_color:     {view_bg_color};
  --view_fg_color:     {view_fg_color};
  --headerbar_bg_color:{headerbar_bg_color};
  --headerbar_fg_color:{headerbar_fg_color};
  --popover_bg_color:  {popover_bg_color};
  --popover_fg_color:  {popover_fg_color};
  --card_bg_color:     {card_bg_color};
  --card_fg_color:     {card_fg_color};
  --sidebar_bg_color:  {sidebar_bg_color};
  --sidebar_fg_color:  {sidebar_fg_color};
  --dark_1:            {dark_1};
  --brown_1:           {brown_1};
  --light_1:           {light_1};
  --blue_1:            {blue_1};
  --blue_2:            {blue_2};
  --green_1:           {green_1};
  --yellow_1:          {yellow_1};
  --orange_1:          {orange_1};
  --red_1:             {red_1};
  --purple_1:          {purple_1};
  --purple_2:          {purple_2};
  --accent_color:      {accent_color};
}}

#main-window,
#browser {{
  background-color: var(--headerbar_bg_color) !important;
  color: var(--window_fg_color) !important;
}}

#star-button {{
	&[starred] {{
		fill: var(--accent_color) !important;
	}}
}}

input[type="checkbox"],
checkbox:not(.treenode-checkbox) > .checkbox-check {{
  appearance: none !important;
	border: 0 !important;
	border-radius: 6px !important;
	background-color: var(--window_bg_color) !important;
	color: var(--window_fg_color) !important;
	height: 20px !important;
	width: 20px !important;
}}

input[type="checkbox"]:checked,
checkbox:not(.treenode-checkbox) > .checkbox-check[checked] {{
	background-color: var(--accent_color) !important;
	background-image: -moz-symbolic-icon(checkmark-symbolic) !important;
	background-size: 14px !important;
	background-repeat: no-repeat;
	background-position: center;
	color: var(--window_bg_color) !important;
	-moz-context-properties: fill;
}}

#nav-bar,
#navigator-toolbox,
#toolbar-menubar,
.browser-toolbar {{
  background-color: var(--headerbar_bg_color) !important;
  color: var(--headerbar_fg_color) !important;
  border-color: var(--dark_1) !important;
}}

#TabsToolbar,
.tabbrowser-arrowscrollbox {{
  background-color: var(--window_bg_color) !important;
}}

.tabbrowser-tab .tab-background {{
  background-color: var(--window_bg_color) !important;
}}

.tabbrowser-tab[selected] .tab-background {{
  background-color: var(--card_bg_color) !important;
}}

.tabbrowser-tab:not([selected]):hover .tab-background {{
  background-color: var(--dark_1) !important;
}}

.tabbrowser-tab .tab-label {{
  color: var(--card_fg_color) !important;
}}

.tabbrowser-tab[selected] .tab-label,
.tabbrowser-tab:not([selected]):hover .tab-label {{
  color: var(--window_fg_color) !important;
}}

.tab-close-button {{
  color: var(--card_fg_color) !important;
  fill: var(--card_fg_color) !important;
}}

#tabs-newtab-button,
.tabs-newtab-button {{
  color: var(--card_fg_color) !important;
  fill: var(--card_fg_color) !important;
}}

#urlbar,
#urlbar-background {{
  background-color: var(--card_bg_color) !important;
  color: var(--window_fg_color) !important;
  border-color: var(--dark_1) !important;
}}

#urlbar {{
    border-radius: 8px;
}}

#urlbar:focus-within,
#urlbar[focused="true"] {{
  background-color: var(--card_bg_color) !important;
  border-color: var(--accent_color) !important;
}}

#urlbar-input,
.urlbar-input {{
  color: var(--window_fg_color) !important;
}}

#identity-box,
#identity-icon {{
  color: var(--card_fg_color) !important;
  fill: var(--card_fg_color) !important;
}}

#tracking-protection-icon-container {{
  color: var(--accent_color) !important;
  fill: var(--accent_color) !important;
}}

toolbar toolbarbutton,
.toolbarbutton-1 {{
  color: var(--card_fg_color) !important;
  fill: var(--card_fg_color) !important;
  background-color: transparent !important;
}}

toolbar toolbarbutton:not([disabled]):hover > .toolbarbutton-icon,
toolbar toolbarbutton:not([disabled]):hover > .toolbarbutton-text,
toolbar toolbarbutton:not([disabled]):hover > .toolbarbutton-badge-stack,
.toolbarbutton-1:not([disabled]):hover > .toolbarbutton-icon,
.toolbarbutton-1:not([disabled]):hover > .toolbarbutton-badge-stack {{
  color: var(--window_fg_color) !important;
  fill: var(--window_fg_color) !important;
}}

toolbar toolbarbutton:not([disabled]):hover,
.toolbarbutton-1:not([disabled]):hover {{
  color: var(--window_fg_color) !important;
  fill: var(--window_fg_color) !important;
}}

toolbar toolbarbutton:hover,
.toolbarbutton-1:hover {{
  background-color: transparent !important;
}}

.toolbarbutton-1:not([disabled]):hover > .toolbarbutton-icon {{
  background-color: var(--dark_1) !important;
}}

toolbar toolbarbutton:active,
.toolbarbutton-1:active,
toolbar toolbarbutton[open="true"] {{
  background-color: transparent !important;
  color: var(--window_fg_color) !important;
  fill: var(--window_fg_color) !important;
}}

#PersonalToolbar,
#bookmarks-toolbar {{
  background-color: var(--headerbar_bg_color) !important;
  border-color: var(--dark_1) !important;
}}

.bookmark-item,
#PersonalToolbar toolbarbutton {{
  color: var(--card_fg_color) !important;
  fill: var(--card_fg_color) !important;
}}

.bookmark-item:hover,
#PersonalToolbar toolbarbutton:hover {{
  background-color: var(--dark_1) !important;
  color: var(--window_fg_color) !important;
}}

menupopup,
panel,
.panel-arrowcontent {{
  color: var(--window_bg_color) !important;
  border-color: var(--dark_1) !important;
}}

panel:not([remote]) {{
	--arrowpanel-background: var(--window_bg_color) !important;
	--arrowpanel-color: var(--window_fg_color) !important;
}}

.menupopup-arrowscrollbox:not(#tabgroup-panel-content) {{
  background: var(--window_bg_color) !important;
  border-color: var(--window_bg_color) !important;
}}

menuitem,
menu {{
  color: var(--window_fg_color) !important;
  background-color: transparent !important;
}}

menuitem:hover,
menu:hover,
menuitem[_moz-menuactive="true"],
menu[_moz-menuactive="true"] {{
  background-color: var(--dark_1) !important;
  color: var(--window_fg_color) !important;
}}

menuseparator {{
  border-color: var(--window_fg_color) !important;
}}

#sidebar-box,
#sidebar {{
  background-color: var(--sidebar_bg_color) !important;
  color: var(--sidebar_fg_color) !important;
  border-color: var(--dark_1) !important;
}}

#sidebar-header {{
  background-color: var(--headerbar_bg_color) !important;
  color: var(--headerbar_fg_color) !important;
  border-color: var(--dark_1) !important;
}}

findbar,
#FindToolbar,
.findbar-container {{
  background-color: var(--card_bg_color) !important;
  color: var(--window_fg_color) !important;
  border-color: var(--dark_1) !important;
}}

.findbar-textbox {{
  background-color: var(--view_bg_color) !important;
  color: var(--view_fg_color) !important;
  border-color: var(--dark_1) !important;
}}

.found-matches {{
  color: var(--accent_color) !important;
}}

notification,
.notificationbox-stack {{
  background-color: var(--card_bg_color) !important;
  color: var(--window_fg_color) !important;
  border-color: var(--dark_1) !important;
}}

scrollbar {{
  background-color: var(--card_bg_color) !important;
}}

scrollbar thumb,
scrollbarbutton {{
  background-color: var(--dark_1) !important;
}}

scrollbar thumb:hover {{
  background-color: var(--card_fg_color) !important;
}}

#urlbar-results,
.urlbarView,
.urlbar-background,
.urlbarView-body-inner,
.urlbarView-body-outer {{
  background-color: var(--window_bg_color) !important;
  border-color: var(--window_bg_color) !important;
}}

.urlbarView-row {{
  color: var(--window_fg_color) !important;
}}

.urlbarView-row[selected],
.urlbarView-row:hover {{
  background-color: var(--dark_1) !important;
}}

.urlbarView-url,
.urlbarView-emphasize {{
  color: var(--accent_color) !important;
}}

.urlbarView-tags,
.urlbarView-title-separator {{
  color: var(--card_fg_color) !important;
}}

#statuspanel-label {{
  background-color: var(--card_bg_color) !important;
  color: var(--window_fg_color) !important;
  border-color: var(--dark_1) !important;
}}

#downloads-button[attention],
#downloads-button[attention="success"] {{
  color: var(--accent_color) !important;
  fill: var(--accent_color) !important;
}}
"""

FFG_TEMPLATE = """
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
}}

:root:-moz-window-inactive {{
    --gnome-window-color: {window_fg_color};
}}

@-moz-document url-prefix("about:home"), url-prefix("about:newtab") {{
 body {{
  --newtab-background-color: #2A2A2E!important;
  --newtab-button-primary-color: #0060DF!important;
  --newtab-button-secondary-color: #38383D!important;
  --newtab-link-primary-color: var(--gnome-accent)!important;
  --newtab-text-primary-color: var(--gnome-accent)!important;
  --newtab-textbox-background-color: var(--gnome-toolbar-background)!important;
  --newtab-textbox-border: var(--gnome-inactive-toolbar-border-color)!important;
  --newtab-search-border-color: rgba(249, 249, 250, 0.2)!important;
  --newtab-search-dropdown-color: #38383D!important;
  --newtab-search-icon-color: rgba(249, 249, 250, 0.6)!important;
  --newtab-card-background-color: var(--gnome-toolbar-background)!important;
 }}
}}
"""

COLORED_TEMPLATE = """
.titlebar-buttonbox {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}


.titlebar-button {{
    border-radius: 100%;
    height: 24px !important;
    width: 42px !important;
    margin: 0 -2px !important;
}}

.titlebar-button.titlebar-close {{
    background-color: alpha(var(--red_1), 0.85) !important;
    color: var(--red_1) !important;

    &:not([disabled]):hover {{
      > image {{
            display: revert !important;
            color: var(--red_1) !important;
            fill: var(--red_1) !important;
        }}
    }}
}}

.titlebar-button.titlebar-min,
.titlebar-button.titlebar-min:hover {{
    background-color: alpha(var(--yellow_1), 0.85) !important;
    color: var(--yellow_1) !important;

    &:not([disabled]):hover {{
      > image {{
            display: revert !important;
            color: var(--yellow_1) !important;
            fill: var(--yellow_1) !important;
        }}
    }}
}}
.titlebar-button.titlebar-restore,
.titlebar-button.titlebar-restore:hover,
.titlebar-button.titlebar-max,
.titlebar-button.titlebar-max:hover {{
    background-color: alpha(var(--green_1), 0.85) !important;
    color: var(--green_1) !important;

   &:not([disabled]):hover {{
      > image {{
            display: revert !important;
            color: var(--green_1) !important;
            fill: var(--green_1) !important;
        }}
    }}
}}
"""

MACOS_TEMPLATE = """
.titlebar-buttonbox {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 2px;
}}

.titlebar-button {{
    border-radius: 100% !important;
    height: 17px !important;
    width: 17px !important;
    transition: filter 0.1s ease;
    position: center;
    margin: 0 4px !important;
    padding: 0 !important;

    &::-moz-window-inactive {{
        filter: opacity(0.4) saturate(0);
    }}
}}

.titlebar-button:not(:hover) > image {{
      display: none;
}}

.titlebar-button.titlebar-close {{
    background: var(--red_1) !important;
    &:not([disabled]):hover {{
        > image {{
            display: revert !important;
            color: var(--window_bg_color) !important;
            fill: var(--window_bg_color) !important;
        }}
    }}
    &:not([disabled]):active {{
        filter: none;
    }}
}}

.titlebar-button.titlebar-min {{
    background: var(--yellow_1) !important;
    &:not([disabled]):hover {{
        > image {{
            display: revert !important;
            color: var(--window_bg_color) !important;
            fill: var(--window_bg_color) !important;
        }}
    }}
    &:not([disabled]):active {{
        filter: none;
    }}
}}

.titlebar-button.titlebar-max,
.titlebar-button.titlebar-restore {{
    background: var(--green_1) !important;
    &:not([disabled]):hover {{
        > image {{
            display: revert !important;
            color: var(--window_bg_color) !important;
            fill: var(--window_bg_color) !important;
        }}
    }}
    &:not([disabled]):active {{
        filter: none;
    }}
}}
"""

HIDDEN_TEMPLATE = """
.titlebar-buttonbox {{
    display: none;
}}
"""

MINT_TEMPLATE = """
.titlebar-buttonbox {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}

.titlebar-button {{
    border-radius: 100%;
    height: 24px !important;
    width: 24px !important;
    margin: 0 4px !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
}}

.titlebar-button.titlebar-close:not(:hover) > image,
.titlebar-button.titlebar-min:not(:hover) > image,
.titlebar-button.titlebar-max:not(:hover) > image,
.titlebar-button.titlebar-restore:not(:hover) > image {{
    background-color: transparent !important;
}}

.titlebar-button.titlebar-close {{
    background-color: var(--accent_color) !important;
    color: var(--window_bg_color) !important;

    &:not([disabled]):hover {{
      > image {{
            display: revert !important;
            color: var(--window_bg_color) !important;
            fill: var(--window_bg_color) !important;
        }}
    }}
}}
"""

BREEZE_TEMPLATE = """
.titlebar-buttonbox {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 2px !important;
    margin: 0 8px !important;
}}

.titlebar-button {{
    border-radius: 100% !important;
    margin: 0 3px !important;
    padding: 0 !important;
    height: 24px !important;
    width: 24px !important;
    align-items: center !important;
    justify-content: center !important;
    transition: background-color 0.15s ease !important;
    color: var(--window_fg_color) !important;
}}

.titlebar-button.titlebar-close > image,
.titlebar-button.titlebar-min > image,
.titlebar-button.titlebar-max > image,
.titlebar-button.titlebar-restore > image {{
    margin: 0 !important;
}}

.titlebar-button:not(:hover) > image {{
    background-color: transparent !important;
}}

.titlebar-button.titlebar-min:hover > image,
.titlebar-button.titlebar-max:hover > image {{
    background-color: var(--card_bg_color) !important;
}}

.titlebar-button.titlebar-max {{
  & > .toolbarbutton-icon {{
    list-style-image: url(chrome://global/skin/icons/arrow-up.svg) !important;
    -moz-context-properties: fill, fill-opacity, stroke, stroke-opacity !important;
    fill: var(--window_fg_color) !important;
    color: transparent !important;
    width: 18px !important;
    height: 18px !important;
  }}

    &:not([disabled]):hover > image {{
      color: transparent !important;
    }}
}}

.titlebar-button.titlebar-close:hover {{
  background-color: var(--red_1) !important;
   &:not([disabled]):hover > image {{
      fill: var(--dark_1) !important;
      color: var(--dark_1) !important;
  }}
}}

.titlebar-button.titlebar-restore {{
  & > .toolbarbutton-icon {{
    background-image: -moz-symbolic-icon(media-playback-stop-symbolic) !important;
    color: var(--window_fg_color);
    width: 18px !important;
    height: 18px !important;
    transform: rotate(45deg);
  }}
}}

.titlebar-button.titlebar-min {{
  & > .toolbarbutton-icon {{
    list-style-image: url(chrome://global/skin/icons/arrow-down.svg) !important;
    -moz-context-properties: fill, fill-opacity, stroke, stroke-opacity !important;
    fill: var(--window_fg_color) !important;
    color: transparent !important;
    width: 18px !important;
    height: 18px !important;
  }}
  &:not([disabled]):hover > image {{
      color: transparent !important;
  }}
}}
"""

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
                            if(Path(f"{result}/chrome/firefox-gnome-theme").exists()):
                                Path(f"{result}/chrome/firefox-gnome-theme").mkdir(mode=0o755, parents=True, exist_ok=True)
                                with open(
                                    f"{result}/chrome/firefox-gnome-theme/customChrome.css",
                                    "w",
                                ) as f:
                                    f.write(FFG_TEMPLATE.format(**self.variables))
                            else:
                                with open(
                                    f"{result}/chrome/userChrome.css",
                                    "w",
                                ) as f:
                                    f.write(DEFAULT_TEMPLATE.format(**self.variables) + f"\n{window_control_map[self.window_controls].format(**self.variables)}")
                    except OSError:
                        pass
            except OSError:
                pass
            except StopIteration:
                pass
            except FileExistsError:
                pass
