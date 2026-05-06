"""
GEESP-Angola Streamlit Dashboard Module

Provides web-based user interface for GEESP-Angola using Streamlit framework.

Consolidated Module Structure:
    - app.py: Main dashboard application
    - components.py: Consolidated UI components (metrics, maps, weights, tables)
    - pages.py: Consolidated dashboard pages (home, data, mcda, results, lcoe)
    - state.py: Unified state management for Streamlit session
    - utils/: Dashboard utilities and helpers (cache, errors, logging, etc.)

Usage:
    streamlit run backend/dashboard/app.py
"""

# Import consolidated modules for easy access
from . import components
from . import pages
from . import state

__all__ = [
    "app",
    "components",
    "pages",
    "state",
    "utils",
]

