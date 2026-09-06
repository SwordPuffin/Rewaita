# css_templates.py
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

# Used in utils.py

no_pill_css = """
#panel .panel-button, .search-entry, .clock {
  border-radius: 12px;
}

.quick-toggle, .quick-toggle-has-menu {
  border-radius: 12px;
}

.quick-toggle-has-menu .quick-toggle {
  min-width: auto;
  max-width: auto;
}

.quick-toggle-has-menu .quick-toggle:ltr {
  border-radius: 12px 0 0 12px;
}

.quick-toggle-has-menu .quick-toggle:rtl {
  border-radius: 0 12px 12px 0;
}

.quick-toggle-has-menu .quick-toggle:ltr:last-child {
  border-radius: 12px;
}

.quick-toggle-has-menu .quick-toggle:rtl:last-child {
  border-radius: 12px;
}

.quick-toggle-has-menu .quick-toggle-menu-button:ltr {
  border-radius: 0 12px 12px 0;
}

.quick-toggle-has-menu .quick-toggle-menu-button:rtl {
  border-radius: 12px 0 0 12px;
}
"""

accent_tab_css_gs = """
#panel .panel-button:hover, .clock:hover,
#panel .panel-button:active, .clock:active{
  color: @accent-color !important;
}
"""

############################################

# Used in custom_theme_page.py

gnome_colors = {
    "Main Colors": {
        "description": "Used as the main window colors",
        "--window-bg-color": "#222226",
        "--window-fg-color": "#ffffff",
    },
    "Success Colors": {
        "description": "Used to indicate successful actions or high levels",
        "--success-color": "#78e9ab",
        "--success-bg-color": "#26a269",
        "--success-fg-color": "#ffffff",
    },
    "Destructive Colors": {
        "description": "Used on buttons to indicate destruction or dangerous actions like deleting files",
        "--destructive-color": "#ff938c",
        "--destructive-bg-color": "#c01c28",
        "--destructive-fg-color": "#ffffff",
    },
    "Warning Colors": {
        "description": "Used on a variety of widgets to indicate warnings or caution",
        "--warning-color": "#ffc252",
        "--warning-bg-color": "#cd9309",
        "--warning-fg-color": "#000000",
    },
    "Interface Colors": {
        "description": "Used on most background UI elements like text-views, buttons, and headerbars",
        "--view-bg-color": "#1d1d20",
        "--view-fg-color": "#ffffff",
        "--headerbar-bg-color": "#2e2e32",
        "--headerbar-fg-color": "#ffffff",
        "--card-bg-color": "#34343a",
        "--card-fg-color": "#ffffff",
    },
    "Named Colors": {
        "description": "Array of palette colors, used to separate UI elements and to give your theme some character",
        "--blue-1": "#99c1f1",
        "--blue-2": "#62a0ea",
        "--green-1": "#8ff0a4",
        "--yellow-1": "#f9f06b",
        "--orange-1": "#ffbe6f",
        "--red-1": "#f66151",
        "--purple-1": "#dc8add",
        "--purple-2": "#c061cb",
        "--brown-1": "#cdab8f",
        "--light-1": "#ffffff",
        "--light-5": "#9a9996",
        "--dark-1": "#77767b",
    }
}

titles = {
    "--window-bg-color": "Window Background Color",
    "--window-fg-color": "Window Text Color",
    "--success-color": "Standalone Color",
    "--success-bg-color": "Background Color",
    "--success-fg-color": "Text Color",
    "--destructive-color": "Standalone Color",
    "--destructive-bg-color": "Background Color",
    "--destructive-fg-color": "Text Color",
    "--warning-color": "Standalone",
    "--warning-bg-color": "Background Color",
    "--warning-fg-color": "Text Color",
    "--view-bg-color": "Text View Background Color",
    "--view-fg-color": "Text Color",
    "--headerbar-bg-color": "Headerbar Background Color",
    "--headerbar-fg-color": "Text Color",
    "--card-bg-color": "Button/Frame Background Color",
    "--card-fg-color": "Text Color",
    "--blue-1": "Blue",
    "--blue-2": "Teal",
    "--green-1": "Green",
    "--yellow-1": "Yellow",
    "--orange-1": "Orange",
    "--red-1": "Red",
    "--purple-1": "Pink",
    "--purple-2": "Purple",
    "--brown-1": "Brown",
    "--light-1": "Light",
    "--light-5": "Slate",
    "--dark-1": "Dark",
}

############################################

# Used in extra_options_box.py
transparency_css = """
.background {
	opacity: 0.92;
}
"""

border_css = """
window {
  border: none;
}

window.csd.maximized, window.csd.fullscreen, window.csd.tiled,
window.csd.tiled-top, window.csd.tiled-right, window.csd.tiled-bottom,
window.csd.tiled-left {
  border-radius: 0;
  border: none;
  transition: none;
}

window.csd:backdrop {
  transition: box-shadow 75ms cubic-bezier(0, 0, 0.2, 1);
  box-shadow: 0 8px 6px -5px rgba(0,0,0,0.2), 0 16px 15px 2px rgba(0,0,0,0.14),
              0 6px 18px 5px rgba(0,0,0,0.12), 0 0 0 2px var(--accent-bg-color),
              0 0 36px transparent;
}

window.csd, window.solid-csd, popover contents, dialog .background {
  transition: none;
  box-shadow: 0 8px 6px -5px rgba(0,0,0,0.2), 0 16px 15px 2px rgba(0,0,0,0.14),
              0 6px 18px 5px rgba(0,0,0,0.12), 0 0 0 2px var(--accent-bg-color),
              0 0 36px transparent;
}
"""

sharp_corners_css = """
* {
   border-radius: 0px;
}
"""

accent_tab_css_gtk4 = """
*:selected {
    color: var(--accent-bg-color);
}

*:checked:not(expander) {
    color: var(--accent-fg-color);
    background-color: var(--accent-bg-color);
}
"""

###############################################

# Used in firefox_gnome_theme.py

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
}}

menuitem,
menu {{
  color: var(--window-fg-color) !important;
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

###############################################

# Used in image_to_css.py

CSS_TEMPLATE = """:root {{
  --window-bg-color: {window_bg};
  --window-fg-color: {window_fg};
  --view-bg-color: {view_bg};
  --view-fg-color: {view_fg};
  --headerbar-bg-color: {headerbar_bg};
  --headerbar-backdrop-color: {headerbar_backdrop};
  --headerbar-fg-color: {headerbar_fg};
  --popover-bg-color: {popover_bg};
  --popover-fg-color: {popover_fg};
  --dialog-bg-color: var(--popover-bg-color);
  --dialog-fg-color: var(--popover-fg-color);
  --card-bg-color: {card_bg};
  --card-fg-color: {card_fg};
  --sidebar-bg-color: {sidebar_bg};
  --sidebar-fg-color: {sidebar_fg};
  --sidebar-backdrop-color: var(--sidebar-bg-color);
  --sidebar-border-color: {sidebar_border};
  --secondary-sidebar-bg-color: var(--sidebar-bg-color);
  --secondary-sidebar-fg-color: var(--sidebar-fg-color);
  --secondary-sidebar-backdrop-color: var(--sidebar-backdrop-color);
  --secondary-sidebar-border-color: var(--sidebar-border-color);
{accent_lines}
}}
toast {{
  background-color: var(--window-bg-color);
  color: var(--window-fg-color);
}}
.inline {{
  background-color: rgba(0, 0, 0, 0);
}}
"""
