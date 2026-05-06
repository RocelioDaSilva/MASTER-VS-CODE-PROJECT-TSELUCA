#!/usr/bin/env python3
import fitz
from pathlib import Path

PKG = Path('cwbook_minimal_package')
PDF = PKG / 'manuscript.pdf'
OUT = PKG / 'preview_pages'
OUT.mkdir(exist_ok=True)

if not PDF.exists():
    print('manuscript.pdf not found at', PDF)
    raise SystemExit(1)

doc = fitz.open(str(PDF))
num_pages = doc.page_count
print('PDF pages:', num_pages)

pages = list(range(min(4, num_pages)))
for i in pages:
    page = doc.load_page(i)
    mat = fitz.Matrix(2.0, 2.0)  # scale 2x
    pix = page.get_pixmap(matrix=mat, alpha=False)
    outpath = OUT / f'page_{i+1:03}.png'
    pix.save(str(outpath))
    print('Saved', outpath)

print('Done.')
