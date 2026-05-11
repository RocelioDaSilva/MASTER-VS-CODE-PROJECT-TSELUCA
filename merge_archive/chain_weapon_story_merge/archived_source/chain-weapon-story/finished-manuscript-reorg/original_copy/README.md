Stylish book template — enhanced

What this template provides
- Per-page POV badge shown on the outer header (`\CurrentPOV` / `\setPOV{...}`)
- Small top and bottom landscape bands with optional location labels (`\setTopLocation{...}` / `\setBottomLocation{...}`)
- Outer chapter "stripe" with markers for each chapter (enable and set count with `\SetTotalChapters{<n>}`)
- Chapter opener styling and helper workflows for drop caps (uses `lettrine`)
- Quote boxes (`quotebox`), scene-break ornament (`\scenebreak`), and improved line-breaking (global `\emergencystretch`)

Files
- [chain-style-v2.tex](chain-style-v2.tex#L1) — the updated template matching the HTML prototype (load in preamble)
- [chain-style.tex](chain-style.tex#L1) — original template (kept for reference)
- [manuscript.tex](manuscript.tex#L1) — a short example demonstrating usage

Requirements
- A LaTeX distribution (TeX Live / MiKTeX)
- Compile with XeLaTeX or LuaLaTeX for full font and TikZ support

Quick compile (from this folder):

```bash
xelatex manuscript.tex
xelatex manuscript.tex
```

Key commands & tips
- `\SetTotalChapters{N}`: Draws N marks in the outer stripe and highlights the current chapter. Set this in the preamble.
- `\setTopLocation{...}` / `\setBottomLocation{...}`: Place short labels inside the landscape bands.
- `\setTopLandscape{...}` / `\setBottomLandscape{...}`: Replace the whole band with custom TikZ or an `\includegraphics{...}`.
- `\POVMarker[<size>]{<color>}{<char>}`: Make a circular initial marker. Use `\POVGraphic{...}` to use an image.
- `\setPOV{...}` and `\POVchapter{<symbol>}{<title>}`: Set the current POV symbol (header) and open chapters.
- `\setPOVChar{<char>}`: Set a single glyph (or unicode icon) used inside the left POV sidebar frame.
- Use `\lettrine` manually at the start of chapters for drop capitals (examples in `manuscript.tex`). Automating lettrine for every chapter can be added if desired.
- `quotebox` environment: callouts and dialogue boxes use `\sloppy` internally to reduce overfull boxes.

Notes about layout issues
- Global `\emergencystretch=3em` is set to help with overfull hboxes (especially italicized or narrow dialog boxes). You can tweak this value in `chain-style.tex`.

Next steps I can do for you
- Add a set of built-in TikZ glyphs (sword, crown, mask) and register them as named symbols
- Produce a small pack of SVG/PDF icons for `\POVGraphic{...}` use
- Convert the template into a clean `.sty` package and add package options
- Add automatic lettrine-on-chapter-start logic (applies lettrine to the first paragraph automatically)

Reply with which enhancements you'd like next (icons / .sty / auto-lettrine / compile & fix PDF warnings). 