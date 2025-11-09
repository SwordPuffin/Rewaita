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

import gi, os, asyncio
gi.require_version('XdpGtk4', '1.0')
from gi.repository import Gtk, GLib, Gio, Xdp, XdpGtk4, Adw, Gdk

from .loading_dialog import LoadingDialog

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

        output_path = os.path.join(parent.data_dir, "recolored_img.jpg")
        img.save(output_path)
        task.return_value(output_path)

    def on_done(task, result, user_data=None):
        spinner.set_can_close(True), spinner.close()
        top = XdpGtk4.parent_new_gtk(parent)
        portal.set_wallpaper(
            top,
            f"file://{os.path.join(parent.data_dir, 'recolored_img.jpg')}",
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


