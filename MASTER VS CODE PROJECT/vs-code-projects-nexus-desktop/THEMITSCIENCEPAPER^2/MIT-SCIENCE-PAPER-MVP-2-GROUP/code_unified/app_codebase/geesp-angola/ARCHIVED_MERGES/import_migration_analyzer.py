#!/usr/bin/env python3
"""
Import Migration Helper Script for Phase 4 Code Consolidation

This script generates a mapping of old imports to new imports and validates
the migration path for all consolidation phases.

Usage:
    python import_migration_analyzer.py > import_mapping_report.txt
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict

# Define import mappings for consolidation
IMPORT_MAPPINGS = {
    # API Layer Consolidation (Phase B1)
    "from ..api.schemas import": "from ..api.models import",
    "from .schemas import": "from .models import",
    "from backend.api.schemas import": "from backend.api.models import",
    
    # Database Models Consolidation (Phase B2)
    "from ..models.scenario import": "from ..database.models import",
    "from ..models.results import": "from ..database.models import",
    "from ..models.models.monitoring import": "from ..database.models import",
    "from backend.models.scenario import": "from backend.database.models import",
    "from backend.models.results import": "from backend.database.models import",
    "from backend.models.models.monitoring import": "from backend.database.models import",
    
    # Analysis Engines (Phase B3)
    "from ..scripts.lcoe_calculator import": "from ..analysis.lcoe import",
    "from ..scripts.mcda_analysis import": "from ..analysis.mcda import",
    "from ..scripts.validation_pipeline import": "from ..analysis.validation_base import",
    "from ..scripts.base import": "from ..analysis.base import",
    "from ..scripts.raster_utils import": "from ..geospatial.raster import",
    "from ..scripts.map_utils import": "from ..geospatial.operations import",
    "from backend.scripts.lcoe_calculator import": "from backend.analysis.lcoe import",
    "from backend.scripts.mcda_analysis import": "from backend.analysis.mcda import",
    "from backend.scripts.validation_pipeline import": "from backend.analysis.validation_base import",
    "from backend.scripts.base import": "from backend.analysis.base import",
    "from backend.scripts.raster_utils import": "from backend.geospatial.raster import",
    "from backend.scripts.map_utils import": "from backend.geospatial.operations import",
    
    # Utilities (Phase B4)
    "from ..utils.core_utils import": "from ..utils.helpers import",
    "from ..utils.import_helpers import": "from ..utils.helpers import",
    "from ..utils.config_manager import": "from ..core.config import",
    "from ..utils.logging_config import": "from ..utils.logging import",
    "from backend.utils.core_utils import": "from backend.utils.helpers import",
    "from backend.utils.import_helpers import": "from backend.utils.helpers import",
    "from backend.utils.config_manager import": "from backend.core.config import",
    "from backend.utils.logging_config import": "from backend.utils.logging import",
}

def find_python_files(root_path: str) -> List[Path]:
    """Find all Python files in the backend."""
    python_files = []
    for path in Path(root_path).rglob("*.py"):
        # Skip __pycache__ and .git
        if "__pycache__" not in str(path) and ".git" not in str(path):
            python_files.append(path)
    return python_files

def check_imports_in_file(file_path: Path) -> Dict[str, List[Tuple[int, str]]]:
    """Find all problematic imports in a file."""
    problematic_imports = defaultdict(list)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            for old_import, new_import in IMPORT_MAPPINGS.items():
                if old_import in line:
                    problematic_imports[old_import].append((line_num, line.strip()))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return problematic_imports

def generate_migration_report(root_path: str) -> None:
    """Generate complete migration report."""
    print("=" * 80)
    print("IMPORT MIGRATION ANALYSIS REPORT")
    print("=" * 80)
    print()
    
    python_files = find_python_files(root_path)
    print(f"Analyzing {len(python_files)} Python files...\n")
    
    all_issues = defaultdict(list)
    
    for file_path in python_files:
        issues = check_imports_in_file(file_path)
        if issues:
            for old_import, occurrences in issues.items():
                all_issues[old_import].extend([(file_path, *occ) for occ in occurrences])
    
    if not all_issues:
        print("[OK] No problematic imports found! All imports are properly consolidated.")
    else:
        print(f"Found {sum(len(v) for v in all_issues.values())} import statements to migrate:\n")
        
        for old_import, occurrences in sorted(all_issues.items()):
            new_import = IMPORT_MAPPINGS[old_import]
            print(f"OLD: {old_import}")
            print(f"NEW: {new_import}")
            print(f"Files affected: {len(set(occ[0] for occ in occurrences))}")
            print()

def generate_find_replace_batch(root_path: str) -> None:
    """Generate batch find-and-replace commands."""
    print("\n" + "=" * 80)
    print("BATCH FIND-AND-REPLACE COMMANDS (PowerShell)")
    print("=" * 80)
    print()
    
    for old_import, new_import in sorted(IMPORT_MAPPINGS.items()):
        # Escape for PowerShell
        old_escaped = old_import.replace('"', '\"')
        new_escaped = new_import.replace('"', '\"')
        
        print(f'# Replace: {old_import} -> {new_import}')
        print(f'Get-ChildItem -Path backend/ -Include "*.py" -Recurse | ' + 
              f'ForEach-Object {{ (Get-Content $_) -replace [regex]::Escape("{old_escaped}"), "{new_escaped}" | ' +
              f'Set-Content $_ }}')
        print()

def validate_file_moves() -> None:
    """Show expected file moves for validation."""
    print("\n" + "=" * 80)
    print("FILE MOVES TO EXECUTE")
    print("=" * 80)
    print()
    
    moves = [
        # Phase B3
        ("backend/scripts/raster_utils.py", "backend/geospatial/raster.py"),
        ("backend/scripts/map_utils.py", "backend/geospatial/operations.py"),
        ("backend/scripts/performance.py", "backend/utils/performance.py"),
        ("backend/scripts/data_loaders_async.py", "backend/services/data.py"),
        
        # Phase B4
        ("backend/utils/config_manager.py", "backend/core/config.py"),
        ("backend/utils/logging_config.py", "backend/utils/logging.py"),
        
        # Phase B5
        ("backend/maps/generate_maps.py", "backend/maps/generator.py"),
        ("backend/maps/enhanced_maps_to_pdf.py", "backend/maps/exporters.py"),
    ]
    
    for i, (old, new) in enumerate(moves, 1):
        print(f"{i}. Move {old}")
        print(f"   -> {new}")
        print()

if __name__ == "__main__":
    backend_path = "backend"
    
    # Ensure we're in the right directory
    if not os.path.exists(backend_path):
        print("Error: 'backend' directory not found.")
        print("Run this script from the geesp-angola project root.")
        exit(1)
    
    generate_migration_report(backend_path)
    generate_find_replace_batch(backend_path)
    validate_file_moves()
    
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Review this report carefully")
    print("2. Create backup before making changes: git tag backup-imports")
    print("3. Execute file moves listed above")
    print("4. Execute find-and-replace commands")
    print("5. Run: python -m pytest tests/ -v")
    print("6. If tests pass: git commit -m 'Phase B/C/D: Import migration complete'")
    print()
