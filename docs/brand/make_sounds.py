#!/usr/bin/env python3
"""Sonidos de la interfaz de SpaceEase: síntesis determinista, sin muestras de terceros.

Paleta sonora "Quiet workspace": marimba con fieltro en una escala pentatónica de Do
(sin intervalos tensos). Reglas (docs/DESIGN.md, sección 11):

- Fundamentales entre 392 y 880 Hz; nada audible por encima de ~4 kHz (filtro paso bajo).
- Ataque de 6 a 10 ms con curva coseno: sin clics ni transitorios duros.
- Caída exponencial; ningún sonido pasa de 0.9 s.
- Picos de -27 a -24 dBFS en el archivo (nunca más de -20); la app puede bajarlos más.
- Solo momentos que la persona provoca o el fin de una espera: nada al navegar ni al elegir
  una opción (skill `ux-sound` de jal-co: lo frecuente con sonido cansa).

Uso: python make_sounds.py [carpeta]   (por defecto apps/mobile/assets/sounds)
"""
import sys
import wave
from pathlib import Path

import numpy as np

SR = 22050  # todo el contenido está por debajo de 4 kHz

# Pentatónica de Do: C4 G4 A4 C5 D5 E5 G5 A5 C6
NOTE = {
    "G4": 392.00, "A4": 440.00, "C5": 523.25, "D5": 587.33,
    "E5": 659.25, "G5": 783.99, "A5": 880.00, "C6": 1046.50,
}


def envelope(n, attack, tau):
    t = np.arange(n) / SR
    env = np.exp(-t / tau)
    a = max(1, int(attack * SR))
    env[:a] *= 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a))
    return env


def mallet(freq, dur, tau, attack=0.008, overtone=0.07):
    """Marimba con fieltro: fundamental + un armónico suave y el sobretono de 4x que se apaga rápido."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * freq * t) * envelope(n, attack, tau)
    body += 0.12 * np.sin(2 * np.pi * 2 * freq * t) * envelope(n, attack, tau * 0.6)
    body += overtone * np.sin(2 * np.pi * 4 * freq * t) * envelope(n, attack, tau * 0.18)
    return body


def blip(f0, f1, dur, glide):
    """Onda triangular (la más suave de las de 8 bits) que sube de f0 a f1: el sonido del pixel art."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    freq = np.where(t < glide, f0 + (f1 - f0) * t / glide, f1)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    tri = (2 / np.pi) * np.arcsin(np.sin(phase))
    return tri * envelope(n, 0.006, dur / 3)


def lowpass(x, cutoff):
    """Dos polos en cascada (12 dB/oct): quita brillo sin colorear el cuerpo del sonido."""
    a = np.exp(-2 * np.pi * cutoff / SR)
    for _ in range(2):
        y = np.empty_like(x)
        acc = 0.0
        for i, v in enumerate(x):
            acc = (1 - a) * v + a * acc
            y[i] = acc
        x = y
    return x


def sequence(events, dur):
    """events: (inicio en s, señal, ganancia)."""
    out = np.zeros(int(dur * SR))
    for start, signal, gain in events:
        i = int(start * SR)
        j = min(len(out), i + len(signal))
        out[i:j] += gain * signal[: j - i]
    return out


def finish(x, peak_db, cutoff=3200):
    x = lowpass(x, cutoff)
    fade = int(0.015 * SR)
    x[-fade:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, fade))
    x[0] = 0.0
    x[-1] = 0.0
    return x / np.max(np.abs(x)) * 10 ** (peak_db / 20)


SOUNDS = {
    # Aceptar un ajuste: dos notas que suben (quinta justa).
    "confirm": lambda: finish(
        sequence([(0, mallet(NOTE["C5"], 0.3, 0.08), 1.0), (0.08, mallet(NOTE["G5"], 0.3, 0.09), 0.8)], 0.4),
        -25,
    ),
    # Algo ayudó y llega a tu escritorio: arpegio corto y cálido.
    "success": lambda: finish(
        sequence(
            [
                (0.00, mallet(NOTE["C5"], 0.5, 0.11), 1.0),
                (0.09, mallet(NOTE["E5"], 0.5, 0.11), 0.85),
                (0.18, mallet(NOTE["G5"], 0.6, 0.14), 0.8),
                (0.30, mallet(NOTE["C6"], 0.6, 0.22, overtone=0.02), 0.3),
            ],
            0.9,
        ),
        -24,
    ),
    # Ya están las posibilidades de la foto y del sonido.
    "reveal": lambda: finish(
        sequence([(0, mallet(NOTE["D5"], 0.3, 0.08), 0.9), (0.07, mallet(NOTE["A5"], 0.35, 0.1), 0.6)], 0.42),
        -26,
    ),
    # Empieza y termina la escucha: subir para empezar, bajar para terminar.
    "listenStart": lambda: finish(
        sequence([(0, mallet(NOTE["G4"], 0.25, 0.07), 1.0), (0.07, mallet(NOTE["C5"], 0.25, 0.08), 0.8)], 0.3),
        -25,
    ),
    "listenEnd": lambda: finish(
        sequence([(0, mallet(NOTE["C5"], 0.25, 0.07), 0.8), (0.07, mallet(NOTE["G4"], 0.3, 0.09), 1.0)], 0.34),
        -25,
    ),
    # Tocar la escena o ver aparecer un objeto: un "blip" de 8 bits, filtrado y bajito.
    "pixel": lambda: finish(blip(NOTE["C5"], NOTE["G5"], 0.12, 0.04), -27, cutoff=2200),
}


def describe(x):
    spectrum = np.abs(np.fft.rfft(x))
    freqs = np.fft.rfftfreq(len(x), 1 / SR)
    centroid = float(np.sum(freqs * spectrum) / np.sum(spectrum))
    above = float(np.sum(spectrum[freqs > 4000] ** 2) / np.sum(spectrum ** 2))
    peak = 20 * np.log10(np.max(np.abs(x)))
    return f"{len(x) / SR:4.2f} s  pico {peak:5.1f} dBFS  centroide {centroid:6.0f} Hz  >4 kHz {above:.4%}"


def main():
    root = Path(__file__).resolve().parents[2]
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "apps" / "mobile" / "assets" / "sounds"
    out.mkdir(parents=True, exist_ok=True)
    for name, make in SOUNDS.items():
        x = make()
        pcm = np.round(np.clip(x, -1, 1) * 32767).astype("<i2")
        with wave.open(str(out / f"{name}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
        print(f"{name:12s} {describe(x)}")


if __name__ == "__main__":
    main()
