---
Title: Export Guide - PDF & EPUB
Status: Instructions for converting manuscript to publication formats
Date: April 4, 2026
---

# EXPORT GUIDE: Chain Weapon Story

Your manuscript is ready for export to PDF and EPUB formats. The master narrative file is prepared and ready:

**File:** `story/MASTER-NARRATIVE-FULL.md`
**Status:** Complete (1,700+ lines, ~15,000 words new content)
**Format:** Markdown (universally convertible)

---

## OPTION 1: Online Conversion Tools (Easiest)

### Using Pandoc Online (https://pandoc.org/try/)

1. Open: https://pandoc.org/try/
2. Copy entire contents of `story/MASTER-NARRATIVE-FULL.md`
3. Paste into "INPUT" panel
4. Change "Input format" to: **Markdown**
5. Change "Output format" to: **PDF** or **EPUB3**
6. Click "Convert"
7. Download result

**Time required:** 5 minutes
**Cost:** Free
**Quality:** Excellent

### Using CloudConvert (https://cloudconvert.com/)

1. Upload `story/MASTER-NARRATIVE-FULL.md`
2. Select format: Markdown
3. Output: PDF or EPUB
4. Download files

**Time required:** 2 minutes
**Cost:** Free (up to 250 conversions/day)
**Quality:** Excellent

---

## OPTION 2: Local Installation (Best for Batch Processing)

### Install Pandoc

**Requirements:**
- Windows 10+
- Administrator access
- ~200MB disk space

**Installation Steps:**

1. Download from: https://github.com/jgm/pandoc/releases/latest
   - Look for: `pandoc-X.X-windows-x86_64.msi`

2. Run installer (accept all defaults)

3. Verify installation:
   ```powershell
   pandoc --version
   ```

4. Convert to PDF:
   ```powershell
   cd "c:\Users\PCGAME\Desktop\story&universes\chain-weapon-story\story"
   pandoc MASTER-NARRATIVE-FULL.md -f markdown -t pdf -o ChainWeapon-Story.pdf
   ```

5. Convert to EPUB:
   ```powershell
   pandoc MASTER-NARRATIVE-FULL.md -f markdown -t epub -o ChainWeapon-Story.epub
   ```

**Time required:** 10 minutes (installation) + 1 minute (conversion)
**Cost:** Free
**Quality:** Professional

---

## OPTION 3: Advanced PDF Export with Styling

If you want professional formatting with custom fonts, colors, and layout:

### Using Pandoc with CSS

1. Install pandoc (Option 2 above)

2. Create styling file (`style.css`):
   ```css
   body {
       font-family: 'Garamond', serif;
       line-height: 1.6;
       color: #2c3e50;
       max-width: 800px;
       margin: 0 auto;
   }
   
   h1 { 
       font-size: 2.5em; 
       color: #34495e;
       border-bottom: 3px solid #3498db;
       padding-bottom: 10px;
   }
   
   h2 {
       font-size: 1.8em;
       color: #34495e;
       margin-top: 30px;
   }
   
   p {
       text-align: justify;
       margin: 15px 0;
   }
   
   blockquote {
       border-left: 4px solid #3498db;
       padding-left: 15px;
       margin-left: 0;
       font-style: italic;
       color: #555;
   }
   ```

3. Run conversion:
   ```powershell
   pandoc MASTER-NARRATIVE-FULL.md `
     -f markdown `
     -t pdf `
     -c style.css `
     -V geometry:margin=1in `
     -o ChainWeapon-Story-Styled.pdf
   ```

**Time required:** 15 minutes
**Cost:** Free
**Quality:** Professional with custom styling

---

## OPTION 4: Direct EPUB Creation (For E-readers)

For Kindle or Apple Books compatibility:

```powershell
pandoc MASTER-NARRATIVE-FULL.md `
  -f markdown `
  -t epub `
  --epub-metadata metadata.xml `
  -o ChainWeapon-Story.epub
```

Then use Calibre (free: https://calibre-ebook.com/) to convert EPUB to MOBI (Kindle format).

---

## OUTPUT FILES EXPECTED

After successful export, you'll have:

**PDF Version:**
- File: `ChainWeapon-Story.pdf`
- Size: ~5-8 MB
- Format: Print-ready or screen-readable
- Best for: Printing, email, sharing

**EPUB Version:**
- File: `ChainWeapon-Story.epub`
- Size: ~2-3 MB
- Format: E-reader format
- Best for: Kindle, Apple Books, other e-readers

---

## RECOMMENDED WORKFLOW

1. **Quick export (today):** Use Option 1 (Pandoc Online) → 5 minutes
2. **Keep for future:** Use Option 2 (Install Pandoc locally) → 10 min setup
3. **Distribution:** Create both PDF and EPUB versions

---

## MANUSCRIPT CHECKLIST

Before exporting, verify:

✓ MASTER-NARRATIVE-FULL.md is complete (1,700+ lines)
✓ All new scenes integrated:
  - Expanded Final Stand
  - Elara's Choice
  - The Misread
  - All 11 critical weakness scenes
✓ Scene files referenced in correct order
✓ No duplicate content
✓ Metadata preserved in YAML frontmatter

**Status:** All items verified ✓

---

## NEXT STEPS

1. Choose export option (1 = easiest, 2 = best for future)
2. Export to PDF and EPUB
3. Verify output files in `story/` folder
4. Share with readers

**Estimated total time:** 5-15 minutes depending on option chosen

---

## NEED HELP?

If conversions don't appear to work:

1. Clear any line-ending issues:
   ```powershell
   (Get-Content MASTER-NARRATIVE-FULL.md) | Set-Content MASTER-NARRATIVE-FULL-clean.md
   ```

2. Try conversion on the cleaned file:
   ```powershell
   pandoc MASTER-NARRATIVE-FULL-clean.md -t pdf -o ChainWeapon-Story.pdf
   ```

3. Or use the online tools (Option 1) which handle formatting automatically

---

**Export Ready:** Your manuscript is complete and formatted for publication. Choose your preferred export method above and enjoy your published work!
