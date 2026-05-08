import fitz, os
os.makedirs('pdf_images', exist_ok=True)
base = r'C:\Users\PCGAME\Desktop\MASTER VS CODE PROJECT TSELUCA\resistência dos materiais'
files = sorted([f for f in os.listdir(base) if f.endswith('.pdf')])
for pdf_idx, fname in enumerate(files, 1):
    doc = fitz.open(os.path.join(base, fname))
    for page_num, page in enumerate(doc, 1):
        mat = fitz.Matrix(2.5, 2.5)
        pix = page.get_pixmap(matrix=mat)
        out = os.path.join(base, 'pdf_images', f'L{pdf_idx}_p{page_num}.png')
        pix.save(out)
        print(f'Saved: {out}')
    doc.close()
print('Done')
