#!/usr/bin/env python3
"""
convert_svgs.py
Convert all env_*.svg files in cwbook_minimal_package to PNG (2400px width)
Copies a default env-top.png/env-bottom.png if missing (prefers dungeon, then city).
"""
import os
import glob
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PKG = ROOT / 'cwbook_minimal_package'
SVG_GLOB = str(PKG / '*.svg')
svgs = sorted(glob.glob(SVG_GLOB))

if not svgs:
    print('No SVG files found in', PKG)
    raise SystemExit(0)

print('Found SVGs:', [os.path.basename(s) for s in svgs])

converted = []
try:
    import cairosvg
    have_cairosvg = True
    print('Using cairosvg for conversion')
except Exception:
    have_cairosvg = False
    print('cairosvg not available')

if not have_cairosvg:
    try:
        from PIL import Image, ImageDraw
        have_pillow = True
        print('Using Pillow fallback for placeholders')
    except Exception:
        have_pillow = False
        print('Pillow not available')

for s in svgs:
    base = os.path.splitext(os.path.basename(s))[0]
    out = PKG / (base + '.png')
    try:
        if have_cairosvg:
            cairosvg.svg2png(url=s, write_to=str(out), output_width=2400)
            print('Converted', s, '->', out)
            converted.append(out)
        elif have_pillow:
            # create a tasteful placeholder gradient with simple silhouettes
            w, h = 2400, 240
            im = Image.new('RGB', (w, h), (220, 220, 220))
            draw = ImageDraw.Draw(im)
            name = base.lower()
            if 'dungeon' in name:
                top = (43, 42, 42); bottom = (20, 20, 20)
            elif 'city' in name:
                top = (232, 217, 196); bottom = (212, 196, 168)
            elif 'wasteland' in name:
                top = (225, 207, 184); bottom = (184, 154, 124)
            elif 'north' in name:
                top = (230, 240, 245); bottom = (192, 215, 230)
            else:
                top = (180, 180, 180); bottom = (120, 120, 120)
            for y in range(h):
                r = int(top[0] + (bottom[0] - top[0]) * (y / h))
                g = int(top[1] + (bottom[1] - top[1]) * (y / h))
                b = int(top[2] + (bottom[2] - top[2]) * (y / h))
                draw.line([(0, y), (w, y)], fill=(r, g, b))
            # simple silhouettes
            if 'dungeon' in name:
                for i in range(60, w, 240):
                    draw.polygon([(i, h - 20), (i + 60, h - 120), (i + 120, h - 20)], fill=(10, 10, 10))
            if 'city' in name:
                for i in range(40, w, 160):
                    draw.rectangle([i, h - 120, i + 40, h - 20], fill=(61, 48, 40))
            if 'wasteland' in name:
                draw.polygon([(0, h), (300, h - 40), (600, h), (900, h - 20), (w, h)], fill=(122, 92, 58))
            if 'north' in name:
                draw.polygon([(0, h), (150, h - 100), (300, h), (500, h - 20), (w, h)], fill=(80, 110, 140))
            im.save(out, dpi=(300,300))
            print('Wrote placeholder PNG', out)
            converted.append(out)
        else:
            print('No conversion tool available to create', out)
    except Exception as e:
        print('Failed to convert', s, '=>', e)

# ensure defaults
def copy_if_missing(src, dst):
    if src.exists() and not dst.exists():
        shutil.copy(src, dst)
        print('Copied default', src.name, '->', dst.name)

# prefer dungeon
dungeon_top = PKG / 'env_dungeon_top.png'
if dungeon_top.exists():
    copy_if_missing(dungeon_top, PKG / 'env-top.png')
    copy_if_missing(PKG / 'env_dungeon_bottom.png', PKG / 'env-bottom.png')
else:
    # pick first converted top as default
    tops = [p for p in converted if p.name.endswith('_top.png')]
    if tops:
        t = tops[0]
        copy_if_missing(t, PKG / 'env-top.png')
        b = Path(str(t).replace('_top.png', '_bottom.png'))
        copy_if_missing(b, PKG / 'env-bottom.png')

print('\nDone. Converted or created', len(converted), 'PNG files.')
