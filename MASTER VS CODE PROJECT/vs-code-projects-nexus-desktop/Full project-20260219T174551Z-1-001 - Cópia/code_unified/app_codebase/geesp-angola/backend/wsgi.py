"""
WSGI application entry point for production deployment.

This module serves as the entry point for WSGI servers like Gunicorn,
used in production deployments with Docker and Kubernetes.

Usage:
    gunicorn --workers 4 --bind 0.0.0.0:8000 backend.wsgi:app
    
    or with environment variables:
    
    gunicorn --workers 4 \\
        --bind 0.0.0.0:${API_PORT} \\
        --timeout 120 \\
        --log-level info \\
        backend.wsgi:app
"""

import sys
from pathlib import Path

# Setup project paths
_root = Path(__file__).resolve().parent
_scripts = _root / "scripts"

# Clear any existing paths
if str(_root) in sys.path:
    sys.path.remove(str(_root))
if str(_scripts) in sys.path:
    sys.path.remove(str(_scripts))

# Insert in correct order (scripts FIRST, then root)
sys.path.insert(0, str(_scripts))
sys.path.insert(0, str(_root))

# Clean up module cache
if "utils" in sys.modules and not hasattr(sys.modules["utils"], "error_handlers"):
    del sys.modules["utils"]

# Import FastAPI application
from api.api import app

# For WSGI servers
application = app

if __name__ == "__main__":
    # This is for development/testing only
    import uvicorn
    
    uvicorn.run(
        application,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
