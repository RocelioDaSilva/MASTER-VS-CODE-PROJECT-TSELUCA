"""
GEESP-Angola unified app launcher (alternate entry point).

Runs geesp_unified_app.py in this module's globals so Streamlit
and "streamlit run geesp-unified-app.py" work. Single source of truth: geesp_unified_app.py
"""
import sys
from pathlib import Path

_APP_FILE = Path(__file__).resolve().parent / "geesp_unified_app.py"
if not _APP_FILE.exists():
    raise FileNotFoundError("geesp_unified_app.py not found")

with open(_APP_FILE, encoding="utf-8") as f:
    _code = compile(f.read(), str(_APP_FILE), "exec")
exec(_code, globals())
