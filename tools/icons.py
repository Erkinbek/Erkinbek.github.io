#!/usr/bin/env python3
"""Draws the site mark: favicon.svg, favicon.ico (16/32/48) and apple-touch-icon.png.

    python tools/icons.py

The mark is an "E" built from three bars, in the colours of the BigText logo, so the
hostname-wide favicon Google shows next to every erkinbek.github.io result fits all projects.
Needs Pillow.
"""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
BG = "#0f172a"
TEAL = "#2dd4bf"
# On a 512 grid: the stem, then the three arms (x0, y0, y1, x1, colour). The middle arm starts
# at the stem's edge so its colour does not cut the stem in two.
STEM_BOX = (120, 96, 204, 416)
ARMS = [(120, 96, 176, 392, TEAL), (204, 216, 296, 340, "#f59e0b"), (120, 336, 416, 392, TEAL)]


def svg():
    x0, y0, x1, y1 = STEM_BOX
    parts = [f'<rect width="512" height="512" rx="112" fill="{BG}"/>',
             f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="18" fill="{TEAL}"/>']
    for ax0, a0, a1, ax1, colour in ARMS:
        parts.append(f'<rect x="{ax0}" y="{a0}" width="{ax1 - ax0}" height="{a1 - a0}" rx="18" fill="{colour}"/>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">' + "".join(parts) + "</svg>\n"


def png(size):
    # Drawn at 8x and scaled down, so small sizes stay sharp enough without hand hinting.
    big = size * 8
    k = big / 512
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, big - 1, big - 1], radius=112 * k, fill=BG)
    x0, y0, x1, y1 = STEM_BOX
    d.rounded_rectangle([x0 * k, y0 * k, x1 * k, y1 * k], radius=18 * k, fill=TEAL)
    for ax0, a0, a1, ax1, colour in ARMS:
        d.rounded_rectangle([ax0 * k, a0 * k, ax1 * k, a1 * k], radius=18 * k, fill=colour)
    return im.resize((size, size), Image.LANCZOS)


def main():
    (ROOT / "favicon.svg").write_text(svg(), encoding="utf-8", newline="\n")
    png(48).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    png(180).save(ROOT / "apple-touch-icon.png", optimize=True)
    print("icons written to", ROOT)


if __name__ == "__main__":
    main()
