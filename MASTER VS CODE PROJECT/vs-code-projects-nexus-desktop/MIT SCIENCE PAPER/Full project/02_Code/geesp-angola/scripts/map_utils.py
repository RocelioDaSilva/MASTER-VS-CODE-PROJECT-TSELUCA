"""Shared map utilities for GEESP-Angola generators

Provides common aptitude calculation and metadata builders so both the
lightweight and full generators share the same logic and weights.
"""
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import logging

logger: logging.Logger = logging.getLogger(__name__)



DEFAULT_WEIGHTS: Dict[str, float] = {
    "irradiacao": 0.25,
    "populacao": 0.25,
    "distancia_rede": 0.20,
    "declividade": 0.15,
    "ndvi": 0.15,
}


def compute_aptitude(
    solar: np.ndarray,
    population: np.ndarray,
    distance: np.ndarray,
    slope: np.ndarray,
    ndvi: np.ndarray,
    weights: Dict[str, float] = None,
) -> np.ndarray:
    """Compute weighted aptitude map using shared normalization and weights.

    Normalization matches the lightweight generator's min/max choices so
    outputs remain consistent across scripts.
    """
    logger.debug("Computing aptitude map with weighted overlay")
    w: Dict[str, float] = DEFAULT_WEIGHTS.copy()
    if weights:
        w.update(weights)
        logger.debug(f"Using custom weights: {w}")

    # Normalize each criterion to [0,1] using the same ranges used in simple generator
    solar_norm = (solar - 5.5) / (6.4 - 5.5)
    population_norm = (population - 10) / (95 - 10)
    distance_norm: np.ndarray[Tuple[np.Any], np.dtype[np.float64]] = 1 - (distance / 45.0)
    slope_norm: np.ndarray[Tuple[np.Any], np.dtype[np.float64]] = 1 - (slope / 30.0)
    ndvi_norm = (ndvi + 0.2) / 0.9

    aptitude = (
        w["irradiacao"] * solar_norm
        + w["populacao"] * population_norm
        + w["distancia_rede"] * distance_norm
        + w["declividade"] * slope_norm
        + w["ndvi"] * ndvi_norm
    )

    result: np.ndarray[Tuple[np.Any], np.dtype[np.floating[np._32Bit]]] = np.clip(aptitude, 0, 1).astype(np.float32)
    logger.info(f"Aptitude map computed: min={np.nanmin(result):.3f}, max={np.nanmax(result):.3f}, mean={np.nanmean(result):.3f}")
    return result


def build_metadata(
    solar, population, distance, slope, ndvi, aptitude, output_shape: Tuple[int, int]
) -> dict:
    """Builds metadata dictionary for all generated maps."""
    logger.debug(f"Building metadata for maps with shape {output_shape}")
    h, w = output_shape
    metadata = {
        "mapa_irradiacao": {
            "descricao": "Irradiação Solar - Huíla, Angola",
            "unidade": "kWh/m²/dia",
            "min": float(np.nanmin(solar)),
            "max": float(np.nanmax(solar)),
            "media": float(np.nanmean(solar)),
            "resolucao_pixels": f"{w}x{h}",
            "shape": [h, w],
        },
        "mapa_populacao": {
            "descricao": "Densidade Populacional (Luzes Noturnas)",
            "unidade": "nanoWatts/cm²/sr",
            "min": float(np.nanmin(population)),
            "max": float(np.nanmax(population)),
            "media": float(np.nanmean(population)),
            "resolucao_pixels": f"{w}x{h}",
            "shape": [h, w],
        },
        "mapa_distancia_rede": {
            "descricao": "Distância à Rede Elétrica Existente",
            "unidade": "km",
            "min": float(np.nanmin(distance)),
            "max": float(np.nanmax(distance)),
            "media": float(np.nanmean(distance)),
            "resolucao_pixels": f"{w}x{h}",
            "shape": [h, w],
        },
        "mapa_declividade": {
            "descricao": "Declividade do Terreno",
            "unidade": "graus",
            "min": float(np.nanmin(slope)),
            "max": float(np.nanmax(slope)),
            "media": float(np.nanmean(slope)),
            "resolucao_pixels": f"{w}x{h}",
            "shape": [h, w],
        },
        "mapa_ndvi": {
            "descricao": "NDVI - Índice de Vegetação",
            "unidade": "adimensional",
            "min": float(np.nanmin(ndvi)),
            "max": float(np.nanmax(ndvi)),
            "media": float(np.nanmean(ndvi)),
            "resolucao_pixels": f"{w}x{h}",
            "shape": [h, w],
        },
        "mapa_aptidao_integrada": {
            "descricao": "Mapa de Aptidão Integrada (Resultado MCDA)",
            "unidade": "[0,1]",
            "min": float(np.nanmin(aptitude)),
            "max": float(np.nanmax(aptitude)),
            "media": float(np.nanmean(aptitude)),
            "resolucao_pixels": f"{w}x{h}",
            "shape": [h, w],
            "metodo": "Weighted Overlay (AHP + MCDA)",
            "pesos": DEFAULT_WEIGHTS,
        },
    }

    logger.info(f"Metadata created for {len(metadata)} maps")
    return metadata
