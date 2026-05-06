#!/usr/bin/env python3
"""
Verification script to test that all consolidated modules work together
Run this to verify the codebase is properly integrated
"""

import sys
from pathlib import Path

# Project root first so "utils" and "models" resolve; then scripts for bare imports
project_root = Path(__file__).parent
_scripts = str(project_root / "scripts")
_root = str(project_root)
for s in (_scripts, _root):
    if s in sys.path:
        sys.path.remove(s)
sys.path.insert(0, _scripts)
sys.path.insert(0, _root)
# If "utils" was ever loaded as scripts/utils.py, remove so package is used
if "utils" in sys.modules and not getattr(sys.modules["utils"], "error_handlers", None):
    del sys.modules["utils"]


def test_imports():
    """Test that all critical modules can be imported"""
    print("=" * 70)
    print("Testing Module Imports")
    print("=" * 70)
    
    errors = []
    
    # Test shared logging
    try:
        from utils.logging_setup import setup_logging
        logger = setup_logging("test_logger")
        print("[OK] Shared logging utility imported")
    except Exception as e:
        errors.append(f"[ERROR] Logging setup: {e}")
        print(f"[ERROR] Logging setup: {e}")
    
    # Test config loader
    try:
        from scripts.config_loader import load_config
        config = load_config()
        print("[OK] Config loader imported")
    except Exception as e:
        errors.append(f"[ERROR] Config loader: {e}")
        print(f"[ERROR] Config loader: {e}")
    
    # Test MCDA
    try:
        from scripts.mcda_analysis import MCDAnalyzer, AHPWeighter
        print("[OK] MCDA analysis imported")
    except Exception as e:
        errors.append(f"[ERROR] MCDA analysis: {e}")
        print(f"[ERROR] MCDA analysis: {e}")
    
    # Test LCOE
    try:
        from scripts.lcoe_calculator import LCOECalculator
        print("[OK] LCOE calculator imported")
    except Exception as e:
        errors.append(f"[ERROR] LCOE calculator: {e}")
        print(f"[ERROR] LCOE calculator: {e}")
    
    # Test map generation
    try:
        from scripts.generate_maps_simple import generate_maps, main
        print("[OK] Map generation imported")
    except Exception as e:
        errors.append(f"[ERROR] Map generation: {e}")
        print(f"[ERROR] Map generation: {e}")
    
    # Test utils
    try:
        from scripts.utils import normalize_for_visualization
        print("[OK] Utils imported")
    except Exception as e:
        errors.append(f"[ERROR] Utils: {e}")
        print(f"[ERROR] Utils: {e}")
    
    # Test error handlers (ensure project root first and utils is the package)
    try:
        if _root not in sys.path or sys.path.index(_root) != 0:
            if _root in sys.path:
                sys.path.remove(_root)
            sys.path.insert(0, _root)
        if "utils" in sys.modules and not hasattr(sys.modules["utils"], "error_handlers"):
            del sys.modules["utils"]
        from utils.error_handlers import handle_exceptions, ValidationError
        print("[OK] Error handlers imported")
    except Exception as e:
        errors.append(f"[ERROR] Error handlers: {e}")
        print(f"[ERROR] Error handlers: {e}")
    
    # Test database models (optional; missing sqlalchemy is not a fatal error)
    try:
        from models.monitoring import get_database_manager, ProjectRepository
        print("[OK] Database models imported")
    except Exception as e:
        print(f"[WARN] Database models: {e} (optional; install sqlalchemy if needed)")
    
    print("\n" + "=" * 70)
    if errors:
        print(f"[ERROR] {len(errors)} import error(s) found")
        return False
    else:
        print("[OK] All critical imports successful!")
        return True

def test_map_paths():
    """Verify map file paths are consistent"""
    print("\n" + "=" * 70)
    print("Testing Map Path Consistency")
    print("=" * 70)
    
    expected_maps = [
        "mapa_irradiacao.npy",
        "mapa_populacao.npy",
        "mapa_distanciarede.npy",
        "mapa_declividade.npy",
        "mapa_ndvi.npy",
        "mapa_aptidao_integrada.npy"
    ]
    
    data_dir = project_root / "data" / "processed"
    missing = []
    
    for map_file in expected_maps:
        path = data_dir / map_file
        if path.exists():
            print(f"[OK] {map_file}")
        else:
            print(f"[WARN] {map_file} (not generated yet)")
            missing.append(map_file)
    
    if missing:
        print(f"\n[WARN] {len(missing)} map(s) not yet generated (run map generation first)")
    else:
        print("\n[OK] All expected maps found!")
    
    return len(missing) == 0

if __name__ == "__main__":
    print("\nGEESP-Angola Integration Verification\n")
    
    imports_ok = test_imports()
    maps_ok = test_map_paths()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if imports_ok and maps_ok:
        print("[OK] All checks passed! Codebase is properly integrated.")
        sys.exit(0)
    elif imports_ok:
        print("[OK] Imports OK | [WARN] Maps need generation")
        print("Tip: Run: python scripts/generate_maps_simple.py")
        sys.exit(0)
    else:
        print("[ERROR] Some imports failed. Check errors above.")
        sys.exit(1)
