#!/usr/bin/env python3
import os, sys, glob

SVG_DIR = os.path.join("outputs","headers_svg")
OUT_DIR = os.path.join("outputs","headers_png")
os.makedirs(OUT_DIR, exist_ok=True)

try:
    from cairosvg import svg2png
except Exception as e:
    print("CAIROSVG_IMPORT_ERROR:" + str(e))
    sys.exit(2)

svgs = sorted(glob.glob(os.path.join(SVG_DIR, "*.svg")))
if not svgs:
    print("NO_SVGS_FOUND")
    sys.exit(3)

converted = []
failed = []
for svg in svgs:
    base = os.path.basename(svg)
    name = os.path.splitext(base)[0]
    if name.endswith("_preview"):
        w, h = 1200, 200
    else:
        w, h = 2400, 400
    out = os.path.join(OUT_DIR, name + ".png")
    try:
        svg2png(url=svg, write_to=out, output_width=w, output_height=h)
        converted.append(out)
    except Exception as e:
        failed.append((svg, str(e)))

print("CONVERTED:", len(converted))
if failed:
    print("FAILED:", len(failed))
    for s, e in failed[:10]:
        print("FAIL:", s, e)
    sys.exit(1)

sys.exit(0)
