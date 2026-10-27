#!/usr/bin/env python3
"""Sonidos de la interfaz de SpaceEase: síntesis determinista, sin muestras de terceros.

Paleta sonora "Quiet workspace": marimba con fieltro en una escala pentatónica de Do (sin
intervalos tensos). Reglas (docs/DESIGN.md, sección 11; evidencia en docs/research/research_notes/
Retencion y experiencia opcional/notas.md):

- Cinco sonidos, de una o dos notas, solo para lo que la persona provoca o el fin de una espera.
- Fundamentales de 440 a 880 Hz. Al menos 20 dB menos de energía entre 2.5 y 5.5 kHz (la banda
  que más molesta) y nada por encima de 5 kHz.
- Ataque de 18 ms con curva coseno y caída larga: sin clics ni transitorios duros.
- Confirmar dura 0.4 s o menos; el resultado, 0.7 s o menos; nada pasa de 1 s.
- Mismo volumen percibido (RMS igualado, ±1 dB) y picos por debajo de -20 dBFS.

Uso: python make_sounds.py [carpeta]   (por defecto apps/mobile/assets/sounds)
Falla si algún sonido no cumple las reglas.
"""
import sys
import wave
from pathlib import Path

import numpy as np

SR = 22050  # todo el contenido está por debajo de 4 kHz

# Pentatónica de Do, de A4 a A5.
NOTE = {"A4": 440.00, "C5": 523.25, "D5": 587.33, "E5": 659.25, "G5": 783.99, "A5": 880.00}

ATTACK = 0.018
CUTOFF = 1800
TARGET_RMS_DB = -33.0


def envelope(n, attack, tau):
    t = np.arange(n) / SR
    env = np.exp(-t / tau)
    a = max(1, int(attack * SR))
    env[:a] *= 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a))
    return env


def mallet(freq, dur, tau):
    """Marimba con fieltro: fundamental y un segundo armónico suave que se apaga antes."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * freq * t) * envelope(n, ATTACK, tau)
    body += 0.12 * np.sin(2 * np.pi * 2 * freq * t) * envelope(n, ATTACK, tau * 0.6)
    return body


def blip(f0, f1, dur, glide):
    """Onda triangular (la más suave de las de 8 bits) que sube de f0 a f1: el sonido del pixel art."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    freq = np.where(t < glide, f0 + (f1 - f0) * t / glide, f1)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    tri = (2 / np.pi) * np.arcsin(np.sin(phase))
    return tri * envelope(n, ATTACK, dur / 2.5)


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


def rms_db(x):
    """RMS de la parte que suena (sin las colas casi mudas): una medida simple del volumen percibido."""
    active = x[np.abs(x) > np.max(np.abs(x)) * 0.05]
    return 20 * np.log10(np.sqrt(np.mean(active ** 2)))


def finish(x, cutoff=CUTOFF):
    x = lowpass(x, cutoff)
    fade = int(0.02 * SR)
    x[-fade:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, fade))
    x[0] = 0.0
    x[-1] = 0.0
    return x * 10 ** ((TARGET_RMS_DB - rms_db(x)) / 20)


SOUNDS = {
    # Aceptar un ajuste: dos notas que suben (quinta justa).
    "confirm": lambda: finish(
        sequence([(0, mallet(NOTE["C5"], 0.32, 0.08), 1.0), (0.08, mallet(NOTE["G5"], 0.32, 0.08), 0.8)], 0.4)
    ),
    # Terminaste una prueba, haya ayudado o no: el mismo sonido siempre (se premia la prueba, no el resultado).
    "result": lambda: finish(
        sequence([(0, mallet(NOTE["C5"], 0.5, 0.12), 1.0), (0.12, mallet(NOTE["E5"], 0.53, 0.13), 0.85)], 0.65)
    ),
    # Ya están las posibilidades de la foto y del sonido.
    "reveal": lambda: finish(
        sequence([(0, mallet(NOTE["D5"], 0.3, 0.08), 0.9), (0.07, mallet(NOTE["A5"], 0.35, 0.09), 0.6)], 0.42)
    ),
    # Empieza la escucha (suena antes de grabar, para no colarse en el análisis).
    "listenStart": lambda: finish(
        sequence([(0, mallet(NOTE["A4"], 0.25, 0.07), 1.0), (0.07, mallet(NOTE["D5"], 0.25, 0.08), 0.8)], 0.32)
    ),
    # Tocar la escena: un "blip" de 8 bits en onda triangular, muy filtrado.
    "pixel": lambda: finish(blip(NOTE["C5"], NOTE["G5"], 0.14, 0.04), cutoff=1500),
}

LIMITS = {"confirm": 0.4, "result": 0.7, "reveal": 0.7, "listenStart": 0.4, "pixel": 0.4}


def measure(x):
    spectrum = np.abs(np.fft.rfft(x)) ** 2
    freqs = np.fft.rfftfreq(len(x), 1 / SR)
    total = np.sum(spectrum)
    band = np.sum(spectrum[(freqs >= 2500) & (freqs <= 5500)]) / total
    high = np.sum(spectrum[freqs > 5000]) / total
    return {
        "dur": len(x) / SR,
        "peak": 20 * np.log10(np.max(np.abs(x))),
        "rms": rms_db(x),
        "band": 10 * np.log10(band + 1e-12),
        "high": 10 * np.log10(high + 1e-12),
    }


def main():
    root = Path(__file__).resolve().parents[2]
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "apps" / "mobile" / "assets" / "sounds"
    out.mkdir(parents=True, exist_ok=True)
    problems = []
    for name, make in SOUNDS.items():
        x = make()
        m = measure(x)
        print(
            f"{name:12s} {m['dur']:4.2f} s  pico {m['peak']:5.1f} dBFS  RMS {m['rms']:5.1f} dBFS"
            f"  2.5–5.5 kHz {m['band']:6.1f} dB  >5 kHz {m['high']:6.1f} dB"
        )
        if m["dur"] > LIMITS[name]:
            problems.append(f"{name}: dura {m['dur']:.2f} s (máx. {LIMITS[name]} s)")
        if m["peak"] > -20:
            problems.append(f"{name}: pico de {m['peak']:.1f} dBFS (máx. -20)")
        if abs(m["rms"] - TARGET_RMS_DB) > 1:
            problems.append(f"{name}: RMS {m['rms']:.1f} dBFS fuera de ±1 dB")
        if m["band"] > -20 or m["high"] > -40:
            problems.append(f"{name}: demasiada energía en agudos")
        pcm = np.round(np.clip(x, -1, 1) * 32767).astype("<i2")
        with wave.open(str(out / f"{name}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
    if problems:
        raise SystemExit("\n".join(problems))


if __name__ == "__main__":
    main()
