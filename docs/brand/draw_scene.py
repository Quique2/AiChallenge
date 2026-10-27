#!/usr/bin/env python3
"""Escena "Tu escritorio": la versión ancha del ícono, por capas, para animarla en la app.

Misma ventana en arco, monitor y planta del ícono (draw_icon.py), en un lienzo de 64x32.
Cada capa es un PNG transparente del tamaño del lienzo, escalado con vecino más cercano,
para apilarlas en la app sin calcular posiciones:

- cielo según la hora (amanecer, día, atardecer, noche), debajo de todo;
- pantalla del monitor: la onda pasa de ruidosa a tranquila (la metáfora del ícono);
- base (pared, repisa, escritorio, monitor) y planta, con un segundo cuadro para mecerse;
- 14 objetos que aparecen cuando un ajuste ayuda, más los cuadros de vapor y del ventilador.

Uso: python draw_scene.py [carpeta_de_la_app]   (por defecto apps/mobile)
Escribe assets/scene/*.png, src/components/desk/layers.ts y docs/brand/scene-preview.png.
"""
import sys
from pathlib import Path

from PIL import Image

from draw_icon import ARCH_FULL, ARCH_HALF, ARCH_TOP, DESK_TOP, PALETTE as ICON_PALETTE, checker, sparse

W, H = 64, 28  # el escritorio termina en la fila 26: abajo solo queda una fila de pared
OX = 16  # el contenido del ícono, desplazado al centro del lienzo
SCALE = 16  # 64 x 16 = 1024 px: un pixel de la escena mide ~16 px de pantalla en un iPhone

PALETTE = {
    **ICON_PALETTE,
    # Cielos (cada rampa cambia de tono, no solo de brillo).
    "day_top": "#bcdcdc", "day_mid": "#d3e7df", "day_low": "#e8efe2", "day_bottom": "#f7eedb",
    "dusk_top": "#6f5a78", "dusk_mid": "#a96f78", "dusk_low": "#d99577", "dusk_bottom": "#e9b58c",
    "night_top": "#1b2f45", "night_mid": "#213a50", "night_low": "#29465a", "night_bottom": "#335466",
    # Objetos.
    "sage_hi": "#b4cdb9", "sage": "#8fae9a", "sage_shadow": "#6d8c7e",
    "blind": "#efe3cc", "blind_shadow": "#cdb994",
    "dim_screen": "#2e5a5a", "dim_hi": "#3a6a66",
}

SKIES = {
    "dawn": ("mist", "cream", "peach", "apricot"),
    "day": ("day_top", "day_mid", "day_low", "day_bottom"),
    "dusk": ("dusk_top", "dusk_mid", "dusk_low", "dusk_bottom"),
    "night": ("night_top", "night_mid", "night_low", "night_bottom"),
}


class Layer:
    def __init__(self):
        self.c = [[None] * W for _ in range(H)]

    def set(self, x, y, key):
        if 0 <= x < W and 0 <= y < H:
            self.c[y][x] = key

    def hline(self, x0, x1, y, key):
        for x in range(x0, x1 + 1):
            self.set(x, y, key)

    def vline(self, x, y0, y1, key):
        for y in range(y0, y1 + 1):
            self.set(x, y, key)

    def rect(self, x0, y0, x1, y1, key):
        for y in range(y0, y1 + 1):
            self.hline(x0, x1, y, key)

    def cells(self, pairs, key):
        for x, y in pairs:
            self.set(x, y, key)

    def box(self):
        xs = [x for y in range(H) for x in range(W) if self.c[y][x]]
        ys = [y for y in range(H) for x in range(W) if self.c[y][x]]
        return [min(xs), min(ys), max(xs), max(ys)] if xs else None


def arch_half(y):
    if y < ARCH_TOP:
        return 0
    i = y - ARCH_TOP
    return ARCH_HALF[i] if i < len(ARCH_HALF) else ARCH_FULL


def in_arch(x, y):
    w = arch_half(y)
    return y < DESK_TOP and w > 0 and OX + 16 - w <= x <= OX + 15 + w


# --- Base ---------------------------------------------------------------------------------

def wall(layer):
    arch = [(ax, ay) for ay in range(H) for ax in range(W) if in_arch(ax, ay)]
    for y in range(H):
        for x in range(W):
            if in_arch(x, y):
                continue
            d = min(((x - ax) ** 2 + (y - ay) ** 2) ** 0.5 for ax, ay in arch)
            if d <= 1.5:
                key = "wall_lit"
            elif d <= 2.5:
                key = "wall_lit" if checker(x, y) else "wall"
            elif d <= 3.5:
                key = "wall"
            elif d <= 4.5:
                key = "wall" if checker(x, y) else "wall_deep"
            else:
                key = "wall_deep"
            layer.set(x, y, key)


def shelf(layer):
    layer.hline(46, 61, 12, "oak_hi")
    layer.hline(46, 61, 13, "oak_shadow")
    for x in (48, 59):
        layer.set(x, 14, "oak_deep")
        layer.set(x, 15, "oak_deep")


def desk(layer):
    t = DESK_TOP
    layer.hline(0, W - 1, t, "oak_hi")
    layer.hline(0, W - 1, t + 1, "oak")
    layer.hline(0, W - 1, t + 2, "oak")
    for a, b in [(2, 8), (18, 25), (33, 40), (50, 57)]:
        layer.hline(a, b, t + 2, "oak_shadow")
    layer.hline(0, W - 1, t + 3, "oak_shadow")
    layer.hline(0, W - 1, t + 4, "oak_deep")
    layer.hline(OX + 8, OX + 14, t, "oak")  # sombra del pie del monitor
    layer.hline(OX + 20, OX + 24, t, "oak")  # sombra de la maceta


def monitor_frame(layer):
    x0 = OX
    layer.rect(x0 + 6, 10, x0 + 16, 18, "ink")
    layer.hline(x0 + 7, x0 + 15, 10, "ink_hi")
    for y in range(11, 17):  # hueco de la pantalla: va en su propia capa
        for x in range(x0 + 7, x0 + 16):
            layer.c[y][x] = None
    layer.rect(x0 + 10, 19, x0 + 12, 20, "ink")
    layer.set(x0 + 10, 19, "ink_hi")
    layer.set(x0 + 10, 20, "ink_hi")
    layer.hline(x0 + 8, x0 + 14, 21, "ink")


WAVES = {
    # De ruidosa a la onda del ícono (que termina plana): el ruido que se calma.
    "noisy": [13, 11, 14, 12, 15, 12, 14],
    "mid": [14, 12, 14, 13, 14, 13, 14],
    "calm": [14, 13, 12, 13, 14, 14, 14],
}


def screen(wave, dim):
    s = Layer()
    fill, glow, line = ("dim_screen", "dim_hi", "screen") if dim else ("screen", "screen_hi", "wave")
    for y in range(11, 17):
        for x in range(OX + 7, OX + 16):
            s.set(x, y, glow if y == 11 else fill)
    ys = WAVES[wave]
    for i, y in enumerate(ys):
        s.set(OX + 8 + i, y, line)
        if i and abs(y - ys[i - 1]) > 1:  # une los saltos de más de un pixel
            step = 1 if y > ys[i - 1] else -1
            for yy in range(ys[i - 1] + step, y, step):
                s.set(OX + 8 + i - (0 if abs(yy - y) < abs(yy - ys[i - 1]) else 1), yy, line)
    return s


def sky(name):
    top, mid, low, bottom = SKIES[name]
    s = Layer()
    transitions = [(5, top, mid), (11, mid, low), (16, low, bottom)]
    for y in range(H):
        for x in range(W):
            if not in_arch(x, y):
                continue
            key = top
            for row, upper, lower in transitions:
                if y < row:
                    break
                if y == row:
                    key = upper if checker(x, y) else lower
                    break
                if y == row + 1:
                    key = upper if sparse(x, y) else lower
                    break
                key = lower
            s.set(x, y, key)
    if name == "night":
        s.cells([(23, 6), (28, 3), (37, 7), (41, 12), (25, 13), (34, 4)], "cream")
        s.rect(37, 3, 38, 4, "cream")  # luna
        s.set(39, 4, "peach")
        s.set(38, 5, "peach")
    return s


def plant(sway):
    p = Layer()
    x0 = OX
    p.hline(x0 + 19, x0 + 25, 17, "pot_hi")
    p.set(x0 + 25, 17, "pot_shadow")
    p.rect(x0 + 20, 18, x0 + 24, 20, "pot")
    p.hline(x0 + 21, x0 + 24, 18, "pot_shadow")
    for y in (19, 20):
        p.set(x0 + 20, y, "pot_hi")
        p.set(x0 + 24, y, "pot_shadow")
    p.hline(x0 + 21, x0 + 23, 21, "pot_shadow")
    lean = 1 if sway else 0  # en el segundo cuadro, las puntas se inclinan un pixel hacia la ventana
    blades = [
        ([(22, 7), (22, 8), (23, 8)] + [(x, y) for y in range(9, 17) for x in (22, 23)],
         [(22, y) for y in range(7, 17)]),
        ([(19, 10), (19, 11), (20, 11), (19, 12), (20, 12), (20, 13), (21, 13),
          (20, 14), (21, 14), (21, 15), (21, 16)],
         [(19, 10), (19, 11), (19, 12), (20, 13), (20, 14), (21, 15)]),
        ([(25, 9), (25, 10), (24, 10), (25, 11), (24, 11), (24, 12), (25, 12),
          (24, 13), (23, 14), (24, 14), (23, 15), (24, 15), (24, 16)],
         [(25, 9), (24, 10), (24, 11), (24, 12), (24, 13), (23, 14), (23, 15)]),
    ]

    def moved(x, y):
        return (x - lean, y) if y <= 9 else (x, y)

    for cells, lit in blades:
        for x, y in cells:
            mx, my = moved(x, y)
            p.set(x0 + mx, my, "leaf")
        for x, y in lit:
            mx, my = moved(x, y)
            p.set(x0 + mx, my, "leaf_hi")
    for x, y in [(22, 16), (23, 16), (24, 16), (21, 16), (23, 15)]:
        p.set(x0 + x, y, "leaf_deep")
    return p


# --- Objetos que se ganan ------------------------------------------------------------------

def headphones():
    """Colgados de la esquina del monitor."""
    h = Layer()
    h.hline(21, 23, 7, "ink_hi")
    h.cells([(20, 8), (24, 8)], "ink_hi")
    h.cells([(19, 9), (19, 10), (24, 9)], "ink")
    h.hline(19, 20, 11, "cream")
    h.rect(18, 12, 20, 13, "cream")
    h.set(18, 13, "blind_shadow")
    h.hline(19, 20, 14, "blind_shadow")
    h.vline(21, 12, 13, "oak_deep")  # almohadilla, contra el monitor
    return h


def lamp(on=True):
    """Lámpara de brazo a la izquierda, con luz cálida sobre el escritorio."""
    l = Layer()
    if on:  # cono de luz: más luz cerca de la pantalla de la lámpara
        for y in range(16, 22):
            spread = (y - 16) // 2
            for x in range(10 - spread, 13 + spread):
                l.set(x, y, "apricot" if sparse(x, y) and y > 17 else "wall_lit")
        l.hline(8, 14, 22, "peach")  # el escritorio iluminado
    l.hline(3, 7, 21, "ink")
    l.hline(4, 6, 20, "ink_hi")
    l.cells([(5, 19), (5, 18), (6, 17), (6, 16), (7, 15), (7, 14), (8, 13)], "ink_hi")
    l.cells([(9, 12), (10, 12)], "ink_hi")
    l.hline(10, 12, 13, "pot_hi")
    l.hline(9, 13, 14, "pot")
    l.set(13, 14, "pot_shadow")
    l.hline(10, 12, 15, "cream")  # el foco
    return l


def tray():
    t = Layer()
    t.cells([(14, 18), (15, 18), (16, 17), (17, 17)], "cream")  # papeles guardados
    t.cells([(15, 17)], "screen_hi")
    t.hline(13, 19, 19, "oak_hi")
    t.rect(13, 20, 19, 21, "oak")
    t.hline(14, 19, 21, "oak_shadow")
    t.set(13, 21, "oak_shadow")
    return t


def divider():
    d = Layer()
    d.rect(0, 7, 2, 21, "sage")
    d.vline(2, 7, 21, "sage_hi")
    d.vline(0, 7, 21, "sage_shadow")
    d.hline(0, 2, 7, "sage_hi")
    for y in range(9, 21, 3):  # costuras del panel de tela
        d.set(1, y, "sage_shadow")
    return d


def frame():
    """Foto de casa en la pared (trabajar desde casa)."""
    f = Layer()
    f.rect(3, 2, 11, 9, "oak")
    f.hline(3, 11, 2, "oak_hi")
    f.rect(4, 3, 10, 8, "day_top")
    f.hline(4, 10, 8, "leaf")  # pasto
    f.set(7, 3, "pot_hi")  # techo
    f.hline(6, 8, 4, "pot")
    f.hline(5, 9, 5, "pot")
    f.rect(5, 6, 9, 7, "cream")
    f.set(7, 7, "oak_shadow")  # puerta
    f.set(6, 6, "screen")  # ventana
    f.hline(3, 11, 9, "oak_shadow")
    return f


def sweater():
    s = Layer()
    s.set(15, 3, "ink_hi")  # gancho
    s.set(15, 4, "ink_hi")
    s.hline(13, 17, 5, "pot_hi")  # hombros
    s.rect(12, 6, 18, 7, "pot")
    s.rect(13, 8, 17, 10, "pot")
    s.cells([(12, 8), (18, 8), (12, 9), (18, 9)], "pot_shadow")  # mangas
    s.set(15, 6, "pot_shadow")  # cuello
    s.hline(13, 17, 11, "apricot")  # puño tejido
    s.set(17, 9, "pot_shadow")
    return s


def speaker():
    s = Layer()
    s.rect(47, 8, 49, 11, "ink")
    s.vline(47, 8, 11, "ink_hi")
    s.set(48, 9, "sage")
    s.set(48, 10, "sage_shadow")
    s.cells([(51, 8), (52, 9), (52, 10), (51, 11)], "sage")  # onda suave
    return s


def fan(blades):
    f = Layer()
    f.rect(54, 7, 56, 9, "ink_hi")
    if blades == 0:
        f.cells([(55, 7), (54, 8), (56, 8), (55, 9)], "screen")
    else:
        f.cells([(54, 7), (56, 7), (54, 9), (56, 9)], "screen")
    f.set(55, 8, "ink")
    f.vline(55, 10, 10, "ink")
    f.hline(54, 56, 11, "ink")
    return f


def succulent():
    s = Layer()
    s.cells([(58, 8), (60, 8)], "leaf_hi")
    s.cells([(59, 8), (58, 9), (59, 9), (60, 9)], "leaf")
    s.hline(58, 60, 10, "pot_hi")
    s.hline(58, 60, 11, "pot")
    return s


def mug():
    m = Layer()
    m.hline(46, 49, 18, "oak_shadow")  # té
    m.rect(46, 19, 49, 21, "cream")
    m.vline(49, 19, 21, "peach")
    m.cells([(50, 19), (51, 20), (50, 21)], "cream")  # asa
    return m


def steam(frame_index):
    s = Layer()
    pairs = [(47, 16), (48, 15), (47, 14), (48, 13)] if frame_index == 0 else [(48, 16), (47, 15), (48, 14), (47, 13)]
    s.cells(pairs[:2], "mist")
    s.cells(pairs[2:], "day_low")
    return s


def sign():
    """Tarjeta de "en concentración" sobre el escritorio."""
    s = Layer()
    s.hline(54, 57, 17, "cream")
    s.rect(53, 18, 58, 21, "cream")
    s.vline(58, 18, 21, "peach")
    s.hline(54, 56, 19, "wave")
    s.hline(54, 55, 20, "leaf_hi")
    return s


def phone():
    """Teléfono de pie con la luna de "no molestar"."""
    p = Layer()
    p.rect(60, 15, 62, 21, "ink")
    p.vline(60, 15, 21, "ink_hi")
    p.set(61, 17, "cream")
    p.set(62, 17, "dim_hi")
    p.set(61, 18, "cream")
    return p


def blinds():
    """Persiana a medio bajar sobre la ventana."""
    b = Layer()
    for y in range(ARCH_TOP, 10):
        for x in range(W):
            if in_arch(x, y):
                b.set(x, y, "blind" if y % 2 == 0 else "blind_shadow")
    b.vline(OX + 22, 10, 12, "blind_shadow")  # cordón
    return b


ITEMS = {
    "headphones": headphones,
    "lamp": lamp,
    "tray": tray,
    "divider": divider,
    "frame": frame,
    "sweater": sweater,
    "speaker": speaker,
    "fan": lambda: fan(0),
    "succulent": succulent,
    "mug": mug,
    "sign": sign,
    "phone": phone,
    "blinds": blinds,
}


# --- Salida ------------------------------------------------------------------------------

def render(layers):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    for layer in layers:
        for y in range(H):
            for x in range(W):
                key = layer.c[y][x]
                if key:
                    h = PALETTE[key].lstrip("#")
                    px[x, y] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
    return img


def save(img, path):
    img.resize((W * SCALE, H * SCALE), Image.NEAREST).save(path, optimize=True)


def main():
    repo = Path(__file__).resolve().parents[2]
    app = Path(sys.argv[1]) if len(sys.argv) > 1 else repo / "apps" / "mobile"
    out = app / "assets" / "scene"
    out.mkdir(parents=True, exist_ok=True)

    base = Layer()
    wall(base)
    shelf(base)
    desk(base)
    monitor_frame(base)

    files = {"base": [base], "plant": [plant(False)], "plantSway": [plant(True)]}
    for name in SKIES:
        files[f"sky-{name}"] = [sky(name)]
    for wave in WAVES:
        files[f"screen-{wave}"] = [screen(wave, False)]
        files[f"screen-dim-{wave}"] = [screen(wave, True)]
    boxes = {}
    for name, make in ITEMS.items():
        layer = make()
        files[f"item-{name}"] = [layer]
        boxes[name] = layer.box()
    files["steam-0"] = [steam(0)]
    files["steam-1"] = [steam(1)]
    files["fan-1"] = [fan(1)]

    for name, layers in files.items():
        save(render(layers), out / f"{name}.png")

    # La pantalla tenue es un objeto más: cambia la paleta del monitor en lugar de sumar una capa.
    boxes["screenDim"] = [OX + 7, 11, OX + 15, 16]

    req = lambda name: f"require('@/assets/scene/{name}.png')"  # noqa: E731
    lines = [
        "// Generado por docs/brand/draw_scene.py. No se edita a mano: se cambia el script y se vuelve a correr.",
        "",
        f"export const SCENE = {{ width: {W}, height: {H} }} as const;",
        "",
        "export const LAYERS = {",
        f"  base: {req('base')},",
        f"  plant: {req('plant')},",
        f"  plantSway: {req('plantSway')},",
        "  sky: {",
        *[f"    {name}: {req('sky-' + name)}," for name in SKIES],
        "  },",
        "  screen: {",
        *[f"    {wave}: {req('screen-' + wave)}," for wave in WAVES],
        "  },",
        "  screenDim: {",
        *[f"    {wave}: {req('screen-dim-' + wave)}," for wave in WAVES],
        "  },",
        f"  steam: [{req('steam-0')}, {req('steam-1')}],",
        f"  fanAlt: {req('fan-1')},",
        "} as const;",
        "",
        "/** Objetos que se ganan, con su caja en pixeles de la escena: [x0, y0, x1, y1]. */",
        "export const ITEMS = {",
        *[
            f"  {name}: {{ source: {req('item-' + name) if name != 'screenDim' else 'null'}, box: {boxes[name]} as const }},"
            for name in [*ITEMS, "screenDim"]
        ],
        "} as const;",
        "",
        "export type ItemId = keyof typeof ITEMS;",
        "export type Sky = keyof typeof LAYERS.sky;",
        "export type Wave = keyof typeof LAYERS.screen;",
        "",
    ]
    ts = app / "src" / "components" / "desk" / "layers.ts"
    ts.parent.mkdir(parents=True, exist_ok=True)
    ts.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    # Vista previa: vacía de día, completa de noche y completa al amanecer con la pantalla tenue.
    empty = render([sky("day"), screen("calm", False), base, plant(False)])
    full = [screen("calm", False), base, plant(False), *[ITEMS[n]() for n in ITEMS if n != "blinds"]]
    night = render([sky("night"), blinds(), *full, steam(0)])
    dawn = render([sky("dawn"), screen("noisy", True), base, plant(True), *[ITEMS[n]() for n in ITEMS], fan(1), steam(1)])
    sheet = Image.new("RGBA", (W * 8, H * 8 * 3 + 16), "#f4eee2")
    for i, img in enumerate([empty, night, dawn]):
        sheet.paste(img.resize((W * 8, H * 8), Image.NEAREST), (0, i * (H * 8 + 8)))
    sheet.save(Path(__file__).resolve().parent / "scene-preview.png")
    print(f"ok: {len(files)} capas -> {out}")


if __name__ == "__main__":
    main()
