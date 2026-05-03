"""
GEESP-Angola Geospatial Module

Earth Engine integration and geospatial data processing utilities.
"""

try:
    from .earth_engine_integration import (
        EarthEngineClient,
        authenticate_ee,
        get_collection,
    )
    __all__ = [
        "EarthEngineClient",
        "authenticate_ee",
        "get_collection",
    ]
except ImportError:
    __all__ = []
