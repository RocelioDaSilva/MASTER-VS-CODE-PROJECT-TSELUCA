"""
GEESP-Angola Backend Package.

Main backend module for GEESP-Angola (Geospatial Energy for Equity & Solar Planning).

Exports:
    - create_app: Application factory function
    - app: FastAPI application instance
    - models: Database ORM models
    - api: REST API module
    - utils: Utility modules
    - scripts: Analysis script modules
    - maps: Map generation module
    - geospatial: Geospatial analysis module
    - dashboard: Streamlit dashboard module
"""

__version__ = "2.0"
__author__ = "ISPTEC - Instituto Superior Politécnico de Tecnologias e Ciências"
__description__ = "Geospatial Energy for Equity & Solar Planning"

# Import application factory
try:
    from .app import create_app
except ImportError:
    create_app = None

# Import FastAPI application
try:
    from .api.api import app
except ImportError:
    app = None

# Import core modules
try:
    from . import api, dashboard, geospatial, maps, models, scripts, utils
except ImportError as e:
    import warnings
    warnings.warn(f"Could not import some modules: {e}")

__all__ = [
    "create_app",
    "app",
    "api",
    "models",
    "utils",
    "scripts",
    "maps",
    "geospatial",
    "dashboard",
    "__version__",
    "__author__",
    "__description__",
]

