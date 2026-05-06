# AI Auto Vectorizer

This folder contains a small Node.js scaffolding to generate raster headers via an image API (example: Replicate), convert them to SVG using ImageTracerJS, and optimize with SVGO.

Files created:
- `generate.js` — main pipeline (Replicate -> ImageTracerJS -> SVGO)
- `prompts.txt` — one prompt per line
- `.env.example` — copy to `.env` and fill keys
- `test_env.js` — quick environment smoke test
- `lib/` — place `imagetracer_v1.2.6.js` here if you prefer the local copy

Quick setup (from `tools/image_pipeline/`):

```bash
npm install
cp .env.example .env
# edit .env to add REPLICATE_API_TOKEN and REPLICATE_MODEL_VERSION
npm run test-env
# when ready:
npm run generate
```

Notes:
- The script defaults to Replicate; you can adapt `generateImageReplicate` to another provider.
- For higher-fidelity vectorization consider Vector Magic or manual tracing in Illustrator/InkScape.
Image Pipeline - Automatic1111 + Upscaling

Files created:
- `mapping.csv` : maps input image filenames (relative to input-dir) to prompt IDs (01-A..16-C)
- `prompts_48.txt` : one-line SDXL img2img prompts with suggested settings for each variant
- `claude_opus_prompt.txt` : the full Claude Opus 4.6 prompt for generating 16 header images
- `batch_img2img.py` : Python script to call Automatic1111 WebUI's img2img API using `mapping.csv`

Prerequisites
1. Automatic1111 WebUI running locally (or reachable) at `http://127.0.0.1:7860`.
   - Repo: https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Python 3.8+ and required packages:

```bash
python -m pip install requests pillow
```

Quick start (recommended)
1. Place your input header source images in the folder:
   `finished-manuscript/cwbook_minimal_package`

2. Run the batch script using the mapping file in this directory:

```powershell
python tools/image_pipeline/batch_img2img.py --input-dir finished-manuscript/cwbook_minimal_package --mapping tools/image_pipeline/mapping.csv --output-dir outputs/headers
```

3. Check `outputs/headers` for generated PNG files named like `01-A.png`, `04-B.png`, etc.

Notes
- `mapping.csv` lines are `input_filename,prompt_id`. The script will look for `input_filename` inside `--input-dir` unless an absolute path is provided.
- `prompts_48.txt` contains the concise prompts and suggested denoise/steps/cfg settings; you can copy them into your WebUI or use them as `--prompt` overrides.
- After generation, run Real-ESRGAN or Topaz Gigapixel for upscaling if desired.

If you want, I can now:
- (A) generate a `mapping.csv` that maps the existing package images automatically (already done), or
- (B) export `prompts_48.txt` as a downloadable file (already created), or
- (C) prepare a PowerShell wrapper to invoke the Python script across multiple parallel workers.

Tell me which next step you want.
