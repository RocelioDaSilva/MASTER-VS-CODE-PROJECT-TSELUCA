"""
Pytest configuration and path setup for GEESP-Angola tests.
Ensures project root is first so 'utils' resolves to the utils package (not scripts/utils.py),
then scripts so that 'import mcda_analysis' etc. find scripts/mcda_analysis.py.
"""
import sys
from pathlib import Path

# Project root (geesp-angola) - must be first so "utils" is the package, not scripts/utils.py
_root = Path(__file__).resolve().parent.parent
_scripts = _root / "scripts"
_root_s, _scripts_s = str(_root), str(_scripts)
# Ensure root is first, then scripts (so utils -> utils/, and bare imports find scripts/)
if _root_s in sys.path:
    sys.path.remove(_root_s)
if _scripts_s in sys.path:
    sys.path.remove(_scripts_s)
sys.path.insert(0, _scripts_s)
sys.path.insert(0, _root_s)
# If "utils" was ever loaded as scripts/utils.py (a module), remove it so the package is used
if "utils" in sys.modules and not hasattr(sys.modules["utils"], "error_handlers"):
    del sys.modules["utils"]


def pytest_configure(config):
    """Run path setup again when pytest starts (before collection)."""
    if _root_s not in sys.path or sys.path.index(_root_s) > 0:
        for p in (_root_s, _scripts_s):
            if p in sys.path:
                sys.path.remove(p)
        sys.path.insert(0, _scripts_s)
        sys.path.insert(0, _root_s)
    if "utils" in sys.modules and not hasattr(sys.modules["utils"], "error_handlers"):
        del sys.modules["utils"]
