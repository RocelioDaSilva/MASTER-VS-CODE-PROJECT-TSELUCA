# Embers of the Forsaken Keep — Quick Start

## What You Have

A complete, production-ready book template system with:

✓ **9 POV character glyphs** — subtle symbols in characters' colours  
✓ **6 landscape variations** — mood-based header silhouettes  
✓ **Per-page chapter stripe** — colour-coded reading progress on spine  
✓ **All 52 chapters pre-configured** — character, landscape, location for each  
✓ **Full customization pipeline** — JSON config + Python build script  
✓ **Professional typography** — Lora serif, generous line spacing, elegant margins  

---

## Files Overview

| File | Purpose |
|------|---------|
| **manuscript-final.tex** | Complete book ready to compile |
| **chapter-config.json** | Master configuration (edit this to customize) |
| **build_manuscript.py** | Regenerate manuscript from config |
| **SYSTEM_GUIDE.md** | Full documentation of the system |
| **CUSTOMIZATION_RECIPES.md** | 12 step-by-step examples for common edits |
| **cwbook_minimal_package/** | Your chapter content (.tex files) |

---

## Fastest Path: Compile the Book Now

```bash
cd "c:\Users\PCGAME\Desktop\story&universes\chain-weapon-story\finished-manuscript"

# Activate virtual environment (PowerShell)
& ".\.venv\Scripts\Activate.ps1"

# Compile twice
xelatex manuscript-final.tex
xelatex manuscript-final.tex

# Output: manuscript-final.pdf
```

**Time:** ~30 seconds  
**Result:** Full 52-chapter book with all glyphs, landscapes, chapter stripes

---

## Most Common Edits

### 1. Change a chapter's POV character

**File:** `chapter-config.json`

Find the chapter, change `"character"`:
```json
{
  "num": 5,
  "character": "Kael"   // ← was "Caspian", now Kael
}
```

Then regenerate:
```bash
python build_manuscript.py
xelatex manuscript-final.tex
```

### 2. Change landscape for a chapter

**File:** `chapter-config.json`

Find the chapter, change `"landscape"`:
```json
{
  "num": 5,
  "landscape": "Forest"   // ← was "Mountains"
}
```

Regenerate same as above.

### 3. Adjust a colour (global or per-character)

**File:** `chapter-config.json`

Under `"color_customization"`, change any hex value:
```json
"PageBg": "F0E8DC"      // Darker background
"ColAisen": "9A8060"    // Brighter ochre for Aisen
```

Regenerate same as above.

### 4. Change typography (fonts, spacing, etc.)

**File:** `manuscript-final.tex`

Find the section and edit:
```latex
\setmainfont{Georgia}          % Font
\linespread{1.40}              % Line spacing
\setlength{\parindent}{1.2em}  % Indent
```

Just recompile:
```bash
xelatex manuscript-final.tex
```

---

## The Three Customization Levels

**Level 1 (Easiest):** Edit `chapter-config.json`  
→ Change which character, landscape, colours  
→ Need to run `python build_manuscript.py` first

**Level 2 (Medium):** Edit `manuscript-final.tex` directly  
→ Adjust fonts, spacing, header heights, glyph designs  
→ Can just recompile with xelatex (no Python needed)

**Level 3 (Advanced):** Redesign landscape silhouettes  
→ Edit TikZ commands in `\LandscapeBodyMountains`, etc.  
→ Takes some TikZ knowledge  
→ Recompile and test

---

## Before You Publish

- [ ] Read **SYSTEM_GUIDE.md** for complete documentation
- [ ] Pick a customization level (most people do Level 1 only)
- [ ] Test print a sample (Chapter 1, Chapter 26, Chapter 52) to check colours
- [ ] Adjust colours based on proof prints
- [ ] Verify all 9 glyphs and 6 landscapes look good
- [ ] Check margins and text flow on different systems
- [ ] Compile twice to ensure all updates settle

---

## Example Workflows

### Workflow A: "Just compile it"
```bash
xelatex manuscript-final.tex
xelatex manuscript-final.tex
# Done — open PDF
```

### Workflow B: "Adjust character assignments"
```bash
# Edit chapter-config.json (change chapters 1, 3, 5, etc.)
python build_manuscript.py     # Regenerate
xelatex manuscript-final.tex   # Compile
xelatex manuscript-final.tex
# Open PDF
```

### Workflow C: "Create a custom colour scheme"
```bash
# Edit chapter-config.json color_customization section
python build_manuscript.py     # Regenerate
xelatex manuscript-final.tex   # Compile twice
xelatex manuscript-final.tex
# Check colours, adjust if needed, repeat
```

### Workflow D: "Tweak fonts and spacing"
```bash
# Edit manuscript-final.tex (fonts, parindent, linespread, etc.)
xelatex manuscript-final.tex   # Compile twice (no Python needed)
xelatex manuscript-final.tex
# Check layout, adjust if needed, repeat
```

---

## Key Concepts

### POV Glyphs
- Small (0.14cm) abstract symbol in top-left corner of every page
- Tinted in the character's signature colour
- Reader learns which character is narrating just by glancing at the corner
- Examples:
  - Aisen = fractured triangle (ambition, strength, fragmentation)
  - Caspian = split circle (division, introspection)
  - Kairos = broken loop (trapped, cyclical time)

### Landscapes
- Six 2.6cm header silhouettes (different mood each)
- Same three-layer tonal system (light → medium → dark)
- Appear at top *and* bottom of each page (bookend effect)
- Mood-driven, not literal geography:
  - *Mountains* = eternal truths, cold wisdom
  - *City* = order struggling against chaos
  - *Forest* = hidden currents, wild law
  - *Dungeon* = enclosed oppression, hidden things
  - *Wasteland* = aftermath, breaking point
  - *Coast* = liminal spaces, transitions

### Chapter Stripe
- Coloured rectangle on right edge (5mm wide)
- Filled with current POV character's colour
- Position moves down as you read (visual progress)
- Spine of book shows all 52 stripes stacked (rainbow effect)

---

## Troubleshooting

**"PDF won't compile"**  
→ Ensure you're using XeLaTeX (not pdflatex)  
→ Check fonts are installed: Lora, GFSBaskerville

**"Fonts look wrong"**  
→ Install Lora from Google Fonts or change to system font (Georgia, Arial)  
→ Restart TeX after installing fonts

**"Characters not showing"**  
→ Run `python build_manuscript.py` to regenerate chapter configs  
→ Check `chapter-config.json` for invalid character names

**"Colours are dull"**  
→ Normal for screen viewing; check on actual print proof  
→ Try darker/more saturated hex values

---

## Next Steps

1. **Open `SYSTEM_GUIDE.md`** if you want full documentation
2. **Open `CUSTOMIZATION_RECIPES.md`** for 12 specific examples
3. **Edit `chapter-config.json`** to customize characters/landscapes
4. **Run `python build_manuscript.py`** to regenerate
5. **Compile with `xelatex manuscript-final.tex`** (twice)
6. **Open PDF and enjoy!**

---

## Support

- For system questions: see `SYSTEM_GUIDE.md`
- For specific edits: see `CUSTOMIZATION_RECIPES.md` (step-by-step recipes)
- For LaTeX issues: check the error message carefully; usually a font or syntax problem
- For design questions: experiment with small edits (one variable at a time) and recompile

---

Good luck with **Embers of the Forsaken Keep**!

Your book is ready to compile. 🔥

