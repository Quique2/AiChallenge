#!/usr/bin/env python3
"""Maqueta del cuarto isométrico (concepto, no es un asset de la app).

Un renderizador de vóxeles mínimo: cada vóxel se dibuja como un bloque de 4x4 pixeles en
proyección 2:1 (cara de arriba, cara +y a la izquierda, cara +x a la derecha), en orden de
profundidad (algoritmo del pintor). Las caras usan la paleta "Quiet workspace" con cambio de
tono entre luz y sombra. Rotar un objeto 90° es rotar sus vóxeles: no hay que redibujarlo.

Uso: python draw_room_mockup.py   (escribe room-mockup.png junto a este script)
"""
from pathlib import Path

from PIL import Image

X, Y, H = 30, 30, 20  # tamaño del cuarto en vóxeles (x hacia abajo a la derecha, y hacia abajo a la izquierda)
SCALE = 5

# material -> (arriba, cara izquierda +y, cara derecha +x)
M = {
    "floor": ("#c98a55", "#a86a43", "#8f5440"),
    "floor_alt": ("#bf7f4c", "#a86a43", "#8f5440"),
    "floor_lit": ("#e9b58c", "#c98a55", "#a86a43"),
    "wall_l": ("#2b5b58", "#20494a", "#20494a"),  # pared de x=0 (se ve su cara +x)
    "wall_r": ("#2b5b58", "#2b5b58", "#173a3d"),  # pared de y=0 (se ve su cara +y)
    "wall_top": ("#3f6e69", "#2b5b58", "#20494a"),
    "trim": ("#e0aa70", "#bf7f4c", "#8f5440"),
    "glass_hi": ("#d3e7df", "#d3e7df", "#d3e7df"),
    "glass": ("#f7eedb", "#f7eedb", "#f7eedb"),
    "glass_low": ("#f3d4b0", "#f3d4b0", "#f3d4b0"),
    "glass_sun": ("#e9b58c", "#e9b58c", "#e9b58c"),
    "blind": ("#efe3cc", "#efe3cc", "#cdb994"),
    "blind_dark": ("#cdb994", "#cdb994", "#b9a27c"),
    "oak": ("#e0aa70", "#bf7f4c", "#8f5440"),
    "oak_dark": ("#8f5440", "#5c3438", "#4a2a2e"),
    "ink": ("#3a4f59", "#1f2c35", "#162028"),
    "screen": ("#e4f5ec", "#c3e6d6", "#c3e6d6"),
    "wave": ("#3f8a7b", "#3f8a7b", "#3f8a7b"),
    "pot": ("#e08a58", "#c0643c", "#8a3f34"),
    "leaf": ("#8db865", "#4f8a55", "#2f5e4c"),
    "leaf_hi": ("#b4d389", "#8db865", "#4f8a55"),
    "cream": ("#f7eedb", "#efe3cc", "#cdb994"),
    "sage": ("#b4cdb9", "#8fae9a", "#6d8c7e"),
    "rug": ("#d99577", "#b86a45", "#8a3f34"),
    "rug_edge": ("#f3d4b0", "#e9b58c", "#c98a55"),
    "lamp": ("#e08a58", "#c0643c", "#8a3f34"),
    "bulb": ("#fff6dc", "#fff6dc", "#fff6dc"),
    "book_a": ("#3f8a7b", "#2f6e62", "#24564c"),
    "book_b": ("#e9b58c", "#c98a55", "#a86a43"),
    "book_c": ("#a96f78", "#8a5560", "#6e4a63"),
    "select": ("#8db865", "#8db865", "#8db865"),
    "grid": ("#b57a4b", "#a86a43", "#8f5440"),
}

voxels = {}


def put(x, y, z, mat):
    voxels[(x, y, z)] = mat


def box(x0, x1, y0, y1, z0, z1, mat):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                put(x, y, z, mat)


def room(edit):
    for x in range(X):
        for y in range(Y):
            lit = 2 <= x <= 13 and 9 <= y <= 22 and (x - 2) <= (y - 6)  # luz de la ventana
            mat = "floor_lit" if lit else ("floor_alt" if (x // 2) % 2 else "floor")
            if edit and (x % 4 == 0 or y % 4 == 0) and not lit:
                mat = "grid"
            put(x, y, 0, mat)
    box(0, 0, 0, Y - 1, 1, H, "wall_l")
    box(0, X - 1, 0, 0, 1, H, "wall_r")
    for y in range(Y):
        put(0, y, H, "wall_top")
    for x in range(X):
        put(x, 0, H, "wall_top")
    # Zoclo de madera.
    box(1, 1, 1, Y - 1, 1, 1, "trim")
    box(1, X - 1, 1, 1, 1, 1, "trim")


def window(blinds):
    y0, y1, z0, z1 = 9, 20, 6, 16
    for y in range(y0, y1 + 1):
        for z in range(z0, z1 + 1):
            frame = y in (y0, y1) or z in (z0, z1)
            if frame:
                put(0, y, z, "trim")
            else:
                band = "glass_hi" if z > 13 else "glass" if z > 10 else "glass_low" if z > 7 else "glass_sun"
                put(0, y, z, band)
    if blinds:
        for z in range(12, z1):
            for y in range(y0 + 1, y1):
                put(1, y, z, "blind" if z % 2 else "blind_dark")


def desk():
    box(5, 20, 1, 7, 8, 8, "oak")  # tablero
    box(5, 20, 7, 7, 7, 7, "oak_dark")
    for x, y in [(5, 7), (20, 7), (5, 2), (20, 2)]:
        box(x, x, y, y, 1, 7, "oak_dark")


def monitor():
    box(9, 15, 2, 3, 10, 15, "ink")
    for x in range(10, 15):
        for z in range(11, 15):
            put(x, 4, z, "screen")
    for x, z in [(10, 12), (11, 13), (12, 12), (13, 12), (14, 12)]:  # la onda que se calma
        put(x, 4, z, "wave")
    box(12, 12, 3, 3, 9, 9, "ink")
    box(11, 13, 3, 4, 9, 9, "ink")


def plant():
    box(17, 19, 3, 5, 9, 10, "pot")
    for x, y, top in [(18, 4, 17), (17, 4, 15), (19, 4, 15), (18, 3, 14), (18, 5, 14)]:
        for z in range(11, top + 1):
            put(x, y, z, "leaf_hi" if z == top else "leaf")


def lamp():
    box(6, 7, 3, 4, 9, 9, "ink")
    for i, z in enumerate(range(10, 15)):
        put(7, 4 + i // 2, z, "ink")
    box(7, 9, 5, 7, 15, 16, "lamp")
    put(8, 6, 14, "bulb")


def headphones(x0=12, y0=6, z0=9):
    box(x0, x0 + 2, y0, y0, z0, z0, "cream")
    put(x0, y0, z0 + 1, "cream")
    put(x0 + 2, y0, z0 + 1, "cream")
    put(x0 + 1, y0, z0 + 2, "ink")


def mug():
    box(16, 17, 6, 7, 9, 10, "cream")
    put(16, 6, 10, "oak_dark")


def chair():
    box(11, 15, 11, 15, 5, 5, "sage")
    box(11, 15, 15, 15, 6, 12, "sage")
    box(13, 13, 13, 13, 1, 4, "ink")
    box(11, 15, 13, 13, 1, 1, "ink")


def rug():
    for x in range(4, 23):
        for y in range(10, 24):
            edge = x in (4, 22) or y in (10, 23)
            put(x, y, 1, "rug_edge" if edge else "rug")


def bookshelf():
    box(1, 4, 23, 28, 1, 14, "oak")
    for z0, z1 in [(2, 5), (7, 10), (12, 13)]:
        for y in range(23, 29):
            mat = ("book_a", "book_b", "book_c")[y % 3]
            box(2, 4, y, y, z0, z1 - (y % 2), mat)


def frame():
    box(19, 25, 1, 1, 11, 16, "oak")
    box(20, 24, 1, 1, 12, 15, "glass_hi")
    box(21, 23, 1, 1, 12, 13, "cream")
    put(22, 1, 14, "pot")


def select_footprint(x0, x1, y0, y1):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if x in (x0, x1) or y in (y0, y1):
                put(x, y, 1, "select")


def render():
    w = (X + Y) * 2 + 4
    h = (X + Y) + H * 2 + 6
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    ox, oy = Y * 2, H * 2

    def paint(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            v = c.lstrip("#")
            px[x, y] = (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16), 255)

    for (x, y, z) in sorted(voxels, key=lambda v: (v[0] + v[1], v[2])):
        top, left, right = M[voxels[(x, y, z)]]
        sx = ox + (x - y) * 2
        sy = oy + (x + y) - z * 2
        for dx in (1, 2):
            paint(sx + dx, sy, top)
        for dx in range(4):
            paint(sx + dx, sy + 1, top)
        for dy in (2, 3):
            paint(sx, sy + dy, left)
            paint(sx + 1, sy + dy, left)
            paint(sx + 2, sy + dy, right)
            paint(sx + 3, sy + dy, right)
    return img.crop(img.getbbox())


def scene(edit):
    voxels.clear()
    room(edit)
    window(blinds=True)
    rug()
    desk()
    monitor()
    plant()
    lamp()
    mug()
    bookshelf()
    frame()
    chair()
    if edit:
        headphones(9, 17, z0=4)  # se está moviendo: levantado sobre su huella marcada en el piso
        select_footprint(8, 12, 16, 18)
    else:
        headphones()
    return render()


def main():
    view, edit = scene(False), scene(True)
    w, h = view.size
    pad = 12
    sheet = Image.new("RGBA", (w * 2 + pad * 3, h + pad * 2), "#f4eee2")
    sheet.paste(view, (pad, pad), view)
    sheet.paste(edit, (w + pad * 2, pad), edit)
    sheet = sheet.resize((sheet.width * SCALE, sheet.height * SCALE), Image.NEAREST)
    out = Path(__file__).resolve().parent / "room-mockup.png"
    sheet.save(out, optimize=True)
    print(f"ok: {len(voxels)} vóxeles -> {out}")


if __name__ == "__main__":
    main()
