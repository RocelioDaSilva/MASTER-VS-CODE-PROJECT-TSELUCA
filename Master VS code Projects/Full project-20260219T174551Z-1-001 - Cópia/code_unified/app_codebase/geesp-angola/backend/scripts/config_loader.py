"""Lightweight ConfigLoader shim for archived tests.

Provides minimal configuration used by tests (study area bounds, country).
This is intentionally small and deterministic to keep tests stable.
"""
from typing import Dict, Any


class ConfigLoader:
    def __init__(self, config_path: str | None = None) -> None:
        self.config_path = config_path

    def get(self) -> Dict[str, Any]:
        # Bounds: [lon_min, lat_min, lon_max, lat_max]
        return {
            "study_area": {
                "country": "Angola",
                "bounds": [11.6, -18.5, 24.1, -4.4],
            }
        }


def load_config(path: str | None = None) -> Dict[str, Any]:
    return ConfigLoader(path).get()


def get_map_shape() -> tuple:
    """Return a default raster shape used by archived tests.

    Using (280, 300) keeps tests consistent with historical expectations.
    """
    return (280, 300)

__all__ = ["ConfigLoader", "load_config"]
