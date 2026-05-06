"""
Convert PNG map images in data/processed to PDF files (one per PNG).
Creates files with same base name and .pdf extension.
"""

from pathlib import Path
from PIL import Image

INPUT_DIR = Path("data/processed")

if not INPUT_DIR.exists():
    print(f"Input directory {INPUT_DIR} not found")
    raise SystemExit(1)

for png in sorted(INPUT_DIR.glob("*.png")):
    pdf_path = png.with_suffix(".pdf")
    try:
        img = Image.open(png).convert("RGB")
        img.save(pdf_path, "PDF", resolution=100.0)
        print(f"Converted {png.name} -> {pdf_path.name}")
    except Exception as e:
        print(f"Failed to convert {png.name}: {e}")
