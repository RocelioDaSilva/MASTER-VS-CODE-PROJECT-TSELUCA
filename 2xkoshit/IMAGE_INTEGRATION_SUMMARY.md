# Vi 2XKO Guide - Image Integration Summary

## What's Been Done ✓

Your `Vishit.tex` LaTeX file has been configured to include:

### 1. Image Directory Structure Created
```
images/
├── notation/     (for 2XKO button notation reference)
├── moves/        (for individual move demonstrations)
└── combos/       (for complete combo sequences)
```

Each directory contains a `README.txt` with specific image requirements.

### 2. LaTeX Configured for Graphics
- Added `\graphicspath` to search all image directories
- Added `\usepackage{graphicx}` for image support
- Added `\usepackage{caption}` for figure labeling
- Configured with proper color scheme (viPink, viGold, etc.)

### 3. Strategic Image Placeholders Added Throughout Guide
- **Notation Section:** Main 2XKO button diagram
- **Normal Moves:** 4 move demonstration images
- **Special Moves:** 4 key technique images  
- **Footwork System:** Dash sequence visualization
- **Electrics:** Normal vs Electric comparison
- **Combos:** 3 full combo breakdowns with flow diagram

### 4. Documentation Created
- `IMAGES_GUIDE.md` - Complete image setup instructions
- `images/notation/README.txt` - Notation image specs
- `images/moves/README.txt` - Move screenshot specs
- `images/combos/README.txt` - Combo demonstration specs

## Next Steps - Image Acquisition

### Quick Start (30 minutes)
1. Go to https://wiki.play2xko.com/en-us/Ekko/Starter_Guide
2. Screenshot the button notation diagram → save to `images/notation/notation-reference.png`
3. Launch 2XKO Training Mode
4. Practice each move and collect 11 screenshots (see `images/moves/README.txt`)
5. Create 3 combo demonstration images (see `images/combos/README.txt`)

### Recommended Sources
- **Official:** https://2xko.riotgames.com/en-us/champions/ekko/
- **Wiki:** https://wiki.play2xko.com/en-us/Ekko/Starter_Guide
- **Guides:** Mobalytics.gg, Games.gg for reference images
- **Game:** Best source for move screenshots - use Training Mode

## File Checklist for Complete Integration

### Notation Images (1 required)
- [ ] `notation-reference.png` - 2XKO button layout

### Move Images (11 required)
- [ ] `vi-5l-jab.png`
- [ ] `vi-5h-heavy.png`
- [ ] `vi-6h-overhead.png`
- [ ] `vi-2h-antiair.png`
- [ ] `vi-footwork-sway.png`
- [ ] `vi-vault-breaker.png`
- [ ] `vi-blast-shield.png`
- [ ] `vi-crater-maker.png`
- [ ] `vi-footwork-combo.png`
- [ ] `vi-upper-normal.png`
- [ ] `vi-upper-electric.png`

### Combo Images (3 required)
- [ ] `vi-combo-structure.png` - Flow diagram
- [ ] `combo-beginner-bnb.png` - Basic BnB combo
- [ ] `combo-limit-strike.png` - Limit strike combo

**Total: 15 images for complete integration**

## Compilation

Once you have images ready:

```bash
pdflatex Vishit.tex
```

The PDF will automatically include all image references. If an image file is missing, LaTeX will:
- Skip that image
- Show a warning in console output
- Continue compilation with a placeholder

## Image Standards

**Recommended Specifications:**
- Format: PNG (lossless) for best quality
- Resolution: 1280×720px or higher
- Color: Keep game colors intact
- Size: 100-300 KB per image
- Aspect Ratio: 16:9 (widescreen)

**Naming Convention:**
- Lowercase with hyphens
- Descriptive names (not `img1.png`)
- No spaces or special characters

## Troubleshooting

**Images not showing in PDF?**
1. Verify file exists in correct directory
2. Check filename matches exactly (case-sensitive on Linux/Mac)
3. Ensure format is PNG or JPG
4. Check terminal for error messages while compiling

**Images too small/large?**
- Adjust `width` parameter in LaTeX
- Current: `[width=0.4\textwidth]` to `[width=0.95\textwidth]`
- Recompile after changes

**Can't capture screenshots?**
- Alternative: Find high-res screenshots from Mobalytics or Games.gg
- Ask community for screenshot contributions
- Use existing YouTube guide videos as reference

## Current State

Your Vishit.tex is **ready for images**. All structural changes are done:
- ✓ Graphics paths configured
- ✓ Image inclusion commands added
- ✓ Proper formatting/styling set up
- ✓ Documentation provided
- ⏳ Now waiting for: Actual image files in `images/` directories

## File Organization Reference

```
2xkoshit/
├── Vishit.tex              (Main guide - UPDATED ✓)
├── IMAGES_GUIDE.md         (How to find/create images)
├── images/
│   ├── notation/
│   │   ├── README.txt
│   │   └── notification-reference.png (ADD HERE)
│   ├── moves/
│   │   ├── README.txt
│   │   ├── vi-5l-jab.png (ADD HERE)
│   │   ├── vi-5h-heavy.png (ADD HERE)
│   │   └── ... (8 more move images)
│   └── combos/
│       ├── README.txt
│       ├── vi-combo-structure.png (ADD HERE)
│       ├── combo-beginner-bnb.png (ADD HERE)
│       └── combo-limit-strike.png (ADD HERE)
└── Vishit.pdf              (Generated output)
```

## Contact Points for Images

The guide references 4 URLs you provided for image sourcing:
1. https://mobalytics.gg/2xko/champions/ekko
2. https://games.gg/2xko/guides/2xko-champion-guide-ekko/
3. https://wiki.play2xko.com/en-us/Ekko/Starter_Guide
4. https://2xko.riotgames.com/en-us/champions/ekko/

**Priority for image capture:**
1. Official 2XKO website (#4)
2. Community wiki (#3)
3. Third-party guides (#1, #2) - note attribution

---

**Status:** LaTeX integration complete. Ready to populate with images.
**Last Updated:** March 13, 2026
