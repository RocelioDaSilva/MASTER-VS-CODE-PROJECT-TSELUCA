---
title: Folder Expansion & Organization Analysis
date: 2026-04-07
status: Ready for Implementation
---

# Folder Expansion & Organization Analysis

## Executive Summary

The repository contains substantial and well-organized content but has **missing files** from the DeepSeek analysis materials and several **organizational opportunities** to consolidate related materials into clearer hierarchies. This document maps gaps and recommends a folder structure aligned with the compendium materials.

---

## PART 1: MISSING FILES (Priority: HIGH)

### Missing from AI/ Folder

**DEEPSEEK-BATCH-1.md** 
- Referenced in attachments as lines 1–5000
- Expected to contain: Cosmology, magic physics, Aelfar origins, Flux system foundations
- **Status**: NOT FOUND — needs creation or recovery

**SCENE-TRIBUNAL.md (mentioned in DEEPSEEK-COMPENDIUM-INDEX.md)**
- Expected at: `story/SCENE-TRIBUNAL.md`
- Mentioned in DEEPSEEK-COMPENDIUM-INDEX.md as a "High-Priority Scene Draft"
- **Status**: File exists as `story/scene-heresy-tribunal.md` but not named consistently

### Verification of Referenced Files

✓ AI/BEASTS.md — Found (bestiary with 20 entries)  
✓ AI/COPILOT-CONVERSATION-TRANSCRIPT.md — Found  
✓ AI/DEEPSEEK-BATCH-2.md through BATCH-9.md — Found  
✓ AI/DEEPSEEK-COMPENDIUM-FULL.md — Found  
✓ AI/DEEPSEEK-COMPENDIUM-INDEX.md — Found  
✓ AI/DEEPSEEK-TALKS-SYNTHESIS.md — Found  
✓ AI/WRITING-EXPANSIONS.md — Found  
✗ AI/DEEPSEEK-BATCH-1.md — **MISSING**  

---

## PART 2: ORGANIZATIONAL OPPORTUNITIES

### Current Scattered Materials

The repository has multiple folders that could benefit from consolidation and clearer hierarchies:

**Scene Files (story/ folder)** 
- 100+ individual scene files
- Naming inconsistent: `scene-XXX.md`, `Chapter-XX-Title.md`, `SCENE-TRIBUNAL.md`, `scene-aldric-execution.md`
- **Recommendation**: Create thematic subfolders within story/ for scenes by arc or theme

**Worldbuilding/Magic System**
- Scattered across: `magic-system/`, `world/`, `ecology/`, `culture/`, `technology/`
- **Recommendation**: Create a unified `worldbuilding/` structure with subsections

**Character Materials**
- Already organized into tiers (TIER-PRIMARY, TIER-SECONDARY, TIER-ENSEMBLE)
- **Status**: Good — minimal changes needed

**Reference Materials in AI/**
- 15 analysis files (batches, compendium, synthesis, bestiary)
- **Recommendation**: Create `reference/` subfolder to distinguish from future AI drafts

---

## PART 3: RECOMMENDED FOLDER STRUCTURE

### A. Create `/AI/reference/` Subfolder

**Purpose**: Organize analysis, synthesis, and compendium materials separately from new drafts

**Files to Move**:
```
AI/reference/
├── DEEPSEEK-BATCH-1.md (CREATE THIS FIRST)
├── DEEPSEEK-BATCH-2.md
├── DEEPSEEK-BATCH-3.md
├── DEEPSEEK-BATCH-4.md
├── DEEPSEEK-BATCH-5.md
├── DEEPSEEK-BATCH-6.md
├── DEEPSEEK-BATCH-7.md
├── DEEPSEEK-BATCH-8.md
├── DEEPSEEK-BATCH-9.md
├── DEEPSEEK-COMPENDIUM-INDEX.md
├── DEEPSEEK-COMPENDIUM-FULL.md
├── DEEPSEEK-TALKS-SYNTHESIS.md
├── BEASTS.md
└── COPILOT-CONVERSATION-TRANSCRIPT.md

AI/ (keep at top level):
├── WRITING-EXPANSIONS.md (active working file)
├── AI-Draft-Template.md (template for future results)
└── reference/ (subfolder above)
```

### B. Create `/worldbuilding/` Folder

**Purpose**: Consolidate all world, magic, ecology, culture, and technology materials

**Structure**:
```
worldbuilding/
├── WORLDBUILDING-INDEX.md (hub document)
├── COSMOLOGY.md (Weave, Flux, Aelfar, origins)
├── MAGIC-SYSTEM/
│   ├── MAGIC-LAWS.md (six laws: Gravity, Energy, Info, Causality, Entropy, Momentum)
│   ├── HARD-MAGIC-RULES.md
│   ├── POWER-ARCHETYPES.md
│   ├── RESONANCE-CRYSTALS.md
│   └── SPELL-CATALOG.md
├── NATIONS-AND-POLITICS.md (six nations, factions, halls)
├── GEOGRAPHY.md (The Spine, Silverrun, Shattered Coast, etc.)
├── TIMELINE.md (eras and major events)
├── CULTURE/
│   ├── Heartland/
│   ├── Island-Fortress/
│   ├── Celestial/
│   ├── Sahelian/
│   ├── Andean/
│   └── Federation/
├── ECOLOGY/
│   ├── CREATURE-BESTIARY.md (link to AI/reference/BEASTS.md)
│   ├── FLUX-ANOMALIES.md
│   ├── ENVIRONMENTAL-CRISIS.md
│   └── FOURTH-PARTY-SYSTEM.md
└── TECHNOLOGY.md (chain weapons, forging, engineering)
```

### C. Organize `/story/` with Thematic Subfolders

**Purpose**: Group 100+ scene files by arc/phase for easier navigation

**Structure**:
```
story/
├── INDEX.md (master list of all chapters and scenes)
├── CHAPTER-BY-CHAPTER/ (rename existing Chapter-XX-Title.md here)
│   ├── Chapter-01-The-Tavern-Opens.md
│   ├── Chapter-02-Caspians-First-Visit.md
│   └── ... (through Chapter-52)
├── SCENES-BY-ARC/
│   ├── ACT-I-CHILDHOOD/
│   │   ├── ALDRIC-EXECUTION-SCENE.md
│   │   ├── FIRST-HUNT.md
│   │   ├── TAVERN-OPENING.md
│   │   └── ... (other childhood scenes)
│   ├── ACT-II-ACADEMY/
│   │   ├── FROSTFANG-TREK.md
│   │   ├── SCENE-TOURNAMENT.md
│   │   ├── CHAIN-SPEAR-TRAINING.md
│   │   └── ... (other academy scenes)
│   └── ACT-III-WAR-AND-FINAL-STAND/
│       ├── BORDER-VILLAGE-DEFENSE.md
│       ├── THORNWOOD-HOLLOW-FINAL-STAND.md
│       ├── EPILOGUE-SCENES.md
│       └── ... (other final arc scenes)
├── CHARACTER-MOMENTS/
│   ├── CASPIAN-SCENES.md
│   ├── CORVIN-SCENES.md
│   ├── KAELEN-SCENES.md
│   └── ... (per-character scene collections)
└── DRAFTS-AND-FRAGMENTS/ (temporary working area)
    ├── scene-DRAFT.md
    └── ... (experimental scenes)
```

### D. Consolidate `/characters/` Further

**Current State**: Already good (TIER-PRIMARY, TIER-SECONDARY, TIER-ENSEMBLE)

**Recommended Addition**: Create `characters/RELATIONSHIP-MAPS/` folder

```
characters/
├── CHARACTER-MASTER-INDEX.md ✓
├── TIER-PRIMARY/ ✓
├── TIER-SECONDARY/ ✓
├── TIER-ENSEMBLE/ ✓
├── RELATIONSHIP-MAPS/
│   ├── AISEN-RELATIONSHIPS.md (allies, mentors, rivals)
│   ├── CASPIAN-RELATIONSHIPS.md
│   ├── FACTION-ALIGNMENTS.md (who supports whom)
│   └── LOVE-INTERESTS-AND-BONDS.md
└── ARCS-AND-DEATHS/ (new)
    ├── CHARACTER-DEATH-TIMELINE.md
    ├── CHARACTER-ARCS-SUMMARY.md
    └── LEGACY-AND-AFTERMATH.md
```

---

## PART 4: ACTION PLAN (Implementation Order)

### Phase 1: Create Missing Files (1–2 hours)

**Step 1.1**: Create `AI/DEEPSEEK-BATCH-1.md`
- Extract from original source or reconstruct from DEEPSEEK-BATCH-2 opening summary
- Content: Cosmology, magic physics, Aelfar origins, Flux foundations (lines 1–5000)
- Add to `AI/reference/` once created

**Step 1.2**: Verify or rename `story/scene-heresy-tribunal.md` 
- Check if content aligns with tribunal description in batches
- Rename to `story/SCENE-TRIBUNAL.md` for consistency with other scaffold names
- OR copy to scene-collection folder

### Phase 2: Create Folder Structure (30 mins – structural setup only)

**Step 2.1**: Create `/AI/reference/` folder  
**Step 2.2**: Create `/worldbuilding/` folder with subfolders  
**Step 2.3**: Create `/story/CHAPTER-BY-CHAPTER/`, `/SCENES-BY-ARC/`, `/CHARACTER-MOMENTS/`, `/DRAFTS/`  
**Step 2.4**: Create `/characters/RELATIONSHIP-MAPS/` and `/ARCS-AND-DEATHS/`  

### Phase 3: Index & Documentation (2–3 hours)

**Step 3.1**: Create `worldbuilding/WORLDBUILDING-INDEX.md`
- Links to all world materials
- Rationale for structure
- Entry points for different topics

**Step 3.2**: Create `story/INDEX.md`
- Master list of all 100+ scene files
- Mapping to chapters and arcs
- Status of each scene (draft, final, etc.)

**Step 3.3**: Update existing index files
- Update `DEEPSEEK-COMPENDIUM-INDEX.md` to reference new paths
- Update `AI/WRITING-EXPANSIONS.md` with new folder layout
- Update main README.md to reference new worldbuilding hub

### Phase 4: Move Files (2–3 hours, no content changes)

**Step 4.1**: Move all `AI/DEEPSEEK-*.md` files to `AI/reference/`  
**Step 4.2**: Move chapter files from `story/` to `story/CHAPTER-BY-CHAPTER/`  
**Step 4.3**: Reorganize scene files into `story/SCENES-BY-ARC/` based on file content  
**Step 4.4**: Create character-specific scene collections in `story/CHARACTER-MOMENTS/`  

### Phase 5: Update Links & References (1–2 hours)

**Step 5.1**: Update all internal markdown links
**Step 5.2**: Update `CHAPTER-STATUS-TRACKER.md` with new paths
**Step 5.3**: Update README and navigation documents

---

## PART 5: IMPLEMENTATION PRIORITY RANKING

| Priority | Task | Time | Impact |
|----------|------|------|--------|
| 🔴 HIGH | Create DEEPSEEK-BATCH-1.md | 1 hr | Completes reference set |
| 🔴 HIGH | Create `/AI/reference/` structure | 0.5 hr | Organizes existing files |
| 🟠 MEDIUM | Create `/worldbuilding/` hub | 2 hrs | Clarifies world materials |
| 🟠 MEDIUM | Create `story/INDEX.md` | 1.5 hrs | Makes scenes discoverable |
| 🟡 LOW | Physically move scene files | 2–3 hrs | Cosmetic; minimal functional impact |
| 🟡 LOW | Create character relationship maps | 1–2 hrs | Reference; nice-to-have |

---

## PART 6: RISK MITIGATION

**Risk**: Breaking existing links when moving files  
**Mitigation**: 
1. Use `git` to track moves as renames (not delete + create)
2. Search workspace for hardcoded paths before moving
3. Create redirect index files if needed

**Risk**: Overwhelm by scope  
**Mitigation**:
1. Start with Phase 1 + high-priority Phase 2 items
2. Defer cosmetic file moves to later
3. Focus on index files first (guides navigation)

---

## PART 7: SUCCESS CRITERIA

- [ ] DEEPSEEK-BATCH-1.md created and placed in AI/reference/
- [ ] New folder structure created (worldbuilding/, story subfolders)
- [ ] Index documents written (worldbuilding/INDEX.md, story/INDEX.md)
- [ ] All DeepSeek analysis files linked from AI/reference/
- [ ] README updated to reflect new structure
- [ ] No broken links in updated documents
- [ ] Git history clean (moves tracked as renames)

---

## NEXT STEPS FOR USER

Choose one of these entry points:

1. **Start Immediately**: Run Phase 1 to unlock DEEPSEEK-BATCH-1 + AI/reference/ structure
2. **Comprehensive**: Execute all 5 phases for complete reorganization (6–8 hours total)
3. **Gradual**: Phase 1 + Phase 2 now; defer Phases 3–5 to next session

**Recommendation**: Phase 1 + Phase 2 now (focuses on discovering/organizing existing materials). Defer file moves to Phase 4 until you've verified the structure serves your writing workflow.
