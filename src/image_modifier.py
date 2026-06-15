# image_modifier.py
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

from PIL import Image
import numpy as np

import gi, os, asyncio, random
gi.require_version('XdpGtk4', '1.0')
from gi.repository import Gtk, GLib, Gio, Xdp, XdpGtk4, Adw, Gdk
from .loading_dialog import LoadingDialog

picture_path = os.path.join(GLib.get_user_data_dir(), "wallpapers")
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def srgb_to_linear(c_uint8: np.ndarray) -> np.ndarray:
    c = c_uint8 / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def linear_to_oklab(rgb_lin: np.ndarray) -> np.ndarray:
    r, g, b = rgb_lin[:, 0], rgb_lin[:, 1], rgb_lin[:, 2]
    l = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b
    m = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b
    s = 0.0883024619*r + 0.2817188376*g + 0.6299787005*b
    l_, m_, s_ = np.cbrt(l), np.cbrt(m), np.cbrt(s)
    return np.stack([
        0.2104542553*l_ + 0.7936177850*m_ - 0.0040720468*s_,
        1.9779984951*l_ - 2.4285922050*m_ + 0.4505937099*s_,
        0.0259040371*l_ + 0.7827717662*m_ - 0.8086757660*s_,
    ], axis=1)

def to_lab(arr_uint8: np.ndarray) -> np.ndarray:
    return linear_to_oklab(srgb_to_linear(arr_uint8.astype(np.float32)))

def kmeans_plus_plus(sample: np.ndarray, k: int) -> np.ndarray:
    centroids = [sample[np.random.randint(len(sample))]]
    for _ in range(1, k):
        diff = sample[:, None, :] - np.array(centroids)[None, :, :]
        dists = np.einsum('ijk,ijk->ij', diff, diff).min(axis=1)
        probs = dists / dists.sum()
        centroids.append(sample[np.random.choice(len(sample), p=probs)])
    return np.array(centroids, dtype=np.float32)

def kmeans(sample: np.ndarray, k: int, max_iter: int) -> np.ndarray:
    centroids = kmeans_plus_plus(sample, k)
    for _ in range(max_iter):
        diff = sample[:, None, :] - centroids[None, :, :]
        labels = np.einsum('ijk,ijk->ij', diff, diff).argmin(axis=1)
        new_centroids = np.array([
            sample[labels == i].mean(axis=0) if np.any(labels == i) else centroids[i]
            for i in range(k)
        ], dtype=np.float32)
        if(np.allclose(centroids, new_centroids, atol=1e-8)):
            break
        centroids = new_centroids
    return centroids

async def remap_palette(image_path, target_palette_hex, n_colors=36, blend=1.0, max_iter=100, sample_size=10000):
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img, dtype=np.float32).reshape(-1, 3)

    arr_lab = to_lab(arr)
    pal_rgb = np.array([hex_to_rgb(h) for h in target_palette_hex], dtype=np.float32)
    pal_lab = to_lab(pal_rgb)

    idx = np.random.choice(len(arr_lab), size=min(sample_size, len(arr_lab)), replace=False)
    sample = arr_lab[idx]
    centroids_lab = kmeans(sample, n_colors, max_iter)

    diff = arr_lab[:, None, :] - centroids_lab[None, :, :]
    all_labels = np.einsum('ijk,ijk->ij', diff, diff).argmin(axis=1)

    diff_p = centroids_lab[:, None, :] - pal_lab[None, :, :]
    closest_pal_idx = np.einsum('ijk,ijk->ij', diff_p, diff_p).argmin(axis=1)
    mapped_palette_rgb = pal_rgb[closest_pal_idx]

    if(blend < 1.0):
        centroids_rgb = np.array([
            arr[all_labels == i].mean(axis=0) if np.any(all_labels == i) else np.zeros(3)
            for i in range(n_colors)
        ], dtype=np.float32)
        blended = mapped_palette_rgb * blend + centroids_rgb * (1.0 - blend)
    else:
        blended = mapped_palette_rgb

    blended = np.clip(blended, 0, 255).astype(np.uint8)

    recolored = blended[all_labels].reshape(img.size[1], img.size[0], 3)
    return Image.fromarray(recolored)

def make_new_image(parent, file_path):
    from .theme_page import load_colors_from_css
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
