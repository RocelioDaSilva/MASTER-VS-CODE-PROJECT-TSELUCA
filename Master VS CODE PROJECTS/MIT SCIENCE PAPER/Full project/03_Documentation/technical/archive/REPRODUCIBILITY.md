Reproducibility and quick build instructions

This document provides minimal steps to reproduce the paper PDF and run the project's tests.

Requirements (Windows / recommended):
- MiKTeX (pdflatex, bibtex)
- Python 3.10+ (venv recommended)
- pip

Build paper (from repository root):

1. Build the working paper (writing/SOL.tex):

```powershell
cd "Full project\writing"
pdflatex -interaction=nonstopmode SOL.tex
bibtex SOL
pdflatex -interaction=nonstopmode SOL.tex
pdflatex -interaction=nonstopmode SOL.tex
```

2. If figures are generated from code, run the extraction/generation scripts in `Coding parts\geesp-angola\scripts` (examples):

```powershell
cd "Full project\Coding parts\geesp-angola"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_maps.py
```

Run tests (unit tests):

```powershell
cd "Full project\Coding parts\geesp-angola"
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

Notes / Next improvements:
- Resolve remaining LaTeX overfull/underfull box warnings by editing paragraph breaks or allowing hyphenation.
- Verify bibliography keys in `writing/referencias.bib` if any citations remain undefined after `bibtex`.
- For publication-quality figures, regenerate `figuras/*.pdf` at higher DPI using the scripts in `Coding parts\geesp-angola\scripts`.
- Consider running `latexmk -pdf` for a more robust build pipeline.

Contact: Rocélio Da Silva (project owner)