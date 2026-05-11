# Phase 3: Implementation Plan (Ready for Execution)

## Overview
This document outlines the exact steps to execute each approved merge from Phase 2 analysis. **Do not modify any files until explicit user approval.**

---

## M001: Delete Duplicate ANPG Service Categories File

**Status:** `READY_TO_EXECUTE`

**Files Involved:**
- Delete: `docs/anpg company service categories.md`
- Keep: `docs/anpg-company-service-categories.md` (standardized filename)

**Steps:**
1. Verify both files are identical (similarity 99%)
2. Delete the non-standardized filename: `docs/anpg company service categories.md`
3. Verify no references exist in other files via grep

**Risk Level:** ⚠️ LOW (Duplicate deletion only)

**Command:**
```powershell
Remove-Item "docs/anpg company service categories.md" -Force
```

---

## M002: Create Unified Company Research Index

**Status:** `READY_TO_DESIGN`

**Files Involved:**
- Source 1: `data/company-directory/*.md` (21 hand-curated major companies)
- Source 2: `data/processed/company_hierarchy/_Profiles/*.md` (3,005 canonical profiles)
- Destination: `docs/company-research-guide.md` (NEW)

**Steps:**
1. Create new file: `docs/company-research-guide.md`
2. Add preamble explaining two-tier database structure:
   - Tier 1: Hand-curated majors (company-directory)
   - Tier 2: Full hierarchy canonicals (_Profiles)
3. Generate index linking to both directories
4. Add explanation of when to use each tier

**Risk Level:** 🟢 LOW (Creation only, no deletions)

**Estimated Lines:** 150–200

---

## M003: Merge Company Filling Scripts

**Status:** `REQUIRES_ANALYSIS`

**Files Involved:**
- Source 1: `scripts/fill_company_md.py` (simple filler)
- Source 2: `data/processed/fill_company_reports.py` (complex, 880+ lines with curated data)
- Destination: `scripts/fill_company_info.py` (NEW, merged)

**Steps:**
1. Read both scripts to identify functional differences
2. Extract common logic into utilities module (`scripts/company_utils.py`)
3. Create unified `scripts/fill_company_info.py` with mode parameter:
   - `--mode simple` → basic template
   - `--mode full` → curated 40+ companies
4. Update all imports across codebase via grep + replace
5. Delete old scripts

**Risk Level:** ⚠️ MEDIUM (Requires functional verification)

**Prerequisite:** Detailed code review of fill_company_reports.py curated data

---

## M004: Archive Redundant XLSX File

**Status:** `READY_TO_EXECUTE`

**Files Involved:**
- Keep: `data/processed/company_hierarchy.csv` (13.3MB, single source of truth)
- Keep: `data/processed/export_hierarchy_to_csv_excel.py` (script to regenerate)
- Archive: `data/processed/company_hierarchy.xlsx` (delete or move to backup folder)

**Steps:**
1. Create backup archive: `data/processed/backups/company_hierarchy.xlsx.bak`
2. Delete original: `data/processed/company_hierarchy.xlsx`
3. Update documentation noting CSV is authoritative

**Risk Level:** 🟢 LOW (XLSX is generated artifact)

**Command:**
```powershell
Move-Item "data/processed/company_hierarchy.xlsx" "data/processed/backups/company_hierarchy.xlsx.bak"
```

---

## M005: Python Pipeline Utilities Consolidation

**Status:** `REQUIRES_DESIGN`

**Files Involved:**
- Source 1: `data/processed/add_backlinks.py`
- Source 2: `data/processed/rename_files_with_company_names.py`
- Source 3: `data/processed/deduplicate_hierarchy.py`
- Destination: `scripts/company_hierarchy_pipeline.py` (NEW, orchestrator)

**Steps:**
1. Identify shared utilities from all three scripts (NIF parsing, CSV loading, etc.)
2. Extract to `scripts/company_utils.py`
3. Create unified pipeline orchestrator: `scripts/company_hierarchy_pipeline.py`
4. Refactor as:
   ```python
   if __name__ == '__main__':
       phase = sys.argv[1]  # 'rename' | 'deduplicate' | 'backlink'
       if phase == 'deduplicate': deduplicate_main()
       elif phase == 'backlink': backlink_main()
       ...
   ```
5. Keep originals for now (until validated)

**Risk Level:** ⚠️ MEDIUM (Requires refactoring + testing)

---

## M006: Consolidate TODO List into SUMMARY.md

**Status:** `READY_TO_EXECUTE`

**Files Involved:**
- Source: `docs/todo-s.md`
- Destination: `docs/SUMMARY.md` (add section)
- Archive: `docs/todo-s.md` (delete after merge)

**Steps:**
1. Read `docs/todo-s.md`
2. Extract all TODO items
3. Create "## Roadmap & TODOs" section in `docs/SUMMARY.md`
4. Convert TODO list to structured checklist
5. Delete `docs/todo-s.md`

**Risk Level:** 🟢 LOW (Consolidation only)

---

## M007: Delete Generated LaTeX File

**Status:** `READY_TO_EXECUTE`

**Files Involved:**
- Delete: `_markdown_anpg-local-content-full-data/ccc3576145d3352a38b7e11ddbc4ef71.md.tex`
- Keep: `tex/anpg-local-content-full-data.tex` (source authoritative file)

**Steps:**
1. Verify source file exists and is complete
2. Delete generated artifact directory: `_markdown_anpg-local-content-full-data/`
3. Confirm no references in code

**Risk Level:** 🟢 LOW (Generated artifact removal)

**Command:**
```powershell
Remove-Item "_markdown_anpg-local-content-full-data" -Recurse -Force
```

---

## M008: Consolidate Pipeline Entry Points

**Status:** `REQUIRES_ANALYSIS`

**Files Involved:**
- Source 1: `run_pipeline.py` (potential entry point)
- Source 2: `data/processed/generate_hierarchy.py` (another entry point)
- Source 3: `scripts/preprocess-anpg-data.py` (another entry point)
- Destination: Unified `run_pipeline.py` (refactored)

**Steps:**
1. Read all three files to determine canonical entry point
2. If `run_pipeline.py` is most general, use as base
3. Refactor to support subcommands:
   ```python
   python run_pipeline.py generate-hierarchy
   python run_pipeline.py preprocess-data
   python run_pipeline.py fill-companies
   ```
4. Move orchestration logic to `run_pipeline.py`
5. Archive old entry points (or delete if redundant)

**Risk Level:** ⚠️ MEDIUM-HIGH (Requires understanding full pipeline)

---

## Execution Priority

### Tier 1 (Safe, Execute Immediately):
- **M001:** Delete duplicate ANPG file (2 min)
- **M006:** Consolidate TODOs (5 min)
- **M007:** Delete generated .tex (2 min)

### Tier 2 (Review Required):
- **M003:** Merge fill scripts (30 min, requires code review)
- **M008:** Consolidate pipeline (20 min, requires architecture review)

### Tier 3 (Nice-to-Have):
- **M002:** [Company research guide](../docs/career/company-research-guide.md) (15 min, creation only)
- **M004:** Archive XLSX (5 min, backup first)
- **M005:** Pipeline utils consolidation (45 min, refactoring)

---

## Approval Pattern

User may respond with:
- `APPROVE MERGE [M001, M006, M007]` → Execute only these
- `APPROVE ALL` → Execute all 8 in priority order
- `APPROVE TIER 1` → Execute M001, M006, M007
- `APPROVE M003 ONLY` → Single merge only

---

## Rollback Strategy

All deletions will follow this pattern:
1. **Before any delete:** Create backup directory `data/backups/` with timestamps
2. **Example:** `git mv docs/anpg\ company\ service\ categories.md data/backups/m001_deleted_2024.md`
3. **After all merges:** Provide rollback script: `restore_from_backup.ps1`

---

## Next Step

**Awaiting user approval to proceed with Phase 3 execution.**

Reply with one of:
```
APPROVE MERGE [M001, M006, M007]
APPROVE ALL
APPROVE TIER 1
APPROVE M003, M006
```

Once approval is provided, Phase 3 implementation will execute immediately.
