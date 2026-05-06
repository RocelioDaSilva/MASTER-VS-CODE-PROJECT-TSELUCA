from .helpers import cached_result, format_number

from pathlib import Path
from typing import Tuple, Dict, Any

import numpy as np


def load_raster(path: str) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Load a raster file for dashboard use.

    Supports:
    - .npy: returns (array, minimal metadata)
    - .tif/.tiff: uses rasterio if available, otherwise raises a clear error.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Raster not found: {p}")

    suffix = p.suffix.lower()
    if suffix == ".npy":
        arr = np.load(p)
        meta: Dict[str, Any] = {
            "driver": "npy",
            "dtype": str(arr.dtype),
            "shape": arr.shape,
        }
        return arr, meta

    if suffix in {".tif", ".tiff"}:
        try:
            import rasterio  # type: ignore
        except Exception as e:
            raise RuntimeError(
                f"rasterio is required to read GeoTIFF files: {e}"
            ) from e

        with rasterio.open(p) as ds:  # type: ignore[name-defined]
            arr = ds.read(1)
            meta = ds.meta.copy()
        return arr, meta

    raise ValueError(f"Unsupported raster format: {p.suffix}")


def save_raster(arr: np.ndarray, path: str) -> None:
    """Save a raster array.

    - .npy: simple NumPy save
    - .tif/.tiff: best-effort GeoTIFF write using rasterio if available
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    suffix = p.suffix.lower()
    if suffix == ".npy":
        np.save(p, arr)
        return

    if suffix in {".tif", ".tiff"}:
        try:
            import rasterio
            from rasterio.transform import from_origin  # type: ignore
        except Exception as e:
            raise RuntimeError(
                f"rasterio is required to write GeoTIFF files: {e}"
            ) from e

        height, width = arr.shape
        transform = from_origin(0.0, 0.0, 1.0, 1.0)

        with rasterio.open(  # type: ignore[name-defined]
            p,
            "w",
            driver="GTiff",
            height=height,
            width=width,
            count=1,
            dtype=arr.dtype,
            crs="EPSG:4326",
            transform=transform,
        ) as dst:
            dst.write(arr, 1)
        return

    raise ValueError(f"Unsupported raster format for saving: {p.suffix}")
