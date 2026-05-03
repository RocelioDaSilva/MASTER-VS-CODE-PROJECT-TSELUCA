# 2XKO Vi Guide - Image Setup Instructions

The LaTeX guide has been configured to include game screenshots and notation diagrams. This document explains how to populate the three image directories.

## Directory Structure

```
images/
├── notation/        # Button notation and UI reference images
├── moves/          # Individual move demonstration screenshots
└── combos/         # Combo sequence screenshots
```

## Required Images by Category

### 1. Notation Images (`images/notation/`)

**File:** `notation-reference.png` (or `.jpg`)
- Contains the complete 2XKO button notation layout
- Should show the button layout: L (Light), M (Medium), H (Heavy), S1, S2
- Numpad notation explanation (1-9, with 5 = neutral)
- **Source:** Grab from official 2XKO wiki or game manual

### 2. Normal Move Demonstrations (`images/moves/`)

Create game screenshots showing Vi performing each move:

- `vi-5l-jab.png` - Standing jab (fastest button)
- `vi-5h-heavy.png` - Standing heavy (launcher)
- `vi-6h-overhead.png` - Overhead attack
- `vi-2h-antiair.png` - Anti-air down-heavy
- `vi-footwork-sway.png` - Footwork/Sway dash in action
- `vi-vault-breaker.png` - Vault Breaker charged rush punch
- `vi-blast-shield.png` - Blast Shield parry counter
- `vi-crater-maker.png` - Crater Maker ground slam

### 3. Special Mechanics (`images/moves/`)

- `vi-footwork-combo.png` - Multiple consecutive Footwork dashes
- `vi-upper-normal.png` - Normal Upper attack
- `vi-upper-electric.png` - Electric Upper (with purple electrical effects)

**Tip:** Run Training Mode in 2XKO and use Print Screen to capture moves. Use photo editing software to crop to get clear, focused images of the action.

### 4. Combo Demonstrations (`images/combos/`)

Full-screen combo sequences:

- `combo-beginner-bnb.png` - Beginner BnB combo progression
  - Input: `5M > 5H > 6S1~L~M~H > 2S2`
  - Should show the full sequence frame by frame or as a breakdown

- `combo-limit-strike.png` - Limit Strike combo example
  - Shows the dash restart and wall slam portion

- `vi-combo-structure.png` - Diagram showing Vi's combo flow
  - Visual representation: Starter → Launcher → Rekka → OTG → Super

## Image Specifications

### Recommended Settings
- **Format:** PNG (lossless) or JPG (compressed)
- **Size:** 1280×720px minimum (720p) for clarity
- **Color:** No color correction needed - game colors are fine
- **Quality:** Ensure text/notation is readable at small sizes
- **Aspect Ratio:** 16:9 (standard widescreen)

### Scaling
- The LaTeX will scale images to fit available space
- Wider images work better (landscape orientation)
- Test how they look when compiled by running `pdflatex Vishit.tex`

## How to Obtain Images

### Option 1: Capture from Game
1. Launch 2XKO Training Mode
2. Select Vi as character
3. Practice the moves/combos shown
4. Use **Print Screen** to capture
5. Edit in Paint/Photoshop to crop and enhance

### Option 2: Official Sources
- **2XKO Wiki:** https://wiki.play2xko.com/en-us/Ekko/Starter_Guide
- **Game Manual:** Check official 2XKO documentation
- **Video Guides:** Screenshot high-quality YouTube guides
- **Official Site:** https://2xko.riotgames.com/en-us/champions/ekko/

### Option 3: Community Content
- Check Mobalytics (mobalytics.gg/2xko/champions/ekko)
- Games.gg guides (games.gg/2xko/guides/)
- Look for high-resolution guide screenshots

## File Naming Convention

- Use lowercase with hyphens: `vi-5l-jab.png` (NOT `Vi 5L Jab.png`)
- Be descriptive: `combo-corner-bnb-full.png` (not `combo1.png`)
- No spaces in filenames
- Include image category in name when relevant

## LaTeX Commands Already Configured

The following are ready to use in the document:

```latex
\includegraphics[width=0.4\textwidth]{notation-reference}
\includegraphics[width=0.7\textwidth]{vi-footwork-combo}
\includegraphics[width=0.95\textwidth]{combo-beginner-bnb}
```

Graphics are automatically resolved from the image directories.

## Testing Your Setup

1. Place PNG/JPG files in appropriate `images/` subdirectories
2. Run: `pdflatex Vishit.tex`
3. Check the generated PDF for image placement
4. If images don't appear, verify:
   - File name matches exactly (case-sensitive on Linux)
   - File exists in correct directory
   - File format is PNG or JPG
   - No spaces or special characters in filename

## Troubleshooting

**Images not appearing in PDF:**
- Check file extension matches what's referenced (`.png` vs `.jpg`)
- Verify file exists in the correct directory
- Ensure filename matches exactly in LaTeX (case-sensitive on some systems)

**Images look blurry:**
- Use higher resolution source images (1280×720 minimum)
- Reduce `width` parameter in LaTeX if image is small

**PDF won't compile:**
- Remove problematic image from LaTeX temporarily
- Check for special characters in paths
- Ensure no circular dependencies

## Optional Enhancements

Once basic images are in place, consider adding:

- **GIF sequences** (some PDF viewers support these)
- **Annotated images** with arrows/text overlays
- **Frame-by-frame breakdown** of complex combos
- **Hitbox visualizations** from game training mode
- **Matchup diagrams** showing favorable/unfavorable matchups

## Contact & Attribution

If using community-created images, ensure proper attribution:
- Credit the source (Mobalytics, Games.gg, streamers, etc.)
- Follow copyright guidelines
- Consider linking to original sources in the guide

---

**Last Updated:** March 2026
**Guide Author:** Vi 2XKO Comprehensive Guide
**Requires:** All subdirectories must have at least placeholder images for LaTeX to compile cleanly
