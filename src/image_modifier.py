# image_modifier.py
#
# Copyright 2025 Nathan Perlman
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

from PIL import Image
import numpy as np

import gi, os, asyncio, random
gi.require_version('XdpGtk4', '1.0')
from gi.repository import Gtk, GLib, Gio, Xdp, XdpGtk4, Adw, Gdk
from .loading_dialog import LoadingDialog

picture_path = os.path.join(GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES), "rewaita")

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def compute_centroids(arr, n_clusters):
    centroids = []
    centroids.append(arr[np.random.choice(len(arr))])
    for _ in range(1, n_clusters):
        dists = np.min(np.linalg.norm(arr[:, None] - np.array(centroids)[None, :], axis=2), axis=1)
        probs = dists / np.sum(dists)
        next_centroid = arr[np.random.choice(len(arr), p=probs)]
        centroids.append(next_centroid)
    return np.array(centroids)

def simple_kmeans(arr, n_clusters=8, max_iter=10):
    centroids = compute_centroids(arr, n_clusters)
    for _ in range(max_iter):
        distances = np.linalg.norm(arr[:, None] - centroids[None, :], axis=2)
        labels = np.argmin(distances, axis=1)
        new_centroids = np.array([
            arr[labels == i].mean(axis=0) if np.any(labels == i) else centroids[i]
            for i in range(n_clusters)
        ])
        if(np.allclose(centroids, new_centroids, atol=1e-2)):
            break
        centroids = new_centroids
    return labels, centroids

async def remap_palette(image_path, target_palette_hex, n_colors=8, blend=1.0):
    target_palette = [hex_to_rgb(h) for h in target_palette_hex]

    img = Image.open(image_path).convert("RGB")
    arr = np.array(img).reshape(-1, 3)

    labels, centers = simple_kmeans(arr, n_clusters=n_colors)

    palette_arr = np.array(target_palette)
    dists = np.linalg.norm(centers[:, None] - palette_arr[None, :], axis=2)
    closest_palette_idx = np.argmin(dists, axis=1)
    mapped_palette = palette_arr[closest_palette_idx]

    blended_colors = (mapped_palette * blend + centers * (1.0 - blend)).astype(np.uint8)

    recolored = blended_colors[labels].reshape(img.size[1], img.size[0], 3)
    recolored = np.clip(recolored, 0, 255)

    return Image.fromarray(recolored)

def make_new_image(parent, file_path):
    from .theme_page import load_colors_from_css
    os.makedirs(picture_path, exist_ok=True)
    output_path = os.path.join(picture_path, f"{os.path.basename(file_path)}-tinted.jpg")

    theme_type = {
        0: "light",
        1: "dark",
        2: "light",
    }

    if(parent.pref in [0, 2]):
        theme = parent.light_theme
    else:
        theme = parent.dark_theme

    portal = Xdp.Portal()

    if(theme == "default"):
        dialog = Adw.AlertDialog.new()
        dialog.set_body(_("Please select a theme first"))

        dialog.add_response("ok", "_OK")

        dialog.set_close_response("ok")
        dialog.set_default_response("ok")

        dialog.present(parent)
        return

    palette_vals = list(load_colors_from_css(os.path.join(parent.data_dir, theme_type[parent.pref], theme)).values())
    palette_vals = [c for c in palette_vals if not c.startswith('@')]

    spinner = LoadingDialog(parent)

    def task_func(task, source_object, task_data, cancellable):
        spinner.present(parent)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        img = loop.run_until_complete(remap_palette(file_path, palette_vals))
        loop.close()

        img.save(f"{output_path}")
        task.return_value(output_path)

    def on_done(task, result, user_data=None):
        spinner.set_can_close(True), spinner.close()
        top = XdpGtk4.parent_new_gtk(parent)
        portal.set_wallpaper(
            top,
            f"file://{output_path}",
            Xdp.WallpaperFlags.PREVIEW
            | Xdp.WallpaperFlags.BACKGROUND
            | Xdp.WallpaperFlags.LOCKSCREEN,
        )

    task = Gio.Task.new(None, None, on_done)
    task.run_in_thread(task_func)

def on_image_opened(file_dialog, result, parent):
    file = file_dialog.open_finish(result)
    file_path = file.get_path()
    make_new_image(parent, file_path)

# ciede2000 Implementation

def rgb_to_xyz(rgb):
    rgb = np.array(rgb) / 255.0

    mask = rgb > 0.04045
    rgb_lin = np.where(mask, ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)

    M = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041]
    ])

    return np.dot(M, rgb_lin) * 100

def xyz_to_lab(xyz):
    xyz = np.array(xyz)
    ref = np.array([95.047, 100.0, 108.883])

    xyz = xyz / ref

    def f(t):
        return np.where(t > 0.008856, t ** (1/3), 7.787 * t + 16/116)

    fx, fy, fz = f(xyz[0]), f(xyz[1]), f(xyz[2])

    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)

    return np.array([L, a, b])

def rgb_to_lab(rgb):
    return xyz_to_lab(rgb_to_xyz(rgb))

def deltaE2000(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2

    avg_L = (L1 + L2) / 2.0
    C1 = np.sqrt(a1*a1 + b1*b1)
    C2 = np.sqrt(a2*a2 + b2*b2)
    avg_C = (C1 + C2) / 2.0

    G = 0.5 * (1 - np.sqrt((avg_C**7) / (avg_C**7 + 25**7)))
    a1p = (1 + G) * a1
    a2p = (1 + G) * a2

    C1p = np.sqrt(a1p*a1p + b1*b1)
    C2p = np.sqrt(a2p*a2p + b2*b2)

    avg_Cp = (C1p + C2p) / 2.0

    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360

    dhp = h2p - h1p
    dhp = np.where(dhp > 180, dhp - 360, dhp)
    dhp = np.where(dhp < -180, dhp + 360, dhp)

    avg_hp = np.where(
        np.abs(h1p - h2p) > 180,
        (h1p + h2p + 360) / 2,
        (h1p + h2p) / 2
    )

    T = (
        1
        - 0.17 * np.cos(np.radians(avg_hp - 30))
        + 0.24 * np.cos(np.radians(2 * avg_hp))
        + 0.32 * np.cos(np.radians(3 * avg_hp + 6))
        - 0.20 * np.cos(np.radians(4 * avg_hp - 63))
    )

    dLp = L2 - L1
    dCp = C2p - C1p
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2))

    S_L = 1 + (0.015 * (avg_L - 50)**2) / np.sqrt(20 + (avg_L - 50)**2)
    S_C = 1 + 0.045 * avg_Cp
    S_H = 1 + 0.015 * avg_Cp * T

    Rt = -2 * np.sqrt((avg_Cp**7) / (avg_Cp**7 + 25**7))
    Rt *= np.sin(np.radians(60 * np.exp(-(((avg_hp - 275) / 25) ** 2))))

    dE = np.sqrt(
        (dLp / S_L)**2 +
        (dCp / S_C)**2 +
        (dHp / S_H)**2 +
        Rt * (dCp / S_C) * (dHp / S_H)
    )
    return dE

def ciede2000(rgb, palette):
    palette = list(palette)

    palette_rgb = [
        tuple(int(h[i:i+2], 16) for i in (1,3,5))
        for h in palette
    ]

    palette_lab = np.array([rgb_to_lab(c) for c in palette_rgb])
    lab_input = rgb_to_lab(rgb)

    diffs = np.array([deltaE2000(lab_input, lab) for lab in palette_lab])

    idx = np.argmin(diffs)
    return palette[idx]

