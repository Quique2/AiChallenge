#!/usr/bin/env python3
"""Íconos de SpaceEase: pixel art propio de 20 × 20, determinista, con la paleta de la marca.

Cada ícono va sobre una baldosa de color fijo con esquinas de pixel: así se lee igual en las 12
paletas de la app y en modo oscuro, y los colores de la baldosa agrupan sin depender solo del color
(la forma del dibujo y su nombre siempre van juntos).

Uso, desde la raíz del repo: python docs/brand/draw_icons.py
Escribe apps/mobile/assets/icons/*.png (×12, para que a 40 y 80 pt caigan pixeles enteros en
pantallas ×3), apps/mobile/src/components/pixel-icons.ts y docs/brand/icons-preview.png.
"""
import sys
from pathlib import Path

from PIL import Image

N = 20
SCALE = 12
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "apps/mobile/assets/icons"
TS = ROOT / "apps/mobile/src/components/pixel-icons.ts"
PREVIEW = ROOT / "docs/brand/icons-preview.png"

C = {
    "ink": "#173a3d", "teal": "#20494a", "lit": "#3f8a7b", "mist": "#d3e7df", "cream": "#f7eedb",
    "paper": "#fbf8f1", "peach": "#f3d4b0", "apricot": "#e9b58c", "oak": "#bf7f4c", "shadow": "#8f5440",
    "sage": "#a9c8a0", "leaf": "#6f9f6a", "pine": "#3f6f55", "sun": "#f2c66d", "rust": "#b86a45",
    "sky": "#a8d2d8", "plum": "#6b5a72",
}
# Baldosa por grupo: fondo y su sombra de abajo.
TILES = {
    "mist": ("mist", "sky"), "peach": ("peach", "apricot"), "sage": ("sage", "leaf"),
    "cream": ("cream", "peach"), "sky": ("sky", "lit"),
}


class Icon:
    def __init__(self, tile):
        self.img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        self.tile = tile
        face, low = TILES[tile]
        for y in range(N):
            for x in range(N):
                cut = (x in (0, N - 1)) + (y in (0, N - 1))
                if cut == 2:
                    continue
                self.dot(x, y, low if y >= N - 2 else face)

    def dot(self, x, y, c):
        if 0 <= x < N and 0 <= y < N:
            h = C[c].lstrip("#")
            self.img.putpixel((x, y), tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,))

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.dot(x, y, c)

    def box(self, x0, y0, x1, y1, fill, line="ink"):
        """Rectángulo con contorno y esquinas recortadas."""
        self.rect(x0 + 1, y0, x1 - 1, y1, line)
        self.rect(x0, y0 + 1, x1, y1 - 1, line)
        self.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill)

    def line(self, pts, c):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            steps = max(abs(x1 - x0), abs(y1 - y0), 1)
            for i in range(steps + 1):
                self.dot(round(x0 + (x1 - x0) * i / steps), round(y0 + (y1 - y0) * i / steps), c)

    def disc(self, cx, cy, r, fill, line="ink"):
        for y in range(cy - r - 1, cy + r + 2):
            for x in range(cx - r - 1, cx + r + 2):
                d = (x - cx) ** 2 + (y - cy) ** 2
                if d <= r * r:
                    self.dot(x, y, fill)
                elif line and d <= (r + 1) * (r + 1) + 1:
                    self.dot(x, y, line)

    def dots(self, pts, c):
        for x, y in pts:
            self.dot(x, y, c)


ICONS = {}


def icon(name, tile):
    def wrap(fn):
        ic = Icon(tile)
        fn(ic)
        ICONS[name] = ic.img
        return fn
    return wrap


# ── Entrada del registro ────────────────────────────────────────────────────────────────────

@icon("sensory", "sky")
def _(i):  # ventana con luz y una planta
    i.box(5, 3, 14, 13, "paper")
    i.rect(6, 4, 13, 12, "sun")
    i.rect(6, 4, 9, 7, "cream")
    i.rect(9, 4, 10, 12, "ink")
    i.rect(6, 8, 13, 8, "ink")
    i.rect(4, 14, 15, 15, "oak")
    i.rect(4, 15, 15, 15, "shadow")


@icon("mind", "peach")
def _(i):  # cabeza de perfil con una chispa adentro
    for y, x0, x1 in ((3, 7, 12), (4, 6, 13), (5, 5, 14), (6, 5, 14), (7, 5, 14), (8, 5, 14), (9, 5, 15), (10, 5, 16),
                      (11, 5, 15), (12, 5, 14), (13, 6, 13), (14, 7, 12), (15, 7, 10), (16, 7, 10)):
        i.rect(x0, y, x1, y, "teal")
    i.line([(9, 5), (9, 10)], "sun")
    i.line([(7, 7), (11, 7)], "sun")
    i.dots([(8, 6), (10, 6), (8, 8), (10, 8)], "cream")


@icon("unsure", "cream")
def _(i):  # signo de pregunta
    i.rect(6, 4, 13, 5, "teal")
    i.rect(12, 5, 13, 9, "teal")
    i.rect(6, 5, 7, 7, "teal")
    i.rect(9, 9, 13, 10, "teal")
    i.rect(9, 10, 10, 12, "teal")
    i.rect(9, 14, 10, 15, "rust")


@icon("zen", "sage")
def _(i):  # hoja
    i.line([(5, 15), (14, 5)], "pine")
    i.rect(8, 5, 13, 6, "cream")
    i.rect(6, 7, 13, 8, "cream")
    i.rect(5, 9, 11, 10, "cream")
    i.rect(5, 11, 9, 12, "cream")
    i.line([(5, 15), (14, 5)], "pine")
    i.line([(8, 5), (5, 9), (5, 13)], "pine")
    i.line([(14, 5), (13, 9), (9, 13), (5, 13)], "pine")


# ── Dominios del entorno ────────────────────────────────────────────────────────────────────

@icon("sound", "mist")
def _(i):  # bocina con ondas
    i.rect(3, 8, 6, 12, "ink")
    i.line([(6, 8), (10, 4)], "ink")
    i.line([(6, 12), (10, 16)], "ink")
    i.rect(10, 4, 10, 16, "ink")
    i.rect(7, 8, 9, 12, "teal")
    i.rect(8, 6, 9, 14, "teal")
    i.line([(12, 8), (13, 9), (13, 11), (12, 12)], "rust")
    i.line([(14, 6), (16, 8), (16, 12), (14, 14)], "rust")


@icon("light", "cream")
def _(i):  # foco
    i.disc(10, 8, 4, "sun")
    i.rect(8, 6, 9, 7, "paper")
    i.rect(8, 13, 11, 13, "shadow")
    i.rect(8, 14, 11, 15, "ink")
    i.dots([(10, 1), (3, 3), (16, 3), (2, 8), (17, 8)], "rust")


@icon("sight", "sky")
def _(i):  # ojo
    i.line([(3, 10), (7, 6), (12, 6), (16, 10), (12, 14), (7, 14), (3, 10)], "ink")
    i.rect(6, 7, 13, 13, "paper")
    i.rect(4, 9, 15, 11, "paper")
    i.line([(3, 10), (7, 6), (12, 6), (16, 10), (12, 14), (7, 14), (3, 10)], "ink")
    i.disc(10, 10, 2, "teal", "ink")
    i.dot(9, 9, "paper")


@icon("body", "peach")
def _(i):  # termómetro
    i.box(8, 2, 11, 12, "paper")
    i.disc(9, 14, 3, "rust")
    i.rect(9, 7, 10, 13, "rust")
    i.dots([(13, 4), (13, 7), (13, 10)], "shadow")
    i.dots([(14, 4), (14, 7), (14, 10)], "shadow")


# ── Tareas ──────────────────────────────────────────────────────────────────────────────────

@icon("reading", "mist")
def _(i):  # libro abierto
    i.rect(2, 5, 17, 14, "ink")
    i.rect(3, 6, 9, 13, "paper")
    i.rect(10, 6, 16, 13, "cream")
    i.rect(2, 15, 17, 15, "teal")
    for y in (8, 10, 12):
        i.rect(4, y, 8, y, "lit")
        i.rect(11, y, 15, y, "oak")


@icon("writing", "cream")
def _(i):  # lápiz
    i.line([(14, 3), (5, 12)], "ink")
    i.line([(16, 5), (7, 14)], "ink")
    i.line([(15, 4), (6, 13)], "sun")
    i.line([(15, 5), (7, 13)], "oak")
    i.rect(14, 3, 16, 5, "rust")
    i.dots([(4, 15), (5, 15), (4, 14), (5, 14), (6, 14), (5, 13)], "ink")
    i.line([(9, 16), (16, 16)], "lit")


@icon("focus", "sky")
def _(i):  # diana
    i.disc(10, 9, 6, "paper")
    i.disc(10, 9, 3, "lit", "ink")
    i.disc(10, 9, 1, "rust", None)


@icon("data", "mist")
def _(i):  # barras
    i.rect(3, 15, 16, 15, "ink")
    i.box(4, 9, 7, 14, "lit")
    i.box(8, 5, 11, 14, "oak")
    i.box(12, 7, 15, 14, "rust")


@icon("calls", "peach")
def _(i):  # audífono de llamada
    i.line([(5, 11), (5, 7), (7, 4), (12, 4), (14, 7), (14, 11)], "ink")
    i.box(3, 10, 6, 15, "teal")
    i.box(13, 10, 16, 15, "teal")
    i.line([(15, 15), (15, 17), (11, 17)], "ink")
    i.rect(10, 16, 11, 17, "rust")


@icon("meetings", "sage")
def _(i):  # dos personas
    i.disc(6, 6, 2, "peach")
    i.disc(13, 6, 2, "apricot")
    i.box(3, 10, 9, 16, "teal")
    i.box(10, 10, 16, 16, "rust")


@icon("creative", "cream")
def _(i):  # paleta de pintor
    i.disc(10, 9, 6, "apricot")
    i.disc(5, 7, 1, "rust", None)
    i.disc(9, 5, 1, "lit", None)
    i.disc(14, 6, 1, "teal", None)
    i.disc(14, 11, 1, "sun", None)
    i.disc(7, 12, 1, "paper", "shadow")


@icon("routine", "sky")
def _(i):  # lista con palomitas
    i.box(4, 2, 15, 16, "paper")
    i.rect(8, 1, 11, 3, "ink")
    for y in (6, 9, 12):
        i.dots([(6, y), (7, y + 1), (8, y)], "lit")
        i.rect(10, y, 13, y, "teal")


@icon("other", "mist")
def _(i):  # tres puntos
    for x in (4, 9, 14):
        i.rect(x, 8, x + 2, 10, "teal")


# ── Cómo se siente ──────────────────────────────────────────────────────────────────────────

@icon("drained", "peach")
def _(i):  # pila baja
    i.box(2, 6, 15, 13, "paper")
    i.rect(16, 8, 17, 11, "ink")
    i.rect(4, 8, 5, 11, "rust")


@icon("charged", "sage")
def _(i):  # pila a la mitad
    i.box(2, 6, 15, 13, "paper")
    i.rect(16, 8, 17, 11, "ink")
    i.rect(4, 8, 5, 11, "lit")
    i.rect(7, 8, 8, 11, "lit")
    i.rect(10, 8, 11, 11, "lit")


@icon("discomfort", "peach")
def _(i):  # onda con picos
    i.line([(2, 10), (5, 10), (7, 4), (9, 15), (11, 6), (13, 13), (15, 10), (17, 10)], "rust")
    i.line([(2, 11), (5, 11), (7, 5), (9, 16), (11, 7), (13, 14), (15, 11), (17, 11)], "ink")


@icon("overload", "cream")
def _(i):  # hojas que se apilan de más
    i.box(5, 12, 15, 16, "paper")
    i.box(3, 8, 13, 12, "mist")
    i.box(6, 4, 16, 8, "peach")
    i.rect(8, 6, 13, 6, "shadow")
    i.rect(7, 14, 12, 14, "lit")


# ── Lo cognitivo ────────────────────────────────────────────────────────────────────────────

@icon("start", "sage")
def _(i):  # bandera de salida
    i.rect(5, 2, 6, 16, "ink")
    i.rect(7, 3, 15, 9, "ink")
    i.rect(7, 4, 14, 8, "cream")
    for x, y in ((8, 4), (11, 4), (9, 6), (12, 6), (8, 8), (11, 8), (14, 5)):
        i.rect(x, y, x + 1 if x < 14 else x, y, "teal")


@icon("organize", "mist")
def _(i):  # tres renglones, uno elegido
    i.box(3, 3, 16, 7, "paper")
    i.rect(5, 5, 13, 5, "lit")
    i.box(3, 8, 16, 11, "cream")
    i.box(3, 12, 16, 15, "cream")
    i.rect(5, 9, 10, 10, "shadow")
    i.rect(5, 13, 12, 14, "shadow")


@icon("onmind", "sky")
def _(i):  # nube de pensamiento
    i.disc(7, 7, 3, "paper")
    i.disc(13, 7, 3, "paper")
    i.disc(10, 6, 3, "paper")
    i.rect(6, 6, 14, 9, "paper")
    i.rect(5, 10, 15, 10, "ink")
    i.rect(8, 6, 12, 6, "paper")
    i.line([(7, 7), (9, 8), (11, 6), (13, 8)], "rust")
    i.rect(7, 12, 8, 13, "ink")
    i.rect(4, 15, 5, 16, "ink")


@icon("changed", "peach")
def _(i):  # dos flechas que cambian de camino
    i.line([(3, 6), (13, 6)], "ink")
    i.line([(3, 7), (13, 7)], "ink")
    i.line([(11, 3), (15, 6), (11, 10)], "teal")
    i.line([(16, 12), (6, 12)], "ink")
    i.line([(16, 13), (6, 13)], "ink")
    i.line([(8, 9), (4, 13), (8, 16)], "rust")


@icon("unclear", "cream")
def _(i):  # hoja con pregunta
    i.box(4, 2, 15, 16, "paper")
    i.rect(7, 5, 12, 5, "teal")
    i.rect(11, 5, 12, 8, "teal")
    i.rect(9, 8, 12, 8, "teal")
    i.rect(9, 9, 10, 11, "teal")
    i.rect(9, 13, 10, 14, "rust")


# ── Minijuegos y accesos ────────────────────────────────────────────────────────────────────

@icon("breath", "sky")
def _(i):  # aire que entra y sale: dos ondas, una entra y otra sale
    i.rect(3, 6, 6, 7, "teal")
    i.rect(6, 5, 11, 6, "teal")
    i.rect(11, 6, 14, 7, "teal")
    i.rect(14, 5, 16, 6, "teal")
    i.rect(3, 12, 5, 13, "paper")
    i.rect(5, 11, 8, 12, "paper")
    i.rect(8, 12, 13, 13, "paper")
    i.rect(13, 11, 16, 12, "paper")


@icon("grounding", "peach")
def _(i):  # mano abierta: cinco dedos, cinco sentidos
    for x, top in ((4, 7), (7, 4), (10, 3), (13, 5)):
        i.rect(x, top, x + 2, 11, "ink")
        i.rect(x + 1, top + 1, x + 1, 11, "cream")
    i.rect(4, 10, 15, 16, "ink")
    i.rect(5, 11, 14, 15, "cream")
    i.line([(15, 11), (17, 9)], "ink")
    i.line([(15, 12), (17, 10)], "ink")
    i.rect(5, 11, 14, 12, "cream")


@icon("garden", "sage")
def _(i):  # brote en maceta
    i.rect(9, 6, 10, 12, "pine")
    i.rect(5, 5, 8, 7, "leaf")
    i.rect(5, 5, 8, 5, "pine")
    i.rect(11, 3, 14, 5, "cream")
    i.rect(11, 5, 14, 5, "pine")
    i.box(5, 12, 14, 16, "rust")
    i.rect(6, 13, 13, 13, "apricot")


@icon("paint", "cream")
def _(i):  # cuadrícula a medio pintar con su pincel
    i.box(3, 3, 14, 14, "paper")
    for x, y, c in ((4, 4, "lit"), (7, 4, "lit"), (10, 4, "sun"), (4, 7, "rust"), (7, 7, "lit"), (4, 10, "rust")):
        i.rect(x, y, x + 2, y + 2, c)
    i.line([(16, 8), (11, 13)], "shadow")
    i.line([(17, 9), (12, 14)], "oak")
    i.rect(10, 13, 12, 15, "ink")
    i.rect(10, 15, 10, 16, "rust")


@icon("decorate", "peach")
def _(i):  # un sillón, como los del cuarto
    i.box(5, 4, 14, 11, "lit")  # respaldo
    i.rect(6, 5, 13, 6, "sage")
    i.box(3, 8, 6, 15, "teal")  # brazos
    i.box(13, 8, 16, 15, "teal")
    i.box(6, 10, 13, 15, "sage")  # asiento
    i.rect(7, 11, 12, 11, "cream")
    i.rect(5, 16, 6, 17, "shadow")  # patas
    i.rect(13, 16, 14, 17, "shadow")


@icon("spoon", "cream")
def _(i):  # cuchara: el hueco lleno, para que no parezca una lupa
    i.rect(11, 2, 15, 8, "teal")
    i.rect(12, 1, 14, 9, "teal")
    i.rect(12, 3, 14, 7, "lit")
    i.rect(10, 8, 12, 10, "teal")
    i.line([(10, 10), (4, 16)], "teal")
    i.line([(11, 10), (5, 16)], "teal")


@icon("energy", "sage")
def _(i):  # pila con un rayo
    i.box(2, 5, 15, 14, "paper")
    i.rect(16, 8, 17, 11, "ink")
    i.rect(4, 7, 13, 12, "leaf")
    i.line([(10, 6), (7, 10), (10, 10), (8, 13)], "cream")
    i.line([(9, 6), (6, 10), (9, 10), (7, 13)], "cream")


@icon("strategies", "mist")
def _(i):  # libro con un foco
    i.box(3, 8, 16, 16, "paper")
    i.rect(9, 9, 10, 15, "ink")
    i.rect(5, 11, 7, 11, "lit")
    i.rect(12, 11, 14, 11, "oak")
    i.rect(5, 13, 7, 13, "lit")
    i.rect(12, 13, 14, 13, "oak")
    i.disc(10, 4, 2, "sun")


@icon("week", "cream")
def _(i):  # calendario
    i.box(3, 4, 16, 16, "paper")
    i.rect(4, 5, 15, 7, "rust")
    i.rect(6, 2, 7, 5, "ink")
    i.rect(12, 2, 13, 5, "ink")
    for y in (9, 12):
        for x in (5, 8, 11, 14):
            i.rect(x, y, x + 1, y + 1, "lit" if (x, y) != (8, 12) else "rust")


# ── Caritas ─────────────────────────────────────────────────────────────────────────────────

def face(i, eyes, mouth, skin="paper"):
    i.disc(9, 9, 6, skin)
    i.dots(eyes, "ink")
    i.dots(mouth, "ink")


@icon("face_calm", "sage")
def _(i):
    face(i, [(7, 7), (12, 7), (7, 8), (12, 8)], [(7, 11), (8, 12), (9, 12), (10, 12), (11, 12), (12, 11)])


@icon("face_worried", "peach")
def _(i):
    face(i, [(6, 6), (13, 6), (7, 8), (12, 8)], [(7, 12), (8, 11), (9, 11), (10, 11), (11, 11), (12, 12)])


@icon("face_tired", "sky")
def _(i):
    face(i, [(6, 8), (7, 8), (8, 8), (11, 8), (12, 8), (13, 8)], [(8, 12), (9, 12), (10, 12), (11, 12)])
    i.dots([(15, 3), (16, 3), (16, 4), (15, 5), (16, 5)], "teal")


@icon("face_overloaded", "peach")
def _(i):
    face(i, [(6, 7), (8, 7), (7, 8), (6, 9), (8, 9), (11, 7), (13, 7), (12, 8), (11, 9), (13, 9)],
         [(7, 12), (8, 11), (9, 12), (10, 11), (11, 12), (12, 11)])


@icon("face_thinking", "cream")
def _(i):
    face(i, [(7, 8), (12, 7), (12, 8)], [(8, 12), (9, 12), (10, 11), (11, 11)], "mist")
    i.rect(6, 6, 8, 6, "ink")


@icon("face_neutral", "mist")
def _(i):
    face(i, [(7, 7), (12, 7), (7, 8), (12, 8)], [(7, 12), (8, 12), (9, 12), (10, 12), (11, 12), (12, 12)])


# ── Salida ──────────────────────────────────────────────────────────────────────────────────

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    names = sorted(ICONS)
    for path in OUT.glob("*.png"):
        path.unlink()
    for name in names:
        big = ICONS[name].resize((N * SCALE, N * SCALE), Image.NEAREST)
        big.quantize(colors=32, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(OUT / f"{name}.png", optimize=True)
    rows = ",\n".join(f"  {name}: require('@/assets/icons/{name}.png')" for name in names)
    TS.write_text(
        "// Generado por docs/brand/draw_icons.py: no editar a mano.\n"
        f"export const PIXEL_ICONS = {{\n{rows},\n}} as const;\n\n"
        "export type IconName = keyof typeof PIXEL_ICONS;\n",
        encoding="utf-8", newline="\n",
    )
    cols = 8
    rows_n = (len(names) + cols - 1) // cols
    k = 5
    sheet = Image.new("RGB", (cols * (N * k + 8) + 8, rows_n * (N * k + 8) + 8), (21, 47, 50))
    half = Image.new("RGB", (sheet.width, sheet.height), (244, 238, 226))
    half_w = sheet.width // 2
    sheet.paste(half.crop((0, 0, half_w, sheet.height)), (0, 0))
    for i, name in enumerate(names):
        tile = ICONS[name].resize((N * k, N * k), Image.NEAREST)
        sheet.paste(tile, (8 + (i % cols) * (N * k + 8), 8 + (i // cols) * (N * k + 8)), tile)
    sheet.save(PREVIEW, optimize=True)
    print(f"ok: {len(names)} íconos; {sum(p.stat().st_size for p in OUT.glob('*.png'))} B")
    return 0


if __name__ == "__main__":
    sys.exit(main())
