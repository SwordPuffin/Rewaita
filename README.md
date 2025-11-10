# 🎨 Rewaita
---

<p align="center">
  <img src="https://github.com/SwordPuffin/Rewaita/blob/main/data/icons/hicolor/scalable/apps/io.github.swordpuffin.rewaita.svg" width="400"/>
</p>

<p align="center">Rewaita gives your Adwaita apps a fresh look by tinting them with popular color schemes.</p>
<br>
<p align="center"> 
    <a href="https://flathub.org/apps/io.github.swordpuffin.rewaita"> 
       <img width="200" alt="Get it on Flathub" src="https://flathub.org/api/badge?svg&locale=en"/> 
    </a>
    <br/>
    <br/>
    (Unofficial AUR build)
    <br/>
    <a href="https://aur.archlinux.org/packages/rewaita">
        <img width="200" alt="Unofficial AUR build" src="https://img.shields.io/aur/version/rewaita?style=for-the-badge">
    </a>
</p>

# ⬇️ Installation 
---
*The AUR package is maintained by third-party developers, and is not tested in upstream production. This version has also had many more bugs in the past.
<br/>
<br/>
**The Flatpak version is the only officially supported format and therefore is recommended for the best experience.**

### Flatpak:
```bash
flatpak install io.github.swordpuffin.rewaita
```
### AUR
```bash
yay -s rewaita
```


# ✅ Permissions 
### Allow Flatpak to edit GTK3/4 themes
```bash
flatpak override --filesystem=xdg-config/gtk-3.0:rw
flatpak override --filesystem=xdg-config/gtk-4.0:rw
```

# 🖼️ Screenshots

<p align="center">
  <img src="https://github.com/SwordPuffin/Rewaita/blob/main/data/screenshots/Screenshot1.png" width="600"/>
  <br><br>
  <img src="https://github.com/SwordPuffin/Rewaita/blob/main/data/screenshots/Screenshot2.png" width="600"/>
</p>

---

# 🐛 Known Bugs
#### Gnome Shell theme is not generating:
1. Power off your computer (like full shutdown, not restart).
2. Turn it back on and try again.
3. If it still doesn't generate:
     1. Go into Flatseal and find Rewaita's page
     2. Find filesystem permissions (you should see ~/.local/share/themes among them)
     3. Change ~/.local/share/themes to: ~/.local/share/themes:create (just append ":create")
     4. If it still doesn't work file an issue.

#### Application window opens but is empty:
#### 1. Flatpak
   
Delete:
```
~/.var/app/io.github.swordpuffin.rewaita/data/prefs.json
```
#### 2. AUR
See upstream [bug](https://github.com/SwordPuffin/Rewaita/issues/48) 

Install xdg-desktop-portal-gtk with:
```bash
sudo pacman -S xdg-desktop-portal-gtk
```
Then reboot.

  

# 🤝 Contributing

Run the following commands in a terminal:

(Make a folder named `Projects` in your home directory if it doesn't already exist)

```bash
cd Projects
git clone https://github.com/SwordPuffin/Rewaita
```

Then, in [Builder](https://apps.gnome.org/Builder/) you can add it to your projects.

---

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
