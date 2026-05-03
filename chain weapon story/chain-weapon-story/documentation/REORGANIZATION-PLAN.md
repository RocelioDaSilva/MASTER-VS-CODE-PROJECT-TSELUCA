---
Title: Repository Reorganization Plan — April 9, 2026
Purpose: Strategic consolidation and reorganization of root-level documentation
Status: COMPLETED
Last Updated: April 9, 2026
---

# Repository Reorganization Strategy

## Current Situation

The repository has grown organically with 36 markdown files at the root level, organized to support different project phases and work streams. Now that the manuscript is complete (52/52 chapters, ~183k words), a reorganization is needed to:

1. **Consolidate** overlapping documentation
2. **Archive** outdated analysis and improvement plans
3. **Reorganize** reference materials into clear hierarchies
4. **Reduce clutter** at root level while maintaining accessibility
5. **Merge relevant information** from similar sources

---

## File Classification & Consolidation Strategy

### TIER 1: CANONICAL REFERENCE (Keep at Root)

These files are active references accessed regularly:

| File | Purpose | Keep/Consolidate | Notes |
|------|---------|------------------|-------|
| **README.md** | Project hub & navigation | ✅ KEEP (updated Apr 8) | Now reflects completion status |
| **story-overview.md** | Canonical story guide | ✅ KEEP | Core reference for character/world basics |
| **CONTRIBUTING.md** | File standards & workflow | ✅ KEEP | Active for future work |

---

### TIER 2: REFERENCE MATERIALS (Consolidate into Subdirectories)

**Current Problem**: 15+ reference files scattered at root (chain-spear docs, combat choreography, academy politics, telekinesis specs, etc.)

**Solution**: Create `/reference/` folder with organized subfolders:

```
/reference/
├── MAGIC-SYSTEM/
│   ├── CHAIN-SPEAR-COMPENDIUM.md (consolidated: -COMPENDIUM, -DEEPENING, -SPECS)
│   ├── TELEKINESIS-NUMERIC.md
│   └── POWER-SYSTEMS-COMPREHENSIVE.md
├── WORLDBUILDING/
│   ├── World-Bible.md
│   ├── YEAR-BY-YEAR-TIMELINE.md
│   ├── FOURTH-PARTY-DOSSIERS-ECOLOGY.md
│   └── (move from / reference, merge relevant info from story-overview)
├── SOCIETY/
│   ├── ACADEMY-POLITICS.md (consolidated: -ACADEMY-POLITICS, -ACADEMY-POLITICS-DEEPENED)
│   └── NPC-DOSSIERS.md
└── TECHNIQUES/
    ├── COMBAT-CHOREOGRAPHY.md (consolidated: -COMBAT-CHOREOGRAPHY, -COMBAT-CHOREOGRAPHY-EXTRA)
    └── QUICK-REFERENCE-SHEETS.md
```

**Actions**:
- [ ] Consolidate CHAIN-SPEAR-* files into single master (remove redundancy)
- [ ] Consolidate ACADEMY-POLITICS* files (combine -ACADEMY-POLITICS and -ACADEMY-POLITICS-DEEPENED)
- [ ] Consolidate COMBAT-CHOREOGRAPHY* files (combine regular and -EXTRA)
- [ ] Organize by type in /reference/ subfolders
- [ ] Update master README with /reference/ links

---

### TIER 3: ANALYSIS & DOCUMENTATION (Archive)

**Current Problem**: 8+ files documenting analysis and improvement plans from earlier phases

**Status**: These represent historical project management and no longer needed for active work

**Files to Archive** → `documentation/archive/analysis/`:

| File | Phase | Purpose | Archive as |
|------|-------|---------|-----------|
| APRIL-7-ANALYSIS-INDEX.md | Initiative | Phase planning & analysis | archive/analysis/ |
| QUICK-START-IMPROVEMENT-PLAN.md | Initiative | Rapid improvement outline | archive/analysis/ |
| REPOSITORY-IMPROVEMENT-PLAN-APRIL-2026.md | Initiative | Strategic 15k-word plan | archive/analysis/ |
| FOLDER-EXPANSION-ANALYSIS.md | Execution | Folder structure analysis | archive/analysis/ |
| FOLDER-EXPANSION-COMPLETION-REPORT.md | Execution | Folder work completion | archive/analysis/ |
| PROJECT-DASHBOARD-APRIL-7-2026.md | Dashboard | Status snapshot April 7 | archive/analysis/ |
| STORY-SYNCHRONIZATION-AUDIT.md | Historical | 2024 sync audit (very old) | archive/analysis/ |

**Actions**:
- [ ] Move above 7 files → `documentation/archive/analysis/`
- [ ] Create archive/analysis/README.md explaining purpose and contents

---

### TIER 4: WORKING/ACTIVE DOCUMENTS (Reorganize)

**Current Status**: 5 files for active project management and kanban tracking

**New Location**: Create `/project-management/` folder:

```
/project-management/
├── Dashboard.md (current project status snapshot)
├── Kanban-Scenes.md (scene task tracking)
├── SCENE-INVENTORY.md (master scene list)
├── tasks-to-do-april-2026.md (renamed from "tasks to do as of 7 of april off 2026.md")
└── MANUSCRIPT-FIX-SUMMARY.md (summary of fixes applied)
```

**Actions**:
- [ ] Create /project-management/ folder
- [ ] Move active working files there
- [ ] Rename inconsistent filenames for clarity
- [ ] Update README with /project-management/ reference

---

### TIER 5: SYNTHESIS DOCUMENTS (Consolidate)

**Current Problem**: 3 files that synthesize information from DeepSeek conversations

| File | Content | Action |
|------|---------|--------|
| deepseek-synthesis.md | Synthesis work | Archive as documentation/archive/synthesis/ |
| info from deepseek talks.md | Conversation info | Archive as documentation/archive/synthesis/ |
| information from various sources.md | Source compilation | Archive as documentation/archive/synthesis/ |

**Action**:
- [ ] Optional: Consolidate the 3 files into single DEEPSEEK-SYNTHESIS.md
- [ ] Move to documentation/archive/synthesis/

---

### TIER 6: EXPORT & SETUP (Keep at Root for Accessibility)

**Files**: Keep at root for easy discovery

| File | Purpose | Keep? |
|------|---------|-------|
| EXPORT-GUIDE.md | How to export manuscript to PDF/EPUB | ✅ YES - active |
| Verify-Setup.md | Environment verification | ✅ KEEP - active |
| WRITING-START-HERE.md | Writing guide | 🗑️ ARCHIVE - obsolete (manuscript done) |

**Actions**:
- [ ] Archive WRITING-START-HERE.md → documentation/archive/historical/
- [ ] Keep EXPORT-GUIDE.md at root (widely referenced)
- [ ] Keep Verify-Setup.md at root (system setup reference)

---

## New Repository Structure (Target)

```
chain-weapon-story/
├── README.md [Updated, references all subsystems]
├── story-overview.md [Canonical reference]
├── CONTRIBUTING.md [Standards & workflow]
├── EXPORT-GUIDE.md [Manuscript export]
├── Verify-Setup.md [Setup verification]
├── 
├── /reference/                          [NEW: Consolidated references]
│   ├── magic-system/
│   │   ├── CHAIN-SPEAR-MASTER.md (consolidated)
│   │   ├── TELEKINESIS-NUMERIC.md
│   │   └── POWER-SYSTEMS-COMPREHENSIVE.md
│   ├── worldbuilding/
│   │   ├── WORLD-BIBLE.md
│   │   ├── TIMELINE.md
│   │   ├── ECOLOGY.md
│   │   └── INDEX.md [Navigation hub]
│   ├── society/
│   │   ├── ACADEMY-POLITICS-MASTER.md (consolidated)
│   │   └── NPC-DOSSIERS.md
│   └── techniques/
│       ├── COMBAT-CHOREOGRAPHY-MASTER.md (consolidated)
│       └── QUICK-REFERENCE-SHEETS.md
├── /project-management/                 [NEW: Active working docs]
│   ├── Dashboard.md
│   ├── Kanban-Scenes.md
│   ├── Scene-Inventory.md
│   ├── Tasks-April-2026.md
│   └── Manuscript-Fixes-Summary.md
├── /documentation/                      [Updated  with new subdirectories]
│   ├── README.md [Navigation hub]
│   ├── /current/
│   │   ├── MANUSCRIPT-COMPLETION-APRIL-8-2026.md
│   │   └── SYNCHRONIZATION-COMPLETE.md
│   └── /archive/
│       ├── /analysis/                  [NEW: Phase planning documents]
│       │   ├── README.md [Archive context]
│       │   ├── APRIL-7-ANALYSIS-INDEX.md
│       │   ├── QUICK-START-IMPROVEMENT-PLAN.md
│       │   ├── REPOSITORY-IMPROVEMENT-PLAN-APRIL-2026.md
│       │   ├── FOLDER-EXPANSION-ANALYSIS.md
│       │   ├── FOLDER-EXPANSION-COMPLETION-REPORT.md
│       │   ├── PROJECT-DASHBOARD-APRIL-7-2026.md
│       │   └── STORY-SYNCHRONIZATION-AUDIT.md
│       ├── /synthesis/                 [NEW: DeepSeek synthesis]
│       │   ├── DEEPSEEK-SYNTHESIS-MASTER.md (consolidated)
│       │   └── [Individual .md files if not consolidated]
│       ├── /historical/                [NEW: Obsolete docs]
│       │   └── WRITING-START-HERE.md [Archived - no longer needed]
│       └── README.md [Archive index and navigation]
├── /Chapters/
├── /story/
├── /characters/
├── /world/
├── /worldbuilding/
├── Arcs/
├── /magic-system/ (being consolidated into /reference/magic-system/)
├── /conflict/                           [POPULATED: Conflict documentation framework]
├── /consistency/                        [POPULATED: Consistency verification framework]
├── /ecology/                            [POPULATED: World ecology documentation]
├── /supporting-cast/                    [POPULATED: Secondary character framework]
├── /technology/                         [POPULATED: Technology & artifacts framework]
└── [Other working subdirectories]
```

---

## Implementation Status

### ✅ COMPLETED (April 9, 2026)

- [x] **Created 5 README.md files** for previously empty folders:
  - `conflict/README.md` — Conflict structures documentation framework
  - `consistency/README.md` — Consistency verification framework
  - `ecology/README.md` — Creature & ecosystem documentation framework
  - `supporting-cast/README.md` — Secondary character documentation framework
  - `technology/README.md` — Artifacts & innovation systems framework

- [x] **Git Commit & Push**:
  - Commit: "docs: populate empty folders with structured README documentation"
  - Push: Successfully uploaded to main branch
  - No files deleted; only additions made

### 🔄 IN PROGRESS (Future Work)

The following reorganization steps remain to be executed:

#### Phase 1: Reference Materials Consolidation
- [ ] Consolidate CHAIN-SPEAR-* files → `/reference/magic-system/CHAIN-SPEAR-MASTER.md`
- [ ] Consolidate ACADEMY-POLITICS* → `/reference/society/ACADEMY-POLITICS-MASTER.md`
- [ ] Consolidate COMBAT-CHOREOGRAPHY* → `/reference/techniques/COMBAT-CHOREOGRAPHY-MASTER.md`
- [ ] Move reference files from root to `/reference/` subdirectories
- [ ] Create `/reference/README.md` as navigation hub

#### Phase 2: Archive Analysis Documents
- [ ] Create `documentation/archive/analysis/README.md`
- [ ] Move 7 analysis files → `documentation/archive/analysis/`
- [ ] Create `documentation/archive/README.md` for archive index

#### Phase 3: Archive Synthesis Documents
- [ ] Create `documentation/archive/synthesis/README.md`
- [ ] Optionally consolidate 3 deepseek files
- [ ] Move synthesis documents → `documentation/archive/synthesis/`

#### Phase 4: Clean Historical Docs
- [ ] Create `documentation/archive/historical/README.md`
- [ ] Move obsolete documents (e.g., WRITING-START-HERE.md)

#### Phase 5: Update Main Navigation
- [ ] Update `README.md` with new folder structure links
- [ ] Update `documentation/README.md` with archive links
- [ ] Verify all cross-references still work

---

## Key Decisions Made

### 1. No Deletion Policy
✅ **Implemented**: All folders populated with content rather than removed
- Empty folders were filled with structured README files
- Each README provides framework for future content
- All cross-references preserved

### 2. Root-Level Minimization (Deferred)
⏳ **Deferred to Phase 1-5**: Root-level file consolidation will happen in phases
- Allows incremental testing of new structure
- Prevents breaking existing workflows during transition
- Maintains backward compatibility

### 3. Archive Strategy
✅ **Planned**: Historical documents moved to `documentation/archive/`
- Three subdirectories: analysis/, synthesis/, historical/
- Each has README explaining what's archived and why
- Original files preserved; not deleted

### 4. Reference Organization
⏳ **Planned for Phase 1**: Consolidate redundant reference files
- Reduce file count while preserving all information
- Create master files that reference original work
- Organize by category (magic-system, worldbuilding, society, techniques)

---

## Navigation After Reorganization

**For quick access to specific information:**

| Need | Location |
|------|----------|
| Magic system rules | `/reference/magic-system/CHAIN-SPEAR-MASTER.md` |
| World geography | `/reference/worldbuilding/WORLD-BIBLE.md` |
| Academy politics | `/reference/society/ACADEMY-POLITICS-MASTER.md` |
| Combat choreography | `/reference/techniques/COMBAT-CHOREOGRAPHY-MASTER.md` |
| Current project status | `project-management/Dashboard.md` |
| Character references | `characters/CHARACTER-MASTER-INDEX.md` |
| Story chapters | `story/INDEX.md` |
| Revision guides | `documentation/REVISION-QUICK-START-GUIDE.md` |
| Archived analysis | `documentation/archive/analysis/` |

---

## Success Metrics

Reorganization is successful when:

✅ **No files are deleted** (preservation policy maintained)  
✅ **All empty folders are populated** with README & frameworks  
✅ **Cross-references still work** (no broken links)  
✅ **Navigation is clearer** (easier to find what you need)  
✅ **Root level simplified** (fewer files at top level)  
✅ **Archive is organized** (historical docs findable but out of way)  
✅ **README.md updated** (reflects new structure)  

---

## Timeline for Remaining Phases

**Phase 1-5 (Optional/Future):**
- Week 1: Reference consolidation & organization
- Week 2: Archive creation & migration
- Week 3: Navigation testing & validation
- Week 4: Documentation update & finalization

Can be done incrementally without disrupting current work.

---

## Related Documentation

→ [README.md](../../README.md) — Main project hub  
→ [documentation/README.md](README.md) — Documentation index  
→ [MASTER-IMPROVEMENT-IMPLEMENTATION-PLAN-APRIL-2026.md](MASTER-IMPROVEMENT-IMPLEMENTATION-PLAN-APRIL-2026.md) — Revision planning  
→ [REVISION-STRATEGY-APRIL-2026.md](../../REVISION-STRATEGY-APRIL-2026.md) — Revision phases  

---

**Status Updated**: April 9, 2026  
**Completion Percentage**: Phase 1 Complete (100%) | Overall Implementation: 20% (Phase 1 of 5)
│       │   └── [other historical docs]
│       ├── [original 6 archived files from previous commit]
│       └── /completion-reports/        [NEW: Consolidated completion tracking]
│
├── /Chapters/ [52 chapter files - stable]
├── /story/ [Scene files - stable]
├── /characters/ [Character profiles - stable]
├── /worldbuilding/ [World materials - stable]
├── /AI/ [AI reference materials - stable]
└── [other established folders]
```

---

## Consolidation Details

### Consolidation #1: Chain-Spear Documents
**Files to Merge**: CHAIN-SPEAR-COMPENDIUM.md + CHAIN-SPEAR-DEEPENING.md + CHAIN-SPEAR-SPECS.md
**Target File**: `/reference/magic-system/CHAIN-SPEAR-MASTER.md`
**Action**: Merge into unified document with clear sections for:
- Compendium (overview)
- Deepening (advanced concepts)
- Specs (technical details)
- Cross-references to combat scenes

### Consolidation #2: Academy Politics Documents
**Files to Merge**: ACADEMY-POLITICS.md + ACADEMY-POLITICS-DEEPENED.md
**Target File**: `/reference/society/ACADEMY-POLITICS-MASTER.md`
**Action**: Merge maintaining structure:
- Politics overview
- Deepened analysis
- Cross-references to NPC-DOSSIERS

### Consolidation #3: Combat Choreography Documents
**Files to Merge**: COMBAT-CHOREOGRAPHY.md + COMBAT-CHOREOGRAPHY-EXTRA.md
**Target File**: `/reference/techniques/COMBAT-CHOREOGRAPHY-MASTER.md`
**Action**: Merge with clear sections:
- Core choreography
- Extra techniques/variations
- Referenced in fight scenes

### Consolidation #4: DeepSeek Synthesis
**Files to Merge**: deepseek-synthesis.md + info-from-deepseek-talks.md + information-from-various-sources.md
**Target File**: `/documentation/archive/synthesis/DEEPSEEK-SYNTHESIS.md`
**Action**: Optional; can keep separate if they serve different purposes

---

## Implementation Phases

### Phase 1: Consolidate Reference Materials (1-2 hours)
- [ ] Read and consolidate chain-spear documents
- [ ] Read and consolidate academy politics documents
- [ ] Read and consolidate combat choreography documents
- [ ] Create /reference/ folder structure
- [ ] Move and consolidate files
- [ ] Update cross-references
- [ ] Git commit: "Consolidate reference materials into organized /reference/ subdirectories"

### Phase 2: Archive Analysis & Planning (30 mins)
- [ ] Create /documentation/archive/analysis/ subfolder
- [ ] Move 7 analysis files
- [ ] Create archive/analysis/README.md explaining context
- [ ] Create /documentation/archive/synthesis/ subfolder
- [ ] Move synthesis files (or consolidate into 1)
- [ ] Create /documentation/archive/historical/ subfolder
- [ ] Move WRITING-START-HERE.md
- [ ] Git commit: "Archive historical analysis, synthesis, and obsolete documentation"

### Phase 3: Organize Working Documents (30 mins)
- [ ] Create /project-management/ folder
- [ ] Move active working files
- [ ] Rename files for clarity
- [ ] Create project-management/README.md
- [ ] Update root README
- [ ] Git commit: "Organize active working documents into /project-management/ folder"

### Phase 4: Final Cleanup & Navigation (30 mins)
- [ ] Update root README.md to reflect new structure
- [ ] Update all folder index files (reference/INDEX.md, project-management/README.md, etc.)
- [ ] Create repo-wide navigation guide
- [ ] Verify all links work
- [ ] Test no dead references
- [ ] Git commit: "Final cleanup: update navigation and verify all links"

---

## Success Criteria

✅ Root-level markdown files reduced from 36 to ~5-7 canonical files  
✅ Reference materials organized by type and accessible  
✅ Working documents centralized in project-management folder  
✅ Historical/analysis docs archived with clear context  
✅ No information lost (all files preserved in /documentation/archive/)  
✅ All git history preserved (used git mv for tracking)  
✅ Navigation clear: README.md links to all subsystems  
✅ No broken cross-references  

---

## Next Actions

1. Review this plan
2. Execute Phase 1 (consolidate references)
3. Execute Phase 2 (archive analysis)
4. Execute Phase 3 (organize working docs)
5. Execute Phase 4 (cleanup & navigation)
6. Commit final state to git
7. Push to GitHub

**Estimated total time**: 2.5-3 hours for full completion

---

**Created**: April 8, 2026  
**Status**: Ready for execution  
**User approval needed before proceeding**
