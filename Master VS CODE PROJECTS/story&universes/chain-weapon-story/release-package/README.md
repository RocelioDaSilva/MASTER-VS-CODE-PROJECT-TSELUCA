CWBook — Final Product (minimal)
================================

Contents
- `manuscript.tex` — main manuscript (uses `chain-style.tex`)
- `chain-style.tex` — style and layout (requires XeLaTeX or LuaLaTeX)
- `cwbook_minimal.cls` — minimal class tailored for this project
- `cwbook_minimal-sample.tex` — a small sample showing usage

Compile
- Recommended engines: `xelatex` or `lualatex` (fontspec is used).
  Run twice to resolve references:

```bash
xelatex -interaction=nonstopmode -halt-on-error manuscript.tex
xelatex -interaction=nonstopmode -halt-on-error manuscript.tex
```

Notes
- The class wraps optional environment header/footer images (`env-top.png`/`env-bottom.png`) using `\IfFileExists`, so missing images won't break compilation.
- Fonts referenced: TeX Gyre Pagella / TeX Gyre Heros. Install them or change fonts in `chain-style.tex`.
