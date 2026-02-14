<p align="center">
  <img src="https://github.com/SwordPuffin/Rewaita/blob/main/data/icons/hicolor/scalable/apps/io.github.swordpuffin.rewaita.svg" width="100" height=100/>
</p>

<h1 align="center">Rewaita</h1>

#### <p align="center">Rewaita brings a fresh look to Adwaita apps using popular color schemes.</p>

<br>
<div align="center">
  <a href="https://flathub.org/apps/io.github.swordpuffin.rewaita">
    <img width="200" alt="Get it on Flathub" src="https://flathub.org/api/badge?svg&locale=en"/>
  </a>&nbsp;&nbsp;
  <a href="https://aur.archlinux.org/packages/rewaita">
    <img width="280" alt="Unofficial AUR build" src="https://img.shields.io/aur/version/rewaita?style=for-the-badge">
  </a>&nbsp;&nbsp;
  <a href="https://build.opensuse.org/package/show/home:ericfrs/rewaita">
    <img width="250" alt="Zypper Package" src="https://img.shields.io/badge/openSUSE-73BA25?logo=opensuse&logoColor=white">
  </a>&nbsp;&nbsp;
  <a href="https://search.nixos.org/packages?channel=unstable&show=rewaita&query=adwaita">
    <img width="180" alt="NixOS Package" src="https://img.shields.io/badge/NixOS-5277C3?logo=nixos&logoColor=fff">
  </a>
</div>

<p align="center">
  <img src="https://github.com/SwordPuffin/Rewaita/blob/main/data/screenshots/Screenshot1.png" width="450"/>
  <img src="https://github.com/SwordPuffin/Rewaita/blob/main/data/screenshots/Screenshot2.png" width="425"/>
</p>

# ⬇️ Installation 
---
*The AUR, Zypper, and Nix packages are maintained by third-party developers, and are not tested in upstream production. Use with caution!!!
<br/>
<br/>
**The Flatpak version is the only officially supported format and therefore is recommended for the best experience.**

### Flatpak:
```bash
flatpak install io.github.swordpuffin.rewaita
```
### AUR
Using yay
```bash
yay -S rewaita
```
Using paru
```bash
paru -S rewaita
```

### OpenSUSE
```bash
# Tumbleweed
sudo zypper ar -cfp 90 https://download.opensuse.org/repositories/home:/ericfrs/openSUSE_Tumbleweed/home:ericfrs.repo
# Slowroll
sudo zypper ar -cfp 90 https://download.opensuse.org/repositories/home:/ericfrs/openSUSE_Slowroll/home:ericfrs.repo

sudo zypper ref
sudo zypper in rewaita
```

### NixOS
```bash
nix-shell -p rewaita
```


# ✅ Permissions 
### Allow Flatpak to edit GTK3/4 themes
#### System installs (default):
```bash
sudo flatpak override --filesystem=xdg-config/gtk-3.0:rw
sudo flatpak override --filesystem=xdg-config/gtk-4.0:rw
```
#### User installs
```bash
flatpak --user override --filesystem=xdg-config/gtk-3.0:rw
flatpak --user override --filesystem=xdg-config/gtk-4.0:rw
```

---

# 🐛 Known Bugs
#### Theme did not go away after Rewaita was deleted:
Run:
```bash
rm ~/.config/gtk-3.0/gtk.css
rm -rf ~/.config/gtk-3.0/assets
rm ~/.config/gtk-4.0/gtk.css
```
#### Gnome Shell theme is not generating:
Update Rewaita to v1.0.9 or greater. Or: 
```bash
mkdir -p $HOME/.local/share/themes
```

#### GTK-3.0 or GTK-4.0 theme is not generating:
```bash
mkdir -p $HOME/.config/gtk-3.0 && mkdir -p $HOME/.config/gtk-4.0
```

#### Autostart file is not generating:
This error message would show when running Rewaita.

> Traceback (most recent call last):
>  File "/app/share/rewaita/rewaita/main.py", line 124, in on_background_response
>    with open(os.path.join(GLib.getenv("HOME"), ".config", "autostart", "rewaita.desktop"), "w") as file:
>         ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> FileNotFoundError: [Errno 2] No such file or directory: '/home/(user)/.config/autostart/rewaita.desktop'
```bash
mkdir $HOME/.config/autostart
```

#### Application window opens but is empty:
#### 1. Flatpak (pre-v1.0.9)
   
Run:
```bash
rm ~/.var/app/io.github.swordpuffin.rewaita/data/prefs.json
```
#### 2. AUR
See upstream [bug](https://github.com/SwordPuffin/Rewaita/issues/48) 

Install xdg-desktop-portal-gnome with:
```bash
sudo pacman -S xdg-desktop-portal-gnome
```
Then reboot.

  

# 🤝 Contributing

## Flatpak
Run the following commands in a terminal:

(Make a folder named `Projects` in your home directory if it doesn't already exist)

```bash
cd Projects
git clone https://github.com/SwordPuffin/Rewaita
```

Then, in [Builder](https://apps.gnome.org/Builder/) you can add it to your projects.

## AUR, OpenSUSE, or NixOS
Please contact the maintainers for instuctions, they are not directly affiliated with any upstream project developer(s).
<br />
Any serious issues should be brought up here, but please indicate you are running a third-party build.

AUR maintainer: [Mark Wagie](https://github.com/yochananmarqos)
<br />
OpenSUSE maintainer: [ericfs](https://github.com/ericfrs)
<br />
NixOS maintainer: [Seth Flynn](https://github.com/getchoo)

---

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

