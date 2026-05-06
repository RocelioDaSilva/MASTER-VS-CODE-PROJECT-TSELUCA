cwbook_minimal_package — Usage Guide

Overview
--------
This folder contains the minimal cwbook LaTeX class and a converted set of chapter files generated from your Markdown manuscript.

Files of interest
- `cwbook_minimal.cls` — the class file providing `\POV`, `\ENV`, glyphs, header/footer strips and chapter stripe.
- `manuscript.tex` — master LaTeX file that `\input{}`s all `chapterNN.tex` files in order.
- `chapter01.tex` ... `chapter52.tex` — converted LaTeX chapters generated from your Markdown sources.
- `env_*.svg` — environment strip artwork (SVG). You can convert to PNG for simpler LaTeX inclusion.

Basic workflow
--------------
1. Edit chapter content: modify `chapterNN.tex` files directly, or edit the original Markdown in `../manuscriptbaseforchapters` and re-run the converter script `convert_md_to_tex.py`.
2. Set POV for a chapter (if needed): each `chapterNN.tex` begins with a `\POV{<glyph>}{<Name>}` line. If a glyph macro exists in `cwbook_minimal.cls` it will be used; otherwise only the name will appear.
   - Known glyph macros: `\glyphAisen`, `\glyphCaspian`, `\glyphCorvin`, `\glyphRyo`, `\glyphKael`, `\glyphKairos`, `\glyphOrin`, `\glyphAmara`, `\glyphRenard`.
   - Example: `\POV{\glyphAisen}{Aisen}`
3. Change environment strips per chapter or scene using `\ENV{top-file.png}{bottom-file.png}` at the start of a chapter or before a scene within a chapter.
   - Example: `\ENV{env_dungeon_top.png}{env_dungeon_bottom.png}`

Compiling
---------
Recommended compilation with XeLaTeX (supports Unicode and custom fonts):

PowerShell (from this folder):

```powershell
Set-Location 'c:\Users\PCGAME\Desktop\story&universes\chain-weapon-story\finished-manuscript\cwbook_minimal_package'
xelatex -interaction=nonstopmode -halt-on-error manuscript.tex
```

Or using `latexmk` for repeated runs and bibliography handling:

```powershell
latexmk -pdf -pdflatex="xelatex -interaction=nonstopmode -halt-on-error %O %S" manuscript.tex
```

SVG vs PNG usage
----------------
- LaTeX (XeLaTeX) can include PNG images via `\includegraphics`. If you prefer to use the SVG files directly, add `\usepackage{svg}` to the class or master file and compile with `--shell-escape` enabled (Inkscape required).
- To convert SVGs to PNG (recommended):
  - Using Inkscape (command-line):

```powershell
inkscape env_dungeon_top.svg --export-type=png --export-filename=env_dungeon_top.png --export-width=2400
```

  - Or batch convert all SVGs:

```powershell
Get-ChildItem -Filter '*.svg' | ForEach-Object { inkscape $_.FullName --export-type=png --export-filename="$($_.DirectoryName)\$($_.BaseName).png" --export-width=2400 }
```

Editing notes
-------------
- If you want to change the default POV glyph set or add glyphs, edit `cwbook_minimal.cls` under the glyph definitions section and define new `\newcommand{\glyph...}` TikZ macros.
- To change the subtle POV marker style (size, position), edit the `fancyhead` block in `cwbook_minimal.cls`.
- To adjust strip height or symbol size quickly: change the `height=0.45cm` values and `scale=0.16` glyph scale in `cwbook_minimal.cls`.

Regenerating chapters
---------------------
If you modify Markdown sources in `manuscriptbaseforchapters`, run the converter script (from workspace root):

```powershell
# from finished-manuscript folder
python convert_md_to_tex.py
```

This will update `chapterNN.tex` files and recreate `manuscript.tex`.

Support
-------
If you'd like, I can:
- Convert the SVGs to PNG and add them to this folder.
- Integrate the refined rune glyphs into `cwbook_minimal.cls`.
- Compile a sample PDF and adjust the three initial parameters (strip height, symbol size, margins) and provide before/after screenshots.

Next step suggestion
--------------------
Would you like me to convert the SVG strips to PNG here and add them to the package (so you can compile with no extra dependencies)?
