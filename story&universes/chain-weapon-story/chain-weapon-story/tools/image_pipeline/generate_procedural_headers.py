"""
Generate 16 procedural header/banner images (2400x400) plus 1200x200 previews.
Saves PNGs to outputs/headers/ and writes metadata JSON.
Designed as a deterministic placeholder for the AI-generated headers.
"""
import os, random, json
from math import floor
from PIL import Image, ImageDraw, ImageFilter, ImageOps

OUT_DIR = os.path.join("outputs","headers")
os.makedirs(OUT_DIR, exist_ok=True)

WIDTH, HEIGHT = 2400, 400
PREVIEW_W, PREVIEW_H = 1200, 200

STYLE_GROUPS = [("A","Vector-flat"),("B","Painterly"),("C","Atmospheric"),("D","Textured")]

PALETTES = {
    'A': [['#7A5A44','#9B8268','#EDE6D9'],['#6B4F3E','#A07F6D','#DDCFC1'],['#5A3E2F','#8A6B5A','#CFC0B6'],['#3E2A21','#6E5449','#BFAFA2']],
    'B': [['#8F6B4B','#B39174','#E6D9CC'],['#4B6B8F','#7693B3','#D9E6F0'],['#7D9A72','#B7D3B0','#EAF6E7'],['#6B4B8F','#9A74B3','#E6D9F0']],
    'C': [['#4B6B6B','#7AA1A1','#D9EFEF'],['#2B2B3B','#6B6B8F','#D9D9F0'],['#7A5A44','#9B8268','#EDE6D9'],['#17202A','#2B4150','#9ABFD0']],
    'D': [['#6B5B4B','#9F8F7F','#E6DED4'],['#5B6B5B','#8F9F8F','#E6EFE6'],['#4B3B2B','#7B6755','#D4C8BD'],['#3B3B3B','#6B6B6B','#CFCFCF']]
}

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def vertical_gradient(w,h,top_color,bottom_color):
    top = Image.new('RGB',(w,h), top_color)
    bottom = Image.new('RGB',(w,h), bottom_color)
    mask = Image.new('L',(w,h))
    for y in range(h):
        v = int(255 * (y / max(1, h-1)))
        mask.paste(v, box=(0,y,w,y+1))
    return Image.composite(top,bottom,mask)

def ridge_polygon(base_y, amplitude, points=14):
    xs = [int(i * WIDTH / (points-1)) for i in range(points)]
    ys = [base_y + random.uniform(-amplitude, amplitude) for _ in xs]
    poly = [(0,HEIGHT)] + list(zip(xs, ys)) + [(WIDTH, HEIGHT)]
    return poly, list(zip(xs, ys))

def interp_y(points, x):
    if x <= points[0][0]:
        return points[0][1]
    for i in range(len(points)-1):
        x0,y0 = points[i]
        x1,y1 = points[i+1]
        if x0 <= x <= x1:
            t = (x - x0) / max(1, (x1-x0))
            return y0*(1-t) + y1*t
    return points[-1][1]

meta = []

# Try to read reproduction prompts if present
prompts = []
prompts_path = os.path.join('tools','image_pipeline','prompts_48.txt')
if os.path.exists(prompts_path):
    with open(prompts_path, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f if line.strip()]

for idx in range(1,17):
    group_idx = (idx-1)//4
    variant_idx = (idx-1)%4
    group_code, group_name = STYLE_GROUPS[group_idx]
    palette_hex = PALETTES[group_code][variant_idx]
    palette_rgb = [hex_to_rgb(h) for h in palette_hex]

    seed = 10000 + idx
    random.seed(seed)

    # background gradient
    bg = vertical_gradient(WIDTH, HEIGHT, palette_rgb[0], palette_rgb[-1])
    img = bg.copy()
    draw = ImageDraw.Draw(img)

    # layers (back-to-front)
    layers = random.randint(4,7)
    for layer_i in range(layers):
        depth = layer_i / max(1, layers-1)
        base_y = int(HEIGHT * (0.2 + 0.65 * (1 - depth)))
        amplitude = int(HEIGHT * (0.03 + 0.07 * (1 - depth)))
        poly, ridge_points = ridge_polygon(base_y, amplitude, points=14)
        color = palette_rgb[layer_i % len(palette_rgb)]
        draw.polygon(poly, fill=color)

    # draw small pine silhouettes on top-most ridge
    top_poly, top_points = ridge_polygon(int(HEIGHT*0.45), 10, points=24)
    num_trees = random.randint(12,40)
    for _ in range(num_trees):
        x = random.randint(0, WIDTH)
        y = int(interp_y(top_points, x))
        h = random.randint(14, int(HEIGHT*0.08))
        w = max(3, h//3)
        # simple triangle tree
        tree_color = (10,10,10)
        draw.polygon([(x, y-h), (x-w, y), (x+w, y)], fill=tree_color)

    # optional sun/moon
    if random.random() < 0.45:
        cx = random.randint(int(WIDTH*0.1), int(WIDTH*0.9))
        cy = random.randint(int(HEIGHT*0.1), int(HEIGHT*0.6))
        r = random.randint(30,90)
        sun_col = tuple(min(255, c+40) for c in palette_rgb[0])
        overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.ellipse((cx-r, cy-r, cx+r, cy+r), fill=sun_col+(40,))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

    # style-specific tweaks
    if group_code == 'B':  # painterly
        img = img.filter(ImageFilter.GaussianBlur(radius=1.4))
        # slight color wash
        wash = Image.new('RGB', (WIDTH, HEIGHT), palette_rgb[-1])
        img = Image.blend(img, wash, alpha=0.08)

    if group_code == 'C':  # atmospheric
        # fog overlay using random noise
        noise = Image.frombytes('L', (WIDTH, HEIGHT), os.urandom(WIDTH*HEIGHT))
        noise = noise.filter(ImageFilter.GaussianBlur(radius=6))
        fog = Image.new('RGB', (WIDTH, HEIGHT), (220,220,220))
        fog = Image.composite(fog, img, noise.point(lambda p: max(0, min(255, int(p*0.6)))))
        img = Image.blend(img, fog, alpha=0.25)
        # occasional stars for dusk/night
        if random.random() < 0.35:
            draw = ImageDraw.Draw(img)
            for _ in range(random.randint(30,120)):
                sx = random.randint(0, WIDTH-1)
                sy = random.randint(0, int(HEIGHT*0.5))
                r = random.choice([0,1,2])
                draw.ellipse((sx-r, sy-r, sx+r, sy+r), fill=(240,240,240))

    if group_code == 'D':  # textured
        grain = Image.frombytes('L', (WIDTH, HEIGHT), os.urandom(WIDTH*HEIGHT))
        grain = grain.point(lambda p: int(p*0.7))
        grain = grain.filter(ImageFilter.GaussianBlur(radius=0.5))
        grain_rgb = Image.merge('RGB', (grain,grain,grain))
        img = Image.blend(img, grain_rgb, alpha=0.06)

    # final small contrast tweak
    img = ImageOps.autocontrast(img, cutoff=1)

    # save final and preview
    final_path = os.path.join(OUT_DIR, f"{idx:02d}.png")
    preview_path = os.path.join(OUT_DIR, f"{idx:02d}_preview.png")
    img.save(final_path, format='PNG', optimize=True)
    preview = img.resize((PREVIEW_W, PREVIEW_H), Image.LANCZOS)
    preview.save(preview_path, format='PNG', optimize=True)

    # metadata entry
    title = f"{group_name} {variant_idx+1}"
    tags = [group_name.lower(), 'minimal', 'silhouette', 'horizon']
    reproduction = prompts[idx-1] if idx-1 < len(prompts) else f"{group_name} layered ridges, pine silhouettes, muted palette, horizontal banner"
    suggested_settings = {
        'model': 'SDXL',
        'mode': 'img2img',
        'denoising_strength': 0.45,
        'sampler': 'Euler a',
        'steps': 28,
        'guidance_scale': 7.5,
        'seed': seed
    }
    meta.append({
        'id': f"{idx:02d}",
        'title': title,
        'style_group': group_code,
        'palette': palette_hex,
        'short_description': f"{group_name} variant with muted tones and layered ridges.",
        'reproduction_prompt': reproduction,
        'suggested_settings': suggested_settings,
        'upscaler_recommendation': 'Real-ESRGAN x2',
        'thumbnail': os.path.basename(preview_path),
        'final_image': os.path.basename(final_path),
        'tags': tags
    })

# write metadata
with open(os.path.join(OUT_DIR, 'metadata.json'), 'w', encoding='utf-8') as mf:
    json.dump(meta, mf, indent=2)

print(f"Generated {len(meta)} images in {OUT_DIR}")
