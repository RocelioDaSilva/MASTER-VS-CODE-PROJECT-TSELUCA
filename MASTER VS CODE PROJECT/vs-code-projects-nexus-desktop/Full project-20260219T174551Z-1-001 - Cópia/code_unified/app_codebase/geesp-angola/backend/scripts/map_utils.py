"""Compatibility map utils shim implementing `compute_aptitude` used in tests.

Uses the `normalize` function to scale inputs and combines them with
weights to produce an integrated aptitude map.
"""
from typing import Dict, Optional
import numpy as np

from .raster_utils import normalize


DEFAULT_WEIGHTS: Dict[str, float] = {
    "irradiacao": 0.3,
    "populacao": 0.2,
    "distancia_rede": 0.2,
    "declividade": 0.15,
    "ndvi": 0.15,
}


def compute_aptitude(
    irradiacao: np.ndarray,
    populacao: np.ndarray,
    distancia_rede: np.ndarray,
    declividade: np.ndarray,
    ndvi: np.ndarray,
    weights: Optional[Dict[str, float]] = None,
) -> np.ndarray:
    """Compute a simple aptitude score from input rasters.

    All inputs are normalized to [0,1]. Distance and slope are inverted
    (smaller values are more suitable).
    """
    w = DEFAULT_WEIGHTS.copy()
    if weights:
        w.update(weights)

    norm = normalize({
        "irradiacao": irradiacao,
        "populacao": populacao,
        "distancia_rede": distancia_rede,
        "declividade": declividade,
        "ndvi": ndvi,
    })

    # Invert distance and slope (higher distance/slope -> lower aptitude)
    dist_inv = 1 - norm["distancia_rede"]
    slope_inv = 1 - norm["declividade"]

    aptitude = (
        w["irradiacao"] * norm["irradiacao"]
        + w["populacao"] * norm["populacao"]
        + w["distancia_rede"] * dist_inv
        + w["declividade"] * slope_inv
        + w["ndvi"] * norm["ndvi"]
    )

    # Ensure numeric array and finite values
    aptitude = np.asarray(aptitude, dtype=float)
    return aptitude


__all__ = ["compute_aptitude"]
