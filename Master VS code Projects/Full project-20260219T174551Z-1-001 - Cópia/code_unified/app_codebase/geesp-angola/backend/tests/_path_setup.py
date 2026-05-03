"""Shared sys.path setup for backend test modules and test utilities."""

from pathlib import Path
import sys


def ensure_backend_paths() -> tuple[str, str]:
    """Ensure backend root and scripts are in sys.path with stable order."""
    tests_dir = Path(__file__).resolve().parent
    backend_root = tests_dir.parent
    scripts_dir = backend_root / "scripts"

    backend_root_str = str(backend_root)
    scripts_dir_str = str(scripts_dir)

    for path in (backend_root_str, scripts_dir_str):
        if path in sys.path:
            sys.path.remove(path)

    # Keep backend root first so `utils` resolves to backend/utils package.
    sys.path.insert(0, scripts_dir_str)
    sys.path.insert(0, backend_root_str)

    # If `utils` was resolved as scripts/utils.py, clear it and let package import win.
    if "utils" in sys.modules and not hasattr(sys.modules["utils"], "error_handlers"):
        del sys.modules["utils"]

    return backend_root_str, scripts_dir_str
