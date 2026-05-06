# Embers of the Forsaken Keep — Integrated Book Template

## System Overview

This is a complete book typesetting system combining:
- **9 character POV glyphs** (abstract TikZ symbols)
- **6 landscape variations** (procedurally-drawn header silhouettes)
- **Per-page chapter stripes** (colour-coded progress bar on right edge)
- **Decorative headers and footers** (monochrome silhouettes)
- **All 52 chapters pre-configured** with character, landscape, and location

## Files

### Core Template
- **`manuscript-final.tex`** — Complete book ready to compile (generated from build script)
- **`build_manuscript.py`** — Python script that generates the final manuscript from config

### Configuration
- **`chapter-config.json`** — Master configuration: maps chapters to characters, landscapes, locations, colours

### Optional References
- `manuscript-integrated.tex` — Template with example chapters 1-2 (for reference)
- `newstuffmadebyclaude7-4/cwbook_final.tex` — Original template source file
- `newstuffmadebyclaude7-4/cwbook_reference.tex` — Visual reference (glyphs and landscapes)

## Compilation

```bash
# Using xelatex (required for fontspec)
xelatex manuscript-final.tex
xelatex manuscript-final.tex    # Run twice for TOC/index updates

# Output: manuscript-final.pdf
```

## System Architecture

### 1. Nine POV Character Glyphs

Each glyph is a small TikZ symbol rendered in the character's colour. They appear:
- In the top-left corner of every page (below the horizon line)
- Small (0.14cm scale), quiet but consistent
- Tinted in the character's accent colour
- Reader learns POV character by visual pattern recognition

**Characters and colours:**
- **Aisen** (ColAisen: `#7A6A50`) — warm ochre, fractured ascent triangle
- **Caspian** (ColCaspian: `#5A6A7A`) — cold slate, split circle
- **Corvin** (ColCorvin: `#4A4A4A`) — ash grey, crossed square
- **Ryo** (ColRyo: `#6A7A5A`) — storm green, lightning fracture
- **Kael** (ColKael: `#7A5A3A`) — earth brown, beast mark (triangle + eye)
- **Kairos** (ColKairos: `#6A5A7A`) — deep violet, broken loop
- **Orin** (ColOrin: `#8A7A6A`) — pale dust, hollow core (nested circles)
- **Amara** (ColAmara: `#6A5A4A`) — bronze, stratified triangle (layered)
- **Renard** (ColRenard: `#5A6A5A`) — forest grey, observer star (8-pointed)

### 2. Six Landscape Variations

Each landscape is a monochrome silhouette drawn procedurally using normalized coordinates. Mood-driven, not geographically literal.

**Landscapes and mood:**
- **Mountains** — steadfast, eternal, cold wisdom (jagged peaks, warm tones)
- **City** — ordered but fractured, human scale (urban skyline)
- **Dungeon** — enclosed, oppressive, hidden truth (low ceiling, dark)
- **Wasteland** — aftermath, void, breaking point (barren, broken)
- **Forest** — organic, hidden currents, natural law (layered canopy)
- **Coast** — liminal, transition, between worlds (wavy water, horizon)

All landscapes are drawn in shades of Stone (grey palette) and appear at the top and bottom of every page.

### 3. Chapter Stripe

A coloured rectangle on the right edge of every page, positioned to show reading progress:
- Filled with the POV character's colour
- Height = page height / total chapters (52)
- Starts at top and moves down as you progress through the book
- Reader sees visual progress bar on the edge of the spine

### 4. Page Layout

```
┌─────────────────────────────────────────────────────┐
│  LANDSCAPE HEADER (2.6cm)                           │
│  [silhouette + horizon line + location + POV glyph] │
├─────────────────────────────────────────────────────┤ ← POV glyph here
│                                                     │
│  BODY TEXT (full width, 52-page line spacing)      │
│  .......................                            │
│  ..... .... .... ..... ... ... ....                 │
│  .......................... ... .... .... .. ...    │
│                                                     │
│  Full margin (3.6cm left, 2.8cm right)             │
│  Ragged top/bottom preserved for decorative effect │
│                                                     │
├─────────────────────────────────────────────────────┤
│  LANDSCAPE FOOTER (2.4cm)                           │
│  [ground plane + page number centered]              │
└────────────────────────────────────────────────────┤← Chapter stripe
                                                      │ right colour bar

```

## Customization Guide

### Option 1: Change Chapter Configuration

Edit `chapter-config.json`:

```json
{
  "chapters": [
    {
      "num": 1,
      "label": "I",
      "title": "A Place to Stand",
      "character": "Aisen",      // Change to different POV
      "landscape": "Mountains",  // Change to different mood
      "location": "The Grey Mountains"  // Location label shown in header
    },
    ...
  ]
}
```

Then regenerate:
```bash
python build_manuscript.py
xelatex manuscript-final.tex
```

### Option 2: Adjust Colours

Edit `chapter-config.json` under `color_customization`:

```json
"color_customization": {
  "PageBg": "F8F3EC",      // Page background (warm cream)
  "Ink": "1C1812",         // Text color (deep charcoal)
  "Stone": "9A8A78",       // Landscape silhouettes (warm grey)
  "ColAisen": "7A6A50",    // Aisen's character colour
  ...
}
```

Or edit directly in `manuscript-final.tex`:
```latex
\definecolor{PageBg}{HTML}{F8F3EC}
\definecolor{ColAisen}{HTML}{7A6A50}
```

Then recompile with xelatex.

### Option 3: Change Landscape Drawings

Landscapes are drawn in `manuscript-final.tex` as TikZ commands.

Example (Mountains):
```latex
\newcommand{\LandscapeBodyMountains}{%
  \fill[Stone!07] (TL) rectangle ($(TR)-(0,\SH cm)$);
  \fill[Stone!20] ...  % lighter peaks
  \fill[Stone!36] ...  % medium peaks
  \fill[Stone!62] ...  % dark base
}
```

To customize:
- **TL/TR** = top-left/top-right page coordinates (normalized)
- **\SH** = strip height (2.6cm for header, 2.4cm for footer)
- **Stone!XX** = tint percentage of Stone colour (01%–99%)

Adjust the interpolation points (`!.25!(TR)`, etc.) to reshape the silhouettes.

### Option 4: Change Glyph Designs

Each glyph is a TikZ miniature in `manuscript-final.tex`:

```latex
\newcommand{\GlyphAisen}{%
  \begin{tikzpicture}[x=1cm,y=1cm,line cap=round,line join=round]
    \draw[line width=0.7pt] (0,0) -- (1,2) -- (2,0) -- cycle;
    \draw[line width=0.5pt] (1,2) -- (1,0.75);
    \draw[line width=0.5pt] (0.5,0.85) -- (0.85,0.85);
  \end{tikzpicture}}
```

Modify line positions, widths, or add fills. All glyphs fit in a normalized 2×2 unit box.

### Option 5: Adjust Typography

In `manuscript-final.tex`:

```latex
\setlength{\parindent}{1.6em}    % Paragraph indent
\setlength{\parskip}{0pt}         % Space between paragraphs
\linespread{1.55}                 % Line spacing
```

Also control fonts:
```latex
\setmainfont{Lora}                % Body font (change to Arial, Georgia, etc.)
\newfontfamily\LabelFont{GFSBaskerville}  % Chapter labels
```

## Workflow: Adding / Editing Chapters

### To add a new chapter:
1. Add entry to `chapter-config.json` under `chapters`
2. Ensure the chapter content file exists in `cwbook_minimal_package/chapterXX.tex`
3. Run `python build_manuscript.py`
4. Recompile: `xelatex manuscript-final.tex`

### To edit an existing chapter:
1. Modify the `.tex` file in `cwbook_minimal_package/`
2. Regenerate: `python build_manuscript.py`
3. Recompile: `xelatex manuscript-final.tex`

### To change POV/landscape mid-chapter:
Not recommended (breaks the page stripe logic). Better approach:
- Split into two chapters
- Update `chapter-config.json`
- Regenerate

## Typography Notes

- **Font:** Lora (Google Fonts) — serif, readable at small sizes
- **Line height:** 1.55× (generous for readability)
- **Margins:** 3.6cm left, 2.8cm right (asymmetric for open book feel)
- **Paragraph indent:** 1.6em (visible but not obtrusive)
- **Colour:** InkMid (#3A3028) — dark brown, easier on eyes than pure black

## Advanced: Per-Chapter Header Override

You can override the landscape/character for a single page by directly editing `manuscript-final.tex`:

```latex
\renewcommand{\ActiveLandscape}{Dungeon}
\renewcommand{\ActiveCharacter}{Kairos}
\renewcommand{\SceneLocation}{The Deep Place}
\renewcommand{\CurrentChapterNum}{7}

\BookChapter{VII}{Chapter Title}

[Chapter content...]

\newpage
```

The page background will update automatically.

## Troubleshooting

### Fonts not found
- Install Lora and GFSBaskerville via package manager
- Or change `\setmainfont{Lora}` to a system font (Arial, Georgia, etc.)

### Landscapes not rendering
- Ensure TikZ is installed: `tlmgr install tikz` (if using TeX Live)
- Check `\SH` and `\FH` macros are defined (they are, in header/footer commands)

### Page stripe not showing
- Verify `\CurrentChapterNum` is set correctly for each chapter
- Check `\POVColor` resolves to a defined colour (should auto-resolve from character)

### Text overflowing margins
- Reduce `\linespread{}` (currently 1.55)
- Reduce font size: change `11pt` in `\documentclass[]{}` to `10pt`

## File Size and Compilation Time

- **Manuscript size:** ~500–700 KB (all glyphs embedded as TikZ)
- **Compilation:** ~10–15 seconds per run (2 runs recommended)
- **PDF output:** ~2–3 MB (depends on chapter count and image content)

## Next Steps

1. Customize colours in `chapter-config.json` to match your brand
2. Adjust landscape drawings if desired (TikZ knowledge helpful)
3. Update chapter titles and locations in `chapter-config.json`
4. Run `python build_manuscript.py` to regenerate
5. Compile with `xelatex manuscript-final.tex` (twice)
6. Export PDF and review layout

Good luck with *Embers of the Forsaken Keep*!
