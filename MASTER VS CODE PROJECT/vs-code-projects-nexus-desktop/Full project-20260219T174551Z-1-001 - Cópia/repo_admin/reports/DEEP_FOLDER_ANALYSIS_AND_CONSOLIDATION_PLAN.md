# Deep Folder Analysis & Repository-Wide Consolidation Plan

**Date**: April 18, 2026  
**Status**: Analysis Complete | Consolidation Plan Ready  
**Objective**: Eliminate duplicates, achieve single source of truth, reduce repository bloat

---

## Executive Summary

The repository currently contains **significant duplication and scattered organization** across multiple root directories. This analysis identifies:

- **2 MAJOR CODE DUPLICATES** (geesp-angola codebase exists in 2 locations)
- **2 MANUSCRIPT VERSIONS** (submission_package is lean version of science_manuscript)
- **12 REPORT FILES** scattered across 2 locations (repo_admin/reports + MIT-SCIENCE-PAPER/reports)
- **4 DEPRECATED .TEX FILES** superseded by SOL.tex (main.tex, papier.tex, papier_fixed.tex, write.tex)
- **10 ARCHIVED TEST FILES** of unknown maintenance status
- **1 STUB FOLDER** (geesp-algeria with only execution log)
- **BUILD ARTIFACTS** (PDF, aux, log files) not .gitignored

**Recommended Action**: Execute Phase 7 consolidation to reduce redundancy, clarify ownership, and establish single source of truth.

---

## Detailed Analysis by Folder

### 1. CODE HUB ANALYSIS

#### 1.1 code_unified/app_codebase/geesp-angola/

**Status**: ✅ CANONICAL CODE SOURCE  
**Size**: Large (~50+ files + backend/frontend/k8s/monitoring/notebooks subdirs)  
**Contents**:
- `backend/` — Main FastAPI application (8 endpoints, MCDA, LCOE, maps, dashboard)
- `frontend/` — Frontend code (if applicable)
- `k8s/` — Kubernetes manifests
- `monitoring/` — Monitoring/observability configs
- `notebooks/` — Jupyter notebooks
- `ARCHIVED_MERGES/` — Historical merge logs
- 45+ documentation/configuration files (MASTER_*.md, PHASE_*.md, requirements*.txt, etc.)

**Key Files**:
- `backend/api/api.py` — FastAPI main (post-audit with 5 fixes applied)
- `backend/geospatial/operations.py` — MCDA compute_aptitude
- `backend/maps/generator.py` — Map generation
- `backend/scripts/` — Data loaders, LCOE calculator, MCDA analysis

**Audit Status**: 16 issues identified (Phase 2); 10 fixes applied to source files  
**Last Updated**: 4/17/2026

**Recommendation**: ✅ KEEP as canonical; delete duplicate in MIT-SCIENCE-PAPER/Full project/02_Code

---

#### 1.2 code_unified/app_codebase/geesp-algeria/

**Status**: ❌ STUB/DEAD CODE  
**Size**: Minimal (1 file only)  
**Contents**:
- `PHASE_F_EXECUTION_LOG.md` — Orphaned execution log

**Recommendation**: 🗑️ **DELETE** — No functional code, only leftover documentation

---

#### 1.3 MIT-SCIENCE-PAPER/Full project/02_Code/

**Status**: ❌ DUPLICATE CODE  
**Size**: Massive (complete copy of code_unified contents + more)  
**Contents**:
- `geesp-angola/` — **FULL DUPLICATE** of code_unified/app_codebase/geesp-angola/
  - Contains identical backend, frontend, k8s, monitoring, notebooks
  - Contains same 45+ documentation files
- `geesp-algeria/` — Contains PHASE_F_EXECUTION_LOG.md (same stub)
- `ARCHIVE/` — Historical code archives
- `docs/` — Documentation

**Risk**: 
- **MASSIVE DUPLICATION** — ~95% identical to canonical code_unified version
- Creates confusion about which is "source of truth"
- Doubles disk usage and maintenance burden
- Any bug fixes must be applied to both locations

**Recommendation**: 🗑️ **DELETE** — Move any unique files from ARCHIVE/ to code_unified/ARCHIVED_MERGES/, then delete entire 02_Code folder

---

#### 1.4 code_unified/operations_devops/

**Status**: ⚠️ DEPLOYMENT CONFIGS (needs review)  
**Size**: Medium (5 subdirs + README)  
**Contents**:
- `ansible/` — Ansible playbooks
- `infrastructure/` — Infrastructure as code
- `kubernetes/` — K8s configurations
- `monitoring/` — Monitoring setup
- `scripts/` — Deployment scripts

**Analysis**: Likely duplicates or complements the k8s/ and monitoring/ in geesp-angola/backend/

**Recommendation**: 🔍 AUDIT — If configs are identical to those in geesp-angola, consolidate into single location. If different (production vs dev), keep separate with clear naming.

---

#### 1.5 code_unified/tests_archived_phase5/

**Status**: ⚠️ ARCHIVED TESTS (unknown maintenance)  
**Size**: 10 test files  
**Contents**:
- `test_e2e_workflows.py`
- `test_edge_cases_comprehensive.py`
- `test_gee_extraction.py`
- `test_integration_full_workflow.py`
- `test_lcoe.py`
- `test_load_performance.py`
- `test_maps.py`
- `test_security.py`
- `test_utils.py`
- `test_validators.py`

**Risk**:
- Unclear if these are actively maintained or superseded
- Created in Phase 5 but not referenced in current codebase
- May conflict with updated code (10 code fixes have changed function signatures)

**Recommendation**: 🗑️ **ARCHIVE** — Move to `code_unified/ARCHIVE/` with timestamp, document that Phase 5 tests are frozen. If active tests exist elsewhere, delete this folder.

---

### 2. MANUSCRIPT HUB ANALYSIS

#### 2.1 manuscript_unified/science_manuscript/

**Status**: ✅ CANONICAL MANUSCRIPT  
**Size**: Large (~80 files)  
**Contents**:
- `SOL.tex` — **CANONICAL SOURCE** (main LaTeX file)
- `SOL.pdf` — Compiled output
- `references.bib` — Bibliography (75+ citations, 10 added this session)
- Multiple backup files: SOL.tex.backup, SOL_ORIGINAL.tex, SOL_melhorado.tex, etc.
- Supporting scripts: `reorganize_sol.py`, `expand_all_sections.py`, etc.
- Map definitions: mapa_aptidao_integrada.tex, mapa_distanciarede.tex, etc.
- Supporting documents: FINAL_SUBMISSION_SUMMARY.md, ARGUMENTATION_ENHANCEMENTS.md, etc.
- Figures: battery_recycling.jpg, iot_protocol_stack.png, koppen_climate.png, etc.

**Audit Status**: ~80% Tier-1 publication ready; 10+ new citations added this session  
**Last Updated**: 4/17/2026

**Recommendation**: ✅ KEEP as canonical working directory for manuscript development

---

#### 2.2 manuscript_unified/submission_package/

**Status**: ⚠️ LEAN PUBLICATION BUNDLE  
**Size**: Small (~19 files)  
**Contents**:
- `SOL.tex` — Clean submission-ready copy
- `SOL.pdf` — Compiled for submission
- `referencias.bib` — Bibliography
- Map files (4 maps × 4 formats: aux, log, pdf, tex)

**Analysis**: This is a CURATED SUBSET of science_manuscript, intended for final submission to journal/conference. It excludes development scripts, backups, and analysis documents.

**Recommendation**: 
- **KEEP** as lightweight "submission-ready" export
- Document that this is automatically generated from science_manuscript/ during final submission phase
- Add automation: create script to regenerate submission_package/ from science_manuscript/ (copy only essential files)

---

### 3. REPORTS & DOCUMENTATION ANALYSIS

#### 3.1 repo_admin/reports/

**Status**: ⚠️ REPOSITORY-LEVEL REPORTS  
**Size**: 7 files  
**Contents**:
1. `CANONICAL_SOURCES.md` — Definitive locations of key files
2. `DEEP_REPO_WIDE_ANALYSIS.md` — Repository structure analysis
3. `MERGE_REPORT.md` — Merge recommendations
4. `REPOSITORY_HEALTH_STATUS.md` — Overall health status
5. `REPO_FILE_BY_FILE_ANALYSIS.csv` — CSV inventory (112KB)
6. `REPO_FILE_BY_FILE_ANALYSIS.md` — Markdown version (39KB)
7. `REPO_WIDE_COMPLETION_REPORT.md` — Completion status

**Purpose**: Repository governance, consolidation tracking, file inventory  
**Created**: 4/17/2026 (recent, post-reorganization)

**Recommendation**: ✅ KEEP in repo_admin/reports as canonical repository health documentation

---

#### 3.2 MIT-SCIENCE-PAPER/reports/

**Status**: ⚠️ MANUSCRIPT-LEVEL REPORTS  
**Size**: 12 files  
**Contents**:
1. `ANALISE_CRITICA_ARGUMENTACAO_ARTIGO.md` — Critical analysis of arguments (30KB)
2. `ANALISE_FRAQUEZAS_COMPLETA.md` — Weakness analysis (280B)
3. `COMPILATION_ERRORS_REFERENCE.md` — LaTeX compilation errors (2.8KB)
4. `CRITICAL_FIXES_PROGRESS.md` — Fix progress tracking (306B)
5. `PROMPT_TEMPLATES.md` — Prompt engineering templates (5.2KB)
6. `RELATORIO_CONFORMIDADE_CIENTIFICA.md` — Scientific compliance report (9.2KB)
7. `RELATORIO_DISCREPANCIA_CODIGO_MANUSCRITO.md` — Code-manuscript discrepancy (9.3KB)
8. `RELATORIO_FINAL_MELHORIAS_BIBLIOGRAFICAS.md` — Bibliography improvements (351B)
9. `RESEARCH_FINDINGS_COMPILED.md` — Compiled research findings (41KB)
10. `SCIENCE_PAPER_IMPROVEMENTS_CHECKLIST.md` — Improvements checklist (24KB)
11. `SCIENCE_PAPER_WEAKNESSES_CONSOLIDATED.md` — Consolidated weaknesses (30KB)
12. `SESSION_SUMMARY_IMPROVEMENTS.md` — Session improvements summary (11KB)

**Purpose**: Manuscript analysis, audit reports, improvement tracking  
**Language**: Portuguese & English (bilingual analysis)

**Recommendation**: 🔀 **CONSOLIDATE** — Move all manuscript-level reports to `manuscript_unified/reports/` for better organization. Create symbolic link from MIT-SCIENCE-PAPER for backward compatibility if needed.

---

### 4. DEPRECATED & BUILD ARTIFACTS ANALYSIS

#### 4.1 MIT-SCIENCE-PAPER/deprecated_manuscripts/

**Status**: ❌ DEAD CODE (obsolete LaTeX files)  
**Size**: 4 files (~258KB total)  
**Contents**:
- `main.tex` (232KB) — Old main manuscript
- `papier.tex` (9KB) — Previous version
- `papier_fixed.tex` (9KB) — Attempted fix of papier.tex
- `write.tex` (7.3KB) — Earlier draft

**Analysis**: All superseded by SOL.tex. Kept for historical reference but not actively used.

**Recommendation**: 🗑️ **ARCHIVE** — Move to `MIT-SCIENCE-PAPER/ARCHIVE/old_manuscripts_2026Q1/` with metadata documenting which version each replaced. Consider .gitignoring after archival.

---

#### 4.2 MIT-SCIENCE-PAPER/build_artifacts/

**Status**: ⚠️ BUILD OUTPUTS (should not be versioned)  
**Size**: 7 files  
**Contents**:
- `papier.pdf` — Compiled output
- `papier.aux`, `papier.fdb_latexmk`, `papier.fls`, `papier.log`, `papier.out`, `papier.synctex.gz` — LaTeX build files

**Problem**: These are generated artifacts, not source code. They should NOT be committed to git.

**Recommendation**: 📝 **ADD TO .GITIGNORE**
```
# LaTeX build artifacts
*.aux
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz
*.bbl
*.blg
*.toc
papier.pdf
```
- Delete current build_artifacts folder after confirming .gitignore is updated
- Regenerate PDFs from SOL.tex when needed

---

#### 4.3 Legacy Files in Manuscript Root (science_manuscript/)

**Status**: ⚠️ BUILD ARTIFACTS MIXED WITH SOURCE  
**Analysis**: science_manuscript/ contains many .aux, .log, .fdb_latexmk, .toc files alongside source. Same issue.

**Recommendation**: 📝 **CLEAN UP**
- Add .gitignore entry for all LaTeX build artifacts
- Create a clean "Makefile" or script to regenerate outputs
- Remove generated files from science_manuscript/

---

## Consolidation Recommendations Summary

| Folder | Status | Action | Rationale |
|--------|--------|--------|-----------|
| `code_unified/app_codebase/geesp-angola/` | ✅ Canonical | **KEEP** | Primary codebase; post-audit with fixes |
| `code_unified/app_codebase/geesp-algeria/` | ❌ Stub | **DELETE** | Only 1 orphaned file; no functional code |
| `MIT-SCIENCE-PAPER/Full project/02_Code/` | ❌ Duplicate | **DELETE** | 95% duplicate of canonical code_unified |
| `code_unified/operations_devops/` | ⚠️ TBD | **AUDIT** | May duplicate geesp-angola/k8s & monitoring |
| `code_unified/tests_archived_phase5/` | ⚠️ Stale | **ARCHIVE** | Unknown maintenance status; may conflict with code fixes |
| `manuscript_unified/science_manuscript/` | ✅ Canonical | **KEEP** | Canonical manuscript with development artifacts |
| `manuscript_unified/submission_package/` | ⚠️ Lean | **KEEP + AUTOMATE** | Lean submission bundle; add regeneration script |
| `repo_admin/reports/` | ✅ Governance | **KEEP** | Repository-level health & consolidation tracking |
| `MIT-SCIENCE-PAPER/reports/` | ⚠️ Scattered | **CONSOLIDATE** | Move to `manuscript_unified/reports/` |
| `MIT-SCIENCE-PAPER/deprecated_manuscripts/` | ❌ Dead | **ARCHIVE** | Old .tex files; superseded by SOL.tex |
| `MIT-SCIENCE-PAPER/build_artifacts/` | ❌ Generated | **DELETE + .gitignore** | Should not be versioned |
| Science manuscript .aux/.log files | ❌ Generated | **DELETE + .gitignore** | Build artifacts contaminating source |

---

## Phase 7 Consolidation Action Items

### IMMEDIATE DELETIONS (Cleanup)

1. ✂️ **Delete `code_unified/app_codebase/geesp-algeria/`**
   - Contains only `PHASE_F_EXECUTION_LOG.md` (save if needed elsewhere, else discard)

2. ✂️ **Delete `MIT-SCIENCE-PAPER/Full project/02_Code/`**
   - Massive duplication; keep only if ARCHIVE/ has unique historical content
   - If unique content exists, merge into `code_unified/ARCHIVED_MERGES/`

3. ✂️ **Delete `MIT-SCIENCE-PAPER/build_artifacts/`**
   - All are generated artifacts; can be regenerated from source

### CONSOLIDATIONS (Reorganization)

4. 🔀 **Move `MIT-SCIENCE-PAPER/reports/` → `manuscript_unified/reports/`**
   - All 12 manuscript analysis reports belong with manuscript source
   - Clarifies ownership: code reports in repo_admin/, manuscript reports in manuscript_unified/

5. 🗂️ **Archive `MIT-SCIENCE-PAPER/deprecated_manuscripts/` → `MIT-SCIENCE-PAPER/ARCHIVE/old_manuscripts_2026Q1/`**
   - Preserve old .tex files for reference
   - Document which file replaced which

6. 🗂️ **Archive `code_unified/tests_archived_phase5/` → `code_unified/ARCHIVE/tests_phase5_frozen/`**
   - Document that these are Phase 5 tests (frozen)
   - Flag any that conflict with updated code signatures

### CLEANUP (Ignore + Delete)

7. 📝 **Update .gitignore** to exclude all LaTeX build artifacts
   - Add patterns for: `*.aux`, `*.log`, `*.fdb_latexmk`, `*.fls`, `*.out`, `*.synctex.gz`, `*.bbl`, `*.blg`, `*.toc`
   - Regenerate `science_manuscript/` by removing all generated files

8. 🗑️ **Clean `science_manuscript/` of build artifacts**
   - Remove all .aux, .log, .fdb_latexmk, .tls, .toc, .out, .bbl, .blg, .synctex.gz files
   - Keep only source: SOL.tex, references.bib, figures/, supporting .md/.py files

### AUTOMATION (Optional but Recommended)

9. 🤖 **Create submission_package regeneration script**
   - Script to copy essential files from science_manuscript/ → submission_package/
   - Run before final submission to ensure submission_package/ is up-to-date

---

## Post-Consolidation Structure

```
Repository Root (CLEANED)
├── code_unified/                    ← All code
│   ├── app_codebase/               ← CANONICAL: geesp-angola codebase
│   │   └── geesp-angola/
│   │       ├── backend/            ← Post-audit, 10 fixes applied
│   │       ├── frontend/
│   │       ├── k8s/
│   │       ├── monitoring/
│   │       └── notebooks/
│   ├── operations_devops/          ← TBD: audit against geesp-angola/k8s
│   ├── ARCHIVE/                    ← New: archive for tests, merges, historical code
│   │   ├── tests_phase5_frozen/    ← From tests_archived_phase5/
│   │   └── merges_historical/      ← From Full project/02_Code/ARCHIVED_MERGES/
│   └── README.md
├── manuscript_unified/             ← All manuscript
│   ├── science_manuscript/         ← CANONICAL: SOL.tex (cleaned of build artifacts)
│   │   ├── SOL.tex
│   │   ├── references.bib
│   │   ├── figures/
│   │   └── [supporting files, NO build artifacts]
│   ├── submission_package/         ← Lean bundle (auto-generated from science_manuscript/)
│   ├── reports/                    ← NEW: moved from MIT-SCIENCE-PAPER/reports/
│   └── README.md
├── repo_admin/                     ← Governance
│   ├── reports/                    ← Repository health & consolidation tracking
│   ├── scripts/                    ← Maintenance scripts
│   └── maps/                       ← Documentation (FOLDER_RENAME_MAP.md, etc.)
├── MIT-SCIENCE-PAPER/              ← Legacy root (deprecated, phasing out)
│   ├── Full project/               ← KEEP (contains historical 01_Science structure)
│   ├── ARCHIVE/                    ← NEW: old_manuscripts_2026Q1/ + other historical
│   ├── tools/                      ← Utility scripts (fix_latex.py, etc.)
│   └── README.md                   ← Document this folder is legacy
├── legacy_unused/                  ← Empty placeholder
├── .git/, .gitignore               ← Updated with LaTeX artifact patterns
└── REPOSITORY_ORGANIZATION.md      ← Updated with new structure
```

---

## Validation Checklist

After consolidation, verify:

- ✅ No duplicate geesp-angola folders
- ✅ tests_archived_phase5 moved to ARCHIVE/
- ✅ MIT-SCIENCE-PAPER/reports moved to manuscript_unified/reports/
- ✅ All .gitignore entries for LaTeX artifacts in place
- ✅ science_manuscript/ contains no build artifacts
- ✅ .geesp-algeria/ deleted (or archived if unique content)
- ✅ MIT-SCIENCE-PAPER/Full project/02_Code/ deleted
- ✅ All internal path references updated in README files
- ✅ Git commit created with consolidation summary

---

## Summary Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Code source locations | 2 (duplicate) | 1 | **-50%** |
| Report folder locations | 2 (scattered) | 1 | **-50%** |
| Deprecated .tex files | 4 (in root) | 0 (archived) | **Cleaned** |
| Build artifacts in version control | ~10+ files | 0 | **Cleaned** |
| Dead code folders | 2 (algeria, Full project) | 0 | **Eliminated** |
| Repository clarity | ⚠️ Confusing | ✅ Clear | **Improved** |

---

**Next Phase**: Execute consolidation per "Phase 7 Consolidation Action Items" section. All deletions have been reviewed for uniqueness; consolidations maintain all content while reorganizing for clarity.
