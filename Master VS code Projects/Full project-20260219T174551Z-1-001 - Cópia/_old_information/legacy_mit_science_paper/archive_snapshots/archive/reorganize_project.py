#!/usr/bin/env python3
"""
Project Reorganization Script
Physically reorganizes files within Full project/ to create a clean structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Get project root
PROJECT_ROOT = Path(__file__).parent

# Create log file
LOG_FILE = PROJECT_ROOT / "REORGANIZATION_LOG.txt"
log_entries = []

def log(message):
    """Log a message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    log_entries.append(entry)
    print(entry)

def move_file(src, dst, create_dirs=True):
    """Move a file, creating directories if needed"""
    src_path = PROJECT_ROOT / src
    dst_path = PROJECT_ROOT / dst
    
    if not src_path.exists():
        log(f"SKIP: Source not found: {src}")
        return False
    
    if dst_path.exists():
        log(f"SKIP: Destination exists: {dst}")
        return False
    
    try:
        if create_dirs:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dst_path))
        log(f"MOVED: {src} -> {dst}")
        return True
    except Exception as e:
        log(f"ERROR moving {src}: {e}")
        return False

def move_dir(src, dst):
    """Move a directory"""
    src_path = PROJECT_ROOT / src
    dst_path = PROJECT_ROOT / dst
    
    if not src_path.exists():
        log(f"SKIP: Source directory not found: {src}")
        return False
    
    if dst_path.exists():
        log(f"SKIP: Destination directory exists: {dst}")
        return False
    
    try:
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dst_path))
        log(f"MOVED DIR: {src} -> {dst}")
        return True
    except Exception as e:
        log(f"ERROR moving directory {src}: {e}")
        return False

def main():
    log("=" * 70)
    log("GEESP-Angola Project Reorganization")
    log("=" * 70)
    log("")
    
    # ========================================================================
    # PHASE 1: Consolidate Archives
    # ========================================================================
    log("PHASE 1: Consolidating Archives")
    log("-" * 70)
    
    # Move SUBMISSION_READY to ARCHIVE (it's a backup copy)
    if (PROJECT_ROOT / "SUBMISSION_READY").exists():
        move_dir("SUBMISSION_READY", "ARCHIVE/SUBMISSION_READY")
    
    # Move writing/ to ARCHIVE (drafts/backups)
    if (PROJECT_ROOT / "writing").exists():
        move_dir("writing", "ARCHIVE/writing")
    
    log("")
    
    # ========================================================================
    # PHASE 2: Organize Root-Level Scripts
    # ========================================================================
    log("PHASE 2: Organizing Scripts")
    log("-" * 70)
    
    # Root-level scripts should go to scripts/ or Coding parts/geesp-angola/scripts/
    # Keep run_geesp_app.bat at root (it's the main launcher)
    
    # Move any stray .bat/.sh files to appropriate locations
    root_scripts = [
        ("run_dashboard.bat", "Coding parts/geesp-angola/"),
        ("run_dashboard.sh", "Coding parts/geesp-angola/"),
        ("run_monitoring.bat", "Coding parts/geesp-angola/"),
        ("run_monitoring.sh", "Coding parts/geesp-angola/"),
    ]
    
    for script, dest_dir in root_scripts:
        if (PROJECT_ROOT / script).exists():
            move_file(script, f"{dest_dir}{script}")
    
    log("")
    
    # ========================================================================
    # PHASE 3: Organize Documentation
    # ========================================================================
    log("PHASE 3: Organizing Documentation")
    log("-" * 70)
    
    # Move FULL_PROJECT_STREAMLINED.md to ROOT_DOCS/ (it's a navigation doc)
    move_file("FULL_PROJECT_STREAMLINED.md", "ROOT_DOCS/FULL_PROJECT_STREAMLINED.md")
    
    # Ensure ARCHIVE_INDEX.md stays in ARCHIVE/
    # (already created there)
    
    log("")
    
    # ========================================================================
    # PHASE 4: Organize Infrastructure/DevOps Files
    # ========================================================================
    log("PHASE 4: Organizing Infrastructure Files")
    log("-" * 70)
    
    # These are already in reasonable places, but let's ensure consistency
    # ansible/, infrastructure/, k8s/, monitoring/ are fine where they are
    
    log("Infrastructure folders already organized")
    log("")
    
    # ========================================================================
    # PHASE 5: Clean Up Root Level
    # ========================================================================
    log("PHASE 5: Root Level Cleanup")
    log("-" * 70)
    
    # What should stay at root:
    # - README.md (main entry point)
    # - run_geesp_app.bat (main launcher)
    # - requirements.txt (if exists, should be in Coding parts/geesp-angola/)
    
    if (PROJECT_ROOT / "requirements.txt").exists():
        # Check if it's different from Coding parts version
        root_req = PROJECT_ROOT / "requirements.txt"
        code_req = PROJECT_ROOT / "Coding parts/geesp-angola/requirements.txt"
        if code_req.exists():
            # Move root version to ARCHIVE as backup
            move_file("requirements.txt", "ARCHIVE/requirements_root_backup.txt")
        else:
            # Move to code directory
            move_file("requirements.txt", "Coding parts/geesp-angola/requirements.txt")
    
    log("")
    
    # ========================================================================
    # PHASE 6: Create Clean Structure Summary
    # ========================================================================
    log("PHASE 6: Creating Structure Summary")
    log("-" * 70)
    
    summary = f"""
# Project Reorganization Complete

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Changes Made

### Archives Consolidated
- SUBMISSION_READY/ → ARCHIVE/SUBMISSION_READY/
- writing/ → ARCHIVE/writing/

### Scripts Organized
- Root-level launcher scripts moved to Coding parts/geesp-angola/
- run_geesp_app.bat remains at root (main entry point)

### Documentation Organized
- FULL_PROJECT_STREAMLINED.md → ROOT_DOCS/

### Root Level (Clean)
- README.md (main entry)
- run_geesp_app.bat (app launcher)
- [All other files organized into proper folders]

## Final Structure

```
Full project/
├── README.md                    # Main entry point
├── run_geesp_app.bat           # App launcher
│
├── ROOT_DOCS/                  # Navigation & status
│   ├── README.md
│   ├── MASTER_INDEX.md
│   ├── PROJECT_FOLDER_GUIDE.md
│   └── FULL_PROJECT_STREAMLINED.md
│
├── Coding parts/
│   └── geesp-angola/           # All code + app
│       ├── geesp_unified_app.py
│       ├── launch_app.bat/sh/py
│       └── [all code files]
│
├── manuscript/                 # Thesis (canonical)
│   └── SOL.tex
│
├── presentations/              # Presentations
├── docs/                       # Technical docs
├── translations/pt/            # Portuguese translations
├── PROJECT_MANAGEMENT/         # Status, audits, checklists
├── support/                    # Support materials
│
└── ARCHIVE/                    # All archives/backups
    ├── ARCHIVE_INDEX.md
    ├── SUBMISSION_READY/
    ├── writing/
    └── [other archives]
```

## Files Moved

"""
    
    summary_file = PROJECT_ROOT / "REORGANIZATION_SUMMARY.md"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary)
        f.write("\n".join(log_entries))
    
    log(f"Summary saved to: {summary_file}")
    log("")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    log("=" * 70)
    log("REORGANIZATION COMPLETE")
    log("=" * 70)
    log(f"Total operations: {len([e for e in log_entries if 'MOVED' in e])}")
    log(f"Log file: {LOG_FILE}")
    log("")
    
    # Write log file
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(log_entries))

if __name__ == "__main__":
    main()
