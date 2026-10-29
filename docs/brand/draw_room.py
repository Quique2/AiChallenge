#!/usr/bin/env python3
"""Cuarto isométrico: sprites a 1×, atlas, manifiesto tipado y catálogo para la API. Determinista.

Cada mueble es un modelo de vóxeles (uniones de cajas, como en draw_scene.py) que se proyecta a 2:1:
la esquina (x, y, z) de un vóxel cae en el pixel (2(x − y), (x + y) − 2z) y cada vóxel se pinta con
un sello de 4 × 4 (arriba, cara +y a la izquierda, cara +x a la derecha). 8 vóxeles = una baldosa de
32 × 16 px. El orden de pintor por x + y + z es exacto en esta proyección. Las caras usan las rampas
de la paleta "Quiet workspace" (luz fija respecto a la cámara), el contorno es selectivo (el tono más
oscuro del material vecino, nunca negro) y los detalles finos van como calcomanías por cara (la onda
del monitor, los cajones) o como dibujos 2D hechos a mano (hojas, audífonos, el castor).

Lo plano (piso, paredes, ventana, cielo, persiana y objetos de pared) se dibuja en 2D sobre su plano
y se corta en la diagonal 2:1 exacta de la baldosa, así los tramos encajan sin costuras.

Giros: un cuarto de vuelta es (x, y) -> (d − 1 − y, x), como rotateCell en iso.ts. El frente de cada
modelo mira a +y con rot 0, así que los objetos con frente usan facings [0, 3] (r3 mira a +x); en r1 y
r2 se verían de espaldas. Las convenciones de anclas, giros y máscaras van en la cabecera de manifest.ts.

Uso: python docs/brand/draw_room.py            (escribe todo)
     python docs/brand/draw_room.py --draft X  (solo la vista previa en X, para iterar el arte)
Escribe apps/mobile/assets/room/atlas.png, apps/mobile/src/components/room/manifest.ts,
apps/api/catalog/room.json y docs/brand/room-preview.png. Antes de escribir revisa (y falla si no se
cumple): solo colores de la paleta, cero pixeles huérfanos fuera del tramado, todos los cuadros de
cada tipo, anclas dentro del sprite, 1 px de separación en el atlas, los `adjustments` iguales a
`ITEM_FOR_ADJUSTMENT` de apps/mobile/src/lib/desk.ts, room.json igual a los tipos del manifiesto y
salida idéntica byte a byte en dos corridas.
"""
import base64
import hashlib
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

from draw_icon import checker, sparse  # noqa: E402
from draw_scene import PALETTE as SCENE_PALETTE, SKIES  # noqa: E402

TILE_W, TILE_H, VOX = 32, 16, 8
WALL_H = 48  # px de arte
WALL_ROW = 16  # cada fila de pared
CAP = 2  # canto superior de la pared, encima de los 48 px
SIZE = (5, 5)  # sala nueva

ATLAS_PNG = REPO / "apps" / "mobile" / "assets" / "room" / "atlas.png"
MANIFEST_TS = REPO / "apps" / "mobile" / "src" / "components" / "room" / "manifest.ts"
ROOM_JSON = REPO / "apps" / "api" / "catalog" / "room.json"
PREVIEW_PNG = HERE / "room-preview.png"
DESK_TS = REPO / "apps" / "mobile" / "src" / "lib" / "desk.ts"

# Paleta de la marca (ícono + escena) y lo mínimo que agrega el cuarto, con el mismo cambio de tono:
# un gris tinta para la cara de arriba de lo oscuro, el canto de la pared verde azulado, un roble
# intermedio para las juntas del piso y la rampa naranja del castor (la mascota del equipo).
PALETTE = {
    **SCENE_PALETTE,
    "ink_lit": "#56707a",
    "wall_cap": "#3f6e69",
    "oak_mid": "#a86a43",
    "fur_hi": "#f0a55c",
    "fur": "#d9813f",
    "fur_shadow": "#a95a34",
}


def rgba(key):
    h = PALETTE[key].lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


RGBA = {k: rgba(k) for k in PALETTE}
LUMA = {k: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] for k, c in RGBA.items()}

# material -> (arriba, cara +y / izquierda, cara +x / derecha, contorno)
MAT = {
    "oak": ("oak_hi", "oak", "oak_shadow", "oak_deep"),
    "oak2": ("oak", "oak_shadow", "oak_deep", "oak_deep"),
    "oak3": ("oak_shadow", "oak_deep", "oak_deep", "oak_deep"),
    "sage": ("sage_hi", "sage", "sage_shadow", "wall"),
    "sage2": ("sage", "sage_shadow", "wall_lit", "wall"),
    "pot": ("pot_hi", "pot", "pot_shadow", "oak_deep"),
    "pot2": ("pot", "pot_shadow", "oak_deep", "oak_deep"),
    "rim": ("pot_hi", "pot_hi", "pot", "oak_deep"),
    "soil": ("oak_deep", "oak_deep", "oak_deep", "oak_deep"),
    "leaf": ("leaf_hi", "leaf", "leaf_deep", "wall_deep"),
    "cream": ("cream", "blind", "blind_shadow", "oak_shadow"),
    "cream2": ("blind", "blind_shadow", "apricot", "oak_shadow"),
    "peach": ("peach", "apricot", "oak", "oak_shadow"),
    "ink": ("ink_lit", "ink_hi", "ink", "ink"),
    "tea": ("oak_shadow", "blind", "blind_shadow", "oak_shadow"),
    "book_teal": ("cream", "wave", "leaf_deep", "wall_deep"),
    "book_apricot": ("cream", "apricot", "oak", "oak_shadow"),
    "book_plum": ("cream", "dusk_mid", "dusk_top", "oak_deep"),
    "book_sage": ("cream", "sage", "sage_shadow", "wall"),
    "book_pot": ("cream", "pot", "pot_shadow", "oak_deep"),
    "book_ink": ("cream", "ink_hi", "ink", "ink"),
}


# --- Sprites -----------------------------------------------------------------------------------

class Sprite:
    """RGBA a 1×, el pixel de anclaje y los pixeles sueltos a propósito (tramado, ojos, estrellas)."""

    __slots__ = ("img", "anchor", "exempt", "height")

    def __init__(self, img, anchor, exempt=frozenset(), height=0):
        self.img, self.anchor, self.exempt, self.height = img, anchor, exempt, height

    def key(self):
        """Huella de los pixeles: cuadros iguales comparten lugar en el atlas (cada uno con su ancla)."""
        return hashlib.sha1(f"{self.img.size}|".encode() + self.img.tobytes()).hexdigest()


def outline(pix):
    """Contorno selectivo: cada hueco vecino (4 lados) toma el contorno más oscuro de lo que toca."""
    out = {}
    for (x, y), (_, _, ol) in pix.items():
        if ol is None:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q in pix:
                continue
            cur = out.get(q)
            if cur is None or (LUMA[ol], ol) < (LUMA[cur], cur):
                out[q] = ol
    for q, ol in out.items():
        pix[q] = (ol, False, None)


def to_sprite(pix, anchor=(0, 0)):
    """pix: {(x, y): (clave, suelto, contorno)} en coordenadas locales; `anchor` también local."""
    xs = [x for x, _ in pix] + [anchor[0]]
    ys = [y for _, y in pix] + [anchor[1]]
    x0, y0 = min(xs), min(ys)
    img = Image.new("RGBA", (max(xs) - x0 + 1, max(ys) - y0 + 1), (0, 0, 0, 0))
    px = img.load()
    exempt = set()
    for (x, y), (key, ex, _) in pix.items():
        px[x - x0, y - y0] = RGBA[key]
        if ex:
            exempt.add((x - x0, y - y0))
    return Sprite(img, (anchor[0] - x0, anchor[1] - y0), frozenset(exempt))


def grid(rows, legend, origin=(0, 0), ol=None):
    """Dibujo 2D en texto -> {(x, y): (clave, suelto, contorno)}; `origin` es el pixel (0, 0).
    En la leyenda, una clave entre corchetes ("[cream]") marca un pixel suelto a propósito."""
    out = {}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in ". ":
                continue
            key = legend[ch]
            ex = key.startswith("[")
            out[(i - origin[0], j - origin[1])] = (key.strip("[]"), ex, ol)
    return out


def mirror(cells):
    """Espejo horizontal alrededor de x = 0 (el borde izquierdo del pixel 0)."""
    return {(-1 - x, y): v for (x, y), v in cells.items()}


# --- Vóxeles -----------------------------------------------------------------------------------

# Sello de un vóxel: (columna, fila, cara, sub-columna, sub-fila). La sub-celda 2 × 2 de cada cara
# visible va de izquierda a derecha en pantalla, así las calcomanías no salen en espejo al girar.
STAMP = (
    (1, 0, "T", 0, 0), (2, 0, "T", 1, 0), (1, 1, "T", 0, 1), (2, 1, "T", 1, 1),
    (0, 1, "+y", 0, 0), (0, 2, "+y", 0, 1), (1, 2, "+y", 1, 0), (1, 3, "+y", 1, 1),
    (2, 2, "+x", 0, 0), (2, 3, "+x", 0, 1), (3, 1, "+x", 1, 0), (3, 2, "+x", 1, 1),
)
TONE = {"T": 0, "+y": 1, "+x": 2}
# Un cuarto de vuelta (x, y) -> (d − 1 − y, x), igual que rotateCell en iso.ts: +x -> +y -> −x -> −y.
TURN_FACE = {"+x": "+y", "+y": "-x", "-x": "-y", "-y": "+x", "T": "T"}
# Hacia dónde avanza la sub-columna de cada cara (izquierda a derecha en pantalla cuando se ve).
FACE_U = {"+y": (1, 0), "+x": (0, -1), "-y": (-1, 0), "-x": (0, 1)}


class Model:
    def __init__(self, w, d):
        self.w, self.d = w, d  # vóxeles en x y en y con rot 0
        self.v = {}
        self.dec = {}  # (x, y, z, cara) -> {(sc, sr): (clave, suelto)}

    def box(self, x, y, z, w, d, h, mat):
        for i in range(x, x + w):
            for j in range(y, y + d):
                for k in range(z, z + h):
                    self.v[(i, j, k)] = mat
        return self

    def cut(self, x, y, z, w, d, h):
        for i in range(x, x + w):
            for j in range(y, y + d):
                for k in range(z, z + h):
                    self.v.pop((i, j, k), None)
        return self

    def paint(self, face, at, rows, legend):
        """Calcomanía a 2 px por vóxel. `at` = vóxel de la esquina superior izquierda en pantalla."""
        ux, uy = FACE_U[face]
        x0, y0, ztop = at
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in ". ":
                    continue
                key = legend[ch]
                vox = (x0 + ux * (i // 2), y0 + uy * (i // 2), ztop - j // 2)
                assert vox in self.v, f"calcomanía fuera del modelo: {vox} {face}"
                self.dec.setdefault((*vox, face), {})[(i % 2, j % 2)] = (key.strip("[]"), key.startswith("["))
        return self

    def turned(self, q):
        m = self
        for _ in range(q % 4):
            r = Model(m.d, m.w)
            r.v = {(m.d - 1 - y, x, z): mat for (x, y, z), mat in m.v.items()}
            r.dec = {(m.d - 1 - y, x, z, TURN_FACE[f]): d for (x, y, z, f), d in m.dec.items()}
            m = r
        return m


def turn_point(p, w, d, q):
    """Un punto continuo del modelo con rot 0 -> el mismo punto con `q` cuartos de vuelta."""
    x, y, z = p
    for _ in range(q % 4):
        x, y, w, d = d - y, x, d, w
    return x, y, z


def project(x, y, z):
    return 2 * (x - y), (x + y) - 2 * z


def render_voxels(model):
    pix = {}
    for (x, y, z), mat in sorted(model.v.items(), key=lambda kv: (sum(kv[0]), kv[0][2], kv[0][0])):
        ramp = MAT[mat]
        ox, oy = 2 * (x - y) - 2, (x + y) - 2 * z - 2
        for c, r, face, sc, sr in STAMP:
            key, ex = ramp[TONE[face]], False
            d = model.dec.get((x, y, z, face))
            if d and (sc, sr) in d:
                key, ex = d[(sc, sr)]
            pix[(ox + c, oy + r)] = (key, ex, ramp[3])
    return pix


def vox(model, facing, over=(), post=()):
    """Gira el modelo, lo proyecta, pone los dibujos 2D (`over`, con contorno) y luego `post`
    (vapor, sin contorno). Cada dibujo va en un punto del modelo con rot 0; con r3 sale en espejo."""
    w, d = model.w, model.d
    pix = render_voxels(model.turned(facing))

    def place(layer):
        point, cells = layer
        assert facing in (0, 3), "los dibujos 2D solo tienen frente (r0) y su espejo (r3)"
        sx, sy = project(*turn_point(point, w, d, facing))
        assert sx == int(sx) and sy == int(sy), f"punto fuera de la rejilla: {point}"
        sx, sy = int(sx), int(sy)
        for (x, y), v in (mirror(cells) if facing == 3 else cells).items():
            pix[(sx + x, sy + y)] = v

    for layer in over:
        place(layer)
    outline(pix)
    for layer in post:
        place(layer)
    sprite = to_sprite(pix)
    # Alto físico en px de arte: lo más alto del modelo, o de un dibujo 2D sobre su punto de apoyo.
    tops = [2 * (z + 1) for (_, _, z) in model.v]
    tops += [2 * p[2] - min(y for _, y in cells) for p, cells in over]
    sprite.height = max(tops)
    return sprite


def flat2d(cells, base=(0, 8), facing=0):
    """Sprite 2D (el castor): `cells` relativo al centro de su base, que cae en el centro de la celda."""
    cells = mirror(cells) if facing == 3 else dict(cells)
    pix = {(x + base[0], y + base[1]): v for (x, y), v in cells.items()}
    outline(pix)
    sprite = to_sprite(pix)
    sprite.height = -min(y for _, y in cells)
    return sprite


# --- Planos: piso y pared ----------------------------------------------------------------------

def diamond(cells_w, cells_d):
    """Pixeles del rombo de una huella (top faces), con (u, v) a 4 por vóxel desde la esquina trasera."""
    out = {}
    H = (cells_w + cells_d) * 8
    for py in range(H):
        for px in range(-cells_d * 16 - 1, cells_w * 16 + 1):
            u, v = 2 * py + px + 1, 2 * py - px
            if 0 <= u < 32 * cells_w and 0 <= v < 32 * cells_d:
                out[(px, py)] = (u, v)
    return out


def wall_map(wall, i, k, span=1):
    """Pixel (i, k) de un tramo de pared -> pantalla, relativo a su esquina inferior trasera.
    i va de izquierda a derecha en pantalla (16 por celda) y k es la altura en px (0 = la primera)."""
    W = 16 * span
    c = i if wall == "right" else W - 1 - i  # columna contada desde la esquina trasera
    sx = c if wall == "right" else -1 - c
    return sx, (c + 1) // 2 - 1 - k


def on_wall(cells, wall, span=1, ol=None):
    """Dibujo 2D sobre una pared: `cells` {(i, k): (clave, suelto)} -> sprite con su ancla."""
    pix = {}
    for (i, k), (key, ex) in cells.items():
        pix[wall_map(wall, i, k, span)] = (key, ex, ol)
    if ol:
        outline(pix)
    return to_sprite(pix)


def wall_grid(rows, legend, i0, k0):
    """Texto -> celdas de pared; la última fila del texto queda en la altura k0."""
    out = {}
    n = len(rows)
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch in ". ":
                continue
            key = legend[ch]
            out[(i0 + i, k0 + n - 1 - j)] = (key.strip("[]"), key.startswith("["))
    return out


FLOORS = {
    # base, junta, canto izquierdo (+y), canto derecho (+x)
    "oak": ("oak", "oak_mid", "oak_shadow", "oak_deep"),
    "oak_dark": ("oak_mid", "oak_shadow", "oak_deep", "oak_deep"),
    "tile": ("blind", "blind_shadow", "blind_shadow", "oak_shadow"),
}


def floor_tile(variant):
    base, seam, side_l, side_r = FLOORS[variant]
    pix = {}
    ends = (5, 21, 13, 29)  # dónde termina cada tabla (en u), alternado como en un piso real
    for (px, py), (u, v) in diamond(1, 1).items():
        if variant == "tile":
            key = seam if (u % 16 in (0, 1) or v % 16 in (0, 1)) else base
        else:
            plank = v // 8
            key = seam if v % 8 in (0, 1) or u in (ends[plank], ends[plank] + 1) else base
        pix[(px, py)] = (key, False, None)
    # Canto del piso: 2 px bajo los bordes de adelante. Las baldosas de delante lo tapan, así solo se
    # ve en la orilla del cuarto (el piso se dibuja de atrás hacia adelante).
    bottoms = {}
    for (px, py) in pix:
        bottoms[px] = max(bottoms.get(px, -1), py)
    for px, b in bottoms.items():
        pix[(px, b + 1)] = (side_l if px < 0 else side_r, False, None)
        pix[(px, b + 2)] = ("oak_deep", False, None)
    return to_sprite(pix)


WALLS = {
    # cara de la pared izquierda (en sombra), de la derecha (con luz) y canto de arriba
    "teal": ("wall", "wall_lit", "wall_cap"),
    "sage": ("sage_shadow", "sage", "sage_hi"),
    "cream": ("blind_shadow", "blind", "cream"),
}
# Zoclo de roble: (dos filas de abajo, filo de arriba) por pared.
BASEBOARD = {"left": ("oak_shadow", "oak"), "right": ("oak", "oak_hi")}
# Hueco de la ventana en coordenadas del tramo: columnas y alturas (incluidas).
HOLE_I, HOLE_K = (2, 13), (18, 39)
MULLION_I, TRANSOM_K = (7, 8), 31  # parteluz de 2 px al centro y travesaño de 1 px


def wall_cells(variant, wall):
    face = WALLS[variant][0 if wall == "left" else 1]
    cap = WALLS[variant][2]
    low, lip = BASEBOARD[wall]
    cells = {}
    for i in range(16):
        for k in range(WALL_H + CAP):
            key = cap if k >= WALL_H else low if k < 2 else lip if k == 2 else face
            cells[(i, k)] = (key, False)
    return cells


def window_cells(variant, wall):
    cells = wall_cells(variant, wall)
    (i0, i1), (k0, k1) = HOLE_I, HOLE_K
    for i in range(i0 - 1, i1 + 2):  # marco de roble
        for k in range(k0 - 1, k1 + 2):
            cells[(i, k)] = ("oak", False)
    for i in range(i0 - 2, i1 + 3):  # repisa que sobresale
        cells[(i, k0 - 2)] = ("oak_shadow", False)
        cells[(i, k0 - 1)] = ("oak_hi", False)
    for i in range(i0, i1 + 1):
        for k in range(k0, k1 + 1):
            if i in MULLION_I or k == TRANSOM_K:
                cells[(i, k)] = ("oak_hi" if i == MULLION_I[0] or k == TRANSOM_K else "oak", False)
            else:
                del cells[(i, k)]
    # Derrame (el grosor del muro dentro del hueco): abajo siempre, y del lado que ve la cámara.
    for i in range(i0, i1 + 1):
        if i not in MULLION_I:
            cells[(i, k0)] = ("oak_shadow", False)
    side = i0 if wall == "right" else i1
    for k in range(k0, k1 + 1):
        if k != TRANSOM_K:
            cells[(side, k)] = (WALLS[variant][0], False)
    return cells


def sky_sprite(name, wall):
    top, mid, low, bottom = SKIES[name]
    hole = [(i, k) for i in range(HOLE_I[0], HOLE_I[1] + 1) for k in range(HOLE_K[0], HOLE_K[1] + 1)]
    pts = {wall_map(wall, i, k): (i, k) for i, k in hole}
    rows = sorted({y for _, y in pts})
    first, n = rows[0], len(rows)
    # Bandas horizontales en pantalla (el cielo está lejos); en cada cambio, una fila al 50 % y otra al 25 %.
    cuts = [(round(n * 0.3), top, mid), (round(n * 0.58), mid, low), (round(n * 0.82), low, bottom)]
    pix = {}
    for (x, y) in pts:
        r = y - first
        key, ex = top, False
        for row, upper, lower in cuts:
            if r < row:
                break
            if r == row:
                key, ex = (upper if checker(x, y) else lower), True
                break
            if r == row + 1:
                key, ex = (upper if sparse(x, y) else lower), True
                break
            key, ex = lower, False
        pix[(x, y)] = (key, ex, None)
    if name == "night":
        for i, k in ((4, 36), (10, 27), (12, 37), (5, 26), (11, 22), (3, 21)):
            pix[wall_map(wall, i, k)] = ("cream", True, None)
        for i, k in ((10, 36), (11, 36), (10, 35), (11, 35)):  # luna
            pix[wall_map(wall, i, k)] = ("cream", False, None)
        pix[wall_map(wall, 11, 35)] = ("peach", True, None)
    return to_sprite(pix)


def blinds_sprite(wall):
    cells = {}
    (i0, i1), (k0, k1) = HOLE_I, HOLE_K
    for i in range(i0, i1 + 1):
        for k in range(29, k1 + 1):
            cells[(i, k)] = ("blind_shadow" if (k1 - k) % 3 == 2 else "blind", False)
        cells[(i, 28)] = ("oak", False)  # riel de abajo
    for k in range(24, 28):  # cordón
        cells[(i1 - 2, k)] = ("blind_shadow", False)
    cells[(i1 - 2, 23)] = ("oak_shadow", False)
    cells[(i1 - 2, 22)] = ("oak_shadow", False)
    return on_wall(cells, wall)


# --- Objetos ------------------------------------------------------------------------------------

def desk(variant, facing, frame=None):
    top, legs = {"oak": ("oak", "oak2"), "sage": ("sage", "sage2")}[variant]
    m = Model(16, 8)
    m.box(0, 0, 6, 16, 8, 1, top)  # tablero: superficie en z = 7 vóxeles (14 px)
    for x in (0, 15):
        for y in (0, 7):
            m.box(x, y, 0, 1, 1, 6, legs)
    m.box(1, 0, 2, 14, 1, 4, legs)  # faldón trasero
    m.box(11, 1, 1, 4, 6, 5, top)  # cajonera bajo el lado derecho
    seam, knob = {"oak": ("oak_shadow", "oak_deep"), "sage": ("sage_shadow", "wall")}[variant]
    m.paint("+y", (11, 6, 5), [
        "........",
        "...kk...",
        "........",
        "........",
        "ssssssss",
        "........",
        "...kk...",
        "........",
        "........",
        "........",
    ], {"s": seam, "k": knob})
    return vox(m, facing)


WAVES = {
    # La onda de la pantalla: de ruidosa a tranquila (el ícono). Filas 0–6 dentro de la pantalla.
    "noisy": [3, 1, 5, 2, 6, 1, 4, 3],
    "mid": [3, 2, 4, 2, 4, 3, 3, 3],
    "calm": [3, 3, 2, 1, 2, 3, 3, 3],
}


def screen_rows(wave, dim):
    fill, glow, line = ("dim_screen", "dim_hi", "screen") if dim else ("screen", "screen_hi", "wave")
    rows = [["."] * 12 for _ in range(10)]
    for j in range(1, 9):
        for i in range(1, 11):
            rows[j][i] = "g" if j == 1 else "f"
    ys = WAVES[wave]
    prev = None
    for n, y in enumerate(ys):
        i, j = 2 + n, 2 + y
        rows[j][i] = "l"
        if prev is not None and abs(y - prev) > 1:  # une los saltos con una columna
            step = 1 if y > prev else -1
            for yy in range(prev + step, y, step):
                col = i if abs(yy - y) < abs(yy - prev) else i - 1
                rows[2 + yy][col] = "l"
        prev = y
    return ["".join(r) for r in rows], {"f": fill, "g": glow, "l": line}


def monitor(variant, facing, frame=None):
    wave = {None: "calm", 0: "noisy", 1: "mid", 2: "calm"}[frame[1] if frame else None]
    m = Model(8, 8)
    m.box(2, 1, 0, 4, 2, 1, "ink")  # pie
    m.box(3, 1, 1, 2, 1, 2, "ink")  # cuello
    m.box(1, 2, 2, 6, 1, 5, "ink")  # pantalla: arriba en z = 7 (14 px)
    rows, legend = screen_rows(wave, variant == "dim")
    m.paint("+y", (1, 2, 6), rows, legend)
    return vox(m, facing)


def chair(variant, facing, frame=None):
    seat = {"sage": "sage", "terracotta": "pot"}[variant]
    m = Model(8, 8)
    m.box(1, 3, 0, 6, 2, 1, "ink")  # base en cruz
    m.box(3, 1, 0, 2, 6, 1, "ink")
    m.box(3, 3, 1, 2, 2, 1, "ink")
    m.box(1, 1, 2, 6, 6, 2, seat)  # asiento: arriba en z = 4 (8 px)
    m.box(1, 0, 4, 6, 1, 5, seat)  # respaldo atrás (el frente mira a +y)
    m.box(3, 0, 2, 2, 1, 2, "ink")  # soporte del respaldo
    return vox(m, facing)


SNAKE_BLADES = [
    # Borde izquierdo de cada hoja, fila por fila desde la tierra hacia arriba (y = 0, −1, …).
    # De izquierda a derecha: cada hoja tapa la sombra de la anterior con su borde de luz.
    [-4, -4, -5, -5, -5, -6, -6, -6, -7, -7, -7, -8, -8],
    [-2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4],
    [0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3],
    [2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6],
]


def snake_leaves():
    cells = {}
    for t in range(5):
        for x in range(-4 + (t > 2), 5 - (t > 2)):
            cells[(x, -t)] = ("leaf_deep" if x >= 3 - (t > 2) else "leaf", False, "wall_deep")
    for lefts in SNAKE_BLADES:
        h = len(lefts)
        for t, x0 in enumerate(lefts):
            width = 3 if t < h - 2 else 2 if t == h - 2 else 1
            for k in range(width):
                key = "leaf_hi" if k == 0 else "leaf_deep" if k == width - 1 or t % 4 == 2 else "leaf"
                cells[(x0 + k, -t)] = (key, False, "wall_deep")
    return cells


def plant(variant, facing, frame=None):
    m = Model(8, 8)
    m.box(2, 2, 0, 4, 4, 3, "pot")
    m.box(2, 2, 3, 4, 4, 1, "rim")
    m.box(3, 3, 3, 2, 2, 1, "soil")
    return vox(m, facing, over=[((4, 4, 4), snake_leaves())])


def headphones(variant, facing, frame=None):
    m = Model(8, 8)
    m.box(3, 3, 0, 2, 2, 1, "oak2")  # base del soporte
    stand = grid([
        "....BBBBBB....",
        "..BBbbbbbbBB..",
        ".Bb...hp...bB.",
        ".b....hp....b.",
        "cc....hp....cc",
        "ccq...hp...qcc",
        "ccq...hp...qcc",
        "ccq...hp...qcc",
        ".c....hp....c.",
        "......hp......",
        "......hp......",
        "......hp......",
    ], {"B": "ink_lit", "b": "ink_hi", "c": "ink_hi", "q": "cream", "h": "oak_hi", "p": "oak"},
        origin=(7, 12), ol="ink")
    return vox(m, facing, over=[((4, 4, 1), stand)])


def speaker(variant, facing, frame=None):
    m = Model(8, 8)
    m.box(2, 3, 0, 4, 2, 5, "oak")
    m.paint("+y", (2, 4, 4), [
        "........",
        ".gggggg.",
        ".gggggg.",
        ".ggddgg.",
        ".gdeedg.",
        ".gdeedg.",
        ".ggddgg.",
        ".gggggg.",
        ".gggggg.",
        "........",
    ], {"g": "sage", "d": "sage_shadow", "e": "wall_lit"})
    return vox(m, facing)


def succulent(variant, facing, frame=None):
    m = Model(8, 8)
    m.box(3, 3, 0, 2, 2, 2, "pot")
    m.box(3, 3, 2, 2, 2, 1, "soil")
    rosette = grid([
        "..h..h..",
        ".hshhsh.",
        "hssbbssh",
        ".sbbbbs.",
        "..dddd..",
    ], {"h": "sage_hi", "s": "sage", "b": "leaf_hi", "d": "sage_shadow"}, origin=(4, 4), ol="wall")
    return vox(m, facing, over=[((4, 4, 3), rosette)])


def phone(variant, facing, frame=None):
    m = Model(8, 8)
    m.box(2, 3, 0, 4, 2, 1, "oak")  # base
    m.box(3, 4, 1, 3, 1, 4, "ink")  # teléfono de pie
    m.paint("+y", (3, 4, 4), [
        "......",
        ".dddd.",
        ".dccd.",
        ".dcpd.",
        ".dddd.",
        ".dddd.",
        ".dddd.",
        "......",
    ], {"d": "dim_screen", "c": "cream", "p": "[peach]"})
    return vox(m, facing)


def sign(variant, facing, frame=None):
    """Tarjeta de "en concentración": un punto verde azulado, dos renglones y la onda tranquila."""
    m = Model(8, 8)
    m.box(1, 3, 0, 6, 2, 1, "oak")
    m.box(1, 4, 1, 6, 1, 4, "cream")
    m.paint("+y", (1, 4, 4), [
        "............",
        ".dd.lllll...",
        ".dd.........",
        "....llll....",
        "............",
        ".wwww.wwww..",
        "............",
        "............",
    ], {"d": "wave", "l": "ink_lit", "w": "sage"})
    return vox(m, facing)


def lamp(variant, facing, frame=None):
    m = Model(8, 8)
    m.box(3, 3, 0, 2, 2, 1, "ink")
    arm = grid([
        "..........sss...",
        ".........sppps..",
        "........spppppo.",
        ".......spppppppo",
        "......a.ooyyyoo.",
        ".....a..........",
        "....a...........",
        "...a............",
        "..a.............",
        "...a............",
        "....a...........",
        ".....a..........",
        "......a.........",
        "......aa........",
    ], {"a": "ink_hi", "s": "pot_hi", "p": "pot", "o": "pot_shadow", "y": "cream"},
        origin=(7, 14), ol="oak_deep")
    return vox(m, facing, over=[((4, 4, 1), arm)])


def tray(variant, facing, frame=None):
    m = Model(8, 8)
    m.box(1, 2, 0, 6, 4, 1, "oak")
    m.box(1, 2, 1, 6, 1, 1, "oak")
    m.box(1, 2, 1, 1, 4, 1, "oak")
    m.box(6, 2, 1, 1, 4, 1, "oak")
    m.box(1, 5, 1, 6, 1, 1, "oak")
    m.box(2, 3, 1, 4, 2, 1, "cream")
    m.box(2, 3, 2, 3, 2, 1, "cream")
    return vox(m, facing)


def divider(variant, facing, frame=None):
    fabric = {"sage": "sage", "cream": "cream"}[variant]
    seam = {"sage": "sage_shadow", "cream": "blind_shadow"}[variant]
    m = Model(8, 8)
    m.box(0, 3, 1, 8, 1, 14, fabric)  # panel: arriba en z = 15 (30 px)
    for x in (1, 6):
        m.box(x, 2, 0, 1, 3, 1, "oak2")  # patas
    seams = ["....s......s...." for _ in range(26)]
    m.paint("+y", (0, 3, 14), seams, {"s": seam})
    m.paint("-y", (7, 3, 14), seams, {"s": seam})
    return vox(m, facing)


def fan(variant, facing, frame=None):
    m = Model(8, 8)
    m.box(3, 3, 0, 2, 2, 1, "cream")
    spin = frame[1] if frame else 0
    head = grid([
        "....rrrr....",
        "..rrbbbbrr..",
        ".rbbb%%bbbr.",
        ".rbbb%%bbbr.",
        "rbbbb%%bbbbr",
        "rb%%%hh%%%br",
        "rb%%%hh%%%br",
        "rbbbb%%bbbbr",
        ".rbbb%%bbbr.",
        ".rbbb%%bbbr.",
        "..rrbbbbrr..",
        "....rrrr....",
        ".....nn.....",
        ".....nn.....",
        "....nnnn....",
    ] if spin == 0 else [
        "....rrrr....",
        "..rrbbbbrr..",
        ".r%%bbbb%%r.",
        ".r%%%bb%%%r.",
        "rbb%%bb%%bbr",
        "rbbbbhhbbbbr",
        "rbbbbhhbbbbr",
        "rbb%%bb%%bbr",
        ".r%%%bb%%%r.",
        ".r%%bbbb%%r.",
        "..rrbbbbrr..",
        "....rrrr....",
        ".....nn.....",
        ".....nn.....",
        "....nnnn....",
    ], {"r": "sage_shadow", "b": "mist", "%": "sage_hi", "h": "sage", "n": "sage_shadow"},
        origin=(6, 15), ol="wall")
    return vox(m, facing, over=[((4, 4, 1), head)])


def sweater_cells(i0, k0):
    return wall_grid([
        "......kk......",
        "......k.......",
        "....hhaahh....",
        "..hhpppppphh..",
        ".ppppppppppppp.",
        "ppppppppppppss",
        "ppp.pppppp.sss",
        "pp..pppppp..ss",
        "pp..pppppp..ss",
        "aa..pppppp..aa",
        "....pppppp....",
        "....pppppp....",
        "....aaaaaa....",
    ], {"k": "ink_hi", "h": "pot_hi", "p": "pot", "s": "pot_shadow", "a": "apricot"}, i0, k0)


def sweater(variant, facing, frame=None):
    return on_wall(sweater_cells(1, 2), "right" if facing == 0 else "left", ol="oak_deep")


def mug(variant, facing, frame=None):
    m = Model(8, 8)
    m.box(3, 3, 0, 2, 2, 2, "cream")
    m.box(3, 3, 1, 2, 2, 1, "tea")
    handle = grid([
        "cc.",
        "..c",
        "..c",
        "cc.",
    ], {"c": "blind"}, origin=(0, 0), ol="oak_shadow")
    steam = []
    if frame:
        wisps = [(0, 0), (1, -1), (0, -2), (1, -3)] if frame[1] == 0 else [(1, 0), (0, -1), (1, -2), (0, -3)]
        cells = {(x, y): ("mist" if n < 2 else "day_low", False, None) for n, (x, y) in enumerate(wisps)}
        steam = [((4, 4, 3), {(x - 1, y - 2): v for (x, y), v in cells.items()})]
    return vox(m, facing, over=[((5, 4, 2), {(x, y - 1): v for (x, y), v in handle.items()})], post=steam)


def frame_cells(i0, k0):
    return wall_grid([
        "oooooooooooo",
        "oskkkkkkkkko",
        "oskkkkrkkkko",
        "oskkkrrrkkko",
        "oskkrrrrrkko",
        "oskrrrrrrrko",
        "oskkcccccsko",
        "oskkcwcdcsko",  # w: ventana de la casa, un pixel a propósito
        "oskkcccdcsko",
        "osgggggggggo",
        "osllllllllgo",
        "oooooooooooo",
    ], {"o": "oak", "s": "oak_shadow", "k": "day_top", "r": "pot", "c": "cream", "w": "[screen]",
        "d": "oak_shadow", "g": "leaf", "l": "leaf_hi"}, i0, k0)


def frame(variant, facing, frame=None):
    return on_wall(frame_cells(2, 2), "right" if facing == 0 else "left", ol="oak_deep")


POSTERS = {
    "hills": ([
        "cccccccccccc",
        "cccccccccccc",
        "ccccccccppcc",
        "cccccccpppcc",
        "ccccccccppcc",
        "cccccccccccc",
        "cccccccccccc",
        "cccccccccccc",
        "ccccsscccccc",
        "cccsssscccss",
        "ccssssssssss",
        "csssssssssss",
        "sssssssggggg",
        "sssssggggggg",
        "ssgggggggggg",
        "gggggggggggg",
        "gggggggggggg",
        "gggggggggggg",
        "gggggggggggg",
        "cccccccccccc",
    ], {"c": "cream", "p": "apricot", "s": "sage_hi", "g": "sage"}),
    "wave": ([
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
        "mmmmmmmmssmm",
        "mmmmmmmmssmm",
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
        "mmmmllmmmmmm",
        "mmllwwllmmmm",
        "llwwmmwwllll",
        "wwmmmmmmwwww",
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
        "mmmmmmmmmmmm",
    ], {"m": "mist", "s": "apricot", "l": "wave", "w": "leaf_deep"}),
}


def poster(variant, facing, frame=None):
    rows, legend = POSTERS[variant]
    return on_wall(wall_grid(rows, legend, 2, 7), "right" if facing == 0 else "left", ol="oak_shadow")


RUGS = {
    # campo, borde, línea, canto
    "terracotta": ("dusk_low", "pot", "peach", "pot_shadow"),
    "sage": ("sage_hi", "sage", "cream", "sage_shadow"),
    "cream": ("cream", "apricot", "sage_hi", "blind_shadow"),
}


def rug(variant, facing, frame=None):
    field, border, line, edge = RUGS[variant]
    pix = {}
    lo, hi = 4, 60  # un vóxel de margen dentro de la huella de 2 × 2
    for (px, py), (u, v) in diamond(2, 2).items():
        if not (lo <= u < hi and lo <= v < hi):
            continue
        d = min(u - lo, hi - 1 - u, v - lo, hi - 1 - v)
        cu, cv = abs(u - 31.5), abs(v - 31.5)
        if d < 4:
            key = border
        elif d in (6, 7):
            key = line
        elif cu + cv <= 10 and not (cu + cv <= 6):
            key = border
        elif cu + cv <= 3:
            key = line
        else:
            key = field
        pix[(px, py)] = (key, False, edge)
    bottoms = {}
    for (px, py) in pix:
        bottoms[px] = max(bottoms.get(px, -1), py)
    for px, b in bottoms.items():
        pix[(px, b + 1)] = (edge, False, edge)
    outline(pix)
    return to_sprite(pix)


BOOKS = ["book_teal", "book_apricot", "book_plum", "book_sage", "book_pot", "book_ink"]


def bookshelf(variant, facing, frame=None):
    wood, back = {"oak": ("oak", "oak3"), "sage": ("sage", "sage2")}[variant]
    m = Model(8, 5)
    m.box(0, 0, 0, 8, 1, 14, back)  # fondo
    m.box(0, 1, 0, 1, 4, 14, wood)
    m.box(7, 1, 0, 1, 4, 14, wood)
    for z in (0, 4, 8):
        m.box(1, 1, z, 6, 4, 1, wood)
    m.box(0, 0, 13, 8, 5, 1, wood)  # tapa: superficie en z = 14 (28 px)
    shelves = [
        # (x, alto, libro) por repisa; huecos a propósito
        [(1, 3, 0), (2, 2, 1), (3, 3, 2), (5, 2, 3), (6, 3, 4)],
        [(1, 2, 5), (2, 3, 3), (3, 3, 0), (4, 2, 4)],
        [(2, 3, 2), (3, 2, 1), (4, 3, 5), (5, 3, 3), (6, 2, 0)],
    ]
    for z0, row in zip((1, 5, 9), shelves):
        for x, h, b in row:
            m.box(x, 1, z0, 1, 3, h, BOOKS[b])
    return vox(m, facing)


def side_table(variant, facing, frame=None):
    top, leg = {"oak": ("oak", "oak2"), "cream": ("cream", "oak2")}[variant]
    m = Model(8, 8)
    m.box(1, 1, 5, 6, 6, 1, top)  # superficie en z = 6 (12 px)
    for x, y in ((1, 1), (6, 1), (1, 6), (6, 6)):
        m.cut(x, y, 5, 1, 1, 1)
    m.box(3, 3, 0, 2, 2, 5, leg)
    m.box(2, 2, 0, 4, 4, 1, leg)
    return vox(m, facing)


def armchair(variant, facing, frame=None):
    fabric, deep = {"sage": ("sage", "sage2"), "terracotta": ("pot", "pot2")}[variant]
    m = Model(8, 8)
    for x, y in ((0, 0), (7, 0), (0, 7), (7, 7)):
        m.box(x, y, 0, 1, 1, 1, "oak2")
    m.box(0, 0, 1, 8, 8, 2, deep)  # base
    m.box(1, 2, 3, 6, 6, 1, fabric)  # cojín: arriba en z = 4 (8 px)
    m.box(0, 1, 3, 1, 7, 3, fabric)  # brazos
    m.box(7, 1, 3, 1, 7, 3, fabric)
    m.box(0, 0, 3, 8, 2, 6, fabric)  # respaldo: arriba en z = 9 (18 px)
    return vox(m, facing)


def floor_lamp(variant, facing, frame=None):
    shade = {"cream": "cream", "terracotta": "pot"}[variant]
    m = Model(8, 8)
    m.box(2, 2, 0, 4, 4, 1, "ink")
    m.box(2, 2, 15, 4, 4, 3, shade)  # pantalla: arriba en z = 18 (36 px)
    for x, y in ((2, 2), (5, 2), (2, 5), (5, 5)):  # esquinas redondeadas
        m.cut(x, y, 0, 1, 1, 1)
        m.cut(x, y, 15, 1, 1, 3)
    # Poste 2D de 2 px, del pie (z = 1) a la pantalla (z = 15), sin tapar la cara de la pantalla.
    pole = {(x, y): ("ink_hi" if x < 0 else "ink", False, "ink") for x in (-1, 0) for y in range(-26, -2)}
    return vox(m, facing, over=[((4, 4, 0), pole)])


def fern(variant, facing, frame=None):
    m = Model(8, 8)
    m.box(2, 2, 0, 4, 4, 3, "cream")
    m.box(2, 2, 3, 4, 4, 1, "cream2")
    m.box(3, 3, 3, 2, 2, 1, "soil")
    fronds = grid([
        "..........hh..........",
        ".......h.hllh.h.......",
        ".....h.hhlllhhlh.h....",
        "...h.hhllllllllhhlh...",
        "..hhhllllllllllllhh...",
        ".hhllllllddllllllllh..",
        ".hlllddlllllllddlllh..",
        "hlllllllldddllllllllh.",
        "hlddlllddlllddllllllh.",
        "lld.llddl...lldd.lldl.",
        "ld...dd.......dd...dd.",
    ], {"h": "leaf_hi", "l": "leaf", "d": "leaf_deep"}, origin=(11, 6), ol="wall_deep")
    return vox(m, facing, over=[((4, 4, 4), fronds)])


BEAVER = [
    # La mascota sentada y tranquila (de frente, un poco hacia la izquierda; la cola atrás).
    # o contorno, h/f/s pelaje, b/a panza, n nariz, w dientes, t/T cola.
    "......ooo......ooo..........",
    ".....offso....offso.........",
    ".....ofsfooooooffso.........",
    "......ohhhhhhhhhfffo........",
    ".....ohhhhhhhhhhffffo.......",
    "....ohhhhhhhhhhhfffffo......",
    "....ohhhhohhhhohfffffo......",
    "....ohhhhohhhhohfffffo......",
    "....ohhhhhbnnbhhffffso......",
    "....ohhhhbbwwbbhffffso......",
    ".....ohhhhbwwbhhfffso.......",
    ".....ohhhhhbbhhhfffso.......",
    ".....ohhhhhhhhhhffffso......",
    "....ohhhhhbbbbbhfffffso.ooo.",
    "....ohhhbbbbbbbbbffffsootTTo",
    "....ohhsbbbbbbbbbsfffsottTTo",
    "....ohhhsbbbbbbbsffffsottTTo",
    "....ohhhhbbbbbbbaffffsotttTo",
    "....ohhhhabbbbbaafffssottTTo",
    ".....ohhhhaaaaaaaffssottTTo.",
    ".....ohhhfffffffffssoottTo..",
    "......ohhffoo..offfsoooooo..",
    ".......oooo.....oooo........",
]
# Saludo: la pata izquierda (en pantalla) sube junto a la cara; dos cuadros que se alternan.
BEAVER_WAVE = [
    # (primera fila, parche); "." deja lo que hay. La marca del brazo en la panza desaparece.
    (7, [
        ".ooo..",
        "ohhho.",
        "ohhho.",
        "ohhfo.",
        ".ohfo.",
        "..ohfh",
        "...ohh",
    ]),
    (6, [
        ".ooo..",
        "ohhho.",
        "ohhho.",
        "ohhfo.",
        ".ohfo.",
        "..ohfo",
        "..ohfh",
        "...ohh",
    ]),
]
BEAVER_LEGEND = {"o": "oak_deep", "h": "fur_hi", "f": "fur", "s": "fur_shadow", "b": "peach", "a": "apricot",
                 "n": "oak_deep", "w": "cream", "t": "pot_shadow", "T": "pot"}


def beaver(variant, facing, frame=None):
    rows = [list(r) for r in BEAVER]
    if frame:
        top, patch = BEAVER_WAVE[frame[1]]
        for j, row in enumerate(patch):
            for i, ch in enumerate(row):
                if ch != ".":
                    rows[top + j][i] = ch
        rows[15][7] = rows[16][8] = "h"
    cells = grid(["".join(r) for r in rows], BEAVER_LEGEND, origin=(13, len(rows)))
    return flat2d(cells, facing=facing)


# --- Catálogo ----------------------------------------------------------------------------------

# Lo mismo que ITEM_FOR_ADJUSTMENT en apps/mobile/src/lib/desk.ts (el script lo comprueba).
ADJUSTMENTS = {
    "headphones": ["noise_cancelling", "earplugs", "ask_noise_source"],
    "speaker": ["soft_masking"],
    "succulent": ["move_from_voices", "book_quiet_room", "move_from_smell", "ask_quiet_desk"],
    "phone": ["silence_notifications", "batch_messages"],
    "sign": ["focus_signal", "ask_focus_hours"],
    "blinds": ["close_blinds", "rotate_screen", "turn_from_light"],
    "screenDim": ["screen_brightness", "bigger_text", "one_window", "ask_antiglare"],
    "lamp": ["desk_lamp", "ask_lighting"],
    "tray": ["clear_desk"],
    "divider": ["face_away", "ask_divider"],
    "fan": ["cooler_spot", "ask_temperature"],
    "sweater": ["warm_layer"],
    "mug": ["short_reset"],
    "frame": ["ask_remote_focus"],
}

FRONT = [0, 3]  # frente visible: r0 mira a +y (abajo a la izquierda) y r3 a +x (abajo a la derecha)
WALL_SIDES = [0, 1]  # objetos de pared: r0 en la pared derecha, r1 en la izquierda (depth.ts)


def T(label_es, label_en, draw, **spec):
    return {**spec, "label": {"es": label_es, "en": label_en}, "draw": draw}


# Las etiquetas de lo ganado repiten las de `desk.items` en src/i18n (es y en).
TYPES = {
    # Base: en todo cuarto nuevo.
    "desk": T("Escritorio", "Desk", desk, place=["floor"], footprint=[2, 1], facings=FRONT,
              surface={"z": 14, "slots": [[0, 0], [1, 0]]}, base=True, variants=["oak", "sage"]),
    "monitor": T("Pantalla", "Screen", monitor, place=["surface"], footprint=[1, 1], facings=FRONT,
                 base=True, variants=["normal", "dim"], anim={"wave": 3}),
    "chair": T("Silla", "Chair", chair, place=["floor"], footprint=[1, 1], facings=[0, 1, 2, 3],
               base=True, variants=["sage", "terracotta"]),
    "plant": T("Planta", "Plant", plant, place=["floor", "surface"], footprint=[1, 1], facings=[0],
               base=True, variants=["default"]),
    # Lo que deja cada prueba terminada.
    "headphones": T("Audífonos", "Headphones", headphones, place=["surface"], footprint=[1, 1],
                    facings=FRONT, variants=["default"]),
    "lamp": T("Lámpara cálida", "Warm lamp", lamp, place=["surface", "floor"], footprint=[1, 1],
              facings=FRONT, variants=["warm"]),
    "tray": T("Bandeja ordenada", "Tidy tray", tray, place=["surface"], footprint=[1, 1],
              facings=FRONT, variants=["default"]),
    "divider": T("Panel divisor", "Divider panel", divider, place=["floor"], footprint=[1, 1],
                 facings=[0, 1], variants=["sage", "cream"]),
    "frame": T("Foto de casa", "Photo of home", frame, place=["wall"], footprint=[1, 1],
               facings=WALL_SIDES, variants=["home"]),
    "sweater": T("Suéter", "Sweater", sweater, place=["wall"], footprint=[1, 1], facings=WALL_SIDES,
                 variants=["default"]),
    "speaker": T("Bocina de sonido suave", "Soft-sound speaker", speaker, place=["surface"],
                 footprint=[1, 1], facings=FRONT, variants=["default"]),
    "fan": T("Ventilador", "Fan", fan, place=["surface", "floor"], footprint=[1, 1], facings=FRONT,
             variants=["default"], anim={"spin": 2}),
    "succulent": T("Planta del rincón tranquilo", "Quiet-corner plant", succulent, place=["surface"],
                   footprint=[1, 1], facings=[0], variants=["default"]),
    "mug": T("Taza para una pausa", "Mug for a break", mug, place=["surface"], footprint=[1, 1],
             facings=FRONT, variants=["default"], anim={"steam": 2}),
    "sign": T("Señal de concentración", "Focus sign", sign, place=["surface"], footprint=[1, 1],
              facings=FRONT, variants=["default"]),
    "phone": T("Teléfono en silencio", "Phone on silent", phone, place=["surface"], footprint=[1, 1],
               facings=FRONT, variants=["default"]),
    "blinds": T("Persiana", "Blinds", None, place=[], footprint=[1, 1], facings=[0], modifies="window",
                variants=["default"]),
    "screenDim": T("Pantalla suave", "Soft screen", None, place=[], footprint=[1, 1], facings=[0],
                   modifies="monitor", variants=["default"]),
    # Decoración libre desde el primer día.
    "rug": T("Tapete", "Rug", rug, place=["floor"], footprint=[2, 2], facings=[0], flat=True, decor=True,
             variants=["terracotta", "sage", "cream"]),
    "bookshelf": T("Librero", "Bookshelf", bookshelf, place=["floor"], footprint=[1, 1], facings=FRONT,
                   surface={"z": 28, "slots": [[0, 0]]}, decor=True, variants=["oak", "sage"]),
    "sideTable": T("Mesita", "Side table", side_table, place=["floor"], footprint=[1, 1], facings=[0],
                   surface={"z": 12, "slots": [[0, 0]]}, decor=True, variants=["oak", "cream"]),
    "armchair": T("Sillón", "Armchair", armchair, place=["floor"], footprint=[1, 1], facings=[0, 1, 2, 3],
                  decor=True, variants=["sage", "terracotta"]),
    "floorLamp": T("Lámpara de pie", "Floor lamp", floor_lamp, place=["floor"], footprint=[1, 1],
                   facings=[0], decor=True, variants=["cream", "terracotta"]),
    "fern": T("Helecho", "Fern", fern, place=["floor", "surface"], footprint=[1, 1], facings=[0],
              decor=True, variants=["default"]),
    "poster": T("Póster", "Poster", poster, place=["wall"], footprint=[1, 2], facings=WALL_SIDES,
                decor=True, variants=["hills", "wave"]),
    "beaver": T("Castor", "Beaver", beaver, place=["floor"], footprint=[1, 1], facings=FRONT,
                decor=True, variants=["default"], anim={"wave": 2}),
}
for _name, _ids in ADJUSTMENTS.items():
    TYPES[_name]["adjustments"] = _ids


# --- Construcción ------------------------------------------------------------------------------

def build_frames():
    frames = {}
    for v in FLOORS:
        frames[f"floor.{v}"] = floor_tile(v)
    for v in WALLS:
        for wall in ("left", "right"):
            frames[f"wall.{v}.{wall}"] = on_wall(wall_cells(v, wall), wall)
            frames[f"window.{v}.{wall}"] = on_wall(window_cells(v, wall), wall)
    for s in SKIES:
        for wall in ("left", "right"):
            frames[f"sky.{s}.{wall}"] = sky_sprite(s, wall)
    for wall in ("left", "right"):
        frames[f"blinds.{wall}"] = blinds_sprite(wall)
    heights = {}
    for name, spec in TYPES.items():
        if spec["draw"] is None:
            heights[name] = 0
            continue
        top = 0
        for variant in spec["variants"]:
            for facing in spec["facings"]:
                base = f"{name}.{variant}.r{facing}"
                frames[base] = spec["draw"](variant, facing)
                top = max(top, frames[base].height)
                for anim, count in (spec.get("anim") or {}).items():
                    for n in range(count):
                        frames[f"{base}:{anim}{n}"] = spec["draw"](variant, facing, (anim, n))
        if "wall" in spec["place"]:
            top = spec["footprint"][1] * WALL_ROW
        elif spec.get("flat"):
            top = 2
        heights[name] = top
    return frames, heights


SPEC_KEYS = ["place", "footprint", "facings", "height", "surface", "flat", "base", "decor", "adjustments",
             "modifies", "variants", "anim", "label"]


def public_spec(spec, height):
    out = {}
    for k in SPEC_KEYS:
        if k == "height":
            out[k] = height
        elif k in spec and spec[k] is not None and spec[k] is not False:
            out[k] = spec[k]
    return out


def mask_of(img):
    w, h = img.size
    alpha = img.getchannel("A").tobytes()
    bits = bytearray((w * h + 7) // 8)
    for i, a in enumerate(alpha):
        if a:
            bits[i >> 3] |= 0x80 >> (i & 7)
    return base64.b64encode(bytes(bits)).decode("ascii")


def pack(unique):
    """Estantes de alto parecido, del más alto al más bajo, con 1 px entre cuadros. Prueba varios
    anchos y se queda con el de menor área (empate: el más cuadrado)."""
    order = sorted(unique, key=lambda k: (-unique[k].img.height, -unique[k].img.width, k))
    best = None
    for max_w in (256, 320, 384, 448, 512):
        x = y = row_h = 0
        rects = {}
        for k in order:
            im = unique[k].img
            if x and x + im.width > max_w:
                x, y, row_h = 0, y + row_h + 1, 0
            rects[k] = (x, y, im.width, im.height)
            x += im.width + 1
            row_h = max(row_h, im.height)
        width = max(r[0] + r[2] for r in rects.values())
        height = y + row_h
        score = (width * height, abs(width - height))
        if best is None or score < best[0]:
            best = (score, width, height, rects)
    _, width, height, rects = best
    atlas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for k, (x, y, _, _) in rects.items():
        atlas.paste(unique[k].img, (x, y))
    return atlas, rects


def build():
    frames, heights = build_frames()
    unique, alias = {}, {}
    for name, sp in frames.items():
        h = sp.key()
        if h not in unique:
            unique[h] = sp
        alias[name] = h
    atlas, rects = pack(unique)
    types = {name: public_spec(spec, heights[name]) for name, spec in TYPES.items()}
    shell = {"floors": list(FLOORS), "walls": list(WALLS)}
    manifest_frames = {}
    for name in sorted(frames):
        sp = frames[name]
        manifest_frames[name] = {
            "rect": list(rects[alias[name]]),
            "anchor": list(sp.anchor),
            "mask": mask_of(sp.img),
        }
    manifest = {
        "tile": [TILE_W, TILE_H],
        "voxelsPerTile": VOX,
        "wallHeight": WALL_H,
        "atlasSize": list(atlas.size),
        "shell": shell,
        "types": types,
        "frames": manifest_frames,
    }
    catalog = {"version": 1, "size": {"w": SIZE[0], "d": SIZE[1]}, "shell": shell, "types": types}
    buf = io.BytesIO()
    atlas.save(buf, format="PNG", optimize=True)
    return {
        "frames": frames,
        "unique": unique,
        "alias": alias,
        "atlas": atlas,
        "atlas_png": buf.getvalue(),
        "manifest": manifest,
        "manifest_ts": manifest_ts(manifest),
        "room_json": json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
    }


# --- Salida TS ---------------------------------------------------------------------------------

IDENT = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")


def ts_value(v, indent=0):
    pad = "  " * indent
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str):
        return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"
    if isinstance(v, list):
        return "[" + ", ".join(ts_value(x, indent) for x in v) + "]"
    if isinstance(v, dict):
        if not v:
            return "{}"
        inner = []
        for k, x in v.items():
            key = k if IDENT.match(k) else ts_value(k)
            inner.append(f"{pad}  {key}: {ts_value(x, indent + 1)},")
        return "{\n" + "\n".join(inner) + f"\n{pad}}}"
    raise TypeError(v)


def ts_inline(v):
    """Objetos cortos en una línea (tipos y cuadros), para que el archivo se pueda leer."""
    if isinstance(v, dict):
        parts = []
        for k, x in v.items():
            key = k if IDENT.match(k) else ts_value(k)
            parts.append(f"{key}: {ts_inline(x)}")
        return "{ " + ", ".join(parts) + " }"
    if isinstance(v, list):
        return "[" + ", ".join(ts_inline(x) for x in v) + "]"
    return ts_value(v)


HEADER = """// Generado por docs/brand/draw_room.py. No se edita a mano: se cambia el script y se vuelve a correr.
/**
 * Atlas del cuarto isométrico (1×, `assets/room/atlas.png`) y lo que hace falta para dibujarlo.
 *
 * - Ancla: el pixel del cuadro que cae en el punto de apoyo; el cuadro va en `punto − anchor`.
 *   Piso: esquina trasera de la huella a z = 0 (`cellToArt(x, y)`). Superficie: esquina trasera de
 *   la celda del slot a `surface.z` del anfitrión. Pared, ventana, cielo y persiana: esquina inferior
 *   trasera del tramo (la de `u` menor) a z = 16 · row (`wallToArt`). Baldosa: su esquina trasera.
 * - Giros: un cuarto de vuelta es `(x, y) → (d − 1 − y, x)` (como `rotateCell`), así que el frente
 *   de un objeto pasa de +y (r0, mira abajo a la izquierda) a −x (r1), −y (r2) y +x (r3). Por eso los
 *   objetos con frente declaran `facings: [0, 3]`: en r1 y r2 se verían de espaldas. Sillas y
 *   sillones traen los cuatro. Lo simétrico (plantas, alfombras) trae solo r0.
 * - Objetos de pared: r0 en la pared derecha (y = 0) y r1 en la izquierda (x = 0), como
 *   `WALL_FACING` en depth.ts. Tramos de pared, ventana, cielo y persiana llevan `.left` / `.right`.
 * - Animaciones de reposo: `tipo.variante.rN:animK` con K desde 0; el cuadro sin sufijo es el reposo
 *   (pantalla: `wave0` ruidosa, `wave1` media, `wave2` tranquila = reposo).
 * - El piso se dibuja de atrás hacia adelante: cada baldosa trae 2 px de canto que tapan las de delante.
 * - Máscara: 1 bit por pixel, por filas, sin relleno por fila (bit i = y · ancho + x, el primero en
 *   el bit más alto de cada byte), en base64 estándar. Cuadros iguales comparten `rect`.
 */"""


def manifest_ts(m):
    lines = [HEADER, "import type { Manifest } from './types';", "",
             "export const ATLAS = require('@/assets/room/atlas.png');", "",
             "export const MANIFEST: Manifest = {",
             f"  tile: {ts_inline(m['tile'])},",
             f"  voxelsPerTile: {m['voxelsPerTile']},",
             f"  wallHeight: {m['wallHeight']},",
             f"  atlasSize: {ts_inline(m['atlasSize'])},",
             f"  shell: {ts_inline(m['shell'])},",
             "  types: {"]
    for name, spec in m["types"].items():
        lines.append(f"    {name}: {ts_inline(spec)},")
    lines += ["  },", "  frames: {"]
    for name, fr in m["frames"].items():
        lines.append(f"    {ts_value(name)}: {ts_inline(fr)},")
    lines += ["  },", "};", "", "export default MANIFEST;", ""]
    return "\n".join(lines)


# --- Revisiones --------------------------------------------------------------------------------

def orphans(img, exempt):
    """Pixeles sin vecino (8 lados) del mismo color, sin contar el tramado y los sueltos a propósito."""
    w, h = img.size
    px = img.load()
    out = []
    for y in range(h):
        for x in range(w):
            c = px[x, y]
            if c[3] == 0 or (x, y) in exempt:
                continue
            if not any(0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy] == c
                       for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy):
                out.append((x, y))
    return out


def parse_desk_ts():
    text = DESK_TS.read_text(encoding="utf-8")
    block = re.search(r"ITEM_FOR_ADJUSTMENT[^{]*\{(.*?)\};", text, re.S).group(1)
    out = {}
    for adj, item in re.findall(r"(\w+):\s*'(\w+)'", block):
        out.setdefault(item, []).append(adj)
    return out


def check(out):
    problems = []
    colors = {rgba(k) for k in PALETTE}  # desde los hex, no desde la tabla con la que se pinta
    frames, alias, unique = out["frames"], out["alias"], out["unique"]
    for h, sp in unique.items():
        name = min(n for n, a in alias.items() if a == h)
        img = sp.img
        data = img.tobytes()
        pixels = {tuple(data[i:i + 4]) for i in range(0, len(data), 4)}
        bad = {c for c in pixels if c[3] and c not in colors}
        if bad or any(0 < c[3] < 255 for c in pixels):
            problems.append(f"{name}: colores fuera de la paleta {sorted(bad)[:3]}")
        orph = orphans(img, sp.exempt)
        if orph:
            problems.append(f"{name}: pixeles huérfanos en {orph[:6]}")
    for name, sp in frames.items():
        ax, ay = sp.anchor
        if not (0 <= ax < sp.img.width and 0 <= ay < sp.img.height):
            problems.append(f"{name}: ancla {sp.anchor} fuera de {sp.img.size}")
    m = out["manifest"]
    for name, spec in m["types"].items():
        if spec.get("modifies"):
            continue
        for variant in spec["variants"]:
            for facing in spec["facings"]:
                base = f"{name}.{variant}.r{facing}"
                need = [base] + [f"{base}:{a}{n}" for a, c in (spec.get("anim") or {}).items() for n in range(c)]
                problems += [f"falta el cuadro {n}" for n in need if n not in frames]
    for kind, variants in (("floor", m["shell"]["floors"]),):
        problems += [f"falta floor.{v}" for v in variants if f"floor.{v}" not in frames]
    for v in m["shell"]["walls"]:
        for wall in ("left", "right"):
            for k in ("wall", "window"):
                if f"{k}.{v}.{wall}" not in frames:
                    problems.append(f"falta {k}.{v}.{wall}")
    for s in SKIES:
        for wall in ("left", "right"):
            if f"sky.{s}.{wall}" not in frames:
                problems.append(f"falta sky.{s}.{wall}")
    for wall in ("left", "right"):
        if f"blinds.{wall}" not in frames:
            problems.append(f"falta blinds.{wall}")
    if "dim" not in m["types"]["monitor"]["variants"]:
        problems.append("screenDim necesita la variante dim del monitor")
    # Atlas: sin traslapes y con 1 px de separación entre cuadros.
    rects = sorted({tuple(f["rect"]) for f in m["frames"].values()})
    for i, a in enumerate(rects):
        for b in rects[i + 1:]:
            if a[0] < b[0] + b[2] + 1 and b[0] < a[0] + a[2] + 1 and a[1] < b[1] + b[3] + 1 and b[1] < a[1] + a[3] + 1:
                problems.append(f"cuadros sin separación en el atlas: {a} y {b}")
    W, H = m["atlasSize"]
    if W > 1024 or H > 1024:
        problems.append(f"atlas de {W}×{H}: más de 1024")
    for name, fr in m["frames"].items():
        x, y, w, h = fr["rect"]
        if x + w > W or y + h > H:
            problems.append(f"{name}: fuera del atlas")
        crop = out["atlas"].crop((x, y, x + w, y + h))
        if crop.tobytes() != frames[name].img.tobytes():
            problems.append(f"{name}: el atlas no coincide con el cuadro")
    # Ajustes: los mismos que desk.ts, en el mismo orden.
    desk_map = parse_desk_ts()
    ours = {n: s["adjustments"] for n, s in m["types"].items() if s.get("adjustments")}
    for item in sorted(set(ours) | set(desk_map)):
        if ours.get(item) != desk_map.get(item):
            problems.append(f"adjustments de {item}: {ours.get(item)} y desk.ts dice {desk_map.get(item)}")
    catalog = json.loads(out["room_json"])
    if catalog["types"] != m["types"] or catalog["shell"] != m["shell"]:
        problems.append("room.json no coincide con los tipos del manifiesto")
    for name, spec in m["types"].items():
        if not spec["label"]["es"] or not spec["label"]["en"]:
            problems.append(f"{name}: sin etiqueta")
        if not spec.get("base") and not spec.get("decor") and not spec.get("adjustments"):
            problems.append(f"{name}: no es base ni decoración y ningún ajuste lo da")
        if spec.get("surface"):
            fw, fd = spec["footprint"]
            if any(not (0 <= x < fw and 0 <= y < fd) for x, y in spec["surface"]["slots"]):
                problems.append(f"{name}: slot fuera de la huella")
    return problems


# --- Vista previa ------------------------------------------------------------------------------

def cell_to_art(x, y, z=0):
    return (x - y) * (TILE_W // 2), (x + y) * (TILE_H // 2) - z


def wall_to_art(wall, u, z=0):
    return cell_to_art(0, u, z) if wall == "left" else cell_to_art(u, 0, z)


def rotate_cell(cx, cy, fp, rot):
    x, y, w, d = cx, cy, fp[0], fp[1]
    for _ in range(rot % 4):
        x, y, w, d = d - 1 - y, x, d, w
    return x, y


def compose(layout, frames):
    """Lo mismo que buildDrawList (depth.ts, tecnica.md §6.4), en Python, para revisar el arte."""
    w, d = layout["size"]
    pad = 2
    W, H = (w + d) * 16 + 2 * pad, (w + d) * 8 + WALL_H + 2 * pad
    ox, oy = d * 16 + pad, WALL_H + pad
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    def put(name, ax, ay):
        sp = frames[name]
        canvas.alpha_composite(sp.img, (ox + ax - sp.anchor[0], oy + ay - sp.anchor[1]))

    for s in range(w + d - 1):
        for x in range(w):
            y = s - x
            if 0 <= y < d:
                put(f"floor.{layout['floor']}", *cell_to_art(x, y))
    items = layout["items"]
    for it in sorted([i for i in items if TYPES[i["type"]].get("flat")], key=lambda i: (i["x"] + i["y"], i["x"])):
        put(f"{it['type']}.{it['variant']}.r{it['rot']}", *cell_to_art(it["x"], it["y"]))
    win_wall, win_u = layout["window"]
    put(f"sky.{layout['sky']}.{win_wall}", *wall_to_art(win_wall, win_u))
    for u in range(max(w, d)):
        for wall in ("left", "right"):
            if u >= (d if wall == "left" else w):
                continue
            kind = "window" if (wall, u) == (win_wall, win_u) else "wall"
            put(f"{kind}.{layout['wall']}.{wall}", *wall_to_art(wall, u))
    if layout.get("blinds"):
        put(f"blinds.{win_wall}", *wall_to_art(win_wall, win_u))
    for it in sorted([i for i in items if "wall" in i], key=lambda i: (i["u"], i["row"])):
        put(f"{it['type']}.{it['variant']}.r{0 if it['wall'] == 'right' else 1}",
            *wall_to_art(it["wall"], it["u"], it["row"] * WALL_ROW))
    solid = [i for i in items if "x" in i and not TYPES[i["type"]].get("flat")]
    entries = []
    for it in solid:
        spec = TYPES[it["type"]]
        name = f"{it['type']}.{it['variant']}.r{it['rot']}" + it.get("anim", "")
        draws = [(name, *cell_to_art(it["x"], it["y"]))]
        for slot, child in enumerate(it.get("on", [])):
            if child is None:
                continue
            cx, cy = rotate_cell(*spec["surface"]["slots"][slot], spec["footprint"], it["rot"])
            ctype, cvar = child[0], child[1]
            cspec = TYPES[ctype]
            facing = it["rot"] if it["rot"] in cspec["facings"] else next(
                (f for f in cspec["facings"] if f % 2 == it["rot"] % 2), cspec["facings"][0])
            cname = f"{ctype}.{cvar}.r{facing}" + (child[2] if len(child) > 2 else "")
            draws.append((cname, *cell_to_art(it["x"] + cx, it["y"] + cy, spec["surface"]["z"])))
        fw, fd = spec["footprint"] if it["rot"] % 2 == 0 else spec["footprint"][::-1]
        l = min(ax - frames[n].anchor[0] for n, ax, ay in draws)
        t = min(ay - frames[n].anchor[1] for n, ax, ay in draws)
        r = max(ax - frames[n].anchor[0] + frames[n].img.width for n, ax, ay in draws)
        b = max(ay - frames[n].anchor[1] + frames[n].img.height for n, ax, ay in draws)
        entries.append({"x0": it["x"], "y0": it["y"], "x1": it["x"] + fw, "y1": it["y"] + fd,
                        "box": (l, t, r, b), "draws": draws})
    n = len(entries)
    indeg, edges = [0] * n, [[] for _ in range(n)]
    for i, a in enumerate(entries):
        for j, bb in enumerate(entries):
            if i == j:
                continue
            al, at, ar, ab = a["box"]
            bl, bt, br, bbm = bb["box"]
            if not (al < br and bl < ar and at < bbm and bt < ab):
                continue
            if (a["x1"] <= bb["x0"] and not bb["y1"] <= a["y0"]) or (a["y1"] <= bb["y0"] and not bb["x1"] <= a["x0"]):
                edges[i].append(j)
                indeg[j] += 1
    done, order = [False] * n, []
    while len(order) < n:
        ready = [k for k in range(n) if not done[k] and indeg[k] == 0] or [k for k in range(n) if not done[k]]
        k = min(ready, key=lambda q: (entries[q]["x0"] + entries[q]["y0"], entries[q]["x0"], q))
        done[k] = True
        order.append(k)
        for j in edges[k]:
            indeg[j] -= 1
    for k in order:
        for name, ax, ay in entries[k]["draws"]:
            put(name, ax, ay)
    return canvas


BASE_ROOM = {
    # Sala nueva: escritorio contra la pared derecha con la pantalla, silla enfrente y la planta en la
    # esquina (donde la pondría autoPlace), ventana de día.
    "size": (5, 5), "floor": "oak", "wall": "teal", "window": ("right", 3), "sky": "day",
    "items": [
        {"type": "desk", "variant": "oak", "x": 1, "y": 0, "rot": 0, "on": [("monitor", "normal"), None]},
        {"type": "chair", "variant": "sage", "x": 1, "y": 1, "rot": 2},
        {"type": "plant", "variant": "default", "x": 0, "y": 0, "rot": 0},
    ],
}

DECO_ROOM = {
    # Decorada, al atardecer con la persiana y la pantalla tenue.
    "size": (5, 5), "floor": "oak", "wall": "sage", "window": ("right", 3), "sky": "dusk", "blinds": True,
    "items": [
        {"type": "rug", "variant": "terracotta", "x": 1, "y": 2, "rot": 0},
        {"type": "desk", "variant": "oak", "x": 1, "y": 0, "rot": 0,
         "on": [("monitor", "dim", ":wave1"), ("lamp", "warm")]},
        {"type": "chair", "variant": "sage", "x": 1, "y": 1, "rot": 2},
        {"type": "bookshelf", "variant": "oak", "x": 0, "y": 0, "rot": 3, "on": [("plant", "default")]},
        {"type": "floorLamp", "variant": "cream", "x": 0, "y": 1, "rot": 0},
        {"type": "armchair", "variant": "terracotta", "x": 0, "y": 2, "rot": 3},
        {"type": "sideTable", "variant": "oak", "x": 0, "y": 3, "rot": 0, "on": [("mug", "default", ":steam0")]},
        {"type": "fern", "variant": "default", "x": 0, "y": 4, "rot": 0},
        {"type": "beaver", "variant": "default", "x": 2, "y": 3, "rot": 0, "anim": ":wave1"},
        {"type": "fan", "variant": "default", "x": 4, "y": 0, "rot": 0, "anim": ":spin1"},
        {"type": "divider", "variant": "sage", "x": 4, "y": 2, "rot": 1},
        {"type": "sideTable", "variant": "cream", "x": 4, "y": 4, "rot": 0, "on": [("headphones", "default")]},
        {"type": "poster", "variant": "hills", "wall": "left", "u": 1, "row": 1},
        {"type": "frame", "variant": "home", "wall": "right", "u": 0, "row": 1},
        {"type": "sweater", "variant": "default", "wall": "right", "u": 4, "row": 1},
    ],
}

TURNED_ROOM = {
    # Giros r3 y r1: escritorio contra la pared izquierda mirando a +x, silla mirándolo, ventana en la
    # pared izquierda y de noche, para revisar anclas, slots girados y el orden de dibujo.
    "size": (5, 5), "floor": "tile", "wall": "cream", "window": ("left", 3), "sky": "night",
    "items": [
        {"type": "rug", "variant": "sage", "x": 2, "y": 2, "rot": 0},
        {"type": "desk", "variant": "sage", "x": 0, "y": 1, "rot": 3,
         "on": [("monitor", "normal", ":wave0"), ("succulent", "default")]},
        {"type": "chair", "variant": "terracotta", "x": 1, "y": 1, "rot": 1},
        {"type": "bookshelf", "variant": "sage", "x": 2, "y": 0, "rot": 0, "on": [("speaker", "default")]},
        {"type": "sideTable", "variant": "cream", "x": 3, "y": 0, "rot": 0, "on": [("phone", "default")]},
        {"type": "armchair", "variant": "sage", "x": 4, "y": 1, "rot": 0},
        {"type": "beaver", "variant": "default", "x": 3, "y": 3, "rot": 3},
        {"type": "floorLamp", "variant": "terracotta", "x": 0, "y": 4, "rot": 0},
        {"type": "divider", "variant": "cream", "x": 1, "y": 4, "rot": 0},
        {"type": "poster", "variant": "wave", "wall": "right", "u": 1, "row": 1},
        {"type": "frame", "variant": "home", "wall": "left", "u": 0, "row": 1},
        {"type": "sweater", "variant": "default", "wall": "right", "u": 4, "row": 1},
    ],
}


def preview(out):
    """Tres salas (×3) arriba y la hoja de contacto (×3) abajo, con vecino más cercano."""
    frames, unique, alias = out["frames"], out["unique"], out["alias"]
    paper = (244, 238, 226, 255)
    S = 3
    font = ImageFont.load_default()
    rooms = [compose(r, frames) for r in (BASE_ROOM, DECO_ROOM, TURNED_ROOM)]
    rw, rh = rooms[0].width * S, rooms[0].height * S
    names = {}
    for name in sorted(frames):
        names.setdefault(alias[name], name)
    cells = sorted(((names[h], unique[h]) for h in names), key=lambda c: c[0])
    W = 3 * rw + 4 * 16
    col_w = 124
    x = y = row_h = 0
    pos = []
    for name, sp in cells:
        w = max(col_w, sp.img.width * S + 8)
        if x + w > W - 32:
            x, y, row_h = 0, y + row_h, 0
        pos.append((name, sp, x, y))
        x += w
        row_h = max(row_h, sp.img.height * S + 20)
    top = 16 + rh + 24
    img = Image.new("RGBA", (W, top + y + row_h + 16), paper)
    draw = ImageDraw.Draw(img)
    for n, room in enumerate(rooms):
        img.alpha_composite(room.resize((rw, rh), Image.NEAREST), (16 + n * (rw + 16), 16))
    for name, sp, cx, cy in pos:
        im = sp.img.resize((sp.img.width * S, sp.img.height * S), Image.NEAREST)
        img.alpha_composite(im, (16 + cx + 4, top + cy + 14))
        draw.text((16 + cx + 4, top + cy + 2), name, fill=(60, 60, 60, 255), font=font)
    return img


def png_bytes(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    first = build()
    problems = check(first)
    if "--draft" in sys.argv:  # solo la vista previa, para iterar el arte aunque falle algo
        out = Path(sys.argv[sys.argv.index("--draft") + 1])
        out.write_bytes(png_bytes(preview(first)))
        print("\n".join(problems) or "sin problemas")
        return
    if problems:
        print("\n".join(problems))
        sys.exit(f"draw_room: {len(problems)} problemas")
    second = build()
    for k in ("atlas_png", "manifest_ts", "room_json"):
        if first[k] != second[k]:
            sys.exit(f"draw_room: la salida {k} cambia entre corridas")
    prev = png_bytes(preview(first))
    if prev != png_bytes(preview(second)):
        sys.exit("draw_room: la vista previa cambia entre corridas")
    ATLAS_PNG.parent.mkdir(parents=True, exist_ok=True)
    ATLAS_PNG.write_bytes(first["atlas_png"])
    MANIFEST_TS.write_text(first["manifest_ts"], encoding="utf-8", newline="\n")
    ROOM_JSON.write_text(first["room_json"], encoding="utf-8", newline="\n")
    PREVIEW_PNG.write_bytes(prev)
    W, H = first["atlas"].size
    print(f"ok: {len(first['frames'])} cuadros ({len(first['unique'])} únicos), atlas {W}×{H} "
          f"({len(first['atlas_png'])} B), manifest.ts {len(first['manifest_ts'])} B")


if __name__ == "__main__":
    main()
