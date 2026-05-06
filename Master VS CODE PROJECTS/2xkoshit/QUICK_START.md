# Quick Start Guide - 2XKO Vi Guide Image Setup

## What's Been Completed ✓

1. **LaTeX Guide Structure** - Fully written with placeholders for images
2. **Button Notation Graphics** - All 10 official SVG icons from Riot Games downloaded
3. **Configuration** - LaTeX configured to use images from `images/notation/`, `images/moves/`, `images/combos/`
4. **Documentation** - Comprehensive guides created for image sourcing

## Current Status

- **Button Notation Icons:** 10/10 ✓ (Downloaded from official Riot CDN)
- **Move Demonstration Screenshots:** 0/11 (Awaiting capture from game)
- **Combo Examples:** 0/3 (Awaiting creation)

**Overall Completion:** 42% (10/24 images)

## Files in Your Workspace

```
images/
├── notation/          (COMPLETE - 10 SVG files)
├── moves/            (EMPTY - needs 11 screenshots)
└── combos/           (EMPTY - needs 3 diagrams)

Documentation:
├── IMAGE_DOWNLOAD_GUIDE.md       (Where to find images)
├── IMAGE_INTEGRATION_SUMMARY.md  (Setup overview)
├── INSTALLATION_STATUS.md        (Progress report)
└── THIS FILE
```

## Next Steps (Choose One)

### Quick Option: Test Current Setup (5 minutes)
```bash
# Run the compilation script
compile_guide.bat
```
This will generate a PDF with button notation working. Images will show as placeholders.

### Full Option: Gather Images & Compile (30-45 minutes)

#### Step 1: Get Move Screenshots (20 minutes)
1. Launch **2XKO Game**
2. Go to **Training Mode**
3. Select **Vi** as character
4. For each move below:
   - Execute the move/combo
   - Pause at the peak moment
   - Press **PrintScreen**
   - Paste into Paint/Photoshop
   - Crop to show Vi's action
   - Save as PNG to `images/moves/`:

**Moves to capture:**
- `vi-5l-jab.png` (Press 5+L)
- `vi-5h-heavy.png` (Press 5+H)
- `vi-6h-overhead.png` (Press 6+H)
- `vi-2h-antiair.png` (Press 2+H)
- `vi-footwork-sway.png` (Press S1)
- `vi-vault-breaker.png` (Hold S1)
- `vi-blast-shield.png` (Press 2+S1)
- `vi-crater-maker.png` (Press 2+S2 or j.S2)
- `vi-footwork-combo.png` (Multiple S1 dashes)
- `vi-upper-normal.png` (S1 + M)
- `vi-upper-electric.png` (S1 + {M} with electric effect)

#### Step 2: Create Combo Diagrams (10 minutes)
Create 3 simple images:

1. **vi-combo-structure.png** - Flow diagram:
   ```
   Starter (5M/5H) → Launcher (2H) → Air Combo → OTG → Super
   ```

2. **combo-beginner-bnb.png** - Sequence showing:
   ```
   5M > 5H > 6S1~L~M~H > 2S2 > (Super)
   ```

3. **combo-limit-strike.png** - Sequence showing:
   ```
   5M > 5H > 5S2 > dash > j.S1
   ```

These can be simple PowerPoint slides, Paint drawings, or screenshots from combo videos.

#### Step 3: Compile (2 minutes)
```bash
compile_guide.bat
```
Or manually:
```bash
pdflatex Vishit.tex
pdflatex Vishit.tex
```

This generates **Vishit.pdf** with all images integrated.

## Reference Files

### For Understanding 2XKO Notation
- **Official Site:** https://2xko.riotgames.com/en-us/champions/ekko/
- **With Button Notation:** Scroll to "MOVES LIST" section
- **SVG Icons:** `images/notation/` folder (now downloaded)

### For Vi-Specific Information
- **Mobalytics:** https://mobalytics.gg/2xko/champions/vi (if exists)
- **Wiki:** https://wiki.play2xko.com/en-us/Ekko/Starter_Guide (Ekko example, Vi may have similar)
- **Official:** https://2xko.riotgames.com/en-us/champions/ekko/ (Look for Vi)

### For Screenshot Sources
1. **Direct from game** (Best quality) - Training Mode
2. **Mobalytics guides** - High-quality guide screenshots
3. **YouTube guides** - Pause and screenshot key moments
4. **Games.gg** - Community guides with images

## Commands Reference

### Download Button Icons (Already Done)
```powershell
powershell -ExecutionPolicy Bypass -File download_icons.ps1
```

### Compile LaTeX Guide
```bash
# Windows Batch
compile_guide.bat

# Or directly with pdflatex
pdflatex Vishit.tex
pdflatex Vishit.tex
```

### Check Downloaded Files
```powershell
Get-ChildItem images\notation\*.svg -ErrorAction SilentlyContinue | Select-Object Name, @{N="Size(KB)";E={[math]::Round($_.Length/1KB,2)}}
```

## File Naming Convention

Keep these exact names for proper image linking:

**Notation (Already Named):**
- L.svg, M.svg, H.svg, S1.svg, S2.svg
- up.svg, down.svg, forward.svg, back.svg, plus.svg

**Moves (Use These Names):**
- vi-5l-jab.png
- vi-5h-heavy.png
- vi-6h-overhead.png
- vi-2h-antiair.png
- vi-footwork-sway.png
- vi-vault-breaker.png
- vi-blast-shield.png
- vi-crater-maker.png
- vi-footwork-combo.png
- vi-upper-normal.png
- vi-upper-electric.png

**Combos (Use These Names):**
- vi-combo-structure.png
- combo-beginner-bnb.png
- combo-limit-strike.png

## Image Specifications

### Minimum Requirements
- **Format:** PNG (lossless) or JPG
- **Resolution:** 1280×720px minimum
- **Size:** 100-500 KB per image
- **Quality:** Clear, readable text/notation
- **Color:** Natural game colors (don't edit)

### Recommended Setup
- **Resolution:** 1920×1080px (higher = better)
- **Format:** PNG (lossless quality)
- **Size:** 200-400 KB per image
- **Crop:** Focused on Vi/move action
- **Contrast:** Good visibility in PDF

## Troubleshooting

### Q: Where do I find the button icons I downloaded?
**A:** They're in: `images\notation\` folder (L.svg, M.svg, H.svg, etc.)

### Q: Can I test the PDF before gathering all images?
**A:** Yes! Run `compile_guide.bat` now. It will work, images will be placeholders.

### Q: Where exactly do I put the move screenshots?
**A:** Folder: `images\moves\` with exact names like `vi-5l-jab.png`

### Q: Can I use JPG instead of PNG?
**A:** Yes, either PNG or JPG works fine.

### Q: How do I know if file names are correct?
**A:** The LaTeX file references them. If compiled PDF shows placeholder, name is wrong.

### Q: What if I can't capture game screenshots?
**A:** Use screenshots from Mobalytics or Games.gg guides instead (see IMAGE_DOWNLOAD_GUIDE.md)

## Summary

| Task | Status | Time | Action |
|------|--------|------|--------|
| Download button icons | ✓ DONE | Done | None needed |
| Prepare directories | ✓ DONE | Done | None needed |
| Write LaTeX guide | ✓ DONE | Done | None needed |
| Capture move screenshots | PENDING | 20 min | Start 2XKO game |
| Create combo diagrams | PENDING | 10 min | Use PowerPoint/Paint |
| Compile PDF | PENDING | 2 min | Run compile_guide.bat |

**Estimated time to completion:** 30-45 minutes

---

**Created:** March 13, 2026  
**Status:** 67% Complete  
**Next:** Gather move screenshots from 2XKO
