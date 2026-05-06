"""Top-level _path_setup helper for test discovery.

Provides `ensure_backend_paths()` so test modules that import
`from _path_setup import ensure_backend_paths` can succeed during pytest
collection.
"""
from pathlib import Path
import sys


def ensure_backend_paths() -> tuple[str, str]:
    root = Path(__file__).resolve().parent
    backend_root = root / "backend"
    scripts_dir = backend_root / "scripts"

    backend_root_str = str(backend_root)
    scripts_dir_str = str(scripts_dir)

    for path in (backend_root_str, scripts_dir_str):
        if path in sys.path:
            sys.path.remove(path)

    # Ensure scripts and backend are at front of sys.path
    sys.path.insert(0, scripts_dir_str)
    sys.path.insert(0, backend_root_str)

    # Remove any accidental module collision for `utils`
    if "utils" in sys.modules and not hasattr(sys.modules["utils"], "error_handlers"):
        del sys.modules["utils"]

    return backend_root_str, scripts_dir_str


__all__ = ["ensure_backend_paths"]
