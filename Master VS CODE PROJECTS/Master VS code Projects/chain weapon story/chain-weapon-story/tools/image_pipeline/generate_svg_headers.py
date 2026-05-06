"""
Generate 16 SVG header/banner images (2400x400 viewBox) plus 1200x200 previews.
Groups: A=Vector-flat, B=Painterly, C=Atmospheric, D=Textured-grit
Outputs to: outputs/headers_svg/
"""
import os, random, json

OUT_DIR = os.path.join("outputs", "headers_svg")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 2400, 400

STYLE_GROUPS = [
    ("A", "Vector-flat"),
    ("B", "Painterly"),
    ("C", "Atmospheric"),
    ("D", "Textured-grit"),
]

TITLES = {
    "A": ["Dawn Ridges — Warm",    "Noon Plains — Ochre",  "Dusk Ridges — Amber",  "Night Ridge — Dark"],
    "B": ["Brushed Dawn — Soft",   "Bloom Noon — Hazy",    "Wash Dusk — Violet",   "Inked Night — Deep"],
    "C": ["Frost Ridge — Snow",    "Fog Dawn — Pale",      "Haze Clear — Teal",    "Starry Dusk — Indigo"],
    "D": ["Grit Dawn — Worn",      "Paper Noon — Aged",    "Grain Dusk — Faded",   "Scratch Night — Dark"],
}

# 4 palettes per group (5 hex colors, light→dark)
PALETTES = {
    "A": [
        ["#EDE6D9", "#C4A875", "#9B8268", "#7A5A44", "#3A2820"],
        ["#F0E8D2", "#D4A860", "#A07040", "#6B4020", "#2A1408"],
        ["#D8C8BC", "#B09080", "#846050", "#5A3828", "#281408"],
        ["#D0D8E4", "#8090A8", "#485870", "#283040", "#101828"],
    ],
    "B": [
        ["#F4E8D8", "#D4A878", "#A07050", "#704030", "#301808"],
        ["#D0E8F4", "#88B8D8", "#5088B8", "#305878", "#102038"],
        ["#D4F0E0", "#88C8A0", "#508868", "#305840", "#102818"],
        ["#E8D0F4", "#C088D8", "#905898", "#583068", "#201028"],
    ],
    "C": [
        ["#F4F8FC", "#C8DCF0", "#78A8CC", "#3868A0", "#182848"],
        ["#F8F0E0", "#E0C898", "#A88858", "#686040", "#282818"],
        ["#D8F0E8", "#90C8B0", "#488878", "#285858", "#102828"],
        ["#181C28", "#283C60", "#5878B0", "#98B0D8", "#E0E8F8"],
    ],
    "D": [
        ["#F0E4D4", "#C8A888", "#987860", "#685040", "#281808"],
        ["#E0F0D8", "#A8C8A0", "#708870", "#485850", "#182018"],
        ["#E8DCD0", "#C0A090", "#907068", "#604850", "#201818"],
        ["#302828", "#504848", "#807070", "#B0A0A0", "#E0D8D8"],
    ],
}

DESCRIPTIONS = {
    "A": [
        "Clean warm dawn with flat ochre ridges and sharp pine silhouettes in pure geometric style.",
        "Bright amber midday with bold flat-colour layered hills, crisp and minimal.",
        "Warm amber dusk with deep-shadowed flat ridges and stylised tree silhouettes.",
        "Cool dark night with minimal flat shapes, crescent moon, and star dots.",
    ],
    "B": [
        "Soft painterly dawn with warm washes and subtly blurred pine shapes.",
        "Hazy noon with gentle colour bloom and loose, blurred brushwork layers.",
        "Violet dusk with painterly gradients and radial vignette glow.",
        "Deep inky night with dark painterly washes and faint warm glow.",
    ],
    "C": [
        "Snowy frost twilight with icy ridges, turbulence-displaced fog, and misty pines.",
        "Foggy pale dawn with soft diffused warmth and hazy layered silhouettes.",
        "Hazy teal clear day with atmospheric depth and moisture-blur feel.",
        "Starry indigo dusk with deep rich sky, turbulence fog, and pinprick stars.",
    ],
    "D": [
        "Gritty worn dawn with fractal-noise grain, displaced ridges, and earthy palette.",
        "Aged paper noon with vintage fractal grain and faint edge displacement.",
        "Faded grain dusk with soft film-grain warmth and displaced tree silhouettes.",
        "Dark scratched night with heavy grain overlay and ink-like displaced forms.",
    ],
}

TAGS = {
    "A": [["dawn","warm","flat","geometric"], ["noon","ochre","clean","minimal"],
          ["dusk","amber","crisp","flat"],    ["night","dark","silhouette","cool"]],
    "B": [["dawn","soft","painterly","warm"], ["noon","bloom","hazy","brushy"],
          ["dusk","violet","gradient","glow"], ["night","deep","inky","painterly"]],
    "C": [["frost","snow","icy","atmospheric"], ["fog","pale","diffused","dawn"],
          ["haze","teal","deep","clear"],       ["stars","indigo","dusk","night"]],
    "D": [["grit","worn","grain","dawn"],  ["aged","paper","sepia","noon"],
          ["faded","grain","film","dusk"], ["dark","scratch","ink","night"]],
}

PROMPTS_SD = {
    "A": [
        "vector flat layered pine ridge silhouette banner 2400x400, warm dawn palette, sharp flat geometric shapes, no texture",
        "vector flat layered hill banner, bold ochre-amber palette, crisp minimal shapes, noon light, no gradient",
        "vector flat dusk ridge banner, amber-brown flat palette, strong contrast, pine tree silhouettes",
        "vector flat night ridge header, cool dark palette, crescent moon, flat star dots, minimal",
    ],
    "B": [
        "painterly soft brushwork pine ridge banner 2400x400, warm dawn palette, gaussian blur, watercolour wash",
        "painterly blue-teal ridge banner, gradient sky, colour bloom noon, blurred pine trees, horizontal strip",
        "painterly violet dusk header, gradient background, pine ridge silhouette, radial vignette glow",
        "painterly deep night ridge banner, dark washes, subtle warm glow, ink-watercolour feel",
    ],
    "C": [
        "atmospheric snowy frost ridge banner 2400x400, icy palette, turbulence fog layer, pine silhouettes, misty",
        "atmospheric foggy pale dawn ridge header, diffused warm light, hazy silhouettes, muted tones",
        "atmospheric hazy teal clear day ridge banner, layered atmospheric depth, moisture blur, pine silhouettes",
        "atmospheric starry indigo night ridge header, deep sky, fractal fog, pinprick stars",
    ],
    "D": [
        "textured gritty dawn ridge banner 2400x400, fractal grain overlay, earthy palette, displaced edges, pines",
        "textured aged paper noon ridge header, fractal grain vintage tone, faint edge displacement",
        "textured faded grain dusk ridge banner, film grain, displaced pines, worn warm tones",
        "textured dark grain night ridge banner, heavy fractal grain, ink-like displaced silhouette",
    ],
}

# ── helpers ──────────────────────────────────────────────────────────────────

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(
        max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
    )

def darken(h, f=0.72):
    r, g, b = hex_to_rgb(h)
    return rgb_to_hex(int(r*f), int(g*f), int(b*f))

def lighten(h, f=1.28):
    r, g, b = hex_to_rgb(h)
    return rgb_to_hex(int(r*f), int(g*f), int(b*f))

def pts(poly):
    return " ".join(f"{int(x)},{int(y)}" for x, y in poly)

def make_ridge(base_y, amp, n, w, h):
    xs = [int(i * w / (n - 1)) for i in range(n)]
    ys = [base_y + random.uniform(-amp, amp) for _ in xs]
    poly = [(0, h)] + list(zip(xs, ys)) + [(w, h)]
    return poly, list(zip(xs, ys))

def interp_y(ridge, tx):
    if tx <= ridge[0][0]:
        return ridge[0][1]
    for i in range(len(ridge) - 1):
        x0, y0 = ridge[i]; x1, y1 = ridge[i+1]
        if x0 <= tx <= x1:
            t = (tx - x0) / max(1, x1 - x0)
            return y0 * (1 - t) + y1 * t
    return ridge[-1][1]

def pine(cx, cy, th, tw):
    return f"{int(cx)},{int(cy-th)} {int(cx-tw)},{int(cy)} {int(cx+tw)},{int(cy)}"

# ── SVG builder ───────────────────────────────────────────────────────────────

def build_svg(idx, gc, pal, title, tags, w=W, h=H):
    seed = 10000 + idx
    random.seed(seed)

    defs   = []   # strings for <defs> block
    body   = []   # strings for SVG body (before optional wrappers)
    after  = []   # overlays drawn on top after main body

    # unique filter IDs
    bg_id    = f"bg{idx}"
    blur_id  = f"bl{idx}"
    fog_id   = f"fg{idx}"
    grain_id = f"gr{idx}"
    disp_id  = f"dp{idx}"
    vig_id   = f"vg{idx}"
    fog_disp_id = f"fd{idx}"

    # ── background ──
    if gc == "A":
        body.append(f'<rect width="{w}" height="{h}" fill="{pal[0]}"/>')
    else:
        c0 = lighten(pal[0], 1.14)
        cm = pal[len(pal) // 2]
        c1 = darken(pal[-1], 0.86)
        defs.append(
            f'<linearGradient id="{bg_id}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{c0}"/>'
            f'<stop offset="55%" stop-color="{cm}"/>'
            f'<stop offset="100%" stop-color="{c1}"/>'
            f'</linearGradient>'
        )
        body.append(f'<rect width="{w}" height="{h}" fill="url(#{bg_id})"/>')

    # ── style filters ──
    if gc == "B":
        defs.append(
            f'<filter id="{blur_id}" x="-3%" y="-3%" width="106%" height="106%">'
            f'<feGaussianBlur stdDeviation="2.4"/>'
            f'</filter>'
        )

    if gc == "C":
        # fog = turbulence-displaced white rect overlay
        defs.append(
            f'<filter id="{fog_disp_id}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.010 0.020" '
            f'numOctaves="4" seed="{seed}" result="nz"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="nz" scale="60" '
            f'xChannelSelector="R" yChannelSelector="G"/>'
            f'</filter>'
        )

    if gc == "D":
        # grain: applied to a wrapper group containing all body elements
        defs.append(
            f'<filter id="{grain_id}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.68" numOctaves="3" '
            f'stitchTiles="stitch" seed="{seed}" result="nz"/>'
            f'<feColorMatrix type="saturate" values="0" in="nz" result="gnz"/>'
            f'<feBlend in="SourceGraphic" in2="gnz" mode="soft-light"/>'
            f'</filter>'
        )
        # displacement for ridge rough edges
        defs.append(
            f'<filter id="{disp_id}">'
            f'<feTurbulence type="turbulence" baseFrequency="0.020" numOctaves="2" '
            f'seed="{seed+7}" result="dn"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="dn" scale="6" '
            f'xChannelSelector="R" yChannelSelector="G"/>'
            f'</filter>'
        )

    # vignette for B and C
    if gc in ("B", "C"):
        ec = darken(pal[-1], 0.62)
        defs.append(
            f'<radialGradient id="{vig_id}" cx="50%" cy="50%" r="74%">'
            f'<stop offset="0%" stop-color="transparent"/>'
            f'<stop offset="100%" stop-color="{ec}" stop-opacity="0.30"/>'
            f'</radialGradient>'
        )

    # ── sun / moon ──
    if random.random() < 0.55:
        cx = random.randint(int(w * 0.10), int(w * 0.90))
        cy = random.randint(int(h * 0.07), int(h * 0.42))
        r  = random.randint(20, 62)
        night = (idx - 1) % 4 == 3
        if gc == "A" and night:
            # crescent moon: two overlapping circles
            mc = lighten(pal[2], 1.6)
            body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{mc}"/>')
            body.append(f'<circle cx="{cx + r//3}" cy="{cy - r//4}" '
                        f'r="{int(r*0.84)}" fill="{pal[0]}"/>')
        else:
            sc = lighten(pal[0], 1.45)
            body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{sc}" opacity="0.74"/>')

    # ── stars ──
    if (gc == "C" and (idx-1)%4 == 3) or (gc == "A" and (idx-1)%4 == 3):
        sc = "#E8EEFF" if gc == "C" else lighten(pal[2], 2.4)
        stars = []
        for _ in range(random.randint(55, 130)):
            sx  = random.randint(0, w)
            sy  = random.randint(0, int(h * 0.44))
            sr  = random.choice([1, 1, 1, 2])
            sop = f"{random.uniform(0.42, 1.0):.2f}"
            stars.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" '
                         f'fill="{sc}" opacity="{sop}"/>')
        body.append(f'<g id="stars{idx}">' + "".join(stars) + "</g>")

    # ── ridges ──
    n_layers  = random.randint(4, 7)
    top_ridge = None
    ridge_elems = []

    for li in range(n_layers):
        depth  = li / max(1, n_layers - 1)
        base_y = int(h * (0.16 + 0.70 * (1 - depth)))
        amp    = int(h * (0.022 + 0.062 * (1 - depth)))
        poly, ridge_top = make_ridge(base_y, amp, 18, w, h)
        if li == n_layers - 1:
            top_ridge = ridge_top
        ci = li % len(pal)
        c  = pal[ci]

        if gc == "B":
            ridge_elems.append(
                f'<polygon points="{pts(poly)}" fill="{c}" opacity="0.93"/>'
            )
        elif gc == "D":
            ridge_elems.append(
                f'<polygon points="{pts(poly)}" fill="{c}" filter="url(#{disp_id})"/>'
            )
        else:
            ridge_elems.append(f'<polygon points="{pts(poly)}" fill="{c}"/>')

    # group B: blur the ridges
    if gc == "B":
        body.append(f'<g filter="url(#{blur_id})">'
                    + "".join(ridge_elems) + "</g>")
    else:
        body.extend(ridge_elems)

    # ── pine trees ──
    if top_ridge:
        n_trees  = random.randint(16, 48)
        tree_col = darken(pal[-1], 0.46)
        tree_elems = []
        for _ in range(n_trees):
            tx = random.randint(0, w)
            ty = int(interp_y(top_ridge, tx))
            th = random.randint(int(h * 0.038), int(h * 0.10))
            tw = max(4, th // 3)
            tree_elems.append(
                f'<polygon points="{pine(tx, ty, th, tw)}" fill="{tree_col}"/>'
            )
        if gc == "B":
            body.append(f'<g filter="url(#{blur_id})" opacity="0.88">'
                        + "".join(tree_elems) + "</g>")
        else:
            body.append('<g id="trees">' + "".join(tree_elems) + "</g>")

    # ── overlays ──
    if gc == "C":
        fog_col = lighten(pal[0], 1.05)
        after.append(
            f'<rect width="{w}" height="{h}" fill="{fog_col}" '
            f'filter="url(#{fog_disp_id})" opacity="0.28"/>'
        )

    if gc in ("B", "C"):
        after.append(f'<rect width="{w}" height="{h}" fill="url(#{vig_id})"/>')

    # ── assemble ──
    defs_block = (
        "\n  <defs>\n    " + "\n    ".join(defs) + "\n  </defs>"
        if defs else ""
    )

    if gc == "D":
        # wrap EVERYTHING in grain filter group
        all_body = "\n  ".join(body + after)
        inner = f'<g filter="url(#{grain_id})">\n  {all_body}\n</g>'
    else:
        inner = "\n  ".join(body + after)

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'shape-rendering="geometricPrecision">\n'
        f'  <!-- {title} | Group {gc} | {", ".join(tags)} -->'
        f'{defs_block}\n'
        f'  {inner}\n'
        f'</svg>'
    )


# ── generate all 16 ──────────────────────────────────────────────────────────

meta = []

for idx in range(1, 17):
    gi = (idx - 1) // 4
    vi = (idx - 1) % 4
    gc, gn = STYLE_GROUPS[gi]
    pal    = PALETTES[gc][vi]
    title  = TITLES[gc][vi]
    desc   = DESCRIPTIONS[gc][vi]
    tags   = TAGS[gc][vi]
    repro  = PROMPTS_SD[gc][vi]

    svg_full    = build_svg(idx, gc, pal, title, tags, w=W, h=H)
    svg_preview = svg_full.replace(
        f'width="{W}" height="{H}"',
        f'width="{W//2}" height="{H//2}"'
    )

    fp = os.path.join(OUT_DIR, f"{idx:02d}.svg")
    pp = os.path.join(OUT_DIR, f"{idx:02d}_preview.svg")

    with open(fp, "w", encoding="utf-8") as f:
        f.write(svg_full)
    with open(pp, "w", encoding="utf-8") as f:
        f.write(svg_preview)

    meta.append({
        "id":                    f"{idx:02d}",
        "title":                 title,
        "style_group":           gc,
        "group_name":            gn,
        "palette":               pal,
        "short_description":     desc,
        "reproduction_prompt":   repro,
        "suggested_settings": {
            "model":             "SDXL",
            "mode":              "img2img",
            "denoising_strength": 0.45 if gc in ("A", "B") else 0.55,
            "sampler":           "Euler a",
            "steps":             28,
            "guidance_scale":    7.5,
            "seed":              10000 + idx,
        },
        "upscaler_recommendation": "Real-ESRGAN x4",
        "thumbnail":             os.path.basename(pp),
        "final_image":           os.path.basename(fp),
        "tags":                  tags,
    })

with open(os.path.join(OUT_DIR, "metadata.json"), "w", encoding="utf-8") as mf:
    json.dump(meta, mf, indent=2)

print(f"Generated {len(meta)} SVG headers in {OUT_DIR}")
print(f"Files: {', '.join(os.listdir(OUT_DIR))}")
