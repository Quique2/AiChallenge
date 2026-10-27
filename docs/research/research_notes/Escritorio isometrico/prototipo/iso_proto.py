#!/usr/bin/env python3
"""Throwaway prototype: voxel -> 2:1 iso pixel sprites, atlas + manifest, sample room.

Not app code. Validates the projection, face shading, rotation, atlas packing and depth sort
proposed in docs/research/research_notes/Escritorio isometrico/tecnica.md.

Projection (art pixels): voxel corner (x, y, z) -> (2 * (x - y), (x + y) - 2 * z).
8 voxels per tile edge -> tile = 32 x 16 px. View direction is (1, 1, 1), so painter's order by
x + y + z is exact for unit voxels.
"""
import json
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "brand"))  # docs/brand
from draw_scene import PALETTE  # noqa: E402

VOX_PER_TILE = 8
TILE_W, TILE_H = 32, 16
OUT = Path(__file__).resolve().parent / "out"

# material -> (top, left, right, outline); every key is from the existing brand palette
RAMPS = {
    "oak": ("oak_hi", "oak", "oak_shadow", "oak_deep"),
    "oakdark": ("oak", "oak_shadow", "oak_deep", "oak_deep"),
    "pot": ("pot_hi", "pot", "pot_shadow", "oak_deep"),
    "leaf": ("leaf_hi", "leaf", "leaf_deep", "wall_deep"),
    "cream": ("cream", "peach", "apricot", "oak_shadow"),
    "ink": ("ink_hi", "ink_hi", "ink", "ink"),
    "sage": ("sage_hi", "sage", "sage_shadow", "wall_deep"),
    "screen": ("screen_hi", "screen", "screen", "ink"),
    "wall": ("wall_lit", "wall", "wall_deep", "wall_deep"),
    "blind": ("blind", "blind", "blind_shadow", "oak_shadow"),
}
# 4x4 stamp of one voxel, relative to the projection of its (x, y, z) corner. T/L/R = face.
STAMP = [".TT.", "LTTR", "LLRR", ".LR."]


def hex_rgba(key):
    h = PALETTE[key].lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


class Model:
    def __init__(self, w, d, h):
        self.w, self.d, self.h = w, d, h  # voxels
        self.v = {}

    def box(self, x, y, z, w, d, h, mat):
        for i in range(x, x + w):
            for j in range(y, y + d):
                for k in range(z, z + h):
                    self.v[(i, j, k)] = mat
        return self

    def rotated(self, quarter):
        """Quarter turns around the vertical axis, keeping the footprint at the origin."""
        m = self
        for _ in range(quarter % 4):
            r = Model(m.d, m.w, m.h)
            r.v = {(m.d - 1 - y, x, z): mat for (x, y, z), mat in m.v.items()}
            m = r
        return m


def render(model, outline=True):
    """Returns (RGBA image, anchor) where anchor is the pixel of the footprint's back corner."""
    # screen bounds of every stamp
    xs, ys = [], []
    for (x, y, z) in model.v:
        sx, sy = 2 * (x - y), (x + y) - 2 * z
        xs += [sx - 2, sx + 2]
        ys += [sy - 2, sy + 2]
    pad = 1 if outline else 0
    x0, y0 = min(xs) - pad, min(ys) - pad
    w, h = max(xs) - x0 + pad, max(ys) - y0 + pad
    buf = [[None] * w for _ in range(h)]
    for (x, y, z), mat in sorted(model.v.items(), key=lambda kv: sum(kv[0])):
        sx, sy = 2 * (x - y) - x0, (x + y) - 2 * z - y0
        for r, row in enumerate(STAMP):
            for c, face in enumerate(row):
                if face != ".":
                    buf[sy - 2 + r][sx - 2 + c] = (mat, face)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for yy in range(h):
        for xx in range(w):
            cell = buf[yy][xx]
            if cell:
                mat, face = cell
                top, left, right, _ = RAMPS[mat]
                px[xx, yy] = hex_rgba({"T": top, "L": left, "R": right}[face])
    if outline:  # selective outline: darkest tone of the neighbouring material, never pure black
        for yy in range(h):
            for xx in range(w):
                if buf[yy][xx]:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = xx + dx, yy + dy
                    if 0 <= nx < w and 0 <= ny < h and buf[ny][nx]:
                        px[xx, yy] = hex_rgba(RAMPS[buf[ny][nx][0]][3])
                        break
    return img, (-x0, -y0)


# --- Objects (footprint in tiles, built in voxels) ----------------------------------------

def desk():
    m = Model(16, 8, 7)
    m.box(0, 0, 6, 16, 8, 1, "oak")
    for x, y in ((0, 0), (15, 0), (0, 7), (15, 7)):
        m.box(x, y, 0, 1, 1, 6, "oakdark")
    m.box(1, 0, 3, 14, 1, 3, "oakdark")  # modesty panel at the back
    return m, (2, 1), "floor"


def chair():
    m = Model(8, 8, 10)
    m.box(1, 1, 3, 6, 6, 1, "sage")
    m.box(1, 0, 4, 6, 1, 6, "sage")  # backrest at the back
    for x, y in ((1, 1), (6, 1), (1, 6), (6, 6)):
        m.box(x, y, 0, 1, 1, 3, "ink")
    return m, (1, 1), "floor"


def plant():
    m = Model(8, 8, 12)
    m.box(2, 2, 0, 4, 4, 4, "pot")
    m.box(3, 3, 4, 2, 2, 7, "leaf")
    m.box(2, 3, 6, 1, 1, 4, "leaf")
    m.box(5, 4, 5, 1, 1, 4, "leaf")
    m.box(4, 2, 7, 1, 1, 4, "leaf")
    return m, (1, 1), "floor"


def bookshelf():
    m = Model(8, 4, 18)
    m.box(0, 0, 0, 8, 4, 18, "oak")
    for z in (1, 6, 11):
        m.box(1, 3, z, 6, 1, 4, "oakdark")  # open shelves facing +y
        m.box(1, 3, z, 2, 1, 3, "cream")
        m.box(4, 3, z, 1, 1, 4, "sage")
        m.box(5, 3, z, 1, 1, 3, "pot")
    return m, (1, 1), "floor"


def lamp():
    m = Model(4, 4, 9)
    m.box(1, 1, 0, 2, 2, 1, "ink")
    m.box(1, 1, 1, 1, 1, 6, "ink")
    m.box(1, 1, 7, 3, 3, 2, "cream")
    return m, (0, 0), "surface"  # stands on a host surface


def rug():
    m = Model(16, 16, 1)
    m.box(0, 0, 0, 16, 16, 1, "blind")
    m.box(2, 2, 0, 12, 12, 1, "sage")
    m.box(4, 4, 0, 8, 8, 1, "cream")
    return m, (2, 2), "flat"


OBJECTS = {"desk": desk, "chair": chair, "plant": plant, "bookshelf": bookshelf, "lamp": lamp, "rug": rug}


def pack(sprites):
    """Shelf packer: tallest first, rows of max width 256. Returns atlas + rects."""
    order = sorted(sprites, key=lambda k: -sprites[k].height)
    max_w, x, y, row_h, rects = 256, 0, 0, 0, {}
    for key in order:
        im = sprites[key]
        if x + im.width > max_w:
            x, y, row_h = 0, y + row_h + 1, 0
        rects[key] = (x, y, im.width, im.height)
        x += im.width + 1  # 1 px gutter so nearest sampling never bleeds
        row_h = max(row_h, im.height)
    atlas = Image.new("RGBA", (max_w, y + row_h), (0, 0, 0, 0))
    for key, (ax, ay, _, _) in rects.items():
        atlas.paste(sprites[key], (ax, ay))
    return atlas, rects


# --- Room ------------------------------------------------------------------------------------

def room_shell(w_tiles, d_tiles, wall_h=24):
    """Floor (planks) + two back walls, one voxel thick, with a window on the right wall."""
    W, D = w_tiles * VOX_PER_TILE, d_tiles * VOX_PER_TILE
    m = Model(W + 1, D + 1, wall_h + 1)
    for x in range(W):
        for y in range(D):
            m.v[(x + 1, y + 1, 0)] = "oak" if (x // 2 + y // 8) % 3 else "oakdark"
    m.box(0, 0, 0, 1, D + 1, wall_h + 1, "wall")  # left wall (x = 0 plane)
    m.box(0, 0, 0, W + 1, 1, wall_h + 1, "wall")  # right wall (y = 0 plane)
    window = [(x, 0, z) for x in range(18, 30) for z in range(9, 21)]
    for p in window:
        m.v.pop(p, None)  # the pane is a hole; the sky is drawn behind the wall
    return m, window


def topo_order(items):
    """items: list of dict with x0, y0, x1, y1 (tile footprint, exclusive max) and screen bbox."""
    def overlap(a, b):
        ax0, ay0, ax1, ay1 = a["bbox"]
        bx0, by0, bx1, by1 = b["bbox"]
        return ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1

    def behind(a, b):  # a must be drawn before b
        if a["x1"] <= b["x0"] and not b["y1"] <= a["y0"]:
            return True
        if a["y1"] <= b["y0"] and not b["x1"] <= a["x0"]:
            return True
        return False

    n = len(items)
    edges = {i: set() for i in range(n)}
    indeg = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j and overlap(items[i], items[j]) and behind(items[i], items[j]):
                if j not in edges[i]:
                    edges[i].add(j)
                    indeg[j] += 1
    ready = sorted((i for i in range(n) if indeg[i] == 0), key=lambda i: items[i]["x0"] + items[i]["y0"])
    out = []
    while ready:
        i = ready.pop(0)
        out.append(i)
        for j in sorted(edges[i]):
            indeg[j] -= 1
            if indeg[j] == 0:
                ready.append(j)
        ready.sort(key=lambda k: items[k]["x0"] + items[k]["y0"])
    assert len(out) == n, "cycle (should not happen with non-overlapping floor footprints)"
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sprites, meta = {}, {}
    for name, make in OBJECTS.items():
        model, foot, kind = make()
        for rot in range(4):
            img, anchor = render(model.rotated(rot))
            key = f"{name}.r{rot}"
            sprites[key] = img
            fw, fd = foot if rot % 2 == 0 else (foot[1], foot[0])
            meta[key] = {"anchor": anchor, "footprint": [fw, fd], "kind": kind}
    atlas, rects = pack(sprites)
    atlas.save(OUT / "atlas.png", optimize=True)
    manifest = {
        "version": 1, "tile": [TILE_W, TILE_H], "voxelsPerTile": VOX_PER_TILE, "atlas": "atlas.png",
        "size": list(atlas.size),
        "frames": {k: {"rect": rects[k], **meta[k]} for k in sorted(rects)},
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))

    # Compose a 6x6 room: shell, sky behind the window, rug, then topo-sorted floor items.
    shell, window = room_shell(6, 6)
    shell_img, shell_anchor = render(shell, outline=False)
    canvas = Image.new("RGBA", (shell_img.width + 8, shell_img.height + 8), hex_rgba("cream"))
    ox, oy = shell_anchor[0] + 4, shell_anchor[1] + 4  # screen of voxel corner (0,0,0)
    sky = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    spx = sky.load()
    for (x, y, z) in window:
        sx, sy = 2 * (x - y) + ox, (x + y) - 2 * z + oy
        key = "day_top" if z > 16 else "day_mid" if z > 12 else "day_low"
        for r in range(-2, 2):
            for c in range(-2, 2):
                spx[sx + c, sy + r] = hex_rgba(key)
    canvas.alpha_composite(sky)
    canvas.alpha_composite(shell_img, (4, 4))

    def tile_origin(gx, gy):  # +1 voxel: the floor starts after the wall thickness
        vx, vy = gx * VOX_PER_TILE + 1, gy * VOX_PER_TILE + 1
        return 2 * (vx - vy) + ox, (vx + vy) + oy - 2  # floor top is z = 1

    layout = [  # (frame, gx, gy)
        ("bookshelf.r0", 0, 0), ("desk.r0", 2, 0), ("chair.r2", 3, 1), ("plant.r0", 5, 0),
        ("plant.r0", 0, 4), ("chair.r1", 4, 4), ("bookshelf.r1", 0, 2),
    ]
    rug_x, rug_y = tile_origin(2, 2)
    fr = manifest["frames"]["rug.r0"]
    canvas.alpha_composite(sprites["rug.r0"], (rug_x - fr["anchor"][0], rug_y - fr["anchor"][1]))
    items = []
    for frame, gx, gy in layout:
        f = manifest["frames"][frame]
        sx, sy = tile_origin(gx, gy)
        px0, py0 = sx - f["anchor"][0], sy - f["anchor"][1]
        im = sprites[frame]
        items.append({"frame": frame, "pos": (px0, py0), "x0": gx, "y0": gy,
                      "x1": gx + f["footprint"][0], "y1": gy + f["footprint"][1],
                      "bbox": (px0, py0, px0 + im.width, py0 + im.height)})
    for i in topo_order(items):
        it = items[i]
        canvas.alpha_composite(sprites[it["frame"]], it["pos"])
        if it["frame"].startswith("desk"):  # surface item: drawn right after its host
            lf = manifest["frames"]["lamp.r0"]
            lx, ly = tile_origin(it["x0"], it["y0"])
            lx, ly = lx + 2 * (3 - 2), ly + (3 + 2) - 2 * 7  # local voxel (3, 2) on top (z = 7)
            canvas.alpha_composite(sprites["lamp.r0"], (lx - lf["anchor"][0], ly - lf["anchor"][1]))
    canvas.save(OUT / "room-1x.png")
    canvas.resize((canvas.width * 4, canvas.height * 4), Image.NEAREST).save(OUT / "room-4x.png")
    atlas.resize((atlas.width * 3, atlas.height * 3), Image.NEAREST).save(OUT / "atlas-3x.png")
    print("room", canvas.size, "atlas", atlas.size, "frames", len(rects))
    for k in ("desk.r0", "chair.r0", "plant.r0", "bookshelf.r0", "lamp.r0", "rug.r0"):
        print(k, rects[k][2:], "anchor", meta[k]["anchor"])


if __name__ == "__main__":
    main()
