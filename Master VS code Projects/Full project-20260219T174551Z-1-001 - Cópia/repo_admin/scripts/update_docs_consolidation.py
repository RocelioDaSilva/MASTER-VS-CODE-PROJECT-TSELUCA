#!/usr/bin/env python3
"""
Phase 8: Post-Consolidation Documentation Updates
Updates critical documentation with new canonical paths after Phase 7 consolidation

Changes:
- CANONICAL_SOURCES.md: Update all paths to reflect post-Phase-7 locations
- MIT-SCIENCE-PAPER/README_DEPRECATION_NOTICE.md: Create deprecation notice
- MERGE_REPORT.md: Add deprecation header
"""

import os
from pathlib import Path
from typing import Dict, Tuple

class DocUpdater:
    """Update documentation after consolidation"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.stats = {
            "files_updated": 0,
            "files_created": 0,
            "replacements_made": 0,
        }
    
    def update_canonical_sources(self) -> Tuple[bool, str]:
        """Update CANONICAL_SOURCES.md with new paths"""
        filepath = self.repo_root / "repo_admin" / "reports" / "CANONICAL_SOURCES.md"
        
        if not filepath.exists():
            return False, f"File not found: {filepath}"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # CHANGE 1: Add warning section at top (after first line break)
            warning_section = """---

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

"""
            
            # Insert warning after first title line
            parts = content.split('---', 1)
            if len(parts) > 1:
                content = parts[0] + '---' + warning_section + parts[1]
            
            # CHANGE 2: Update primary manuscript path
            content = content.replace(
                '**Location:** `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/SOL.tex`',
                '**Location:** `manuscript_unified/science_manuscript/SOL.tex` ← **NEW POST-PHASE-7 LOCATION**\n**Previous Location:** `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/SOL.tex` (deprecated, read-only)'
            )
            
            # CHANGE 3: Update last updated date
            content = content.replace(
                '**Last Updated:** April 17, 2026 (cost-benefit section, validation clarifications, Results expansion)',
                '**Last Updated:** April 18, 2026 (Phase 7 consolidation - moved to manuscript_unified/)'
            )
            
            # CHANGE 4: Update bibliography path
            content = content.replace(
                '**Location:** `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/referencias.bib`',
                '**Location:** `manuscript_unified/science_manuscript/referencias.bib` ← **NEW POST-PHASE-7 LOCATION**\n**Previous Location:** `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/referencias.bib` (deprecated, read-only)'
            )
            
            # CHANGE 5: Update figure sources path
            content = content.replace(
                '**Location:** `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/figures/`',
                '**Location:** `manuscript_unified/science_manuscript/figures/` ← **NEW POST-PHASE-7 LOCATION**\n**Previous Location:** `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/figures/` (deprecated)'
            )
            
            # CHANGE 6: Update workflow section
            content = content.replace(
                '1. **Always edit:** `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/SOL.tex` (canonical only)',
                '1. **Always edit:** `manuscript_unified/science_manuscript/SOL.tex` (canonical only) ← **POST-PHASE-7**\n   - Old path: `MIT-SCIENCE-PAPER/Full project/01_Science/manuscript/SOL.tex` (now deprecated)'
            )
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.stats["files_updated"] += 1
                self.stats["replacements_made"] += 6
                return True, f"Updated: {filepath.relative_to(self.repo_root)}"
            else:
                return True, "No changes needed"
        
        except Exception as e:
            return False, f"Error updating CANONICAL_SOURCES.md: {str(e)}"
    
    def create_deprecation_notice(self) -> Tuple[bool, str]:
        """Create MIT-SCIENCE-PAPER/README_DEPRECATION_NOTICE.md"""
        filepath = self.repo_root / "MIT-SCIENCE-PAPER" / "README_DEPRECATION_NOTICE.md"
        
        content = """# MIT-SCIENCE-PAPER/ - DEPRECATION NOTICE

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
"""
        
        try:
            # Create directory if needed
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.stats["files_created"] += 1
            return True, f"Created: {filepath.relative_to(self.repo_root)}"
        except Exception as e:
            return False, f"Error creating deprecation notice: {str(e)}"
    
    def update_merge_report(self) -> Tuple[bool, str]:
        """Add deprecation header to MERGE_REPORT.md"""
        filepath = self.repo_root / "repo_admin" / "reports" / "MERGE_REPORT.md"
        
        if not filepath.exists():
            return False, f"File not found: {filepath}"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if deprecation notice already exists
            if "DEPRECATED REPORT" in content:
                return True, "Deprecation notice already present"
            
            # Add deprecation notice after first title
            deprecation = """⚠️ **DEPRECATED REPORT**: This documents June 2025 merge phase.  
For Phase 7 (April 2026) consolidation status, see [CONSOLIDATION_COMPLETION_SUMMARY.md](CONSOLIDATION_COMPLETION_SUMMARY.md).

---

"""
            
            # Insert after first line/title
            lines = content.split('\n', 1)
            if len(lines) > 1:
                content = lines[0] + '\n\n' + deprecation + lines[1]
            else:
                content = lines[0] + '\n\n' + deprecation + content
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.stats["files_updated"] += 1
            return True, f"Updated: {filepath.relative_to(self.repo_root)}"
        
        except Exception as e:
            return False, f"Error updating MERGE_REPORT.md: {str(e)}"
    
    def run(self):
        """Execute all updates"""
        print("=" * 80)
        print("PHASE 8: POST-CONSOLIDATION DOCUMENTATION UPDATES")
        print("=" * 80)
        print()
        
        operations = [
            ("Updating CANONICAL_SOURCES.md", self.update_canonical_sources),
            ("Creating deprecation notice", self.create_deprecation_notice),
            ("Updating MERGE_REPORT.md", self.update_merge_report),
        ]
        
        for name, operation in operations:
            print(f"[*] {name}...")
            success, message = operation()
            status = "✅" if success else "❌"
            print(f"    {status} {message}")
        
        print()
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Files updated: {self.stats['files_updated']}")
        print(f"Files created: {self.stats['files_created']}")
        print(f"Replacements made: {self.stats['replacements_made']}")
        print()
        print("Next steps:")
        print("1. Review changes in VS Code")
        print("2. Commit to git: git commit -m 'fix(docs): Phase 7 post-consolidation path updates'")
        print("3. Create backup branch: git branch backup/pre-phase7-consolidation HEAD~1")


if __name__ == "__main__":
    # Find repo root (parent of repo_admin)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent  # From repo_admin/scripts -> repo_admin -> root
    
    if not (repo_root / "repo_admin").exists():
        print("ERROR: Could not find repo_admin folder. Are you in the right directory?")
        exit(1)
    
    updater = DocUpdater(repo_root)
    updater.run()
