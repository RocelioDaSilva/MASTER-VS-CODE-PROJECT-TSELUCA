#!/usr/bin/env python3
"""
Batch img2img for Automatic1111 WebUI.

Usage:
  python batch_img2img.py --input-dir inputs --mapping mapping.csv --output-dir outputs
Prereqs:
  - Automatic1111 WebUI running at http://127.0.0.1:7860
  - Python 3.8+, packages: requests, pillow
    pip install requests pillow
Notes:
  - mapping.csv (optional) rows: input_filename,prompt_id
  - If mapping.csv is omitted, the script will use --default-input for every prompt.
  - Prompts dict contains prompt text and recommended settings.
"""

import os
import sys
import time
import base64
import argparse
import json
import requests
from PIL import Image
from io import BytesIO

API_URL_DEFAULT = "http://127.0.0.1:7860"

# Prompts dictionary: key -> {prompt, denoise, steps, cfg, sampler}
PROMPTS = {
    "01-A": {"prompt":"Rustic crossroads tavern at dusk, stag-antler sign silhouette, warm golden window light spilling onto wet cobbles, layered low hills behind, painterly brushwork, soft film grain","denoise":0.22,"steps":28,"cfg":7.5,"sampler":"Euler a"},
    "01-B": {"prompt":"Rustic crossroads tavern, rainy evening with reflective puddles and amber glows, subtle mist, cinematic low light","denoise":0.26,"steps":30,"cfg":7.5,"sampler":"Euler a"},
    "01-C": {"prompt":"Flat vector tavern header: clean shapes, warm gradient sky, minimal texture, crisp silhouettes","denoise":0.12,"steps":22,"cfg":6.5,"sampler":"Euler a"},

    "02-A": {"prompt":"Layered forest ridges with flowering grove foreground, warm shafts of light, soft painterly bloom","denoise":0.24,"steps":28,"cfg":7.0,"sampler":"Euler a"},
    "02-B": {"prompt":"Flowering grove at golden hour with strong backlight and petal dust, saturated greens","denoise":0.26,"steps":30,"cfg":7.0,"sampler":"Euler a"},
    "02-C": {"prompt":"Stylized flat-graphic flower grove: simplified shapes, high-clarity silhouettes, harmonious greens","denoise":0.14,"steps":22,"cfg":6.5,"sampler":"Euler a"},

    "03-A": {"prompt":"Academy training yard panorama with rows of spears and wooden dummies, stone halls in background, crisp mid-day light","denoise":0.22,"steps":28,"cfg":7.5,"sampler":"Euler a"},
    "03-B": {"prompt":"Training yard at overcast dawn with cool desaturated tones and soft shadows, atmospheric haze","denoise":0.26,"steps":30,"cfg":7.5,"sampler":"Euler a"},
    "03-C": {"prompt":"Minimal vector training yard: clean repeating spear silhouettes, muted palette, geometric clarity","denoise":0.12,"steps":20,"cfg":6.5,"sampler":"Euler a"},

    "04-A": {"prompt":"Aldric's Crossing skyline: layered towers and bridges with warm window glows and soft atmospheric haze","denoise":0.24,"steps":28,"cfg":7.5,"sampler":"Euler a"},
    "04-B": {"prompt":"City skyline at dusk with rim light and cool-blue upper sky, subtle fog in valleys","denoise":0.26,"steps":30,"cfg":7.5,"sampler":"Euler a"},
    "04-C": {"prompt":"Stylized skyline vector with flat color blocks and gentle gradient sky, clear silhouettes","denoise":0.14,"steps":22,"cfg":6.5,"sampler":"Euler a"},

    "05-A": {"prompt":"Frostfang ridge panoramic: jagged cold peaks, thin snow dust, low sun casting long blue shadows","denoise":0.26,"steps":30,"cfg":8.0,"sampler":"Euler a"},
    "05-B": {"prompt":"Frostfang at pale dawn with pink-cold horizon and drifting flurries, soft edges","denoise":0.28,"steps":32,"cfg":8.0,"sampler":"Euler a"},
    "05-C": {"prompt":"Clean geometric cold-peak variant: simple layered peaks, minimal texture, cool desaturated palette","denoise":0.14,"steps":22,"cfg":6.8,"sampler":"Euler a"},

    "06-A": {"prompt":"Narrow mountain pass with rope bridge silhouettes and wind-blown banners, rim-lighting, cinematic tension","denoise":0.24,"steps":28,"cfg":7.8,"sampler":"Euler a"},
    "06-B": {"prompt":"Pass shrouded in thin cloud and drifting snow, muted tones and soft light","denoise":0.28,"steps":30,"cfg":8.0,"sampler":"Euler a"},
    "06-C": {"prompt":"Minimal silhouette bridge scene: stark shapes, strong horizon line, high-clarity contrast","denoise":0.12,"steps":20,"cfg":6.5,"sampler":"Euler a"},

    "07-A": {"prompt":"Misty river at dawn with low wooden boats half-hidden, reed silhouettes and soft reflections","denoise":0.24,"steps":28,"cfg":7.2,"sampler":"Euler a"},
    "07-B": {"prompt":"River at twilight with cooler tones, moon shimmer and thin fog layer","denoise":0.26,"steps":30,"cfg":7.2,"sampler":"Euler a"},
    "07-C": {"prompt":"Flat graphic river banner: long horizontal reeds and clean boat silhouettes, muted palette","denoise":0.14,"steps":22,"cfg":6.5,"sampler":"Euler a"},

    "08-A": {"prompt":"Border village at dusk with watchfires, low huts, smoke trails, textured-grit feel","denoise":0.28,"steps":30,"cfg":8.0,"sampler":"Euler a"},
    "08-B": {"prompt":"Village at dawn with faint blue light, embers fading, low-angle soft shadows","denoise":0.26,"steps":30,"cfg":7.8,"sampler":"Euler a"},
    "08-C": {"prompt":"Simplified village strip: clean hut silhouettes, warm central glow, minimal texture","denoise":0.14,"steps":22,"cfg":6.5,"sampler":"Euler a"},

    "09-A": {"prompt":"Refugee camp twilight with rows of tents and lantern glows, muted compassionate palette","denoise":0.24,"steps":28,"cfg":7.5,"sampler":"Euler a"},
    "09-B": {"prompt":"Camp at pre-dawn with cool-blue lamps and damp ground reflections, gentle atmosphere","denoise":0.26,"steps":30,"cfg":7.5,"sampler":"Euler a"},
    "09-C": {"prompt":"Vector-style camp header: orderly tent silhouettes, single warm focal light","denoise":0.12,"steps":20,"cfg":6.5,"sampler":"Euler a"},

    "10-A": {"prompt":"Archive vault with high stacks and lamplight, dust motes and deep perspective, warm chiaroscuro","denoise":0.24,"steps":28,"cfg":7.8,"sampler":"Euler a"},
    "10-B": {"prompt":"Archive cool variant with pale lamplight and strong rim highlights, dusty shafts","denoise":0.26,"steps":30,"cfg":7.8,"sampler":"Euler a"},
    "10-C": {"prompt":"Clean graphic stacks: repeating shelf silhouettes, uniform warm-tan palette","denoise":0.14,"steps":22,"cfg":6.8,"sampler":"Euler a"},

    "11-A": {"prompt":"Ruined temple with crumbled pillars and faint rune glow, low fog and magical particles","denoise":0.26,"steps":30,"cfg":8.0,"sampler":"Euler a"},
    "11-B": {"prompt":"Temple at moonlit night with faint bioluminescent rune dust and cool highlights","denoise":0.28,"steps":32,"cfg":8.0,"sampler":"Euler a"},
    "11-C": {"prompt":"Stylized temple shapes with simplified glowing lines and minimal detail","denoise":0.14,"steps":22,"cfg":6.8,"sampler":"Euler a"},

    "12-A": {"prompt":"Dungeon mouth rim with stalactite silhouettes and warm inner torchlight, deep shadow contrast","denoise":0.28,"steps":30,"cfg":8.0,"sampler":"Euler a"},
    "12-B": {"prompt":"Cave entrance with cold blue exterior and single distant torch inside, high contrast","denoise":0.30,"steps":32,"cfg":8.0,"sampler":"Euler a"},
    "12-C": {"prompt":"Clean silhouette dungeon edge: bold rock shapes and single warm glow","denoise":0.14,"steps":22,"cfg":6.8,"sampler":"Euler a"},

    "13-A": {"prompt":"Wasteland dunes, layered ridges with sparse scrub, muted sandy palette, minimal horizon","denoise":0.22,"steps":28,"cfg":7.0,"sampler":"Euler a"},
    "13-B": {"prompt":"Wasteland at sunset with long warm shadows and subtle dust in air","denoise":0.26,"steps":30,"cfg":7.2,"sampler":"Euler a"},
    "13-C": {"prompt":"Flat geometric dunes: simple layered waves of color, clean edges","denoise":0.12,"steps":20,"cfg":6.5,"sampler":"Euler a"},

    "14-A": {"prompt":"Snow plain with soft powder and distant wind-carved ridges, pale sky, calm minimalist composition","denoise":0.22,"steps":28,"cfg":7.2,"sampler":"Euler a"},
    "14-B": {"prompt":"Snow plain at blue hour with gentle auroral tint and faint drifting snow","denoise":0.26,"steps":30,"cfg":7.5,"sampler":"Euler a"},
    "14-C": {"prompt":"Clean cold-vector plain: broad pale bands, minimal detail","denoise":0.12,"steps":20,"cfg":6.5,"sampler":"Euler a"},

    "15-A": {"prompt":"Under-city vaulted arches with shallow reflective pools and amber lamplight, moody cinematic contrast","denoise":0.26,"steps":30,"cfg":8.0,"sampler":"Euler a"},
    "15-B": {"prompt":"Under-city with cool-green bioluminescent accents and misted pools, eerie quiet","denoise":0.28,"steps":32,"cfg":8.0,"sampler":"Euler a"},
    "15-C": {"prompt":"Graphic undercity strip: repeating arch silhouettes and single reflection band","denoise":0.14,"steps":22,"cfg":6.8,"sampler":"Euler a"},

    "16-A": {"prompt":"Dusk battlefield ridge with rows of spear and banner silhouettes, low fires and haze, somber cinematic light","denoise":0.26,"steps":30,"cfg":8.0,"sampler":"Euler a"},
    "16-B": {"prompt":"Battlefield ridge at sunrise with cool mist and backlit spears, quieter tone","denoise":0.28,"steps":32,"cfg":8.0,"sampler":"Euler a"},
    "16-C": {"prompt":"High-contrast silhouette battlefield: bold flags and spear lines, minimal color, textured paper grain","denoise":0.14,"steps":24,"cfg":7.0,"sampler":"Euler a"},
}

def encode_image_to_dataurl(path, width, height, resize_mode=0):
    im = Image.open(path).convert("RGBA")
    if im.size != (width, height):
        im = im.resize((width, height), Image.LANCZOS)
    buffer = BytesIO()
    im.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"

def call_img2img(api_url, init_image_dataurl, prompt, denoise, steps, cfg, sampler, width, height, seed=-1):
    payload = {
        "init_images": [init_image_dataurl],
        "prompt": prompt,
        "negative_prompt": "",
        "denoising_strength": denoise,
        "steps": steps,
        "sampler_index": sampler,
        "cfg_scale": cfg,
        "seed": seed,
        "width": width,
        "height": height,
        "batch_size": 1
    }
    r = requests.post(f"{api_url}/sdapi/v1/img2img", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()

def save_base64_image(b64str, out_path):
    img_bytes = base64.b64decode(b64str)
    with open(out_path, "wb") as f:
        f.write(img_bytes)

def load_mapping_csv(path):
    mappings = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 2:
                mappings.append((parts[0], parts[1]))
    return mappings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-url", default=API_URL_DEFAULT, help="Automatic1111 WebUI API base URL")
    parser.add_argument("--input-dir", default="inputs", help="Folder with input images")
    parser.add_argument("--output-dir", default="outputs", help="Folder to save results")
    parser.add_argument("--mapping", default=None, help="Optional CSV mapping file: input_filename,prompt_id")
    parser.add_argument("--default-input", default=None, help="If mapping omitted, use this input for all prompts (path)")
    parser.add_argument("--width", type=int, default=2400)
    parser.add_argument("--height", type=int, default=400)
    parser.add_argument("--sleep", type=float, default=1.0, help="Seconds between requests")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Build work list
    work = []
    if args.mapping:
        mappings = load_mapping_csv(args.mapping)
        for input_fn, prompt_id in mappings:
            prompt_id = prompt_id.strip()
            if prompt_id not in PROMPTS:
                print(f"Warning: prompt id {prompt_id} not in PROMPTS dict; skipping.")
                continue
            input_path = input_fn if os.path.isabs(input_fn) else os.path.join(args.input_dir, input_fn)
            work.append((input_path, prompt_id))
    else:
        if not args.default_input:
            print("No mapping provided and no --default-input set. Exiting.")
            sys.exit(1)
        # use default input for every prompt in PROMPTS
        for pid in PROMPTS.keys():
            work.append((args.default_input, pid))

    print(f"Prepared {len(work)} jobs.")

    for idx, (input_path, pid) in enumerate(work, start=1):
        if not os.path.exists(input_path):
            print(f"[{idx}/{len(work)}] Input not found: {input_path} - skipping.")
            continue
        dataurl = encode_image_to_dataurl(input_path, args.width, args.height)
        meta = PROMPTS[pid]
        print(f"[{idx}/{len(work)}] Sending {pid} -> {os.path.basename(input_path)}")
        try:
            result = call_img2img(api_url=args.api_url, init_image_dataurl=dataurl,
                                  prompt=meta["prompt"], denoise=meta["denoise"],
                                  steps=meta["steps"], cfg=meta["cfg"], sampler=meta["sampler"],
                                  width=args.width, height=args.height)
        except Exception as e:
            print(f"Error calling API for {pid}: {e}")
            continue

        images = result.get("images", [])
        if not images:
            print(f"No images returned for {pid}")
            continue

        out_base = os.path.join(args.output_dir, f"{pid}")
        # If multiple images in batch, save indexed
        for i, b64 in enumerate(images):
            out_path = f"{out_base}"
            if len(images) > 1:
                out_path = f"{out_base}_{i+1}.png"
            else:
                out_path = f"{out_base}.png"
            # If file exists, add numeric suffix
            suffix = 1
            base_out_path = out_path
            while os.path.exists(out_path):
                out_path = base_out_path.replace(".png", f"_{suffix}.png")
                suffix += 1
            save_base64_image(b64, out_path)
            print(f"Saved {out_path}")

        time.sleep(args.sleep)

if __name__ == "__main__":
    main()
