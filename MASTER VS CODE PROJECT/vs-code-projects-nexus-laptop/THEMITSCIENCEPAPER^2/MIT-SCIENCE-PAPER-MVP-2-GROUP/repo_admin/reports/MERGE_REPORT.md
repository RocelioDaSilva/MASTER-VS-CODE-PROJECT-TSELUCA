# Repository-Wide Merge Report

⚠️ **DEPRECATED REPORT**: This documents June 2025 merge phase.  
For Phase 7 (April 2026) consolidation status, see [CONSOLIDATION_COMPLETION_SUMMARY.md](CONSOLIDATION_COMPLETION_SUMMARY.md).

---


**Date:** June 2025  
**Scope:** Eliminate duplicate code, consolidate overlapping documentation, clean manuscript variants

---

## Code Merges

### 1. API Duplicate: `endpoints.py` → re-export shim
- **Files:** `backend/api/endpoints.py` (12,761 bytes) was byte-identical to `backend/api/api.py`
- **Action:** Replaced `endpoints.py` with 7-line re-export: `from .api import app`
- **Updated:** `backend/api/__init__.py` now imports directly from `api.py`
- **Savings:** ~12.6 KB duplicate code eliminated

### 2. LCOE Duplicate: `analysis/lcoe.py` → re-export shim
- **Files:** `backend/analysis/lcoe.py` (18,148 bytes) duplicated `backend/scripts/lcoe_calculator.py` (19,011 bytes)
- **Canonical:** `scripts/lcoe_calculator.py` (contains `SolarParameters` dataclass + `LCOECalculator`)
- **Action:** Replaced `analysis/lcoe.py` with re-export from `scripts.lcoe_calculator`
- **Savings:** ~18 KB duplicate code eliminated

### 3. MCDA Duplicate: `analysis/mcda.py` → re-export shim
- **Files:** `backend/analysis/mcda.py` (16,612 bytes) duplicated `backend/scripts/mcda_analysis.py` (18,275 bytes)
- **Canonical:** `scripts/mcda_analysis.py` (contains `AHPWeighter` + `MCDAnalyzer`)
- **Action:** Replaced `analysis/mcda.py` with re-export from `scripts.mcda_analysis`
- **Savings:** ~16.5 KB duplicate code eliminated

### 4. Dead Dashboard: `app_refactored.py` → deprecation stub
- **File:** `backend/dashboard/app_refactored.py` (3,877 bytes)
- **Issue:** Imported non-existent modules (`home`, `data_explore`, `session_state`, `page_router`)
- **Action:** Replaced with deprecation stub raising `ImportError`
- **Working dashboard:** `backend/dashboard/app.py`

### 5. Analysis `__init__.py` Updated
- Updated `backend/analysis/__init__.py` to reflect new re-export architecture
- `__all__` now exports actual class names (`AHPWeighter`, `MCDAnalyzer`, `SolarParameters`)

---

## Manuscript Merges (5 files, ~1.7 MB saved)

### Exact Duplicates Replaced with Pointer Stubs:
| File | Original Size | Identical To |
|------|--------------|--------------|
| `SOL_BACKUP_20260305_234021.tex` | 534,390 B | `SOL_ORIGINAL.tex` |
| `08_Archive/.../submission_backup/SOL.tex` | 96,796 B | `SOL_SUBMISSION.tex` |
| `08_Archive/.../submission_backup/referencias.bib` | 2,048 B | `referencias_submission.bib` |

### Near-Duplicates Replaced with Pointer Stubs:
| File | Original Size | Near-Identical To |
|------|--------------|-------------------|
| `SOL_melhorado_BACKUP_20260315_172151.tex` | 549,633 B | `SOL_melhorado.tex` (<300 B diff) |
| `SOL_melhorado_FIXED_STRUCTURE.tex` | 549,329 B | `SOL_melhorado.tex` (<300 B diff) |

### Root .tex Files Marked Deprecated:
- `main.tex` (227 KB), `papier.tex` (8 KB), `papier_fixed.tex` (8 KB), `write.tex` (7 KB)
- All now have header: `% DEPRECATED: Canonical manuscript is Full project/01_Science/manuscript/SOL.tex`

---

## Documentation Merges (3 files, ~36 KB saved)

| Superseded File | Consolidated Into |
|----------------|-------------------|
| `ANALISE_FRAQUEZAS_COMPLETA.md` (16 KB) | `SCIENCE_PAPER_WEAKNESSES_CONSOLIDATED.md` (30 KB) |
| `CRITICAL_FIXES_PROGRESS.md` (10 KB) | `SESSION_SUMMARY_IMPROVEMENTS.md` (11 KB) |
| `RELATORIO_FINAL_MELHORIAS_BIBLIOGRAFICAS.md` (10 KB) | `Full project/MELHORIAS_BIBLIOGRAFICAS_CONCLUSAO.md` |

---

## Other Cleanups

### Operations Scripts Deprecated:
- `04_Operations/scripts/api.py` — marked deprecated (use `backend/api/api.py`)
- `04_Operations/scripts/earth_engine_integration.py` — marked deprecated (use `backend/geospatial/earth_engine_integration.py`)

### Frontend README Fixed:
- `frontend/README.md` — replaced Google AI Studio boilerplate with GEESP-Angola frontend documentation

---

## Canonical Source Map

| Component | Canonical Location |
|-----------|-------------------|
| REST API | `backend/api/api.py` |
| LCOE Calculator | `backend/scripts/lcoe_calculator.py` |
| MCDA Analysis | `backend/scripts/mcda_analysis.py` |
| Dashboard | `backend/dashboard/app.py` |
| Manuscript | `Full project/01_Science/manuscript/SOL.tex` |
| Bibliography | `Full project/01_Science/manuscript/referencias.bib` |
| Submission Version | `Full project/01_Science/manuscript/SOL_SUBMISSION.tex` |
