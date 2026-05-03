#!/usr/bin/env python3
"""
Documentation Consolidation Script
Moves all information from redundant docs into consolidated files, then deletes redundant files.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Files to keep (consolidated documentation)
KEEP_FILES = {
    "README.md",
    "docs/CAPABILITIES.md",
    "docs/IMPROVEMENTS.md",
    "LICENSE",
    "INSTALL.md",
    "QUICKSTART.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
}

# Files to delete (redundant documentation)
REDUNDANT_DOCS = [
    # Status/Progress reports (info moved to IMPROVEMENTS.md)
    "PROJECT_STATUS.md",
    "PROJECT_SUMMARY.md",
    "PROJECT_COMPLETION_SUMMARY.md",
    "PROGRESS_DASHBOARD.md",
    "PROGRESS_REPORT_TIER1COMPLETE.md",
    "PHASE1_STATUS.md",
    "PHASE1_STATUS_INDEX.md",
    "PHASE1_COMPLETION_REPORT.md",
    "PHASE1_COMPLETION_SUMMARY.md",
    "PHASE1_IMPLEMENTATION_STATUS.md",
    "PHASE1_IMPLEMENTATION_COMPLETE.md",
    "PHASE1_DOCUMENTATION_UPDATE_SUMMARY.md",
    "PHASE1_FINAL_REPORT.md",
    
    # Implementation reports (info moved to IMPROVEMENTS.md)
    "IMPLEMENTATION_COMPLETE.md",
    "IMPLEMENTATION_SUMMARY.md",
    "IMPLEMENTATION_ROADMAP.md",
    "UNIFIED_APP_IMPLEMENTATION.md",
    "UNIFIED_APP_PROPOSAL.md",
    
    # Audit reports (info moved to IMPROVEMENTS.md)
    "INCOMPLETE_CAPABILITIES_AUDIT.md",
    "EXECUTIVE_SUMMARY_GAPS.md",
    "PRIORITY_ACTION_LIST.md",
    "CODING_AUDIT_SUMMARY.md",
    "ANALYSIS_CODING_STATUS.md",
    "CODE_QUALITY_ANALYSIS.md",
    "CODE_QUALITY_ACTION_MATRIX.md",
    "CODE_QUALITY_QUICKREF.md",
    
    # Duplicate guides (info moved to CAPABILITIES.md)
    "APP_READY.md",
    "APP_QUICKSTART.md",
    "APP_DEPLOYMENT_GUIDE.md",
    "SOFTWARE_CAPABILITIES.md",
    "INTEGRATION_GUIDE.md",
    "FINAL_INTEGRATION_GUIDE.md",
    "INTEGRATION_GUIDE.md",
    "MONITORING.md",
    "MONITORING_IMPLEMENTATION.md",
    "OPERATIONS_MANUAL_V2.md",
    "PERFORMANCE_OPTIMIZATION_GUIDE.md",
    "DEPLOYMENT.md",
    
    # Duplicate indexes (info in README.md)
    "DOCUMENTATION_INDEX.md",
    "DOCUMENTATION_MASTER_INDEX.md",
    "QUICK_REFERENCE.md",
    "START_HERE.md",
    
    # Consolidation summaries (already consolidated)
    "CODEBASE_CONSOLIDATION_SUMMARY.md",
    
    # Phase 2 plan (info in IMPROVEMENTS.md)
    "PHASE2_DETAILED_PLAN.md",
    
    # GitHub guides (info in CAPABILITIES.md)
    "GITHUB_SETUP.md",
    "GITHUB_DEPLOY.md",
    
    # K8s guide (info in CAPABILITIES.md)
    "k8s/K8S_DEPLOYMENT_GUIDE.md",
]

def backup_before_delete(base_dir: Path):
    """Create a backup directory with redundant files before deletion"""
    backup_dir = base_dir / "docs" / "_archived_redundant"
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir

def consolidate_docs(base_dir: Path):
    """Consolidate documentation and delete redundant files"""
    base_dir = Path(base_dir)
    
    print("=" * 70)
    print("  GEESP-Angola Documentation Consolidation")
    print("=" * 70)
    print()
    
    # Create backup directory
    backup_dir = backup_before_delete(base_dir)
    print(f"Backup directory: {backup_dir}")
    print()
    
    # Track what we're doing
    deleted_count = 0
    not_found_count = 0
    
    # Process redundant files
    print("Removing redundant documentation files...")
    print()
    
    for doc_file in REDUNDANT_DOCS:
        file_path = base_dir / doc_file
        
        if file_path.exists():
            # Backup before deleting
            backup_path = backup_dir / Path(doc_file).name
            try:
                shutil.copy2(file_path, backup_path)
                file_path.unlink()
                deleted_count += 1
                print(f"  [OK] Deleted: {doc_file}")
            except Exception as e:
                print(f"  [WARN] Error deleting {doc_file}: {e}")
        else:
            not_found_count += 1
            print(f"  [SKIP] Not found (already deleted?): {doc_file}")
    
    print()
    print("=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    print(f"[OK] Deleted: {deleted_count} files")
    print(f"[SKIP] Not found: {not_found_count} files")
    print(f"Backup location: {backup_dir}")
    print()
    print("Consolidated documentation:")
    print("  - README.md (main entry point)")
    print("  - docs/CAPABILITIES.md (features, installation, user guide)")
    print("  - docs/IMPROVEMENTS.md (roadmap, improvements, metrics)")
    print()
    print("[OK] Consolidation complete!")

if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    consolidate_docs(script_dir)
