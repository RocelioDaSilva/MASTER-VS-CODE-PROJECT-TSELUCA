#!/usr/bin/env python3
# Exporta cada slide do PPTX para PNG usando automação do PowerPoint (Windows)

import sys
from pathlib import Path

PPTX = Path(r"c:\Users\PCGAME\Desktop\reservatórios\Historia_Eng_Reservatorios_ISPTEC.pptx")
OUT_DIR = Path("slide_images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

if not PPTX.exists():
    print(f"Arquivo PPTX não encontrado: {PPTX}")
    sys.exit(1)

try:
    import win32com.client
except Exception:
    print("Módulo win32com (pywin32) não encontrado. Instale com: pip install pywin32")
    sys.exit(2)

app = None
pres = None
try:
    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = False
    pres = app.Presentations.Open(str(PPTX), False, False, False)

    exported = 0
    for slide in pres.Slides:
        idx = int(slide.SlideIndex)
        out_path = OUT_DIR / f"slide_{idx:02d}.png"
        slide.Export(str(out_path), "PNG", 1920, 1080)
        exported += 1

    pres.Close()
    app.Quit()
    print(f"Exported {exported} slides to {OUT_DIR.resolve()}")
    sys.exit(0)
except Exception as e:
    print("Erro ao exportar slides:", e)
    try:
        if pres is not None:
            pres.Close()
    except Exception:
        pass
    try:
        if app is not None:
            app.Quit()
    except Exception:
        pass
    sys.exit(3)
