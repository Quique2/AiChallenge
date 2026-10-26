# Pixel-art prompt brief — SpaceEase calm desk window

**Style mode:** hi-fi
**Subject:** scene (single-subject interior vignette, used as an app icon)
**Palette:** Quiet workspace (custom; not in the skill catalog — anchors below)

## Model-agnostic prompt (works in any generator)

```
[STYLE] hi-fi pixel art — crafted pixel work with sharp pixel edges,
deliberate hue shifts in shadow ramps (warm lights, cooler plum and
blue-green shadows), cluster studies with no orphan pixels, ordered
dithering only at sky and wall light transitions, clean block fills on
the desk objects; square app-icon composition, full-bleed, no border

[PALETTE] quiet workspace — deep teal wall #20494a (shadow #173a3d,
lit #2b5b58), window sky mint #d3e7df → cream #f7eedb → peach #f3d4b0
→ apricot #e9b58c, oak desk #bf7f4c (light #e0aa70, shadow #8f5440,
plum shade #5c3438), ink monitor #1f2c35, screen mint #c3e6d6, wave
teal #3f8a7b, sage leaves #4f8a55 (light #8db865), terracotta pot #c0643c

[SUBJECT] a calm, uncluttered desk in front of a tall arched window:
a small monitor whose screen shows a single soft wave that settles into
a flat line, and a potted snake plant; nothing else on the desk

[COMPOSITION] front elevation, eye-line at the desk top (lower third);
foreground: warm oak desk spanning the width; midground: monitor
left of centre and snake plant in a terracotta pot right of centre;
background: arched window centred, filled with a soft dawn sky, framed
by a deep teal wall; focal point: the monitor's calm wave

[LIGHTING] dawn, soft diffuse daylight from the window behind the desk,
gentle rim light on the monitor's top edge and the plant blades, light
spilling onto the wall around the arch and falling off toward the
corners; low contrast, no glare, no hard sun

[DENSITY] modern indie-density (Stardew Valley / Celeste aesthetic) —
chunky, legible pixels that still read at 60 px; ordered Bayer dither
only in the sky gradient and the wall glow; block fills on objects

[MOOD] calm, warm, quiet, welcoming, low-stimulus

[NEGATIVE] no anti-aliasing, no blur, no soft edges, no photo-real
textures, no 3D rendering, no JPEG artifacts, no text, no letters, no
signatures or watermarks, no living-artist style references, no orphan
pixels, no banding in large surfaces, no pure-lightness shadows without
hue shift, no clutter, no bright saturated accents, no lens flare
```

## Per-model variants (optional nudges)

### Imagen / Nano Banana (Gemini — the team has challenge credits)

Paste the universal block, and add to `[STYLE]` and `[NEGATIVE]`:
*"chunky pixel rendering, hard pixel edges, no AA, no smoothing"*.
Name the palette in plain words too: *"deep teal wall, dawn window of
mint, cream and peach, warm oak desk, sage-green plant, terracotta pot"*.

### OpenAI Image / DALL-E 3

Lead with *"pixel art with hard pixel edges, no anti-aliasing, no blur,
nearest-neighbor upscale aesthetic, every pixel clearly visible"*. Avoid
the word "illustration". Move the negatives into positive phrasing
(*"crisp pixel edges, no smoothing, no text"*).

## Post-process (required for a generated version)

Generated output is pseudo pixel art. Snap it to a real grid with the
fixed palette so the brand colours survive exactly:

```
python3 <pixel-art-2>/scripts/quantize.py generated.png --format png --grid 64 --scale 16 \
  --ramp "#173a3d,#20494a,#2b5b58,#d3e7df,#f7eedb,#f3d4b0,#e9b58c,#e0aa70,#bf7f4c,#8f5440,#5c3438,#1f2c35,#3a4f59,#e4f5ec,#c3e6d6,#3f8a7b,#8db865,#4f8a55,#2f5e4c,#e08a58,#c0643c,#8a3f34"
```

## Notes

- This prompt is model-agnostic; the per-model variants only add small phrasing nudges.
- Paste the `[NEGATIVE]` block verbatim into the generator's negative-prompt field where supported.
- Verify the output against the craft-marker checklist in `references/anti-patterns.md` (hi-fi needs at least 5 of 6 markers).
- The shipped icon is the hand-placed 32×32 version from `draw_icon.py`; use this brief only for a higher-density marketing variant.
