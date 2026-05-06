from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image, ImageFont, ImageDraw
import textwrap

# Read ONE_PAGE_SUMMARY.md
root = Path('.')
md_path = root / 'ONE_PAGE_SUMMARY.md'
if not md_path.exists():
    print('ONE_PAGE_SUMMARY.md not found')
    raise SystemExit(1)
text = md_path.read_text(encoding='utf-8')

# Create an image with text
W, H = 2480, 3508  # A4 at 300dpi roughly
img = Image.new('RGB', (W, H), color='white')
draw = ImageDraw.Draw(img)

# Choose a font (fallback to default)
try:
    font = ImageFont.truetype('arial.ttf', 28)
    title_font = ImageFont.truetype('arialbd.ttf', 36)
except Exception:
    font = ImageFont.load_default()
    title_font = font

# Draw header
lines = text.splitlines()
y = 60
margin = 80
for i, line in enumerate(lines):
    if i == 0:
        f = title_font
    else:
        f = font
    wrapped = textwrap.wrap(line, width=120)
    for wl in wrapped:
        draw.text((margin, y), wl, font=f, fill='black')
        # compute height of text safely
        # Pillow versions differ; use font.getbbox if available
        try:
            bbox = f.getbbox(wl)
            h = bbox[3] - bbox[1]
        except Exception:
            try:
                w_, h = draw.textbbox((margin, y), wl, font=f)[2:4]
            except Exception:
                # fallback estimate
                h = 18
        y += h + 6
    y += 8
    if y > H - 200:
        break

# Save PNG and PDF
out_png = root / 'ONE_PAGE_SUMMARY.png'
out_pdf = root / 'ONE_PAGE_SUMMARY.pdf'
img.save(out_png, dpi=(300,300))
img.save(out_pdf, dpi=(300,300))
print('Wrote', out_png, out_pdf)
