"""
GEESP-Angola: Lightweight Map Generator (sem dependências externas de GIS)
Gera mapas raster simples em formato numpy/PIL

Refactored into a typed `generate_maps` function for improved importability
and type checking.
"""

from typing import Dict, Tuple, Optional, NoReturn
import numpy as np
from numpy.typing import NDArray
from pathlib import Path
import json
import logging
from logging.handlers import RotatingFileHandler

try:
    # When imported as part of the `scripts` package
    from .config_loader import load_config, get_map_shape
    from .type_annotations import RasterArray
except ImportError:
    # Fallback when imported as a top-level module (e.g., from Streamlit app)
    from config_loader import load_config, get_map_shape
    from type_annotations import RasterArray

# Ensure project root on path and load utils.error_handlers (avoid scripts/utils.py shadowing)
import sys as _sys
_geesp_root = Path(__file__).resolve().parent.parent
_root_s = str(_geesp_root)
if _root_s not in _sys.path:
    _sys.path.insert(0, _root_s)
try:
    from utils.error_handlers import handle_exceptions, ValidationError
except (ModuleNotFoundError, AttributeError):
    import importlib.util
    _err_path = _geesp_root / "utils" / "error_handlers.py"
    if _err_path.exists():
        _spec = importlib.util.spec_from_file_location("utils.error_handlers", _err_path)
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        handle_exceptions = _mod.handle_exceptions
        ValidationError = _mod.ValidationError
    else:
        raise

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging() -> logging.Logger:
    """Configure structured logging for map generation module"""
    logger = logging.getLogger(__name__)
    
    if logger.handlers:
        return logger
    
    config = load_config()
    log_config = config.get_logging_config()
    log_level = log_config.get("level", "INFO")
    log_file = log_config.get("file", "logs/geesp.log")
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=log_config.get("max_bytes", 10485760),
        backupCount=log_config.get("backup_count", 5)
    )
    file_handler.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(
        log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    return logger

logger = setup_logging()


@handle_exceptions(default=None, swallow=False)
def generate_maps(output_dir: Path | str = Path("data/processed")) -> Optional[None]:
    """Generate all simplified maps and save to `output_dir`.

    Args:
        output_dir: Directory where generated maps and metadata are saved.

    Returns:
        None
    
    Raises:
        ValidationError: If output directory cannot be created
    """
    config = load_config()
    map_shape: Tuple[int, int] = get_map_shape()

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 70)
    logger.info("🗺️  GEESP-Angola Map Generator - Versão Simplificada")
    logger.info("=" * 70)
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Map shape: {map_shape}")

    # 1. IRRADIAÇÃO SOLAR
    logger.info("Generating Solar Irradiance map...")
    np.random.seed(42)
    a: RasterArray = np.linspace(np.float32(6.4), np.float32(5.5), map_shape[0], dtype=np.float32)[:, np.newaxis]
    b: RasterArray = np.linspace(np.float32(0.0), np.float32(0.2), map_shape[1], dtype=np.float32)[np.newaxis, :]
    c: RasterArray = np.random.normal(0.0, 0.1, map_shape).astype(np.float32)
    solar: RasterArray = (a + b + c).astype(np.float32)
    solar = np.clip(solar, 5.5, 6.4).astype(np.float32)
    np.save(output_dir / "mapa_irradiacao.npy", solar)
    logger.info(f"✓ Solar Irradiance: Min={solar.min():.2f}, Max={solar.max():.2f}, Mean={solar.mean():.2f} kWh/m²/day")

    # 2. DENSIDADE POPULACIONAL
    logger.info("Generating Population Density map...")
    population: RasterArray = np.zeros(map_shape, dtype=np.float32)
    for cy, cx, intensity in [(70, 135, 45), (210, 195, 60), (155, 90, 55)]:
        y = np.arange(map_shape[0])
        x = np.arange(map_shape[1])
        Y, X = np.meshgrid(x, y)
        gaussian = intensity * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / 1500)
        population += gaussian
    population += np.random.poisson(5, map_shape).astype(np.float32)
    population = np.clip(population, 10, 95).astype(np.float32)
    np.save(output_dir / "mapa_populacao.npy", population)
    logger.info(f"✓ Population Density: Min={population.min():.1f}, Max={population.max():.1f}, Mean={population.mean():.1f}")

    # 3. DISTÂNCIA À REDE ELÉTRICA
    logger.info("Generating Grid Distance map...")
    distance: RasterArray = (np.ones((map_shape[0], map_shape[1]), dtype=np.float32) * 30).astype(np.float32)
    distance[int(0.3 * map_shape[0]), :] = np.linspace(0, 45, map_shape[1], dtype=np.float32)
    distance[:, int(0.4 * map_shape[1])] = np.linspace(0, 45, map_shape[0], dtype=np.float32)
    for i in range(map_shape[0]):
        distance[i, min(int(0.18 * i), map_shape[1] - 1)] = 0
    distance = np.clip(distance, 0, 45).astype(np.float32)
    np.save(output_dir / "mapa_distanciarede.npy", distance)
    logger.info(f"✓ Grid Distance: Min={distance.min():.2f}, Max={distance.max():.2f}, Mean={distance.mean():.2f} km")

    # 4. DECLIVIDADE
    logger.info("Generating Slope map...")
    slope: RasterArray = np.random.uniform(2, 28, (map_shape[0], map_shape[1])).astype(np.float32)
    slope = slope + np.linspace(5, -2, map_shape[0], dtype=np.float32)[:, np.newaxis]
    slope = np.clip(slope, 0, 30).astype(np.float32)
    np.save(output_dir / "mapa_declividade.npy", slope)
    logger.info(f"✓ Slope: Min={slope.min():.2f}, Max={slope.max():.2f}, Mean={slope.mean():.2f}°")

    # 5. NDVI
    logger.info("Generating NDVI (Vegetation) map...")
    ndvi: RasterArray = (
        0.3 + 0.35 * np.linspace(1, 0, map_shape[0], dtype=np.float32)[:, np.newaxis] + np.random.normal(0, 0.08, (map_shape[0], map_shape[1])).astype(np.float32)
    )
    ndvi = np.clip(ndvi, -0.2, 0.7).astype(np.float32)
    np.save(output_dir / "mapa_ndvi.npy", ndvi)
    logger.info(f"✓ NDVI: Min={ndvi.min():.3f}, Max={ndvi.max():.3f}, Mean={ndvi.mean():.3f}")

    # 6. APTIDÃO INTEGRADA
    logger.info("Generating Integrated Aptitude map (MCDA)...")
    try:
        # Preferred import when part of `scripts` package
        from .map_utils import compute_aptitude, build_metadata
    except ImportError:
        # Fallback when module is imported as top-level
        from map_utils import compute_aptitude, build_metadata

    aptitude: RasterArray = compute_aptitude(solar, population, distance, slope, ndvi)
    np.save(output_dir / "mapa_aptidao_integrada.npy", aptitude)
    logger.info(f"✓ Integrated Aptitude: Min={aptitude.min():.3f}, Max={aptitude.max():.3f}, Mean={aptitude.mean():.3f}")
    logger.info("=" * 70)
    logger.info("✓ All maps generated successfully!")
    logger.info("=" * 70)

    metadata: Dict = build_metadata(solar, population, distance, slope, ndvi, aptitude, output_shape=tuple(map_shape))
    metadata_path = output_dir / "mapas_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n" + "=" * 70)
    print("✅ GERAÇÃO DE MAPAS CONCLUÍDA!")
    print("=" * 70)


def main() -> Optional[None]:
    """Entry point used by the unified Streamlit app."""
    return generate_maps()


if __name__ == "__main__":
    generate_maps()
