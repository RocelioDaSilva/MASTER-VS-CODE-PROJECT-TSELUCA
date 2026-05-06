"""
FastAPI REST API module for GEESP-Angola.

Exports:
    - app: FastAPI application instance
    - models: Pydantic request/response schemas
"""

try:
    from .api import app
except ImportError:
    app = None

try:
    from . import models
except ImportError:
    models = None

__all__ = ["app", "models"]
