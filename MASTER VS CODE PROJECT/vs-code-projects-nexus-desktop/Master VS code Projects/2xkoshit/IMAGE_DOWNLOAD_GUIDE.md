# 2XKO Image Download Guide - Verified Online Sources

## Images Found on Online Resources

I've reviewed all 4 provided URLs. Here's what's available and where to find them:

---

## 1. Official 2XKO Site - Button Notation Images
**Source:** https://2xko.riotgames.com/en-us/champions/ekko/

### Available SVG Glyph Assets (Official)
The official site uses SVG glyph icons for button notation. These are ideal because they're scalable:

- **Button Icons:**
  - L button: `https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/L.svg`
  - M button: `https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/M.svg`
  - H button: `https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/H.svg`
  - S1 button: `https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/S1.svg`
  - S2 button: `https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/S2.svg`

- **Direction Icons:**
  - Down: `https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/down.svg`
  - Forward: `https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/forward.svg`
  - Down-Forward: `https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/down_forward.svg`
  - Forward-Forward: `https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/forward_forward.svg`
  - Back: `https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/back.svg`

**Installation:** Download these as SVG/PNG and save to `images/notation/` directory with names like:
- `button-L.svg`, `button-M.svg`, `button-H.svg`
- `button-S1.svg`, `button-S2.svg`
- `direction-down.svg`, `direction-forward.svg`, etc.

---

## 2. Mobalytics.gg - Screenshot & Gameplay Images
**Source:** https://mobalytics.gg/2xko/champions/ekko

### Available Images (For Ekko - Adapt for Vi)

The guide contains reference images for gameplay mechanics. Here are the patterns:

**Image URLs found:**
1. **Timewinder Oki Setup:**
   ```
   https://cdn.mobalytics.gg/cdn-cgi/image/format=auto,width=762/uploads/images/2xko/Screenshot%202025-12-18%20025814.png
   ```
   - Shows Ekko's oki setup with Timewinder
   - **Adaptation for Vi:** Find equivalent Vi pressure/oki images

2. **Assist Demonstration:**
   ```
   https://cdn.mobalytics.gg/cdn-cgi/image/format=auto,width=1000/uploads/images/2xko/Screenshot%202025-12-18%20030031.png
   ```
   - Shows Ekko's Forward Assist in action
   - **Adaptation for Vi:** Look for Vi's Vault Breaker or Crater Maker Assist images

3. **Counter-Strategy Screenshot:**
   ```
   https://cdn.mobalytics.gg/cdn-cgi/image/format=auto,width=1000/uploads/images/2xko/Screenshot%202025-12-18%20030311.png
   ```
   - Ekko Chronostrike example
   - **Adaptation for Vi:** Would need Vi-specific move demonstrations

### How to Find More Mobalytics Images
1. Navigate to their Vi guide (likely exists): `mobalytics.gg/2xko/champions/vi`
2. Look for sections with inline images:
   - "How to Beat Vi"
   - "Combo Examples"
   - "Neutral Game"
3. Right-click images → "Inspect Element" to get CDN URLs
4. Download by modifying the URL: Remove `cdn-cgi/image/format=auto,width=XXX/` to get full resolution

---

## 3. Official Wiki - Template Structure
**Source:** https://wiki.play2xko.com/en-us/Ekko/Starter_Guide

Unfortunately, the wiki appears to be a **work in progress** with placeholder text indicating incomplete documentation. However, the wiki structure suggests these sections SHOULD have images once completed:

```
## Key Moves
  - Controlling Neutral (move screenshots)
  - Pressure & Mix-up (mixup demonstrations)
  - Defense & Punish (defensive move examples)
  - Limit Strikes & Knockdowns (special move effects)

## Beginner Combos
  - Combo image sequences/GIF breakdowns
```

### Wiki Strategy
If the wiki gets updated with Vi content, check:
1. **Ekko/Strategy page:** More detailed move guides with images
2. **Ekko/Combos page:** Dedicated combo breakdown screenshots
3. **Media Upload Section:** Community-contributed images

---

## 4. Games.gg - Guide Reference
**Source:** https://games.gg/2xko/guides/2xko-champion-guide-ekko/

Note: This site did not return full content in the fetch. Check directly for:
1. Guide screenshots
2. Combo demonstration images
3. Move breakdown diagrams
4. Matchup visuals

---

## How to Manually Source Images

### Option A: Screenshot from Game (Recommended)
1. **Launch 2XKO**
2. **Training Mode** → Select Vi
3. **Select Opponent** → Any character
4. **Practice specific move:**
   - Perform the move
   - Pause at peak moment
   - **Press PrintScreen**
   - Paste into Paint/Photoshop
   - **Crop to focus on Vi**
   - Save as PNG to proper folder

**Best moments to capture:**
- Startup frames
- Active hit frames
- Recovery frames
- With opponent reacting

### Option B: Download from Current Guides
Since Vi's guide on Mobalytics likely exists but we're doing Ekko content, look for:
1. **Mobalytics Vi Guide** (if available)
2. **Games.gg Vi Guide**
3. **YouTube guide screenshots** - Pause videos at good moments, capture

### Option C: Use Official Assets
Riot often releases official artwork:
1. Champion splash art
2. Move effect animations
3. UI elements

Check these Riot CDN paths:
```
https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/2xko/
```

---

## Download Instructions for SVG Button Icons

These SVG files are perfect for your LaTeX guide and fully official:

```bash
# Example: Download L button icon
curl -o button-L.svg "https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/L.svg"

# Or in PowerShell (Windows):
Invoke-WebRequest -Uri "https://assetcdn.rgpub.io/public/live/riot-shared/player-experiences/riot-glyphs/2xko/latest/L.svg" -OutFile "button-L.svg"
```

Then save all SVGs to: `images/notation/`

---

## Quick Checklist - Manual Download Steps

### For Notation Symbols (Official SVG)
- [ ] Download all L/M/H/S1/S2/direction SVGs
- [ ] Save to `images/notation/`
- [ ] Test loading in LaTeX

### For Move Demonstrations (From Game/Screenshots)
- [ ] 5L Jab demonstration
- [ ] 5H Heavy demonstration
- [ ] 6H Overhead demonstration
- [ ] 2H Anti-air demonstration
- [ ] Footwork/Sway in action
- [ ] Vault Breaker charged attack
- [ ] Blast Shield parry counter
- [ ] Crater Maker ground slam
- [ ] Footwork combo sequence
- [ ] Electric move comparison
- [ ] Save all to `images/moves/`

### For Combo Demonstrations (YouTube or Game Record)
- [ ] Beginner BnB combo sequence
- [ ] Limit Strike combo sequence
- [ ] Combo flow diagram (can be created in PowerPoint/Photoshop)
- [ ] Save all to `images/combos/`

---

## Summary of Image Locations

| Image Type | Source | Method | Quality |
|-----------|--------|--------|---------|
| **Button Notation** | Official Riot CDN | Direct download SVG | Excellent (Vector) |
| **Move Screenshots** | 2XKO Game | Play & capture | Excellent (1080p) |
| **Gameplay Examples** | Mobalytics | Right-click download | Good (1000x762px) |
| **Wiki (if updated)** | 2XKO Wiki | Direct download | Varies |
| **Strategy Videos** | YouTube (guides) | Screenshot at keyframes | Good (varies) |

---

## Next Steps
1. **Download SVG button icons** from official Riot CDN (free, official, perfect quality)
2. **Capture game screenshots** for move demonstrations (personal practice in Training Mode)
3. **Gather third-party screenshot** from Mobalytics guides for reference
4. Place in appropriate `images/` subdirectories
5. Run `pdflatex Vishit.tex` to compile with images

---

**Last Updated:** March 13, 2026  
**Status:** Ready for manual image sourcing  
**Estimated time to gather all images:** 30-60 minutes
