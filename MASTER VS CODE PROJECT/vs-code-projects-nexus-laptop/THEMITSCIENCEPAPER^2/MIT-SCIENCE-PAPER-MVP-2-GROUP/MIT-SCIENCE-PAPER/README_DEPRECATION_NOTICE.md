# MIT-SCIENCE-PAPER/ - DEPRECATION NOTICE

**Status**: LEGACY FOLDER (Being phased out as of Phase 7, April 18, 2026)

This folder is no longer the canonical source for code or manuscript. All new work should use the consolidated locations below.

---

## 📍 WHERE TO FIND THINGS NOW (Post-Phase 7 Consolidation)

### **Code** ✅ CANONICAL
```
Location:  code_unified/app_codebase/geesp-angola/
Contains:  Backend (FastAPI, MCDA, LCOE), Frontend, K8s, Monitoring
Status:    ACTIVE - Edit here
Old Path:  MIT-SCIENCE-PAPER/Full project/02_Code/ [DELETED in Phase 7]
```

### **Manuscript** ✅ CANONICAL  
```
Location:  manuscript_unified/science_manuscript/SOL.tex
Contains:  Canonical LaTeX source + references.bib + figures/
Status:    ACTIVE - Edit here
Old Path:  MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/ [NOW READ-ONLY LEGACY]
```

### **Reports** 📊
```
Governance:  repo_admin/reports/
             (Repository health, consolidation status)
             
Manuscript:  manuscript_unified/reports/
             (Manuscript analysis, improvements, weaknesses)
             
Old Path:    MIT-SCIENCE-PAPER/reports/ [MOVED in Phase 7]
```

### **Deployment/Operations** ⚙️
```
Location:  code_unified/operations_devops/ (or geesp-angola/k8s/)
Status:    Post-consolidation verification pending
```

---

## 📂 WHAT'S STILL HERE (READ-ONLY REFERENCE ONLY)

| Folder | Status | Purpose | Action |
|--------|--------|---------|--------|
| `Full project/` | Deprecated | Historical project structure (reference only) | Phase 9: Delete |
| `ARCHIVE/old_manuscripts_2026Q1/` | Archived | Old .tex files (main.tex, papier.tex, etc.) | Retain for history |
| `tools/` | Legacy | Utility scripts | Migrate to repo_admin/scripts/ |

---

## 🔄 QUICK MIGRATION REFERENCE

### If looking for...

| Item | Old Path | New Path | Status |
|------|----------|----------|--------|
| **Code** | `Full project/02_Code/geesp-angola/` | `code_unified/app_codebase/geesp-angola/` | ✅ Use new |
| **Manuscript** | `Full project/01_Science/manuscript/SOL.tex` | `manuscript_unified/science_manuscript/SOL.tex` | ✅ Use new |
| **Bibliography** | `Full project/01_Science/manuscript/referencias.bib` | `manuscript_unified/science_manuscript/referencias.bib` | ✅ Use new |
| **Reports** | `MIT-SCIENCE-PAPER/reports/` | `repo_admin/reports/` or `manuscript_unified/reports/` | ✅ Use new |
| **Tests** | N/A | `code_unified/ARCHIVE/tests_phase5_frozen/` | Archived |

---

## 📋 NEXT STEPS

- [ ] Update all hardcoded path references in code/docs/scripts
- [ ] Inform team of consolidation (point to CANONICAL_SOURCES.md)
- [ ] Update internal documentation/links
- [ ] Phase 9: Plan full deletion of this folder (target: May 15, 2026)

---

## 📚 REFERENCE DOCUMENTATION

- **[CANONICAL_SOURCES.md](../repo_admin/reports/CANONICAL_SOURCES.md)** — Authoritative canonical locations (UPDATED for Phase 7)
- **[REPOSITORY_ORGANIZATION.md](../REPOSITORY_ORGANIZATION.md)** — Full repository structure
- **[CONSOLIDATION_COMPLETION_SUMMARY.md](../repo_admin/reports/CONSOLIDATION_COMPLETION_SUMMARY.md)** — Phase 7 consolidation details

---

**Deprecated**: April 18, 2026  
**Consolidation Phase**: Phase 7  
**Next Review**: May 1, 2026 (Phase 9 planning)  
**Target Deletion**: May 15, 2026
