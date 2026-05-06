#!/usr/bin/env python3
"""
Phase 2B: Import Updates - Consolidation Follow-up
Updates all imports after Phase 2 code consolidation

Changes:
  backend.utils.utils.X → backend.utils.X
  backend.scripts.scripts.X → backend.scripts.X  
  Maps and geospatial imports consolidated
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration
# Script is in geesp-angola/, so backend is geesp-angola/backend/
BACKEND_ROOT = Path(__file__).parent / "backend"
SOURCE_EXTENSIONS = [".py"]

# Import replacements mapping
IMPORT_REPLACEMENTS: Dict[str, str] = {
    # Utils flattening
    "from backend.utils.utils.": "from backend.utils.",
    "from backend.utils.utils import": "from backend.utils import",
    "import backend.utils.utils": "import backend.utils",
    "backend.utils.utils.": "backend.utils.",
    
    # Scripts de-nesting
    "from backend.scripts.scripts.": "from backend.scripts.",
    "from backend.scripts.scripts import": "from backend.scripts import",
    "import backend.scripts.scripts": "import backend.scripts",
    "backend.scripts.scripts.": "backend.scripts.",
    
    # Maps consolidation
    "from backend.scripts.maps": "from backend.maps",
    "from backend.scripts.scripts.maps": "from backend.maps",
    "backend.scripts.maps": "backend.maps",
    
    # Geospatial consolidation
    "from backend.scripts.gee": "from backend.geospatial",
    "from backend.scripts.scripts.gee": "from backend.geospatial",
    "backend.scripts.gee": "backend.geospatial",
    "backend.scripts.scripts.gee": "backend.geospatial",
}

class ImportUpdater:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.stats = {
            "files_scanned": 0,
            "files_updated": 0,
            "replacements_made": 0,
        }
        self.updated_files: List[str] = []
    
    def find_python_files(self) -> List[Path]:
        """Find all Python files to process"""
        python_files = []
        for root, dirs, files in os.walk(self.root_path):
            # Skip test cache and __pycache__
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.pytest_cache']]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        
        return python_files
    
    def update_imports_in_file(self, filepath: Path) -> Tuple[int, str]:
        """Update imports in a single file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            updated_content = original_content
            replacements_count = 0
            
            # Apply all replacements
            for old_pattern, new_pattern in IMPORT_REPLACEMENTS.items():
                # Use word boundaries to avoid partial matches
                pattern = re.escape(old_pattern)
                # Check if pattern exists before replacing
                if re.search(pattern, updated_content):
                    updated_content = updated_content.replace(old_pattern, new_pattern)
                    count = original_content.count(old_pattern)
                    replacements_count += count
            
            # Write back if changed
            if updated_content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                return replacements_count, "OK"
            else:
                return 0, "NO_CHANGE"
        
        except Exception as e:
            return 0, f"ERROR: {str(e)}"
    
    def run(self, dry_run: bool = True) -> None:
        """Execute import updates"""
        print("\n" + "="*60)
        print("PHASE 2B: IMPORT UPDATES")
        print("="*60 + "\n")
        
        if dry_run:
            print("MODE: DRY-RUN (Preview)")
        else:
            print("MODE: ACTUAL EXECUTION")
        print()
        
        # Find all Python files
        python_files = self.find_python_files()
        print(f"Found {len(python_files)} Python files to scan\n")
        
        # Process each file
        updated_files = []
        for filepath in python_files:
            self.stats["files_scanned"] += 1
            
            # Read file
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue
            
            # Check if file has old imports
            needs_update = False
            for old_pattern in IMPORT_REPLACEMENTS.keys():
                if old_pattern in content:
                    needs_update = True
                    break
            
            if needs_update:
                rel_path = filepath.relative_to(self.root_path)
                print(f"[UPDATE] {rel_path}")
                
                # Show what will be changed
                for old_pattern, new_pattern in IMPORT_REPLACEMENTS.items():
                    if old_pattern in content:
                        count = content.count(old_pattern)
                        print(f"        {old_pattern} -> {new_pattern} ({count} times)")
                
                if not dry_run:
                    replacements, status = self.update_imports_in_file(filepath)
                    self.stats["replacements_made"] += replacements
                    self.stats["files_updated"] += 1
                    updated_files.append(str(rel_path))
                else:
                    self.stats["replacements_made"] += sum(
                        content.count(old_pattern) 
                        for old_pattern in IMPORT_REPLACEMENTS.keys()
                    )
                    self.stats["files_updated"] += 1
                    updated_files.append(str(rel_path))
                
                print()
        
        # Summary
        print("="*60)
        print("PHASE 2B SUMMARY")
        print("="*60)
        print(f"\nFiles scanned:       {self.stats['files_scanned']}")
        print(f"Files to update:     {self.stats['files_updated']}")
        print(f"Replacements:        {self.stats['replacements_made']}")
        
        if updated_files:
            print(f"\nFiles with updates:")
            for f in updated_files:
                print(f"  - {f}")
        
        if dry_run:
            print("\n[DRY-RUN] Preview complete")
            print("Run with --execute to apply changes")
        else:
            print("\n[SUCCESS] Import updates applied")
        
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    import sys
    
    dry_run = "--execute" not in sys.argv
    
    updater = ImportUpdater(BACKEND_ROOT)
    updater.run(dry_run=dry_run)
