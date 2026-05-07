# Visual Button Notation System - 2XKO Guides

## Overview
Both Ekkoshit.tex (Ekko guide) and Vishit.tex (Vi guide) now feature **visual, colored button notation** that replaces text-only input descriptions. This creates a more intuitive and visually appealing representation of controller inputs.

## Button Display System

### Visual Elements

#### Character-Themed Button Colors
- **Ekkoshit (Ekko)**: Cyan Blue (#00D4FF) with dark background boxes
- **Vishit (Vi)**: Hot Pink (#FF69B4) with dark background boxes

#### Button Types

Each button is displayed as a **bordered box** with character color:

```
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│  L  │  │  M  │  │  H  │  │  T  │
└─────┘  └─────┘  └─────┘  └─────┘
Light    Medium   Heavy    Throw

┌──────┐  ┌──────┐  ┌─┐  ┌─┐
│  S1  │  │  S2  │  │↓│  │→│
└──────┘  └──────┘  └─┘  └─┘
Super 1   Super 2   Down  Forward
```

### Notation Commands (LaTeX)

#### Button Input Commands
- `\btnL` → Light button (boxed)
- `\btnM` → Medium button (boxed)
- `\btnH` → Heavy button (boxed)
- `\btnS{1}` → Super 1 button (boxed)
- `\btnS{2}` → Super 2 button (boxed)
- `\btnT` → Throw button (boxed)

#### Direction Commands
- `\dirDown` → ↓ Down (boxed)
- `\dirForward` → → Forward (boxed)
- `\dirBack` → ← Back (boxed)
- `\dirUp` → ↑ Up (boxed)

#### Connector Symbols
- `\plus` → + (Gold, unboxed)
- `\arrow` → > (Gold, unboxed)

### Example Combo Display

**In LaTeX source:**
```latex
\dirDown\btnL \arrow \dirDown\btnM \arrow 
\dirDown\btnH \arrow \dirUp\btnM \arrow \dirUp\btnH
```

**In PDF:**
```
┌─┐ 
│↓│┌─────┐    ┌─┐┌─────┐    ┌─┐┌─────┐    ┌─┐┌─────┐    ┌─┐┌─────┐
└─┘│  L  │>   │↓││  M  │>   │↓││  H  │>   │↑││  M  │>   │↑││  H  │
   └─────┘    └─┘└─────┘    └─┘└─────┘    └─┘└─────┘    └─┘└─────┘
```

## Reference Table - Button Notation Guide

Both guides include a **visual button reference table** showing:
- All standard buttons (L, M, H, S1, S2, T)
- All directional inputs (↓, →, ↑, ←)
- Connector symbols (+, >)

This table appears in Chapter 2 (Move List Reference) under "Notation Guide".

## Key Features

✅ **Visually Distinct**: Bordered boxes make buttons stand out from text
✅ **Color-Coded**: Character-specific colors (Ekko = Blue, Vi = Pink)
✅ **Scalable**: Text-based rendering scales perfectly in PDF
✅ **Consistent**: Same notation used throughout both guides
✅ **Readable**: High contrast between button and background
✅ **Character-Branding**: Visual style matches each champion's aesthetic

## Implementation Details

### Ekkoshit.tex (Ekko Guide)
- Primary Color: ekkoBlue (#00D4FF)
- Accent Color: ekkoGold (#FFD700)
- Box Background: tablerow (#0F0F28)
- Button Style: `\fcolorbox{ekkoGray}{tablerow}{...}`

### Vishit.tex (Vi Guide)
- Primary Color: viPink (#FF69B4)
- Accent Color: viGold (#FFD700)
- Box Background: tablerow (#150815)
- Button Style: `\fcolorbox{viGray}{tablerow}{...}`

## Combo Sections

All combo inputs throughout the guides now use this visual notation system:

- **Beginner Combos**: Foundational sequences with clear notation
- **Intermediate Combos**: Advanced techniques with mixed inputs
- **Advanced Combos**: Complex sequences with directionality emphasis
- **Team Combos**: Partner-specific routines

Examples:
- Ekko: "Pulse Combo — Ground Starters"
- Vi: "Beginner BnB - Anywhere"
- Both: Full visual input sequences with button boxes and directions

## Notes for User

- **No Image Dependencies**: The button notation works without external image files
- **Universal Rendering**: Displays identically across all PDF viewers
- **Customizable**: Easy to adjust colors or sizing in LaTeX source
- **Future-Ready**: When actual gameplay screenshots are available, they can replace the placeholder images while keeping this notation system

## Compiled PDFs

- `Ekkoshit.pdf` (457.8 KB) - Updated 13:31:11
- `Vishit.pdf` (523.1 KB) - Updated 13:31:32

Both files regenerated with complete visual button notation system.
