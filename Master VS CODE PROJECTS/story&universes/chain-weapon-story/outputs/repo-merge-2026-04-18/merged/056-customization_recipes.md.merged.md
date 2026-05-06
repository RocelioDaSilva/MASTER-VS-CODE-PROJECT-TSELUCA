# Merged Artifact: customization_recipes.md

This file preserves all source content exactly.

## Sources

- finished-manuscript/CUSTOMIZATION_RECIPES.md (sha256: 48cca0f63a5c02d9369aa03db8d054114ab7e81a2599c96aeb7cc9732943f03e)
- finished-manuscript-reorg/original_copy/CUSTOMIZATION_RECIPES.md (sha256: 48cca0f63a5c02d9369aa03db8d054114ab7e81a2599c96aeb7cc9732943f03e)

---

## Source: finished-manuscript/CUSTOMIZATION_RECIPES.md

# Embers of the Forsaken Keep — Customization Recipes

This guide shows exact edits for common customizations.

## Recipe 1: Swap Character Mapping

**Goal:** Change Chapter 3 from Ryo POV to Kairos POV

**File:** `chapter-config.json`

```json
{
  "chapters": [
    ...
    {
      "num": 3,
      "label": "III",
      "title": "The Scout's Return",
      "character": "Kairos",        // ← Change from "Ryo" to "Kairos"
      "landscape": "Mountains",
      "location": "The Garrison Pass"
    },
    ...
  ]
}
```

**Regenerate:** `python build_manuscript.py` then `xelatex manuscript-final.tex`

---

## Recipe 2: Change Landscape Mood for Multiple Chapters

**Goal:** Make all "oppressive" scenes use Dungeon, not City

**File:** `chapter-config.json`

Find all chapters you want to change, update the `landscape` field:

```json
{
  "num": 6,
  "title": "Three Doors",
  "landscape": "Dungeon"    // ← Change from "City" to "Dungeon"
},
{
  "num": 11,
  "title": "The Bargain Spoken",
  "landscape": "Dungeon"    // ← Change from "City" to "Dungeon"
},
```

**Regnerate:** `python build_manuscript.py` then `xelatex manuscript-final.tex`

---

## Recipe 3: Create a Custom Colour Scheme

**Goal:** Warm, sepia-toned book (like an old manuscript)

**File:** `chapter-config.json` — update `color_customization`:

```json
"color_customization": {
  "PageBg": "FFF8F0",        // Very light cream instead of F8F3EC
  "Ink": "2A2015",           // Darker brown instead of 1C1812
  "InkMid": "4A3F2A",        // Warmer brown instead of 3A3028
  "Stone": "A89080",         // Warmer grey instead of 9A8A78
  "StoneLight": "D4C0A8",    // Warmer light grey instead of C8B8A8
  
  "ColAisen": "8B7355",      // Warm reddish-brown (ochre shift)
  "ColCaspian": "6B7A7A",    // Still slate-ish
  "ColCorvin": "5A5545",     // Darker warm grey
  "ColRyo": "7A8B5A",        // Olive-green instead of storm green
  "ColKael": "8B6A4A",       // Warm, earthy
  "ColKairos": "7A6A8A",     // Slightly warmer violet
  "ColOrin": "9A9080",       // More saturated dust
  "ColAmara": "7A6A5A",      // Warmer bronze
  "ColRenard": "6A7A6A"      // Warmer forest grey
}
```

**Apply:** 
1. Edit the JSON file above
2. Run `python build_manuscript.py`
3. Compile: `xelatex manuscript-final.tex`

The entire book will now render in sepia tones.

---

## Recipe 4: Darken the Page Background for Print

**Goal:** Adjust page colour for offset printing (higher ink density)

**File:** `chapter-config.json`:

```json
"PageBg": "F0E8DC"    // Much darker cream for print density
```

**Or** edit directly in `manuscript-final.tex`:

```latex
\definecolor{PageBg}{HTML}{F0E8DC}  % Darker cream
```

Then recompile. Check proof prints and adjust the hex value.

---

## Recipe 5: Adjust Typography for Tighter or Looser Layout

**Goal:** Make the book denser (fit in fewer pages)

**File:** `manuscript-final.tex`

Find the typography section and adjust:

```latex
% ══════════════════════════════════════════════════════════════════════════════
%  TYPOGRAPHY & SPACING
% ══════════════════════════════════════════════════════════════════════════════

\setlength{\parindent}{1.2em}    % ← Reduce from 1.6em (tighter indent)
\setlength{\parskip}{0pt}         % Keep at 0
\linespread{1.40}                 % ← Reduce from 1.55 (tighter lines)
```

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 6: Change Fonts Throughout

**Goal:** Use Georgia instead of Lora for a more classical feel

**File:** `manuscript-final.tex`

Find the font section and change:

```latex
\setmainfont{Georgia}    % ← Change from Lora

\newfontfamily\LabelFont{GFSBaskerville}  % Keep or change to Garamond
```

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 7: Adjust Header/Footer Heights

**Goal:** Make the header strip thinner

**File:** `manuscript-final.tex`

Find the `\HeaderStrip` macro:

```latex
\newcommand{\HeaderStrip}{%
  \begin{tikzpicture}[remember picture, overlay]
    ...
    \pgfmathsetmacro{\SH}{2.0}   % ← Change from 2.6 (thinner header)
```

**And** update `\FooterStrip`:

```latex
\newcommand{\FooterStrip}{%
  ...
  \pgfmathsetmacro{\FH}{1.8}   % ← Change from 2.4
```

**Warning:** Smaller headers may cut off landscape detail. Test before committing.

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 8: Intensify or Fade Character Colours

**Goal:** Make character stripes more vivid (increase saturation)

**File:** `chapter-config.json`:

Original (muted):
```json
"ColAisen": "7A6A50"
```

More vivid (increase saturation):
```json
"ColAisen": "9A8060"   // Brighter ochre
```

More muted (decrease saturation):
```json
"ColAisen": "6A5A40"   // Duller ochre
```

**Tool:** Use a hex colour picker (like [colorhexa.com](https://www.colorhexa.com)) to experiment.

**Apply and recompile:** `python build_manuscript.py` then `xelatex manuscript-final.tex`

---

## Recipe 9: Customize Individual Landscape Silhouettes

**Goal:** Make the Mountains landscape more jagged (more dramatic peaks)

**File:** `manuscript-final.tex`

Find `\LandscapeBodyMountains`:

```latex
\newcommand{\LandscapeBodyMountains}{%
  \fill[Stone!07] (TL) rectangle ($(TR)-(0,\SH cm)$);
  \fill[Stone!20]
    ($(TL)-(0,\SH cm*.18)$)
    --($(TL)!.09!(TR)-(0,\SH cm*.54)$)--($(TL)!.19!(TR)-(0,\SH cm*.32)$)  % ← Peaks
    % ... more peaks ...
```

To create more peaks, add more interpolation points:

```latex
    ($(TL)!.09!(TR)-(0,\SH cm*.54)$)      % Peak 1 at 9%, height 54%
    --($(TL)!.12!(TR)-(0,\SH cm*.30)$)    % ← NEW: valley at 12%, height 30%
    --($(TL)!.19!(TR)-(0,\SH cm*.32)$)    % Peak 2
```

The format is: `($(TL)!{x-percent}!(TR)-(0,\SH cm*{y-percent}$)`
- `{x-percent}` = horizontal 0 to 1 (left to right)
- `{y-percent}` = vertical 0.1 to 1 (bottom to top of strip)

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 10: Change Glyph Designs

**Goal:** Redesign the Aisen glyph to be more abstract

**File:** `manuscript-final.tex`

Find `\GlyphAisen`:

```latex
\newcommand{\GlyphAisen}{%
  \begin{tikzpicture}[x=1cm,y=1cm,line cap=round,line join=round]
    \draw[line width=0.7pt] (0,0) -- (1,2) -- (2,0) -- cycle;       % Triangle
    \draw[line width=0.5pt] (1,2) -- (1,0.75);                      % Center line
    \draw[line width=0.5pt] (0.5,0.85) -- (0.85,0.85);              % Horizontal
  \end{tikzpicture}}
```

Replace with a new design (example: concentric circles + rays):

```latex
\newcommand{\GlyphAisen}{%
  \begin{tikzpicture}[x=1cm,y=1cm,line cap=round,line join=round]
    % Outer circle
    \draw[line width=0.7pt] (1,1) circle (0.90cm);
    % Inner circle
    \draw[line width=0.5pt] (1,1) circle (0.45cm);
    % Rays
    \draw[line width=0.4pt] (1,1.90) -- (1,0.10);
    \draw[line width=0.4pt] (0.10,1) -- (1.90,1);
  \end{tikzpicture}}
```

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 11: Adjust Chapter Stripe Width

**Goal:** Make the right-edge colour bar wider (more visible)

**File:** `manuscript-final.tex`

Find `\ChapterStripe`:

```latex
\newcommand{\ChapterStripe}{%
  \begin{tikzpicture}[remember picture, overlay]
    ...
    \pgfmathsetmacro{\BarW}{0.50}    % ← Width in cm (currently 5mm)
    % Change to:
    \pgfmathsetmacro{\BarW}{0.75}    % 7.5mm — more visible
    % Or:
    \pgfmathsetmacro{\BarW}{0.35}    % 3.5mm — more subtle
```

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 12: Print-Ready Setup

**Goal:** Prepare manuscript for offset printing

**Changes needed:**

1. **Darken page background** (Recipe 4)
2. **Reduce glyph/landscape opacity** slightly for printing:

In `manuscript-final.tex`, find `\HeaderStrip`:

```latex
    \draw[Stone!45, line width=0.3pt]  % ← Already good for print
```

The Stone colours should print well. If too light, increase the percentage:

```latex
    \draw[Stone!50, line width=0.4pt]  % ← Slightly darker
```

3. **Test print** on your target paper stock
4. **Adjust colours iteratively** based on proof

---

## Batch Edits: Changing All Colours at Once

**Use find-and-replace in VS Code:**

1. Open `chapter-config.json`
2. Press `Ctrl+H` (Find & Replace)
3. Find: `"PageBg": "F8F3EC"`
4. Replace: `"PageBg": "F0E8DC"`
5. Click the "Replace All" button

This is faster than manual edits for global colour changes.

---

## Testing Your Changes

Always follow this workflow:

```bash
# 1. Edit chapter-config.json or manuscript-final.tex
# 2. Regenerate (if you changed chapter-config.json):
python build_manuscript.py

# 3. Compile with xelatex:
xelatex manuscript-final.tex

# 4. Check the PDF:
open manuscript-final.pdf  # or double-click the file

# 5. If colors are still off, adjust and repeat steps 1-4
```

The full compile cycle takes ~30 seconds. Each iteration lets you see results immediately.

---

Good luck customizing your book!


---

## Source: finished-manuscript-reorg/original_copy/CUSTOMIZATION_RECIPES.md

# Embers of the Forsaken Keep — Customization Recipes

This guide shows exact edits for common customizations.

## Recipe 1: Swap Character Mapping

**Goal:** Change Chapter 3 from Ryo POV to Kairos POV

**File:** `chapter-config.json`

```json
{
  "chapters": [
    ...
    {
      "num": 3,
      "label": "III",
      "title": "The Scout's Return",
      "character": "Kairos",        // ← Change from "Ryo" to "Kairos"
      "landscape": "Mountains",
      "location": "The Garrison Pass"
    },
    ...
  ]
}
```

**Regenerate:** `python build_manuscript.py` then `xelatex manuscript-final.tex`

---

## Recipe 2: Change Landscape Mood for Multiple Chapters

**Goal:** Make all "oppressive" scenes use Dungeon, not City

**File:** `chapter-config.json`

Find all chapters you want to change, update the `landscape` field:

```json
{
  "num": 6,
  "title": "Three Doors",
  "landscape": "Dungeon"    // ← Change from "City" to "Dungeon"
},
{
  "num": 11,
  "title": "The Bargain Spoken",
  "landscape": "Dungeon"    // ← Change from "City" to "Dungeon"
},
```

**Regnerate:** `python build_manuscript.py` then `xelatex manuscript-final.tex`

---

## Recipe 3: Create a Custom Colour Scheme

**Goal:** Warm, sepia-toned book (like an old manuscript)

**File:** `chapter-config.json` — update `color_customization`:

```json
"color_customization": {
  "PageBg": "FFF8F0",        // Very light cream instead of F8F3EC
  "Ink": "2A2015",           // Darker brown instead of 1C1812
  "InkMid": "4A3F2A",        // Warmer brown instead of 3A3028
  "Stone": "A89080",         // Warmer grey instead of 9A8A78
  "StoneLight": "D4C0A8",    // Warmer light grey instead of C8B8A8
  
  "ColAisen": "8B7355",      // Warm reddish-brown (ochre shift)
  "ColCaspian": "6B7A7A",    // Still slate-ish
  "ColCorvin": "5A5545",     // Darker warm grey
  "ColRyo": "7A8B5A",        // Olive-green instead of storm green
  "ColKael": "8B6A4A",       // Warm, earthy
  "ColKairos": "7A6A8A",     // Slightly warmer violet
  "ColOrin": "9A9080",       // More saturated dust
  "ColAmara": "7A6A5A",      // Warmer bronze
  "ColRenard": "6A7A6A"      // Warmer forest grey
}
```

**Apply:** 
1. Edit the JSON file above
2. Run `python build_manuscript.py`
3. Compile: `xelatex manuscript-final.tex`

The entire book will now render in sepia tones.

---

## Recipe 4: Darken the Page Background for Print

**Goal:** Adjust page colour for offset printing (higher ink density)

**File:** `chapter-config.json`:

```json
"PageBg": "F0E8DC"    // Much darker cream for print density
```

**Or** edit directly in `manuscript-final.tex`:

```latex
\definecolor{PageBg}{HTML}{F0E8DC}  % Darker cream
```

Then recompile. Check proof prints and adjust the hex value.

---

## Recipe 5: Adjust Typography for Tighter or Looser Layout

**Goal:** Make the book denser (fit in fewer pages)

**File:** `manuscript-final.tex`

Find the typography section and adjust:

```latex
% ══════════════════════════════════════════════════════════════════════════════
%  TYPOGRAPHY & SPACING
% ══════════════════════════════════════════════════════════════════════════════

\setlength{\parindent}{1.2em}    % ← Reduce from 1.6em (tighter indent)
\setlength{\parskip}{0pt}         % Keep at 0
\linespread{1.40}                 % ← Reduce from 1.55 (tighter lines)
```

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 6: Change Fonts Throughout

**Goal:** Use Georgia instead of Lora for a more classical feel

**File:** `manuscript-final.tex`

Find the font section and change:

```latex
\setmainfont{Georgia}    % ← Change from Lora

\newfontfamily\LabelFont{GFSBaskerville}  % Keep or change to Garamond
```

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 7: Adjust Header/Footer Heights

**Goal:** Make the header strip thinner

**File:** `manuscript-final.tex`

Find the `\HeaderStrip` macro:

```latex
\newcommand{\HeaderStrip}{%
  \begin{tikzpicture}[remember picture, overlay]
    ...
    \pgfmathsetmacro{\SH}{2.0}   % ← Change from 2.6 (thinner header)
```

**And** update `\FooterStrip`:

```latex
\newcommand{\FooterStrip}{%
  ...
  \pgfmathsetmacro{\FH}{1.8}   % ← Change from 2.4
```

**Warning:** Smaller headers may cut off landscape detail. Test before committing.

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 8: Intensify or Fade Character Colours

**Goal:** Make character stripes more vivid (increase saturation)

**File:** `chapter-config.json`:

Original (muted):
```json
"ColAisen": "7A6A50"
```

More vivid (increase saturation):
```json
"ColAisen": "9A8060"   // Brighter ochre
```

More muted (decrease saturation):
```json
"ColAisen": "6A5A40"   // Duller ochre
```

**Tool:** Use a hex colour picker (like [colorhexa.com](https://www.colorhexa.com)) to experiment.

**Apply and recompile:** `python build_manuscript.py` then `xelatex manuscript-final.tex`

---

## Recipe 9: Customize Individual Landscape Silhouettes

**Goal:** Make the Mountains landscape more jagged (more dramatic peaks)

**File:** `manuscript-final.tex`

Find `\LandscapeBodyMountains`:

```latex
\newcommand{\LandscapeBodyMountains}{%
  \fill[Stone!07] (TL) rectangle ($(TR)-(0,\SH cm)$);
  \fill[Stone!20]
    ($(TL)-(0,\SH cm*.18)$)
    --($(TL)!.09!(TR)-(0,\SH cm*.54)$)--($(TL)!.19!(TR)-(0,\SH cm*.32)$)  % ← Peaks
    % ... more peaks ...
```

To create more peaks, add more interpolation points:

```latex
    ($(TL)!.09!(TR)-(0,\SH cm*.54)$)      % Peak 1 at 9%, height 54%
    --($(TL)!.12!(TR)-(0,\SH cm*.30)$)    % ← NEW: valley at 12%, height 30%
    --($(TL)!.19!(TR)-(0,\SH cm*.32)$)    % Peak 2
```

The format is: `($(TL)!{x-percent}!(TR)-(0,\SH cm*{y-percent}$)`
- `{x-percent}` = horizontal 0 to 1 (left to right)
- `{y-percent}` = vertical 0.1 to 1 (bottom to top of strip)

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 10: Change Glyph Designs

**Goal:** Redesign the Aisen glyph to be more abstract

**File:** `manuscript-final.tex`

Find `\GlyphAisen`:

```latex
\newcommand{\GlyphAisen}{%
  \begin{tikzpicture}[x=1cm,y=1cm,line cap=round,line join=round]
    \draw[line width=0.7pt] (0,0) -- (1,2) -- (2,0) -- cycle;       % Triangle
    \draw[line width=0.5pt] (1,2) -- (1,0.75);                      % Center line
    \draw[line width=0.5pt] (0.5,0.85) -- (0.85,0.85);              % Horizontal
  \end{tikzpicture}}
```

Replace with a new design (example: concentric circles + rays):

```latex
\newcommand{\GlyphAisen}{%
  \begin{tikzpicture}[x=1cm,y=1cm,line cap=round,line join=round]
    % Outer circle
    \draw[line width=0.7pt] (1,1) circle (0.90cm);
    % Inner circle
    \draw[line width=0.5pt] (1,1) circle (0.45cm);
    % Rays
    \draw[line width=0.4pt] (1,1.90) -- (1,0.10);
    \draw[line width=0.4pt] (0.10,1) -- (1.90,1);
  \end{tikzpicture}}
```

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 11: Adjust Chapter Stripe Width

**Goal:** Make the right-edge colour bar wider (more visible)

**File:** `manuscript-final.tex`

Find `\ChapterStripe`:

```latex
\newcommand{\ChapterStripe}{%
  \begin{tikzpicture}[remember picture, overlay]
    ...
    \pgfmathsetmacro{\BarW}{0.50}    % ← Width in cm (currently 5mm)
    % Change to:
    \pgfmathsetmacro{\BarW}{0.75}    % 7.5mm — more visible
    % Or:
    \pgfmathsetmacro{\BarW}{0.35}    % 3.5mm — more subtle
```

**Recompile:** `xelatex manuscript-final.tex`

---

## Recipe 12: Print-Ready Setup

**Goal:** Prepare manuscript for offset printing

**Changes needed:**

1. **Darken page background** (Recipe 4)
2. **Reduce glyph/landscape opacity** slightly for printing:

In `manuscript-final.tex`, find `\HeaderStrip`:

```latex
    \draw[Stone!45, line width=0.3pt]  % ← Already good for print
```

The Stone colours should print well. If too light, increase the percentage:

```latex
    \draw[Stone!50, line width=0.4pt]  % ← Slightly darker
```

3. **Test print** on your target paper stock
4. **Adjust colours iteratively** based on proof

---

## Batch Edits: Changing All Colours at Once

**Use find-and-replace in VS Code:**

1. Open `chapter-config.json`
2. Press `Ctrl+H` (Find & Replace)
3. Find: `"PageBg": "F8F3EC"`
4. Replace: `"PageBg": "F0E8DC"`
5. Click the "Replace All" button

This is faster than manual edits for global colour changes.

---

## Testing Your Changes

Always follow this workflow:

```bash
# 1. Edit chapter-config.json or manuscript-final.tex
# 2. Regenerate (if you changed chapter-config.json):
python build_manuscript.py

# 3. Compile with xelatex:
xelatex manuscript-final.tex

# 4. Check the PDF:
open manuscript-final.pdf  # or double-click the file

# 5. If colors are still off, adjust and repeat steps 1-4
```

The full compile cycle takes ~30 seconds. Each iteration lets you see results immediately.

---

Good luck customizing your book!


---

