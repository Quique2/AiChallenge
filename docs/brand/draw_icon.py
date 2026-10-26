#!/usr/bin/env python3
"""SpaceEase app icon: hand-placed 32x32 pixel art, fully deterministic.

Concept: an arched window (the "space") with a calm desk in front of it:
a monitor whose wave settles into a flat line (noise easing off) and a
snake plant. Soft dawn light from the window; nothing else competes.

Usage: python draw_icon.py [out_dir]   (default: this script's directory)
Writes icon.png, adaptive-icon.png, splash-icon.png, favicon.png,
preview.png and grid.png (32x32 at 1x, for inspection).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

N = 32

# "Quiet workspace" palette: every ramp hue-shifts (warm lights, cooler/plum shadows).
PALETTE = {
    "wall_deep":  "#173a3d",
    "wall":       "#20494a",
    "wall_lit":   "#2b5b58",
    "mist":       "#d3e7df",
    "cream":      "#f7eedb",
    "peach":      "#f3d4b0",
    "apricot":    "#e9b58c",
    "oak_hi":     "#e0aa70",
    "oak":        "#bf7f4c",
    "oak_shadow": "#8f5440",
    "oak_deep":   "#5c3438",
    "ink":        "#1f2c35",
    "ink_hi":     "#3a4f59",
    "screen_hi":  "#e4f5ec",
    "screen":     "#c3e6d6",
    "wave":       "#3f8a7b",
    "leaf_hi":    "#8db865",
    "leaf":       "#4f8a55",
    "leaf_deep":  "#2f5e4c",
    "pot_hi":     "#e08a58",
    "pot":        "#c0643c",
    "pot_shadow": "#8a3f34",
}

# Arch: half-width per row from y=2; cells 16-w .. 15+w. Steps 2,1,1,1,1 then
# vertical runs of 2 and 3 give a clean pixel arc.
ARCH_TOP = 2
ARCH_HALF = [4, 6, 7, 8, 9, 10, 10, 11, 11, 11]
ARCH_FULL = 12
DESK_TOP = 22


def checker(x, y):
    return (x + y) % 2 == 0


def arch_half(y):
    if y < ARCH_TOP:
        return 0
    i = y - ARCH_TOP
    return ARCH_HALF[i] if i < len(ARCH_HALF) else ARCH_FULL


def in_arch(x, y):
    w = arch_half(y)
    return y < DESK_TOP and w > 0 and 16 - w <= x <= 15 + w


class Layer:
    def __init__(self):
        self.c = [[None] * N for _ in range(N)]
        self.dither = set()

    def set(self, x, y, key):
        if 0 <= x < N and 0 <= y < N:
            self.c[y][x] = key

    def hline(self, x0, x1, y, key):
        for x in range(x0, x1 + 1):
            self.set(x, y, key)

    def rect(self, x0, y0, x1, y1, key):
        for y in range(y0, y1 + 1):
            self.hline(x0, x1, y, key)


def wall_layer():
    wall = Layer()
    arch = [(ax, ay) for ay in range(N) for ax in range(N) if in_arch(ax, ay)]
    for y in range(N):
        for x in range(N):
            if in_arch(x, y):
                continue
            # Daylight from the window falls off with distance: lit, dither, wall, dither, deep.
            d = min(((x - ax) ** 2 + (y - ay) ** 2) ** 0.5 for ax, ay in arch)
            if d <= 1.5:
                key = "wall_lit"
            elif d <= 2.5:
                key = "wall_lit" if checker(x, y) else "wall"
                wall.dither.add((x, y))
            elif d <= 3.5:
                key = "wall"
            elif d <= 4.5:
                key = "wall" if checker(x, y) else "wall_deep"
                wall.dither.add((x, y))
            else:
                key = "wall_deep"
            wall.set(x, y, key)
    return wall


def sparse(x, y):
    """25% ordered-dither mask."""
    return (x + 2 * (y % 2)) % 4 == 0


def sky_layer():
    sky = Layer()
    # (first row, upper, lower): row = 50% checker, row+1 = lower with 25% upper dots.
    transitions = [(5, "mist", "cream"), (11, "cream", "peach"), (16, "peach", "apricot")]
    for y in range(N):
        for x in range(N):
            if not in_arch(x, y):
                continue
            key = "mist"
            for row, upper, lower in transitions:
                if y < row:
                    break
                if y == row:
                    key = upper if checker(x, y) else lower
                    sky.dither.add((x, y))
                    break
                if y == row + 1:
                    key = upper if sparse(x, y) else lower
                    sky.dither.add((x, y))
                    break
                key = lower
            sky.set(x, y, key)
    return sky


def desk_layer(x0, x1):
    desk = Layer()
    t = DESK_TOP
    desk.hline(x0, x1, t, "oak_hi")
    desk.hline(x0, x1, t + 1, "oak")
    desk.hline(x0, x1, t + 2, "oak")
    for a, b in [(2, 8), (17, 24)]:  # long, thin grain streaks
        desk.hline(max(a, x0), min(b, x1), t + 2, "oak_shadow")
    desk.hline(x0, x1, t + 3, "oak_shadow")
    desk.hline(x0, x1, t + 4, "oak_deep")
    # Contact shadows under the monitor base and the pot.
    desk.hline(8, 14, t, "oak")
    desk.hline(20, 24, t, "oak")
    return desk


def monitor_layer():
    m = Layer()
    # Frame x6..16, y10..18; rim light from the window on the top edge.
    m.rect(6, 10, 16, 18, "ink")
    m.hline(7, 15, 10, "ink_hi")
    # Screen x7..15, y11..16 with a soft top glow.
    for y in range(11, 17):
        for x in range(7, 16):
            key = "screen_hi" if y == 11 else "screen"
            m.set(x, y, key)
    # A wave that settles into a flat line: noise easing off.
    for x, y in [(8, 14), (9, 13), (10, 12), (11, 13), (12, 14), (13, 14), (14, 14)]:
        m.set(x, y, "wave")
    # Neck and base.
    m.rect(10, 19, 12, 20, "ink")
    m.set(10, 19, "ink_hi")
    m.set(10, 20, "ink_hi")
    m.hline(8, 14, 21, "ink")
    return m


def plant_layer():
    p = Layer()
    # Pot: rim y17 x19..25, body y18..20 x20..24, foot y21 x21..23.
    p.hline(19, 25, 17, "pot_hi")
    p.set(25, 17, "pot_shadow")
    p.rect(20, 18, 24, 20, "pot")
    p.hline(21, 24, 18, "pot_shadow")
    for y in (19, 20):
        p.set(20, y, "pot_hi")
        p.set(24, y, "pot_shadow")
    p.hline(21, 23, 21, "pot_shadow")
    # Snake-plant blades: (cells, lit-edge cells). Lit from the window (up-left).
    blades = [
        # centre blade, tallest
        ([(22, 7), (22, 8), (23, 8)] + [(x, y) for y in range(9, 17) for x in (22, 23)],
         [(22, y) for y in range(7, 17)]),
        # left blade, leaning out
        ([(19, 10), (19, 11), (20, 11), (19, 12), (20, 12), (20, 13), (21, 13),
          (20, 14), (21, 14), (21, 15), (21, 16)],
         [(19, 10), (19, 11), (19, 12), (20, 13), (20, 14), (21, 15)]),
        # right blade
        ([(25, 9), (25, 10), (24, 10), (25, 11), (24, 11), (24, 12), (25, 12),
          (24, 13), (23, 14), (24, 14), (23, 15), (24, 15), (24, 16)],
         [(25, 9), (24, 10), (24, 11), (24, 12), (24, 13), (23, 14), (23, 15)]),
    ]
    for cells, lit in blades:
        for x, y in cells:
            p.set(x, y, "leaf")
        for x, y in lit:
            p.set(x, y, "leaf_hi")
    # Deep shade where the blades cross and at the base.
    for x, y in [(22, 16), (23, 16), (24, 16), (21, 16), (23, 15)]:
        p.set(x, y, "leaf_deep")
    return p


def compose(layers):
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    px = img.load()
    dither = set()
    for layer in layers:
        for y in range(N):
            for x in range(N):
                key = layer.c[y][x]
                if key:
                    h = PALETTE[key].lstrip("#")
                    px[x, y] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
                    if (x, y) in layer.dither:
                        dither.add((x, y))
                    else:
                        dither.discard((x, y))
    img.info["dither"] = dither
    return img


def orphans(img, dither):
    """Pixels with no same-coloured 8-neighbour, ignoring intentional ordered-dither cells."""
    px = img.load()
    out = []
    for y in range(N):
        for x in range(N):
            c = px[x, y]
            if c[3] == 0 or (x, y) in dither:
                continue
            same = any(
                0 <= x + dx < N and 0 <= y + dy < N and px[x + dx, y + dy] == c
                for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy
            )
            if not same:
                out.append((x, y))
    return out


def upscale(img, k):
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def place_centered(sprite, size, max_frac, circle=False):
    """Integer nearest-neighbour scale so the sprite fits max_frac of a size x size canvas.

    With circle=True every opaque cell must sit inside a centred circle of diameter
    max_frac * size (Android adaptive-icon safe zone), not just the square.
    """
    if circle:
        cx, cy = sprite.width / 2, sprite.height / 2
        a = sprite.getchannel("A").load()
        reach = max(
            ((max(abs(x - cx), abs(x + 1 - cx))) ** 2 + (max(abs(y - cy), abs(y + 1 - cy))) ** 2) ** 0.5
            for y in range(sprite.height) for x in range(sprite.width) if a[x, y]
        )
        k = int(size * max_frac / 2 // reach)
    else:
        k = int(size * max_frac) // max(sprite.width, sprite.height)
    big = upscale(sprite, k)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(big, ((size - big.width) // 2, (size - big.height) // 2), big)
    return canvas


def rounded_mask(size):
    m = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size * 4 - 1, size * 4 - 1], radius=int(size * 4 * 0.2237), fill=255)
    return m.resize((size, size), Image.LANCZOS)


def preview(icon1024):
    sizes = [60, 120, 180]
    pad = 24
    w = sum(sizes) + pad * (len(sizes) + 1)
    h = (max(sizes) + pad * 2) * 2
    sheet = Image.new("RGB", (w, h), "#f2f2f7")
    ImageDraw.Draw(sheet).rectangle([0, h // 2, w, h], fill="#1c1c1e")
    for row in range(2):
        x = pad
        for s in sizes:
            small = icon1024.convert("RGB").resize((s, s), Image.LANCZOS)
            y = row * (h // 2) + pad + (max(sizes) - s) // 2
            sheet.paste(small, (x, y), rounded_mask(s))
            x += s + pad
    return sheet


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
    out.mkdir(parents=True, exist_ok=True)

    icon = compose([wall_layer(), sky_layer(), desk_layer(0, N - 1), monitor_layer(), plant_layer()])
    # Subject only (no wall) with a finite desk, for Android adaptive + splash.
    subject = compose([sky_layer(), desk_layer(4, 27), monitor_layer(), plant_layer()])
    subject = subject.crop(subject.getbbox())

    bad = orphans(icon, icon.info["dither"])
    if bad:
        print("orphan pixels:", bad)

    icon_rgb = upscale(icon, 1024 // N).convert("RGB")  # opaque for iOS
    icon_rgb.save(out / "icon.png")
    upscale(icon, 1).save(out / "grid.png")
    place_centered(subject, 1024, 0.66, circle=True).save(out / "adaptive-icon.png")
    place_centered(subject, 1024, 0.92).save(out / "splash-icon.png")
    icon_rgb.resize((48, 48), Image.BOX).save(out / "favicon.png")
    preview(icon_rgb).save(out / "preview.png")
    colors = {icon.getpixel((x, y)) for y in range(N) for x in range(N)}
    print(f"ok: {len(colors)} colours, {len(bad)} orphans -> {out}")


if __name__ == "__main__":
    main()
