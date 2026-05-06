"""Shared map utilities for GEESP-Angola generators

Provides common aptitude calculation and metadata builders so both the
lightweight and full generators share the same logic and weights.
"""
import hashlib
from pathlib import Path
from typing import Dict, Tuple
import numpy as np

from utils.logging import setup_logging
from utils.constants import MCDAConstants
from .raster import normalize  # Phase 5B: Use unified normalization

logger = setup_logging(__name__)



def compute_aptitude(
    solar: np.ndarray,
    population: np.ndarray,
    distance: np.ndarray,
    slope: np.ndarray,
    ndvi: np.ndarray,
    nighttime_lights: np.ndarray = None,
    weights: Dict[str, float] = None,
) -> np.ndarray:
    """Compute weighted aptitude map using unified normalization (Phase 5B consolidation).

    Uses raster_utils.normalize() for consistent, cached normalization across all modules.
    All 6 MCDA criteria are applied when nighttime_lights data is provided; otherwise
    the 5-criterion weights are renormalised to sum to 1.0 to prevent bias.
    """
    logger.debug("Computing aptitude map with unified normalization")
    w: Dict[str, float] = MCDAConstants.RASTER_WEIGHTS.copy()
    if weights:
        w.update(weights)
        logger.debug("Using custom weights: %s", w)

    raster_batch: Dict[str, np.ndarray] = {
        'solar': solar,
        'population': population,
        'distance': distance,
        'slope': slope,
        'ndvi': ndvi,
    }
    if nighttime_lights is not None:
        raster_batch['nighttime_lights'] = nighttime_lights

    # Build a content-addressable cache key so different input arrays never
    # collide on the shared normalization cache (M3 fix).
    _hasher = hashlib.md5(usedforsecurity=False)
    for _arr in raster_batch.values():
        _hasher.update(_arr.data if _arr.data.c_contiguous else np.ascontiguousarray(_arr).data)
    _cache_key = f"aptitude_{_hasher.hexdigest()[:16]}"

    # Phase 5B Consolidation: Use unified normalization with batch processing
    normalized_batch = normalize(raster_batch, cache_key=_cache_key)

    solar_norm = normalized_batch['solar']
    population_norm = normalized_batch['population']
    distance_norm = 1 - normalized_batch['distance']      # Inverse: farther is worse
    slope_norm = 1 - normalized_batch['slope']            # Inverse: steeper is worse
    ndvi_norm = normalized_batch['ndvi']

    aptitude = (
        w["irradiacao"] * solar_norm
        + w["populacao"] * population_norm
        + w["distancia_rede"] * distance_norm
        + w["declividade"] * slope_norm
        + w["ndvi"] * ndvi_norm
    )

    # Apply 6th MCDA criterion: nighttime lights (luminosidade_noturna, weight 0.10)
    if nighttime_lights is not None and "luminosidade_noturna" in w:
        nl_norm = normalized_batch['nighttime_lights']
        aptitude += w["luminosidade_noturna"] * nl_norm
        active_keys = ["irradiacao", "populacao", "distancia_rede", "declividade", "ndvi", "luminosidade_noturna"]
    else:
        active_keys = ["irradiacao", "populacao", "distancia_rede", "declividade", "ndvi"]

    # Renormalize if applied weights do not sum to 1.0 (prevents systematic underestimation)
    weight_sum = sum(w[k] for k in active_keys if k in w)
    if abs(weight_sum - 1.0) > 1e-6:
        logger.warning(
            f"MCDA weights sum to {weight_sum:.4f} ≠ 1.0 — renormalizing to prevent bias"
        )
        aptitude = aptitude / weight_sum

    result: np.ndarray = np.clip(aptitude, MCDAConstants.APTITUDE_LOW, MCDAConstants.APTITUDE_HIGH).astype(np.float32)
    logger.info(f"Aptitude map computed: min={np.nanmin(result):.3f}, max={np.nanmax(result):.3f}, mean={np.nanmean(result):.3f}")
    return result


def build_metadata(
    solar, population, distance, slope, ndvi, aptitude, output_shape: Tuple[int, int]
) -> dict:
    """Builds metadata dictionary for all generated maps."""
    logger.debug("Building metadata for maps with shape %s", output_shape)
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
            "pesos": MCDAConstants.DEFAULT_WEIGHTS,
        },
    }

    logger.info(f"Metadata created for {len(metadata)} maps")
    return metadata
