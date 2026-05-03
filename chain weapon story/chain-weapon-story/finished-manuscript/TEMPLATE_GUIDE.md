# Stylish Book Template — LaTeX Guide

## Overview

This is a professional book template in LaTeX designed for narrative fiction with:
- **Character POV indicators** (symbol column with color-coded character markers)
- **Chapter stripe** (side indicator like Bible chapter tabs)
- **Environment banners** (top/bottom scenic descriptions)
- **Elegant typography** (drop caps, dialogue styling, scene breaks)
- **Character legend** (visual reference for all POV characters)

## Features

### 1. Chapter Stripe (Left Margin)
A dark decorative stripe runs vertically down the left side of every page, creating a visual anchor similar to Bible chapter markers. This helps readers quickly navigate and visually ground themselves in the book.

### 2. POV Symbol Column
Adjacent to the chapter stripe is a narrow column displaying the current POV character's symbol. Each character has:
- **Unique symbol**: ⚔ (Aelindra), 🜂 (Dorian), ☽ (Seren), ⚗ (Mael)
- **Color**: Gold, blue, green, or rose respectively
- **Name label**: Character name in small capitals below the symbol

Use `\povmargin{symbol}{name}{color}` to set the POV at any point in a chapter.

### 3. Landscape Banners
**Top Banner** (`\landscapetop{location}`):
- Mountain range scene
- Perfect for indicating setting

**Bottom Banner** (`\landscapebottom{location}`):
- Valley/path scene
- Indicates environmental transition

Example:
```latex
\landscapetop{THE GREY MOUNTAINS · DUSK}
...chapter content...
\landscapebottom{VALLEY OF ASHENVEIL · TWILIGHT}
```

### 4. Character Legend
Appears at the start of each chapter, displaying all four characters with their symbols and colors. Helps readers remember character associations.

```latex
\characterlegend
```

### 5. Typography Features

**Drop Caps**:
```latex
\dropcapfirst{T}he wind came down from the mountains...
```

**Scene Breaks**:
```latex
\scenebreak
```
Produces: `. . . † . . .`

**Dialogue/Quote Styling**:
```latex
\dialogue{charAelindra}{\textit{``We should proceed,''} she said.}
```
Creates colored boxes matching the character's color.

## Customization

### Change Character Information
In the preamble, modify:
```latex
\definecolor{charAelindra}{HTML}{c8a84b}  % Change hex color
\newcommand{\charAelindraSym}{⚔}         % Change symbol
```

### Expand to More Characters
Add new colors and symbols, then use them in `\povmargin`:
```latex
\definecolor{charNewChar}{HTML}{hexcode}
\newcommand{\charNewCharSym}{symbol}
\povmargin{symbol}{Name}{charNewChar}
```

### Customize Landscape Banners
Edit `\landscapetop` and `\landscapebottom` commands to create custom TikZ drawings, or replace with `\includegraphics` for custom artwork.

### Adjust Colors
Main color palette (all in preamble):
- **Parchment background**: `#f5ede0`
- **Text (ink)**: `#1a1410`
- **Sepia accents**: `#7a5c3a`
- **Gold highlights**: `#c8a84b`
- **Chapter stripe**: `#2a1f14`

## Basic Document Structure

```latex
\documentclass{book}
% ... (preamble already set up)
\begin{document}

\chapter{Chapter Title}

\characterlegend
\landscapetop{LOCATION DESCRIPTION}

\povmargin{⚔}{Aelindra}{charAelindra}
\dropcapfirst{T}he story begins...

\dialogue{charDorian}{\textit{``Dialogue here,''} character said.}

\scenebreak

More narrative text...

\landscapebottom{LOCATION DESCRIPTION}

\end{document}
```

## Compilation

Compile with:
```bash
pdflatex stylish_book_template.tex
```

Or for better Unicode support:
```bash
xelatex stylish_book_template.tex
```

## File Structure

- `stylish_book_template.tex` — Main template file (ready to customize)
- `stylish_book_template.pdf` — Compiled example (10 pages with 3 sample chapters)

## Tips

1. **POV Changes Mid-Chapter**: You can call `\povmargin` multiple times in a chapter to indicate switches between perspectives.

2. **Colors**: Character colors should be distinct but harmonious. The template uses muted, literary tones.

3. **Banners**: Keep location descriptions brief (one line). They're visual anchors, not detailed descriptions.

4. **Line Spacing**: The template uses 1.85× line spacing for readability. Adjust `\setstretch{1.85}` if needed.

5. **Margins**: Wide left margin (1.5in) accommodates the chapter stripe + POV column. Adjust `geometry` package options if needed.

## Example Usage

See the compiled PDF for a complete working example with three chapters demonstrating:
- Character POV indicators
- Dialogue styling
- Scene breaks
- Landscape banners
- Character legend

---

**Created**: April 2026  
**Format**: LaTeX (pdflatex/xelatex compatible)  
**License**: Free to use and modify
