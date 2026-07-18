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
  --window-bg-color:   {window-bg-color};
  --window-fg-color:   {window-fg-color};
  --view-bg-color:     {view-bg-color};
  --view-fg-color:     {view-fg-color};
  --headerbar-bg-color:{headerbar-bg-color};
  --headerbar-fg-color:{headerbar-fg-color};
  --popover-bg-color:  {popover-bg-color};
  --popover-fg-color:  {popover-fg-color};
  --card-bg-color:     {card-bg-color};
  --card_fg_color:     {card-fg-color};
  --sidebar-bg-color:  {sidebar-bg-color};
  --sidebar-fg-color:  {sidebar-fg-color};
  --dark-1:            {dark-1};
  --brown-1:           {brown-1};
  --light-1:           {light-1};
  --blue-1:            {blue-1};
  --blue-2:            {blue-2};
  --green-1:           {green-1};
  --yellow-1:          {yellow-1};
  --orange-1:          {orange-1};
  --red-1:             {red-1};
  --purple-1:          {purple-1};
  --purple-2:          {purple-2};
  --accent-color:      {accent-color};
}}

#main-window,
#browser {{
  background-color: var(--headerbar-bg-color) !important;
  color: var(--window-fg-color) !important;
}}

#star-button {{
	&[starred] {{
		fill: var(--accent-color) !important;
	}}
}}

#input:not([type="checkbox"]) {{
  background-color: var(--card-bg-color) !important;
  border: none !important;
  outline: none !important;
}}

#input:not([type="checkbox"]):focus {{
  border: 2px var(--accent-color) solid !important;
}}

input[type="checkbox"],
checkbox:not(.treenode-checkbox) > .checkbox-check {{
  appearance: none !important;
	border: 0 !important;
	border-radius: 6px !important;
	background-color: var(--window-bg-color) !important;
	color: var(--window-fg-color) !important;
	height: 20px !important;
	width: 20px !important;
}}

input[type="checkbox"]:checked,
checkbox:not(.treenode-checkbox) > .checkbox-check[checked] {{
	background-color: var(--accent-color) !important;
	background-image: -moz-symbolic-icon(checkmark-symbolic) !important;
	background-size: 14px !important;
	background-repeat: no-repeat;
	background-position: center;
	color: var(--window-bg-color) !important;
	-moz-context-properties: fill;
}}

#nav-bar,
#navigator-toolbox,
#toolbar-menubar,
.browser-toolbar {{
  background-color: var(--headerbar-bg-color) !important;
  color: var(--headerbar-fg-color) !important;
  border-color: var(--dark-1) !important;
}}

#TabsToolbar,
.tabbrowser-arrowscrollbox {{
  background-color: var(--window-bg-color) !important;
}}

.tabbrowser-tab .tab-background {{
  background-color: var(--window-bg-color) !important;
}}

.tabbrowser-tab[selected] .tab-background {{
  background-color: var(--card-bg-color) !important;
}}

.tabbrowser-tab:not([selected]):hover .tab-background {{
  background-color: var(--dark-1) !important;
}}

.tabbrowser-tab .tab-label {{
  color: var(--card_fg_color) !important;
}}

.tabbrowser-tab[selected] .tab-label,
.tabbrowser-tab:not([selected]):hover .tab-label {{
  color: var(--window-fg-color) !important;
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

#sidebar-main > * #tabs-newtab-button:hover,
#sidebar-main > * .tabs-newtab-button:hover {{
  background-color: var(--dark-1) !important;
}}

#urlbar,
#urlbar-background {{
  background-color: var(--card-bg-color) !important;
  color: var(--window-fg-color) !important;
  border-color: var(--dark-1) !important;
}}

#urlbar {{
    border-radius: 8px;
}}

#urlbar:focus-within,
#urlbar[focused="true"] {{
  background-color: var(--card-bg-color) !important;
  border-color: var(--accent-color) !important;
}}

#urlbar-input,
.urlbar-input {{
  color: var(--window-fg-color) !important;
}}

#identity-box,
#identity-icon {{
  color: var(--card_fg_color) !important;
  fill: var(--card_fg_color) !important;
}}

#tracking-protection-icon-container {{
  color: var(--accent-color) !important;
  fill: var(--accent-color) !important;
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
  color: var(--window-fg-color) !important;
  fill: var(--window-fg-color) !important;
}}

toolbar toolbarbutton:not([disabled]):hover,
.toolbarbutton-1:not([disabled]):hover {{
  color: var(--window-fg-color) !important;
  fill: var(--window-fg-color) !important;
}}

toolbar toolbarbutton:hover,
.toolbarbutton-1:hover {{
  background-color: transparent !important;
}}

.toolbarbutton-1:not([disabled]):hover > .toolbarbutton-icon {{
  background-color: var(--card-bg-color) !important;
}}

toolbar toolbarbutton:active,
.toolbarbutton-1:active,
toolbar toolbarbutton[open="true"] {{
  background-color: transparent !important;
  color: var(--window-fg-color) !important;
  fill: var(--window-fg-color) !important;
}}

#PersonalToolbar,
#bookmarks-toolbar {{
  background-color: var(--headerbar-bg-color) !important;
  border-color: var(--dark-1) !important;
}}

.bookmark-item,
#PersonalToolbar toolbarbutton {{
  color: var(--card_fg_color) !important;
  fill: var(--card_fg_color) !important;
}}

.bookmark-item:hover,
#PersonalToolbar toolbarbutton:hover {{
  background-color: var(--card-bg-color) !important;
  color: var(--window-fg-color) !important;
}}

menupopup,
panel,
.panel-arrowcontent {{
  color: var(--window-fg-color) !important;
}}

panel > * {{
    background-color: var(--window-bg-color) !important;
    color: var(--window-fg-color) !important;
}}

panel:not([remote]) {{
	--arrowpanel-background: var(--window-bg-color) !important;
	--arrowpanel-color: var(--window-fg-color) !important;
}}

.menupopup-arrowscrollbox:not(#tabgroup-panel-content) {{
  background: var(--window-bg-color) !important;
  border-color: var(--window-bg-color) !important;
}}

menuitem,
menu {{
  color: var(--window-fg-color) !important;
  background-color: transparent !important;
}}

menuitem:hover,
menu:hover,
menuitem[_moz-menuactive="true"],
menu[_moz-menuactive="true"] {{
  background-color: var(--dark-1) !important;
  color: var(--window-fg-color) !important;
}}

menuseparator {{
  border-color: var(--window-fg-color) !important;
}}

#sidebar-box,
#sidebar {{
  background-color: var(--sidebar-bg-color) !important;
  color: var(--sidebar-fg-color) !important;
  border-color: var(--dark-1) !important;
}}

#sidebar-header {{
  background-color: var(--headerbar-bg-color) !important;
  color: var(--headerbar-fg-color) !important;
  border-color: var(--dark-1) !important;
}}

findbar,
#FindToolbar,
.findbar-container {{
  background-color: var(--card-bg-color) !important;
  color: var(--window-fg-color) !important;
  border-color: var(--dark-1) !important;
}}

.findbar-textbox {{
  background-color: var(--view-bg-color) !important;
  color: var(--view-fg-color) !important;
  border-color: var(--dark-1) !important;
}}

.found-matches {{
  color: var(--accent-color) !important;
}}

notification,
.notificationbox-stack {{
  background-color: var(--card-bg-color) !important;
  color: var(--window-fg-color) !important;
  border-color: var(--dark-1) !important;
}}

scrollbar {{
  background-color: var(--card-bg-color) !important;
}}

scrollbar thumb,
scrollbarbutton {{
  background-color: var(--dark-1) !important;
}}

scrollbar thumb:hover {{
  background-color: var(--card_fg_color) !important;
}}

#urlbar-results,
.urlbarView,
.urlbar-background,
.urlbarView-body-inner,
.urlbarView-body-outer {{
  background-color: var(--card-bg-color) !important;
  border-color: var(--card-bg-color) !important;
}}

.urlbarView-row {{
  color: var(--window-fg-color) !important;
}}

.urlbarView-row[selected],
.urlbarView-row:hover {{
  background-color: var(--dark-1) !important;
}}

.urlbarView-url,
.urlbarView-emphasize {{
  color: var(--accent-color) !important;
}}

.urlbarView-tags,
.urlbarView-title-separator {{
  color: var(--card_fg_color) !important;
}}

#statuspanel-label {{
  background-color: var(--card-bg-color) !important;
  color: var(--window-fg-color) !important;
  border-color: var(--dark-1) !important;
}}

#downloads-button[attention],
#downloads-button[attention="success"] {{
  color: var(--accent-color) !important;
  fill: var(--accent-color) !important;
}}

popupnotification {{
  background-color: var(--card-bg-color) !important;
  color: var(--card_fg_color) !important;
  border-color: var(--card-bg-color) !important;
  outline-color: var(--card-bg-color) !important;
}}

.popup-notification-primary-button {{
  background-color: var(--accent-color) !important;
  color: var(--window-bg-color) !important;
}}

#PopupAutoComplete {{
  --panel-background-color: var(--window-bg-color) !important;
  --panel-border-color: transparent !important;
}}
"""

FFG_TEMPLATE = """
* {{
  color: {window-fg-color};
}}

:root {{
    --gnome-browser-before-load-background:        {window-bg-color};
    --gnome-accent-bg:                             {accent-color};
    --gnome-accent:                                {accent-color};
    --gnome-window-background:                     {window-bg-color};
    --gnome-window-color:                          {window-fg-color};
    --gnome-tabbar-tab-color:                      {window-fg-color};
    --gnome-tabbar-tab-active-color:               {window-fg-color};
    --gnome-toolbar-background:                    {window-bg-color};
    --gnome-toolbar-color:                         {window-fg-color};
    --gnome-toolbar-icon-fill:                     {window-fg-color};
    --gnome-inactive-window-background:            {window-bg-color};
    --gnome-inactive-toolbar-color:                {window-bg-color};
    --gnome-inactive-toolbar-border-color:         {headerbar-bg-color};
    --gnome-inactive-toolbar-icon-fill:            {window-fg-color};
    --gnome-menu-background:                       {window-bg-color};
    --gnome-headerbar-background:                  {window-bg-color};
    --gnome-button-destructive-action-background:  {red-1};
    --gnome-entry-color:                           {view-fg-color};
    --gnome-inactive-entry-color:                  {view-fg-color};
    --gnome-selected-color:                        {card-bg-color};
    --gnome-sidebar-background:                    {window-bg-color};
    --gnome-switch-slider-background:              {view-bg-color};
    --gnome-switch-active-slider-background:       {accent-color};
    --gnome-inactive-tabbar-tab-background:        {window-bg-color};
    --gnome-inactive-tabbar-tab-active-background: {card-bg-color};
    --gnome-tabbar-tab-background:                 {card-bg-color};
    --gnome-tabbar-tab-hover-background:           {headerbar-bg-color};
    --gnome-tabbar-tab-active-background:          {card-bg-color};
    --gnome-tabbar-tab-active-hover-background:    {card-bg-color};
    --gnome-tabbar-tab-active-background-contrast: transparent;
    --gnome-tabbar-tab-close-overlay-bg:           transparent;
}}

:root:-moz-window-inactive {{
    --gnome-window-color: {window-fg-color};
}}


.tab-background {{
  &:is([selected], [multiselected]) {{
    background-color: var(--gnome-tabbar-tab-active-background) !important;
  }}
}}

.tab-content {{
    #tabbrowser-tabs[orient="horizontal"] & {{
        &:not([pinned])::before {{
			background: transparent !important;
		}}
	}}
}}

.menupopup-arrowscrollbox,
panel > * {{
	background-color: var(--gnome-window-background) !important;
}}

#tab-preview-panel {{
  --panel-background-color: var(--gnome-window-background) !important;
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
    background-color: alpha(var(--red-1), 0.85) !important;
    color: var(--red-1) !important;

    &:not([disabled]):hover {{
      > image {{
            display: revert !important;
            color: var(--red-1) !important;
            fill: var(--red-1) !important;
        }}
    }}
}}

.titlebar-button.titlebar-min,
.titlebar-button.titlebar-min:hover {{
    background-color: alpha(var(--yellow-1), 0.85) !important;
    color: var(--yellow-1) !important;

    &:not([disabled]):hover {{
      > image {{
            display: revert !important;
            color: var(--yellow-1) !important;
            fill: var(--yellow-1) !important;
        }}
    }}
}}
.titlebar-button.titlebar-restore,
.titlebar-button.titlebar-restore:hover,
.titlebar-button.titlebar-max,
.titlebar-button.titlebar-max:hover {{
    background-color: alpha(var(--green-1), 0.85) !important;
    color: var(--green-1) !important;

   &:not([disabled]):hover {{
      > image {{
            display: revert !important;
            color: var(--green-1) !important;
            fill: var(--green-1) !important;
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
    background: var(--red-1) !important;
    &:not([disabled]):hover {{
        > image {{
            display: revert !important;
            color: var(--window-bg-color) !important;
            fill: var(--window-bg-color) !important;
        }}
    }}
    &:not([disabled]):active {{
        filter: none;
    }}
}}

.titlebar-button.titlebar-min {{
    background: var(--yellow-1) !important;
    &:not([disabled]):hover {{
        > image {{
            display: revert !important;
            color: var(--window-bg-color) !important;
            fill: var(--window-bg-color) !important;
        }}
    }}
    &:not([disabled]):active {{
        filter: none;
    }}
}}

.titlebar-button.titlebar-max,
.titlebar-button.titlebar-restore {{
    background: var(--green-1) !important;
    &:not([disabled]):hover {{
        > image {{
            display: revert !important;
            color: var(--window-bg-color) !important;
            fill: var(--window-bg-color) !important;
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
    background-color: var(--accent-color) !important;
    color: var(--window-bg-color) !important;

    &:not([disabled]):hover {{
      > image {{
            display: revert !important;
            color: var(--window-bg-color) !important;
            fill: var(--window-bg-color) !important;
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
    color: var(--window-fg-color) !important;
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

.titlebar-button.titlebar-min:hover,
.titlebar-button.titlebar-max:hover,
.titlebar-button.titlebar-restore:hover {{
    background-color: var(--window-fg-color) !important;
    & > .toolbarbutton-icon {{
        -moz-context-properties: fill, fill-opacity, stroke, stroke-opacity !important;
        fill: var(--window-bg-color) !important;
    }}
}}

.titlebar-button.titlebar-restore:hover {{
    & > .toolbarbutton-icon {{
        box-shadow: inset 0 0 0 2px var(--window-bg-color) !important;
    }}
}}

.titlebar-button.titlebar-max {{
  & > .toolbarbutton-icon {{
    list-style-image: url(chrome://global/skin/icons/arrow-up.svg) !important;
    -moz-context-properties: fill, fill-opacity, stroke, stroke-opacity !important;
    fill: var(--window-fg-color) !important;
    color: transparent !important;
    width: 18px !important;
    height: 18px !important;
  }}

    &:not([disabled]):hover > image {{
      color: transparent !important;
    }}
}}

.titlebar-button.titlebar-close {{
  & > .toolbarbutton-icon {{
    list-style-image: url(chrome://global/skin/icons/close.svg) !important;
    -moz-context-properties: fill, fill-opacity, stroke, stroke-width !important;
    fill: var(--window-fg-color) !important;
    color: transparent !important;
    width: 13px !important;
    height: 13px !important;
  }}

    &:not([disabled]):hover > image {{
      color: transparent !important;
    }}
}}

.titlebar-button.titlebar-close:hover {{
  background-color: var(--red-1) !important;
   &:not([disabled]):hover > image {{
      fill: var(--window-bg-color) !important;
  }}
}}

.titlebar-button.titlebar-restore {{
  & > .toolbarbutton-icon {{
    background-image: none !important;
    box-shadow: inset 0 0 0 2px var(--window-fg-color) !important;
    border-radius: 1px !important;
    width: 13px !important;
    height: 13px !important;
    transform: rotate(45deg) !important;
  }}
}}

.titlebar-button.titlebar-min {{
  & > .toolbarbutton-icon {{
    list-style-image: url(chrome://global/skin/icons/arrow-down.svg) !important;
    -moz-context-properties: fill, fill-opacity, stroke, stroke-opacity !important;
    fill: var(--window-fg-color) !important;
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
