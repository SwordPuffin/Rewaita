# image_to_css.py
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

import gi, os, colorsys
import numpy as np
from PIL import Image
from gi.repository import GLib
from .utils import run_loading_task, add_new_theme_button, open_toast, hex_to_rgb, rgb_to_hex
from .css_templates import CSS_TEMPLATE

def relative_luminance(rgb):
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)

def contrast_ratio(rgb1, rgb2):
    l1 = relative_luminance(rgb1) + 0.05
    l2 = relative_luminance(rgb2) + 0.05
    return max(l1, l2) / min(l1, l2)

def rgb_to_hsl(rgb):
    r, g, b = (c / 255.0 for c in rgb)
    h, l, s = colorsys.rgb_to_hls(r, g, b)[0], colorsys.rgb_to_hls(r, g, b)[1], colorsys.rgb_to_hls(r, g, b)[2]
    return h, s, l

def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h % 1.0, max(0.0, min(1.0, l)), max(0.0, min(1.0, s)))
    return (r * 255, g * 255, b * 255)

def adjust_lightness(rgb, delta):
    r, g, b = (c + (delta * 10) for c in rgb)
    return (r, g, b)

def set_lightness(rgb, l, s_min=0.25):
    h, s, _ = rgb_to_hsl(rgb)
    s = max(s, s_min)
    return hsl_to_rgb(h, s, l)

def ensure_contrast(fg_rgb, bg_rgb, min_ratio=4.5):
    h, s, l = rgb_to_hsl(fg_rgb)
    bg_is_dark = relative_luminance(bg_rgb) < 0.5
    step = 0.03 if bg_is_dark else -0.03
    rgb = fg_rgb
    tries = 0
    while(contrast_ratio(rgb, bg_rgb) < min_ratio and 0.0 <= l <= 1.0 and tries < 30):
        l += step
        l = max(0.0, min(1.0, l))
        rgb = hsl_to_rgb(h, s, l)
        tries += 1
    return rgb

def kmeans_palette(pixels, n_colors, max_iter=50):
    rng = np.random.default_rng(0)
    n = pixels.shape[0]
    n_colors = min(n_colors, n)

    centers = np.empty((n_colors, 3), dtype=np.float64)
    first = rng.integers(0, n)
    centers[0] = pixels[first]
    closest_sq = np.sum((pixels - centers[0]) ** 2, axis=1)
    
    for i in range(1, n_colors):
        total = closest_sq.sum()
        if(total <= 0):
            idx = rng.integers(0, n)
        else:
            probs = closest_sq / total
            idx = rng.choice(n, p=probs)
        centers[i] = pixels[idx]
        dist_sq = np.sum((pixels - centers[i]) ** 2, axis=1)
        closest_sq = np.minimum(closest_sq, dist_sq)

    labels = np.zeros(n, dtype=np.int64)
    for _ in range(max_iter):
        dists = np.sum((pixels[:, None, :] - centers[None, :, :]) ** 2, axis=2)
        new_labels = np.argmin(dists, axis=1)
        if(np.array_equal(new_labels, labels) and _ > 0):
            labels = new_labels
            break
        labels = new_labels
        for i in range(n_colors):
            mask = labels == i
            if(mask.any()):
                centers[i] = pixels[mask].mean(axis=0)
            else:
                dist_sq = np.sum((pixels - centers[i]) ** 2, axis=1)
                centers[i] = pixels[np.argmax(dist_sq)]

    counts = np.array([(labels == i).sum() for i in range(n_colors)])
    order = np.argsort(-counts)
    return centers[order], counts[order]

def extract_palette(image_path, n_colors=24, sample_size=20000, max_iter=50):
    img = Image.open(image_path).convert("RGB")
    arr = np.asarray(img).reshape(-1, 3)

    if(arr.shape[0] > sample_size):
        rng = np.random.default_rng(0)
        idx = rng.choice(arr.shape[0], size=sample_size, replace=False)
        sample = arr[idx]
    else:
        sample = arr

    centers, counts = kmeans_palette(sample, n_colors, max_iter=max_iter)
    return centers, counts

HUE_DEG = {
    "red": 0,
    "orange": 30,
    "yellow": 50,
    "green": 120,
    "blue": 215,
    "purple": 280,
}

def circular_hue_dist(h1_deg, h2_deg):
    d = abs(h1_deg - h2_deg) % 360
    return min(d, 360 - d)

def pick_seed_for_hue(palette_hsl, target_deg, min_sat=0.18):
    best = None
    best_score = None
    for h, s, l, weight in palette_hsl:
        if(s < min_sat):
            continue
        hue_deg = h * 360
        dist = circular_hue_dist(hue_deg, target_deg)
        score = dist - (s * 40) - (weight * 10)
        if(best_score is None or score < best_score):
            best_score = score
            best = (h, s, l)
    if(best is None):
        return (target_deg / 360, 0.45, 0.55)
    return best

def five_shades(seed_hsl, dark_theme):
    h, s, l = seed_hsl
    s = max(0.35, min(0.85, s))
    lightnesses = [0.68, 0.60, 0.52, 0.44, 0.36] if dark_theme else \
                  [0.72, 0.62, 0.52, 0.42, 0.32]
    hue_drift = [0, 6, -6, 10, -10]
    return [rgb_to_hex(hsl_to_rgb((h + d / 360) % 1.0, s, ll))
            for d, ll in zip(hue_drift, lightnesses)]
 
def neutral_shades(seed_hsl, dark_theme, kind):
    h, _, _ = seed_hsl
    s = 0.12 if kind != "brown" else 0.18
    if(kind == "light"):
        lightnesses = [0.88, 0.92, 0.96, 0.35, 0.55]
    elif(kind == "dark"):
        lightnesses = [0.28, 0.32, 0.22, 0.16, 0.10]
    else: 
        lightnesses = [0.38, 0.32, 0.26, 0.20, 0.88]
    return [rgb_to_hex(hsl_to_rgb((h + i * 0.01) % 1.0, s, ll)) for i, ll in enumerate(lightnesses)]

def build_theme(image_path, n_colors=24, sample_size=20000, max_iter=50, blend=1.0, force_mode=None):
    centers, counts = extract_palette(image_path, n_colors=n_colors, sample_size=sample_size, max_iter=max_iter)
    total = counts.sum()
    weights = counts / max(total, 1)

    hsl_list = [rgb_to_hsl(tuple(c)) for c in centers]
    palette_hsl = [(h, s, l, w) for (h, s, l), w in zip(hsl_list, weights)]

    avg_luminance = float(np.average([relative_luminance(tuple(c)) for c in centers], weights=weights))
    if(force_mode == "dark"):
        dark_theme = True
    elif(force_mode == "light"):
        dark_theme = False
    else:
        dark_theme = avg_luminance < 0.5

    def luminance_of(i):
        return relative_luminance(tuple(centers[i]))

    order_by_weight = list(np.argsort(-counts))
    bg_candidates = [i for i in order_by_weight
                      if (luminance_of(i) < 0.45) == dark_theme]
    bg_idx = bg_candidates[0] if bg_candidates else order_by_weight[0]
    bg_rgb = tuple(centers[bg_idx])

    target_l = 0.16 if dark_theme else 0.96
    bg_rgb = set_lightness(bg_rgb, target_l, s_min=0.06)

    fg_seed = (0.0, 0.0, 0.92 if dark_theme else 0.15)
    fg_rgb = hsl_to_rgb(*fg_seed)
    fg_rgb = ensure_contrast(fg_rgb, bg_rgb, min_ratio=7.0)
    
    if(blend > 0):
        dominant_rgb = tuple(centers[order_by_weight[0]])
        def mix(a, b, t):
            return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))
        bg_rgb = mix(bg_rgb, dominant_rgb, blend)
        
    step = 1.0 if dark_theme else -1.0
    headerbar_rgb = adjust_lightness(bg_rgb, step)
    card_rgb = adjust_lightness(bg_rgb, step * 1.6)
    sidebar_rgb = adjust_lightness(bg_rgb, step * -1.6)
    sidebar_border_rgb = adjust_lightness(bg_rgb, step)

    fg_rgb = ensure_contrast(fg_rgb, bg_rgb, min_ratio=7.0)

    accents = {}
    for name, target_deg in HUE_DEG.items():
        seed_hsl = pick_seed_for_hue(palette_hsl, target_deg)
        accents[name] = five_shades(seed_hsl, dark_theme)

    bg_h, bg_s, _ = rgb_to_hsl(bg_rgb)
    accents["brown"] = neutral_shades((bg_h, bg_s, 0), dark_theme, "brown")
    accents["light"] = neutral_shades((bg_h, bg_s, 0), dark_theme, "light")
    accents["dark"] = neutral_shades((bg_h, bg_s, 0), dark_theme, "dark")

    colors = {
        "window-bg": rgb_to_hex(bg_rgb),
        "window-fg": rgb_to_hex(fg_rgb),
        "view-bg": rgb_to_hex(bg_rgb),
        "view-fg": rgb_to_hex(fg_rgb),
        "headerbar-bg": rgb_to_hex(headerbar_rgb),
        "headerbar-backdrop": rgb_to_hex(headerbar_rgb),
        "headerbar-fg": rgb_to_hex(fg_rgb),
        "popover-bg": rgb_to_hex(bg_rgb),
        "popover-fg": rgb_to_hex(fg_rgb),
        "card-bg": rgb_to_hex(card_rgb),
        "card-fg": rgb_to_hex(fg_rgb),
        "sidebar-bg": rgb_to_hex(sidebar_rgb),
        "sidebar-fg": rgb_to_hex(fg_rgb),
        "sidebar-border": rgb_to_hex(sidebar_border_rgb),
    }
    return colors, accents

ACCENT_ORDER = ["blue", "green", "yellow", "orange", "red", "purple", "brown", "light", "dark"]

ACCENT_INDICES = [
    ("blue", [1, 2]),
    ("green", [1]),
    ("yellow", [1]),
    ("red", [1]),
    ("purple", [1, 2]),
    ("orange", [1]),
    ("brown", [1]),
    ("light", [1, 5]),
    ("dark", [1]),
]

def render_css(colors, accents):
    accent_lines = []
    for name, indices in ACCENT_INDICES:
        for i in indices:
            hexval = accents[name][i - 1]
            accent_lines.append(f"  --{name}-{i}: {hexval};")
    return CSS_TEMPLATE.format(
        window_bg=colors["window-bg"], window_fg=colors["window-fg"],
        view_bg=colors["view-bg"], view_fg=colors["view-fg"],
        headerbar_bg=colors["headerbar-bg"],
        headerbar_backdrop=colors["headerbar-backdrop"],
        headerbar_fg=colors["headerbar-fg"],
        popover_bg=colors["popover-bg"], popover_fg=colors["popover-fg"],
        card_bg=colors["card-bg"], card_fg=colors["card-fg"],
        sidebar_bg=colors["sidebar-bg"], sidebar_fg=colors["sidebar-fg"],
        sidebar_border=colors["sidebar-border"],
        accent_lines="\n".join(accent_lines),
    )

def make_new_theme(parent, image_path, output, light):
    folder = "light" if light else "dark"
    theme_file = os.path.join(GLib.get_user_data_dir(), folder, output + ".css")
    
    def do_create_theme():
        colors, accents = build_theme(image_path, force_mode=light)
        return render_css(colors, accents)

    def on_css_ready(css):
        with open(theme_file, "w") as f:
            f.write(css)
        
        if(folder == "light"):
            flowbox = parent.light_flowbox
        else:
            flowbox = parent.dark_flowbox
        
        add_new_theme_button(theme_file, flowbox, parent.on_theme_button_clicked, folder)
        open_toast(parent, output + _(" Has Been Saved"))
        
    run_loading_task(parent, do_create_theme, on_css_ready)
