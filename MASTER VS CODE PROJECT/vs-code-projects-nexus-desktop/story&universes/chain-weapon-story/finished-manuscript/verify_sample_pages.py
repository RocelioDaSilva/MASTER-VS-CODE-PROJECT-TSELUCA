#!/usr/bin/env python3
import fitz
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PDF = ROOT / 'cwbook_minimal_package' / 'manuscript.pdf'
OUT = ROOT / 'cwbook_minimal_package' / 'verify_pages'
OUT.mkdir(exist_ok=True)

pages = [2, 20, 40, 60, 80, 90]

doc = fitz.open(str(PDF))
for p in pages:
    if p <= doc.page_count:
        page = doc.load_page(p-1)
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out = OUT / f'verify_page_{p:03}.png'
        pix.save(str(out))
        print('Saved', out)
print('Done')
