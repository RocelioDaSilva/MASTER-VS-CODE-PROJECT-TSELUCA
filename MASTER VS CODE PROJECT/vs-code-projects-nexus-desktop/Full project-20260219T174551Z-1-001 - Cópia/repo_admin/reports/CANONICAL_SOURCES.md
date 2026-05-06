# Canonical Sources - Single Source of Truth
**Date:** April 17, 2026  
**Purpose:** Establish definitive manuscript, bibliography, and figure sources to eliminate edit divergence and compilation confusion

------

## ⚠️ PHASE 7 CONSOLIDATION UPDATE (April 18, 2026)

**CRITICAL**: The canonical manuscript locations have changed due to repository consolidation.

**OLD Locations** (Pre-Phase 7):
- Manuscript: `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/SOL.tex`
- Bibliography: `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/referencias.bib`

**NEW Locations** (Post-Phase 7): ✅ **USE THESE**
- Manuscript: `manuscript_unified/science_manuscript/SOL.tex`
- Bibliography: `manuscript_unified/science_manuscript/referencias.bib`

All team members must update bookmarks and scripts to use NEW consolidated locations.

The old `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/` folder is now **READ-ONLY LEGACY REFERENCE** only.

See [CONSOLIDATION_COMPLETION_SUMMARY.md](CONSOLIDATION_COMPLETION_SUMMARY.md) for Phase 7 details.



## 📌 CANONICAL SOURCES (OFFICIAL)

### Primary Manuscript
**Location:** `manuscript_unified/science_manuscript/SOL.tex` ← **NEW POST-PHASE-7 LOCATION**
**Previous Location:** `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/SOL.tex` (deprecated, read-only)  
**Status:** ✅ ACTIVE - This is the only working copy; all edits happen here  
**Last Updated:** April 18, 2026 (Phase 7 consolidation - moved to manuscript_unified/)  
**Lines:** ~5,848  
**Language:** Portuguese  
**Purpose:** Primary peer-reviewed manuscript for GEESP-Angola framework

**Citation Key:**
```bibtex
@article{geesp_angola_2026,
  title={GEESP-Angola: Framework de Análise Multi-Critério para Seleção de Sítios Solares},
  author={...},
  year={2026}
}
```

---

### Bibliography/References
**Location:** `manuscript_unified/science_manuscript/referencias.bib` ← **NEW POST-PHASE-7 LOCATION**
**Previous Location:** `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/referencias.bib` (deprecated, read-only)  
**Status:** ✅ ACTIVE - Single authoritative bibliography  
**Entries:** 114 total (99 cited, 15 unused)  
**Language:** Mixed (Portuguese keys, English/Portuguese metadata)  
**Last Citation Audit:** April 17, 2026 (fixed: `Governo_Angola_2022` case sensitivity)

**Verification Status:**
- Citation keys in SOL.tex: 99 (all matched)
- Unused entries in .bib: 15 (archival only, not used)
- Missing keys: 0 (all citations resolved)

---

### Figure Sources
**Location:** `manuscript_unified/science_manuscript/figures/` ← **NEW POST-PHASE-7 LOCATION**
**Previous Location:** `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/figures/` (deprecated)  
**Status:** ⚠️ NEEDS VERIFICATION - No figures directory found yet  
**Expected Content:** Map outputs, MCDA result visualizations, sensitivity charts  
**Action Required:** If figures are generated from code, document generation scripts here

---

## 📑 NON-CANONICAL VARIANTS (DO NOT EDIT)

### Submission Variants (Archive Only)
These are exports for journal submission; **DO NOT EDIT** — regenerate from canonical when needed.

| Path | Purpose | Status | Last Updated |
|------|---------|--------|---|
| `Full project/Coding parts/SUBMISSION_READY/SOL.tex` | Export for submission formatting | Archive | Unknown |
| `Full project/01_Science/manuscript/SOL_SUBMISSION.tex` | Journal submission copy | Archive | Unknown |

**Action:** Mark as read-only; regenerate from canonical `SOL.tex` before any journal submission.

---

### Development/Improvement Variants (Archive Only)
These are experimental versions; **DO NOT EDIT** — archive only, for reference.

| Path | Purpose | Status | Last Updated |
|------|---------|--------|---|
| `Full project/01_Science/manuscript/SOL_melhorado.tex` | "Improved" version (experimental) | Archive | ~March 2026 |
| `Full project/01_Science/manuscript/SOL_melhorado_FIXED_STRUCTURE.tex` | Structure-fixed variant | Archive | ~March 2026 |
| `Full project/01_Science/manuscript/SOL_ORIGINAL.tex` | Original baseline | Archive | Pre-2026 |
| `Full project/01_Science/manuscript/SOLEX.tex` | Purpose unknown | Archive | Unknown |

**Action:** Move to `08_Archive/development_variants/` for clarity.

---

### Timestamped Backups (Archive Only)
Automated/manual backup snapshots; **DO NOT EDIT**.

| Path | Timestamp | Status |
|------|-----------|--------|
| `Full project/01_Science/manuscript/SOL_melhorado_BACKUP_20260315_172151.tex` | 2026-03-15 17:21:51 | Archive |
| `Full project/01_Science/manuscript/SOL_BACKUP_20260305_234021.tex` | 2026-03-05 23:40:21 | Archive |

**Action:** Move to `08_Archive/timestamped_backups/` with consistent naming: `SOL_BACKUP_YYYYMMDD_HHMMSS.tex`.

---

### Archived Versions (08_Archive/)
Historical archive snapshots; **READ-ONLY for reference only**.

| Path | Purpose | Status |
|------|---------|--------|
| `Full project/08_Archive/archive/OLD_VERSIONS/old_manuscripts/SOL.tex` | Old version snapshot | Archive |
| `Full project/08_Archive/archive/OLD_VERSIONS/old_manuscripts/SOL_backup_20260207_230841.tex` | Dated backup | Archive |
| `Full project/08_Archive/archive/OLD_VERSIONS/old_manuscripts/SOLV2IMPROVBYPT.TEX` | Experimental variant | Archive |
| `Full project/08_Archive/archive/BACKUP_SNAPSHOTS/submission_backup/SOL.tex` | Submission snapshot | Archive |

---

### Translations (06_Translations/)
Language-specific versions; **DERIVED from canonical**, update when canonical changes.

| Path | Language | Status | Action Required |
|------|----------|--------|---|
| `Full project/06_Translations/translations/pt/manuscript/SOL.tex` | Portuguese | Derived | Re-sync when canonical updated |

---

## 🔄 WORKFLOW

### When Making Edits
1. **Always edit:** `manuscript_unified/science_manuscript/SOL.tex` (canonical only) ← **POST-PHASE-7**
   - Old path: `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/SOL.tex` (now deprecated)
2. **Never edit:** Any variant listed as "Archive," "Backup," or "Derived"
3. **Update bibliography:** `referencias.bib` (same directory as canonical)
4. **Document changes:** Update last-updated date and commit message

### When Preparing Submission
1. **Generate from canonical:** Copy `SOL.tex` → `SOL_SUBMISSION.tex` (format as needed for journal)
2. **Maintain link:** Document generation date and source version
3. **Archive result:** Keep submission copy in `08_Archive/submission_${DATE}/`

### When Updating Figures
1. **Store sources:** Code scripts that generate figures in `figures/scripts/`
2. **Store outputs:** Generated figures in `figures/outputs/`
3. **Link to text:** Reference relative paths in canonical manuscript

### When Archiving
1. **Use consistent naming:** `VARIANT_BACKUP_YYYYMMDD_HHMMSS.tex` for timestamped backups
2. **Document purpose:** Add comment in first 5 lines explaining variant's purpose
3. **Location:** Archive in `08_Archive/` with clear subdirectory structure

---

## ✅ VERIFICATION CHECKLIST

After implementing this policy:

- [ ] Canonical `SOL.tex` is the only active working file in `01_Science/manuscript/`
- [ ] All other variants are marked as archived/derived in clear subdirectories
- [ ] Bibliography `referencias.bib` is synchronized with canonical manuscript
- [ ] Citation audit passes: 0 missing keys, 0 duplicate entries
- [ ] Submission exports are regenerated from canonical before each submission attempt
- [ ] Translations are flagged as "derived from canonical as of DATE"
- [ ] All team members aware of canonical source location
- [ ] No edits made to archived variants (version control shows read-only or no commits)

---

## � DEPLOYMENT & OPERATIONS (Phase 7 Consolidation Decision - April 18, 2026)

### Primary Deployment Configs
**Location:** `code_unified/operations_devops/`  
**Status:** ✅ CANONICAL - Production infrastructure configurations  
**Contents:**
- `kubernetes/` — Production Kubernetes manifests (geesp-production namespace, statefulsets)
- `monitoring/` — Prometheus, Alertmanager, Grafana dashboards
- `ansible/` — Infrastructure provisioning scripts
- `infrastructure/` — IaC and infrastructure definitions
- `scripts/` — Deployment and maintenance utilities

### Relationship to Application Code
- `code_unified/app_codebase/geesp-angola/k8s/` — Application-specific k8s (development namespace, geesp-angola)
- `code_unified/app_codebase/geesp-angola/monitoring/` — Application monitoring code (monitoring_app.py)
- **Consolidation Decision:** KEEP SEPARATE (complementary, not duplicated)
  - operations_devops = infrastructure/production configs
  - geesp-angola/k8s = application deployment manifests
  - geesp-angola/monitoring = application-side monitoring code

**Rationale:** Different namespaces (geesp-production vs geesp-angola), different purposes (infrastructure vs application). Keeping separate enables independent lifecycle management.

---

## 📞 CONTACT & QUESTIONS

If unsure whether to edit a file:
1. Check this document for file path
2. If not listed as "ACTIVE," **DO NOT EDIT**
3. Contact project lead for clarification

---

**Established:** April 17, 2026  
**Last Updated:** April 18, 2026 (Phase 7 Consolidation Decision - operations_devops audit)  
**Enforced by:** Manuscript source-of-truth policy  
**Next Review:** June 2026 (after submission)
