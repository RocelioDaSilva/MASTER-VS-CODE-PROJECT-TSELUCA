"""
GEESP-Angola: Utility Functions
Funções auxiliares para processamento de dados, validação e I/O
"""

import numpy as np
import pandas as pd
import logging
import json
from pathlib import Path
from typing import Union, Tuple, List, Optional, Any
import warnings

# Optional geospatial dependencies (import lazily / tolerate absence)
try:
    import rasterio
    from rasterio.features import geometry_mask
    from rasterio.transform import Affine

    HAS_RASTERIO = True
except Exception:
    rasterio = None
    geometry_mask = None
    Affine = None
    HAS_RASTERIO = False

try:
    import geopandas as gpd
    from shapely.geometry import box

    HAS_GEOPANDAS = True
except Exception:
    gpd = None
    box = None
    HAS_GEOPANDAS = False
warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)


# ============================================================================
# FILE I/O & DATA LOADING
# ============================================================================


def load_raster(filepath: str) -> Tuple[np.ndarray, Optional[dict]]:
    """
    Carrega arquivo GeoTIFF e retorna matriz + metadados

    Args:
        filepath (str): Caminho para o raster

    Returns:
        Tuple[np.ndarray, dict]: (dados, metadados)
    """
    # If rasterio is not available, allow loading .npy fallback files
    if not HAS_RASTERIO:
        if str(filepath).lower().endswith(".npy"):
            try:
                arr = np.load(str(filepath))
                logger.info(
                    f"✓ Raster (npy) carregado: {Path(filepath).name} ({arr.shape})"
                )
                return arr, None
            except Exception as e:
                logger.error(f"✗ Erro ao carregar .npy {filepath}: {e}")
                raise
        raise ImportError(
            "rasterio is required for load_raster; install rasterio or use .npy fallback files"
        )

    try:
        with rasterio.open(filepath) as src:
            data = src.read(1).astype(np.float32)
            metadata = src.meta

            # Substitui NoData por NaN
            if src.nodata is not None:
                data[data == src.nodata] = np.nan

            logger.info(
                f"✓ Raster carregado: {Path(filepath).name} "
                f"({data.shape[0]} x {data.shape[1]} pixels)"
            )
            return data, metadata

    except Exception as e:
        # If rasterio fails to open the file and the path ends with .npy,
        # attempt to load as numpy array as a safe fallback. This makes
        # `load_raster` resilient in environments where GeoTIFFs are not
        # available and tests use .npy fallback files.
        logger.error(f"✗ Erro ao carregar raster {filepath}: {e}")
        if str(filepath).lower().endswith(".npy"):
            try:
                arr = np.load(str(filepath))
                logger.info(f"✓ Raster (npy fallback) carregado: {Path(filepath).name} ({arr.shape})")
                return arr, None
            except Exception as ne:
                logger.error(f"✗ Erro ao carregar .npy {filepath}: {ne}")
                raise
        raise


def save_raster(data: np.ndarray, filepath: str, metadata: Optional[dict] = None):
    """
    Salva array como GeoTIFF

    Args:
        data (np.ndarray): Dados a salvar
        filepath (str): Caminho de saída
        metadata (dict): Metadados rasterio (CRS, transform, etc)
    """
    try:
        # If filepath ends with .npy, always use numpy fallback (safe portable option)
        if str(filepath).lower().endswith(".npy"):
            np.save(str(filepath), data)
            logger.info(f"✓ Raster salvo (npy fallback): {Path(filepath).name}")
            return

        # If rasterio is available, save as GeoTIFF
        if HAS_RASTERIO:
            if metadata is None:
                metadata = {
                    "driver": "GTiff",
                    "dtype": rasterio.float32,
                    "width": data.shape[1],
                    "height": data.shape[0],
                    "count": 1,
                    "crs": "EPSG:32733",  # UTM Zone 33S (Angola)
                    "transform": rasterio.transform.Affine(30, 0, 0, 0, -30, 0),
                }

            metadata.update(
                {
                    "dtype": rasterio.float32,
                    "width": data.shape[1],
                    "height": data.shape[0],
                    "count": 1,
                }
            )

            with rasterio.open(filepath, "w", **metadata) as dst:
                dst.write(np.nan_to_num(data, nan=-9999), 1)

            logger.info(f"✓ Raster salvo: {Path(filepath).name}")
            return

        # Fallback: if filepath ends with .npy, save as numpy array
        if str(filepath).lower().endswith(".npy"):
            np.save(str(filepath), data)
            logger.info(f"✓ Raster salvo (npy fallback): {Path(filepath).name}")
            return

        raise ImportError(
            "rasterio is required to save GeoTIFF; install rasterio or save as .npy"
        )

    except Exception as e:
        logger.error(f"✗ Erro ao salvar raster: {e}")
        raise


def load_shapefile(filepath: str) -> object:
    """
    Carrega shapefile e retorna GeoDataFrame

    Args:
        filepath (str): Caminho do shapefile

    Returns:
        gpd.GeoDataFrame: Dados geoespaciais
    """
    try:
        gdf = gpd.read_file(filepath)
        logger.info(f"✓ Shapefile carregado: {len(gdf)} feições")
        return gdf

    except Exception as e:
        logger.error(f"✗ Erro ao carregar shapefile: {e}")
        raise


def save_shapefile(gdf, filepath: str):
    """Salva GeoDataFrame como shapefile"""
    try:
        gdf.to_file(filepath)
        logger.info(f"✓ Shapefile salvo: {Path(filepath).name}")
    except Exception as e:
        logger.error(f"✗ Erro ao salvar shapefile: {e}")
        raise


# ============================================================================
# DATA VALIDATION & STATISTICS
# ============================================================================


def validate_raster(data: np.ndarray, name: str = "Raster") -> dict:
    """
    Valida qualidade do raster (NaN, extremos, etc)

    Args:
        data (np.ndarray): Dados do raster
        name (str): Nome para logs

    Returns:
        dict: Estatísticas de validação
    """
    valid_mask = np.isfinite(data)
    valid_count = np.sum(valid_mask)
    total_count = data.size

    stats = {
        "name": name,
        "total_pixels": total_count,
        "valid_pixels": valid_count,
        "valid_percent": (valid_count / total_count * 100) if total_count > 0 else 0,
        "nan_count": np.sum(~valid_mask),
        "inf_count": np.sum(np.isinf(data)),
        "min": float(np.nanmin(data)) if valid_count > 0 else None,
        "max": float(np.nanmax(data)) if valid_count > 0 else None,
        "mean": float(np.nanmean(data)) if valid_count > 0 else None,
        "std": float(np.nanstd(data)) if valid_count > 0 else None,
        "median": float(np.nanmedian(data)) if valid_count > 0 else None,
    }

    if stats["valid_percent"] < 70:
        logger.warning(
            f"⚠ {name}: Apenas {stats['valid_percent']:.1f}% " "de pixels válidos"
        )

    return stats


def compare_rasters_stats(rasters_dict: dict) -> pd.DataFrame:
    """
    Compara estatísticas entre múltiplos rasters

    Args:
        rasters_dict (dict): {nome: array}

    Returns:
        pd.DataFrame: Comparação estatística
    """
    stats_list = []

    for name, data in rasters_dict.items():
        stats = validate_raster(data, name)
        stats_list.append(stats)

    df = pd.DataFrame(stats_list)
    logger.info(f"✓ Comparação de {len(df)} rasters gerada")

    return df


# ============================================================================
# SPATIAL OPERATIONS
# ============================================================================


def clip_raster_by_geometry(
    raster: np.ndarray, geometry, transform, crs="EPSG:32733"
) -> np.ndarray:
    """
    Recorta raster pela geometria de um shapefile

    Args:
        raster (np.ndarray): Dados do raster
        geometry: Geometria shapely
        transform: rasterio.transform.Affine
        crs (str): Sistema de coordenadas

    Returns:
        np.ndarray: Raster recortado
    """
    if not HAS_RASTERIO:
        raise ImportError("rasterio is required for clip_raster_by_geometry")

    try:
        # Cria máscara da geometria
        mask = geometry_mask(
            [geometry],
            out_shape=raster.shape,
            transform=transform,
            invert=False,  # True = dentro, False = fora
        )

        # Aplica máscara (valores fora = NaN)
        clipped = raster.copy()
        clipped[~mask] = np.nan

        logger.info(f"✓ Raster recortado pela geometria")
        return clipped

    except Exception as e:
        logger.error(f"✗ Erro ao recortar raster: {e}")
        raise


def extract_pixels_by_geometry(raster: np.ndarray, geometry, transform) -> np.ndarray:
    """
    Extrai valores de pixels dentro de uma geometria

    Args:
        raster (np.ndarray): Dados
        geometry: Geometria shapely
        transform: Transform rasterio

    Returns:
        np.ndarray: Valores extraídos (1D)
    """
    if not HAS_RASTERIO:
        raise ImportError("rasterio is required for extract_pixels_by_geometry")

    try:
        mask = geometry_mask(
            [geometry], out_shape=raster.shape, transform=transform, invert=False
        )

        values = raster[mask]
        valid_values = values[np.isfinite(values)]

        logger.info(f"✓ {len(valid_values)} pixels extraídos")
        return valid_values

    except Exception as e:
        logger.error(f"✗ Erro ao extrair pixels: {e}")
        raise


def create_aoi_from_bbox(
    bounds: Tuple[float, float, float, float], buffer: float = 0
) -> object:
    """
    Cria geometria de AOI a partir de bounds

    Args:
        bounds (Tuple): (minx, miny, maxx, maxy)
        buffer (float): Buffer em graus

    Returns:
        shapely.geometry.box: Geometria da AOI
    """
    minx, miny, maxx, maxy = bounds

    if buffer > 0:
        minx -= buffer
        miny -= buffer
        maxx += buffer
        maxy += buffer

    return box(minx, miny, maxx, maxy)


# ============================================================================
# CONVERSION & FORMATTING
# ============================================================================


def raster_to_dataframe(
    raster: np.ndarray, transform, include_coords: bool = True
) -> pd.DataFrame:
    """
    Converte raster em DataFrame

    Args:
        raster (np.ndarray): Dados do raster
        transform: rasterio.transform.Affine
        include_coords (bool): Incluir coordenadas (x, y)

    Returns:
        pd.DataFrame: Dados tabulares
    """
    if not HAS_RASTERIO:
        raise ImportError("rasterio is required for raster_to_dataframe")

    try:
        valid_mask = np.isfinite(raster)
        y_indices, x_indices = np.where(valid_mask)
        values = raster[valid_mask]

        if include_coords:
            xs = transform.c + x_indices * transform.a
            ys = transform.f + y_indices * transform.e

            df = pd.DataFrame({"x": xs, "y": ys, "value": values})
        else:
            df = pd.DataFrame({"value": values})

        logger.info(f"✓ {len(df)} pontos convertidos para DataFrame")
        return df

    except Exception as e:
        logger.error(f"✗ Erro ao converter raster: {e}")
        raise


# ============================================================================
# VISUALIZATION HELPERS
# ============================================================================


def normalize_for_visualization(
    data: np.ndarray, vmin=None, vmax=None, clip_outliers: bool = True
) -> np.ndarray:
    """
    Normaliza dados para visualização [0, 255]

    Args:
        data (np.ndarray): Dados originais
        vmin, vmax (float): Limites de visualização
        clip_outliers (bool): Recorta outliers em percentil 2/98

    Returns:
        np.ndarray: Dados normalizados
    """
    valid_data = data[np.isfinite(data)]

    # Guard: if no finite data present, return zeros of same shape
    if valid_data.size == 0:
        return np.zeros_like(data, dtype=np.uint8)

    if clip_outliers:
        p2, p98 = np.percentile(valid_data, [2, 98])
        vmin = vmin or p2
        vmax = vmax or p98
    else:
        vmin = vmin or np.nanmin(valid_data)
        vmax = vmax or np.nanmax(valid_data)

    # Avoid division by zero when vmin == vmax
    if vmax == vmin:
        scaled = np.zeros_like(data, dtype=np.uint8)
        return scaled

    # Normaliza
    normalized = np.clip(data, vmin, vmax)
    normalized = (normalized - vmin) / (vmax - vmin) * 255
    normalized = np.nan_to_num(normalized, nan=0).astype(np.uint8)

    return normalized


# ============================================================================
# REPORT GENERATION
# ============================================================================


def generate_analysis_report(results: dict, output_path: str = "report.txt"):
    """
    Gera relatório textual dos resultados MCDA

    Args:
        results (dict): Resultados da análise
        output_path (str): Caminho do arquivo de saída
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("GEESP-Angola: Relatório de Análise MCDA-SIG\n")
            f.write("=" * 80 + "\n\n")

            for key, value in results.items():
                if isinstance(value, dict):
                    f.write(f"\n{key}:\n")
                    for k, v in value.items():
                        f.write(f"  {k}: {v}\n")
                else:
                    f.write(f"{key}: {value}\n")

        logger.info(f"✓ Relatório salvo: {output_path}")

    except Exception as e:
        logger.error(f"✗ Erro ao gerar relatório: {e}")
        raise


# ============================================================================
# CONFIG & LOGGING
# ============================================================================


# NOTE: setup_logging, load_config, and save_config have been moved to centralized modules:
# - Logging: Use utils/logging_setup.py::setup_logging()
# - Config: Use scripts/config_loader.py::load_config()
# These functions are kept here for backward compatibility but delegate to centralized versions

def setup_logging(log_file: str = "geesp-angola.log"):
    """DEPRECATED: Use utils.logging_setup.setup_logging() instead"""
    import warnings
    warnings.warn(
        "scripts.utils.setup_logging is deprecated. Use utils.logging_setup.setup_logging() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    logger.info("✓ Logging configurado")


def load_config(config_path: str) -> dict:
    """DEPRECATED: Use scripts.config_loader.load_config() instead"""
    import warnings
    warnings.warn(
        "scripts.utils.load_config is deprecated. Use scripts.config_loader.load_config() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        logger.info(f"✓ Configuração carregada de {config_path}")
        return config
    except Exception as e:
        logger.error(f"✗ Erro ao carregar configuração: {e}")
        raise


def save_config(config: dict, config_path: str):
    """DEPRECATED: Use scripts.config_loader.ConfigLoader.save_section() instead"""
    import warnings
    warnings.warn(
        "scripts.utils.save_config is deprecated. Use scripts.config_loader.ConfigLoader.save_section() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
        logger.info(f"✓ Configuração salva em {config_path}")
    except Exception as e:
        logger.error(f"✗ Erro ao salvar configuração: {e}")
        raise
