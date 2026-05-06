# REPOSITORY ANALYSIS — Full File-by-File Audit

> **Date:** April 12, 2026  
> **Commit Base:** `fe7246b` (pre-reorganization)  
> **Scope:** Every file and folder in `chain-weapon-story/`

---

## Executive Summary

| Metric | Before Reorg | After Reorg |
|--------|-------------|-------------|
| Top-level folders | 42 | 30 |
| Tracked files (git) | ~2,100 | ~1,950 |
| Git-tracked bloat (PDFs/logs/zips/JSON) | ~210 MB | 0 MB |
| Duplicate folders | 2 (`duplicates_for_review/`, root manuscript copies) | 0 |
| Near-empty folders | 3 (`chain-story/`, `full-information/`, `full information w/`) | 0 |
| Single-file folders | 10 | 2 (`scripts/`, `culture/`) |
| Manuscript output | Broken builds, demo-only content | **105-page PDF**, 52 chapters, enhanced typography |

### Actions Taken
1. **Deleted** `duplicates_for_review/` (88 duplicate character files)
2. **Deleted** `chain-story/` (abandoned 3-line Obsidian vault)
3. **Deleted** `full-information/` (empty)
4. **Untracked** all chat JSON files from git (~210 MB saved in repo history going forward)
5. **Untracked** all build artifacts (PDFs, logs, zips, .aux files)
6. **Consolidated** 8 single-file folders into `worldbuilding/`, `documentation/`, `characters/`
7. **Moved** misplaced files to correct locations
8. **Built** enhanced 105-page manuscript PDF with title page, TOC, act dividers, and visual system

---

## Repository Structure (Post-Reorganization)

```
chain-weapon-story/
├── .gitignore                    # Updated with comprehensive ignore rules
├── BUILD-MANUSCRIPT-FOR-REVIEW.py
├── CHARACTER-APPEARANCE-INDEX.md
├── CONTRIBUTING.md
├── CROSS-REFERENCE-HUB.md
├── README.md
├── story-overview.md
├── SYSTEMS-TO-DOCUMENTATION-INDEX.md
│
├── AI/                           # AI drafting tools & reference transcripts
│   ├── AI-Draft-Template.md
│   ├── WRITING-EXPANSIONS.md
│   └── reference/                # 14 files: DEEPSEEK batches, BEASTS, Copilot transcript
│
├── Arcs/                         # Act outlines & character arc notes
│   ├── ACT-I-OUTLINE.md
│   ├── ACT-II-OUTLINE.md
│   ├── ACT-III-OUTLINE.md
│   ├── ARC-TO-SCENES-INDEX.md
│   └── Character-Arcs/           # 15 character arc NOTES.md files
│
├── assets/                       # Image assets (currently empty placeholder)
│   ├── README.md
│   └── images/.gitkeep
│
├── audits/                       # Quality audits & diagnostics
│   ├── 3 ACT1 chapter audits (stubs)
│   ├── DETAILED-FILE-BY-FILE-AUDIT.md
│   ├── MANUSCRIPT-DIAGNOSTIC-TEMPLATE.md
│   ├── METADATA-SCAN-REPORT.md + .csv
│   ├── KIRITO-TEST-REPORT.md     # (moved from characters/)
│   ├── file_audit.csv + .json
│   └── 3 thematic audits
│
├── Chapters/                     # 65 chapter files (canonical story content)
│   ├── 01-52 numbered chapters
│   ├── Chapter-01.md             # Possible duplicate of 01-Tavern-Opening
│   ├── 4 Childhood-*.md preludes
│   └── Training-Drills-Master-States.md
│
├── characters/                   # 117 character files across 12 subfolders
│   ├── Root: 34 major character documents
│   ├── allies/          7 files
│   ├── antagonists/     8 files
│   ├── main/            5 files  (aisen-korv + 4 stubs)
│   ├── mentors/         7 files
│   ├── family/          2 files  (stubs)
│   ├── side/            5 files  (stubs)
│   ├── supporting-cast/ 19 files (MANIFEST + profiles + 10 stubs)
│   ├── TIER-PRIMARY/    5 files  (complete)
│   ├── TIER-SECONDARY/  9 files  (complete)
│   ├── TIER-ENSEMBLE/   8 files  (complete)
│   ├── duplicates-archive/       2 files
│   ├── RULE-BREAKER-GUIDES/      2 files
│   └── character-world-integration/ 1 file
│
├── chatsbyjson/                  # AI conversation archives (JSON untracked)
│   ├── CONVERSATION-RECONSTRUCTION.md  (tracked)
│   └── decifered.md                    (tracked)
│
├── culture/                      # Cultural framework
│   └── synthesis-framework.md
│
├── documentation/                # Project documentation & archive
│   ├── README.md
│   ├── REORGANIZATION-COMPLETION-STATUS.md
│   ├── REORGANIZATION-PLAN.md
│   ├── MARKDOWN-GUIDE.md         # (moved from markdown/)
│   ├── archive/                  # 21 files across analysis/, historical/, synthesis/
│   ├── current/                  # 2 files
│   └── revisions/                # 6 files
│
├── finished-manuscript/          # LaTeX manuscript build system
│   ├── Build scripts: build_manuscript.py, build_manuscript_v3.py, convert_md_to_tex.py
│   ├── Templates: manuscript.tex, manuscript-final.tex, manuscript-integrated.tex
│   ├── Style files: chain-style.tex, cwbook.tex
│   ├── Visual systems: character-glyphs-complete.tex, landscape-regions-complete.tex
│   ├── Config: chapter-config.json + 3 regional variants
│   ├── Documentation: 8 guide .md files
│   ├── cwbook_minimal_package/   # ★ PRIMARY BUILD — 52 .tex chapters + enhanced build
│   │   ├── cwbook_enhanced.cls   # NEW: Enhanced class with fontspec + visual system
│   │   ├── manuscript-enhanced.tex  # NEW: Full 52-chapter manuscript with act structure
│   │   ├── cwbook_minimal.cls    # Original class
│   │   ├── manuscript.tex        # Original 52-chapter build
│   │   ├── chapter01-52.tex      # Converted chapter content
│   │   └── env_*.png             # 10 environment strip images
│   ├── final_product/            # 8 files (demo build)
│   ├── manuscriptbaseforchapters/ # 52 Markdown source files
│   ├── archive_removed_by_copilot_2026-04-07/ # 10 archived .tex files
│   ├── newstuffmadebyclaude7-4/  # 4 experimental files
│   └── simplified stucture/      # 2 demo files
│
├── friend-review-package/        # Review distribution package
│   ├── README.md
│   ├── manuscript-review.md
│   └── manuscript-review.txt
│
├── magic-system/                 # 19 comprehensive magic system documents
│
├── micro-scenes/                 # Short narrative scenes
│   ├── scene-001.md
│   ├── scene-002.md
│   ├── aisen-ryo-campfire-scene.md  # (moved from characters/)
│   └── ryo-vision-chasm-prose.md    # (moved from characters/)
│
├── notes/                        # Working notes & archives
│   ├── full information&deepseek.md  (12K lines)
│   ├── lost-info.md              # (moved from root, extension added)
│   ├── Manuscript corrections.md (stub)
│   ├── Meta-Copilot-Archive.md   # (moved from Chapters/)
│   ├── RANDOMNESS-ARCHIVE.md
│   ├── temp-master-archive.txt   # (moved from story/)
│   └── LEGACY-DOCUMENTS/        # 3 legacy reference files
│
├── pacing/                       # 2 files: chapter pacing + intensity map
├── profiles/                     # 5 restructured character profiles + tracking CSV
├── project-management/           # 6 files: dashboard, kanban, tasks
├── reconstruction of the past/   # 5 files: compendium reconstruction
├── reference/                    # 14 files across magic-system/, society/, techniques/
├── scripts/                      # repo_audit.py
│
├── story/                        # 203 files: scenes, chapter-by-chapter drafts, indices
│   ├── INDEX.md
│   ├── COMPREHENSIVE-CONTENT-INDEX.md
│   ├── MASTER-NARRATIVE-FULL.md  (1922 lines)
│   ├── CHAPTER-BY-CHAPTER/       # 52 files (Ch 01-08 complete, 09-52 stubs)
│   ├── SCENES-BY-ARC/            # ACT-I, ACT-II (stubs), ACT-III scenes
│   ├── ~80 named scene files
│   └── 3 sample fight scenes
│
├── structure/                    # 34 files: story structure, beat maps, Sanderson guide
├── style/                        # 2 files: narrative style + prose polish guide
├── Templates/                    # 3 templates: Chapter, Character, Scene
├── timelines/                    # 10 files: chronology, ages, continuity
│
├── world/                        # 41 files across 12 subfolders
│   ├── artifact-catalog/
│   ├── conflict-mechanics/
│   ├── cultural-depth/
│   ├── ecology/                  # 7 creature/biome files
│   ├── economic-society/
│   ├── magic-society/
│   ├── nations/                  # shukei (6), therryn-umara (1), valdimere (9)
│   ├── post-war/
│   └── technology/
│
├── worldbuilding/                # 22 files (expanded with consolidated content)
│   ├── COSMOLOGY.md
│   ├── WORLDBUILDING-INDEX.md
│   ├── CONFLICT-OVERVIEW.md      # (moved from conflict/)
│   ├── CONSISTENCY-OVERVIEW.md   # (moved from consistency/)
│   ├── ECOLOGY-OVERVIEW-ROOT.md  # (moved from ecology/)
│   ├── TECHNOLOGY-OVERVIEW.md    # (moved from technology/)
│   ├── CULTURE/                  # 8 files (original 6 + cross-cultural-mobility + prejudice-as-narrative)
│   ├── ECOLOGY/                  # 2 files
│   └── MAGIC-SYSTEM/             # 6 files
│
└── writingtutorials/             # 46 files: Sanderson lectures, exercises, craft reference
```

---

## File-by-File Status by Folder

### Root Files (8 files post-reorg)

| File | Lines | Status |
|------|-------|--------|
| `.gitignore` | 32 | ✅ Updated |
| `BUILD-MANUSCRIPT-FOR-REVIEW.py` | 151 | ✅ Complete |
| `CHARACTER-APPEARANCE-INDEX.md` | 182 | ✅ Complete |
| `CONTRIBUTING.md` | 176 | ✅ Complete |
| `CROSS-REFERENCE-HUB.md` | 224 | ✅ Complete |
| `README.md` | 101 | ✅ Complete |
| `story-overview.md` | 489 | ✅ Complete |
| `SYSTEMS-TO-DOCUMENTATION-INDEX.md` | 261 | ✅ Complete |

### Chapters/ (65 files)

**Full prose (3,000+ words):** Chapters 01–08 are fully drafted
**Summary/outline form:** Chapters 09–52 range from 200–1,500 words (structural outlines, not full prose)

| Issue | Files | Action Needed |
|-------|-------|---------------|
| Numbering conflicts | Two `04-*`, two `05-*`, three `30-*` files | Resolve canonical versions |
| Possible duplicate | `Chapter-01.md` vs `01-Tavern-Opening.md` | Verify & consolidate |
| Combined + individual overlap | `41-44-War-Operations` + individual `41-44` files | Pick canonical format |

### characters/ (117 files)

**Complete profiles (50+ lines, structured):** ~60 files
**Stubs (<15 lines):** ~25 files

| Category | Stubs Needing Expansion |
|----------|------------------------|
| `main/` | AMARA, PIETER-VAN-DER-BERG, REN-SHIRAKAWA, TUPAC |
| `family/` | MIRA, TAVERN-KEEPER-FATHER |
| `side/` | GARETH, GRIOT-SANA, LIRA, QUARTERMASTER-DAUGHTER, RETIRED-SOLDIER |
| `mentors/` | MASTER-WEI, SERGEANT-HARALD, TAROVIN (stub vs tarovin-blacksun full) |
| `antagonists/` | LYSANDRA (stub), SER-CORVIN-ASHFORD (stub vs CORVIN-ASHFORD full) |
| `allies/` | KAELEN-THORNWOOD (stub), RIN-SHIRAKAWA (stub) |
| `supporting-cast/` | 10 tier-3 stubs (GAEL, HELGA, ILLYAN, KOFI, MARTA, etc.) |

**TODO/TBD markers remaining:** ~25 across various character files (mostly in allies/ and antagonists/ variants)

### story/ (203 files)

**CHAPTER-BY-CHAPTER/:** Ch 01–08 complete drafts (43–103 lines), Ch 09–52 stubs (11–15 lines each)
**Named scenes:** 15 substantial scenes (30–182 lines), 20 stub scenes (17 lines each, templated)
**Master files:** MASTER-NARRATIVE-FULL.md (1,922 lines) — comprehensive
**Indices:** INDEX.md (311 lines), COMPREHENSIVE-CONTENT-INDEX.md (315 lines)

### magic-system/ (19 files) — ✅ ALL COMPLETE

No stubs, no TODOs. Ranges from 76–610 lines. Strongest folder in the repo.

### world/ (41 files) — ✅ ALL COMPLETE

Well-organized with regional subfolders. 22–448 lines per file.

### worldbuilding/ (22 files post-consolidation) — ✅ ALL COMPLETE

Absorbed content from 4 former single-file folders.

### structure/ (34 files) — ✅ NEARLY COMPLETE

One TODO remaining in `CHAPTER-BEAT-MAP.md` line 103.

### finished-manuscript/ (~170 content files)

| Component | Status |
|-----------|--------|
| `cwbook_minimal_package/` | ✅ **Builds successfully** — 105 pages, 52 chapters |
| `cwbook_enhanced.cls` | ✅ NEW — fontspec, TeX Gyre Pagella, act dividers, scene breaks |
| `manuscript-enhanced.tex` | ✅ NEW — title page, TOC, act structure, environment mapping |
| `chain-style.tex` | ⚠️ Has 4 known issues (color defs, tcolorbox skins) — not used in enhanced build |
| `landscape-regions-complete.tex` | ⚠️ Missing color definitions — not used in enhanced build |
| `character-glyphs-complete.tex` | ⚠️ Only 42/180 variants defined — not used in enhanced build |
| `manuscriptbaseforchapters/` | ✅ 52 Markdown source files |

---

## Incomplete Parts Summary

### Critical (Blocks publication)

| Item | Location | Status |
|------|----------|--------|
| Chapters 09–52 need full prose | `Chapters/`, `manuscriptbaseforchapters/` | Only outlines exist |
| Chapter numbering conflicts | `04-*/05-*/30-*` duplicate numbers | Need canonical resolution |
| Chapter 01 continuity error | `01-Tavern-Opening.md` line ~3 | Harald called "father" (should be guard mentor) |

### Important (Quality gaps)

| Item | Count | Location |
|------|-------|----------|
| Character profile stubs | ~25 | `characters/main/`, `family/`, `side/`, `mentors/` |
| Scene stubs (17 lines each) | ~20 | `story/scene-011` through `scene-030` |
| CHAPTER-BY-CHAPTER stubs | 44 | `story/CHAPTER-BY-CHAPTER/` Ch 09–52 |
| ACT-II scene stubs | 3 | `story/SCENES-BY-ARC/ACT-II-ACADEMY/` |
| TODO/TBD markers | ~82 | Distributed across characters, documentation, notes |

### Minor (Cleanup)

| Item | Location |
|------|----------|
| `Verify-Setup.md` stub (9 lines) still on disk | Root |
| `Character-Example.md` template in characters/ | Could move to Templates/ |
| `chatsbyjson/copendium.json` 125MB on disk | Consider archival |
| `finished-manuscript/.venv/` 89MB on disk | Safe to delete (not tracked) |
| `finished-manuscript/inkscape-1.4.3.msi` 162MB on disk | Safe to delete |
| Archive .tex files in `archive_removed_by_copilot_2026-04-07/` | Already archived |

---

## Manuscript Build Instructions

### Quick Build (Enhanced — Recommended)

```powershell
cd finished-manuscript/cwbook_minimal_package
xelatex -interaction=nonstopmode manuscript-enhanced.tex
xelatex -interaction=nonstopmode manuscript-enhanced.tex  # Second pass for TOC
```

**Output:** `manuscript-enhanced.pdf` — 105 pages with:
- Title page with Aisen's glyph
- Copyright page
- Table of Contents
- Act I/II/III divider pages
- 52 chapters with per-chapter environment strips
- Character POV glyphs in headers
- Chapter progress stripe on right edge
- TeX Gyre Pagella serif typography

### Original Build (Simpler visual system)

```powershell
cd finished-manuscript/cwbook_minimal_package
xelatex -interaction=nonstopmode manuscript.tex
xelatex -interaction=nonstopmode manuscript.tex
```

### Updating Chapter Content

1. Edit Markdown sources in `manuscriptbaseforchapters/`
2. Run `python convert_md_to_tex.py` from `finished-manuscript/`
3. Rebuild with XeLaTeX as above

---

## Reorganization Changelog

### Deleted
- `duplicates_for_review/` — 88 files (exact copy of characters/)
- `chain-story/` — 6 files (abandoned Obsidian vault, 3-line content)
- Root `manuscript-review.md` + `.txt` — duplicates of friend-review-package/
- `characters/allies/## GitHub Copilot Chat.md` — garbage auto-generated file

### Moved
| From | To |
|------|----|
| `lost info` (no extension) | `notes/lost-info.md` |
| `characters/AISEN-RYO-CAMPFIRE-SCENE.md` | `micro-scenes/aisen-ryo-campfire-scene.md` |
| `characters/RYO-VISION-CHASM-PROSE.md` | `micro-scenes/ryo-vision-chasm-prose.md` |
| `characters/KIRITO-TEST-REPORT.md` | `audits/KIRITO-TEST-REPORT.md` |
| `Chapters/Meta-Copilot-Archive.md` | `notes/Meta-Copilot-Archive.md` |
| `story/temp_master.txt` | `notes/temp-master-archive.txt` |

### Consolidated (single-file folders → parent)
| Former Folder | New Location |
|---------------|-------------|
| `conflict/README.md` | `worldbuilding/CONFLICT-OVERVIEW.md` |
| `consistency/README.md` | `worldbuilding/CONSISTENCY-OVERVIEW.md` |
| `ecology/README.md` | `worldbuilding/ECOLOGY-OVERVIEW-ROOT.md` |
| `hierarchies/cross-cultural-mobility.md` | `worldbuilding/CULTURE/cross-cultural-mobility.md` |
| `markdown/README.md` | `documentation/MARKDOWN-GUIDE.md` |
| `technology/README.md` | `worldbuilding/TECHNOLOGY-OVERVIEW.md` |
| `theme/prejudice-as-narrative.md` | `worldbuilding/CULTURE/prejudice-as-narrative.md` |
| `supporting-cast/README.md` | `characters/supporting-cast/SUPPORTING-CAST-README.md` |

### Git Tracking Changes
| Action | Files | Impact |
|--------|-------|--------|
| Untracked `chatsbyjson/*.json` | 10 files | ~210 MB removed from future commits |
| Untracked `finished-manuscript/*.pdf` | 12 files | Build artifacts excluded |
| Untracked `finished-manuscript/*.log` | 8 files | Build logs excluded |
| Untracked `finished-manuscript/*.zip` | 5 files | Archives excluded |
| Untracked `finished-manuscript/*.aux/.fls/.fdb_latexmk` | 3 files | LaTeX aux excluded |
| Updated `.gitignore` | Comprehensive rules | Prevents future bloat |

### Created
| File | Purpose |
|------|---------|
| `cwbook_minimal_package/cwbook_enhanced.cls` | Enhanced LaTeX class with fontspec, better typography |
| `cwbook_minimal_package/manuscript-enhanced.tex` | Full 52-chapter manuscript with title page, TOC, act dividers |
| `audits/REPOSITORY-ANALYSIS-2026-04-12.md` | This document |
