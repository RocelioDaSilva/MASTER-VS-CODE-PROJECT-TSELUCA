#!/usr/bin/env python3
"""
Comprehensive Project Reorganization Script
Moves files to proper locations and updates path references
"""

import os
import shutil
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent
LOG_FILE = PROJECT_ROOT / "REORGANIZATION_LOG.txt"
log_entries = []

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    log_entries.append(entry)
    print(entry)

def move_file(src, dst, create_dirs=True):
    """Move a file"""
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

def update_paths_in_file(file_path, path_mappings):
    """Update path references in a file"""
    file_path_obj = PROJECT_ROOT / file_path
    if not file_path_obj.exists():
        return False
    
    try:
        with open(file_path_obj, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for old_path, new_path in path_mappings.items():
            # Update various path formats
            patterns = [
                (f'({old_path})', new_path),
                (f'({old_path}/)', f'{new_path}/'),
                (f'({old_path}\\\\)', new_path.replace('/', '\\')),
                (f'`({old_path})`', f'`{new_path}`'),
                (f'\[({old_path})\]', f'[{new_path}]'),
            ]
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(file_path_obj, 'w', encoding='utf-8') as f:
                f.write(content)
            log(f"UPDATED PATHS: {file_path}")
            return True
    except Exception as e:
        log(f"ERROR updating paths in {file_path}: {e}")
    
    return False

def main():
    log("=" * 70)
    log("COMPREHENSIVE PROJECT REORGANIZATION")
    log("=" * 70)
    log("")
    
    path_updates = {}
    
    # ========================================================================
    # PHASE 1: Move Archives
    # ========================================================================
    log("PHASE 1: Consolidating Archives")
    log("-" * 70)
    
    # Check and move SUBMISSION_READY
    if (PROJECT_ROOT / "SUBMISSION_READY").exists():
        if move_dir("SUBMISSION_READY", "ARCHIVE/SUBMISSION_READY"):
            path_updates["SUBMISSION_READY"] = "ARCHIVE/SUBMISSION_READY"
    else:
        log("SUBMISSION_READY/ not found (may already be archived)")
    
    # Check and move writing/
    if (PROJECT_ROOT / "writing").exists():
        if move_dir("writing", "ARCHIVE/writing"):
            path_updates["writing"] = "ARCHIVE/writing"
    else:
        log("writing/ not found (may already be archived)")
    
    # Move reorganization scripts to ARCHIVE after we're done
    log("")
    
    # ========================================================================
    # PHASE 2: Organize Root-Level Files
    # ========================================================================
    log("PHASE 2: Organizing Root-Level Files")
    log("-" * 70)
    
    # Move reorganization logs/summaries to ARCHIVE
    if (PROJECT_ROOT / "REORGANIZATION_LOG.txt").exists():
        move_file("REORGANIZATION_LOG.txt", "ARCHIVE/REORGANIZATION_LOG.txt")
    
    if (PROJECT_ROOT / "REORGANIZATION_SUMMARY.md").exists():
        move_file("REORGANIZATION_SUMMARY.md", "ARCHIVE/REORGANIZATION_SUMMARY.md")
    
    # Keep reorganize_project.py and reorganize_comprehensive.py for now
    # (will move to ARCHIVE at end)
    
    log("")
    
    # ========================================================================
    # PHASE 3: Check for Nested "Full project" Directory
    # ========================================================================
    log("PHASE 3: Checking for Nested Directories")
    log("-" * 70)
    
    nested_full_project = PROJECT_ROOT / "Full project"
    if nested_full_project.exists() and nested_full_project.is_dir():
        log(f"WARNING: Found nested 'Full project' directory at: {nested_full_project}")
        log("This may be a duplicate - consider reviewing contents")
        # Don't auto-move this - user should review first
    
    log("")
    
    # ========================================================================
    # PHASE 4: Update Path References in Documentation
    # ========================================================================
    log("PHASE 4: Updating Path References")
    log("-" * 70)
    
    docs_to_update = [
        "ROOT_DOCS/README.md",
        "ROOT_DOCS/MASTER_INDEX.md",
        "ROOT_DOCS/PROJECT_FOLDER_GUIDE.md",
        "ROOT_DOCS/FULL_PROJECT_STREAMLINED.md",
        "README.md",
        "ARCHIVE/ARCHIVE_INDEX.md",
    ]
    
    for doc in docs_to_update:
        if path_updates:
            update_paths_in_file(doc, path_updates)
    
    log("")
    
    # ========================================================================
    # PHASE 5: Final Cleanup
    # ========================================================================
    log("PHASE 5: Final Cleanup")
    log("-" * 70)
    
    # Move reorganization scripts to ARCHIVE
    if (PROJECT_ROOT / "reorganize_project.py").exists():
        move_file("reorganize_project.py", "ARCHIVE/reorganize_project.py")
    
    # Keep reorganize_comprehensive.py for now (user may want to run again)
    # But create a note that it can be archived
    
    log("")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    log("=" * 70)
    log("REORGANIZATION COMPLETE")
    log("=" * 70)
    
    moved_count = len([e for e in log_entries if 'MOVED' in e])
    updated_count = len([e for e in log_entries if 'UPDATED PATHS' in e])
    
    log(f"Files/Directories moved: {moved_count}")
    log(f"Files with paths updated: {updated_count}")
    log(f"Log file: {LOG_FILE}")
    log("")
    log("Root level should now be clean with only:")
    log("  - README.md (main entry)")
    log("  - run_geesp_app.bat (app launcher)")
    log("  - reorganize_comprehensive.py (can be archived after review)")
    log("")
    
    # Write log
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(log_entries))

if __name__ == "__main__":
    main()
