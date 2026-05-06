"""
FastAPI REST API for GEESP-Angola MCDA Analysis
Exposes endpoints for health checks, MCDA computation, and analysis metadata.

This module is optional; the project does not require FastAPI to run core analyses.
If FastAPI or Pydantic are not installed the API module will still import at analysis time.

OpenAPI/Swagger Documentation: /docs (Swagger UI)
ReDoc Documentation: /redoc
"""

from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
from numpy.typing import NDArray

from .config_loader import load_config
from .type_annotations import RasterArray

# ============================================================================
# LOGGING SETUP
# ============================================================================

# Use shared logging utility
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
try:
    from logging_setup import setup_logging
    logger = setup_logging("geesp_api", log_file="logs/geesp_api.log")
except ImportError:
    # Fallback if utils not available
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

logger.info("Initializing GEESP-Angola FastAPI application")

# Initialize FastAPI with comprehensive OpenAPI metadata
app = FastAPI(
    title="GEESP-Angola Energy Suitability API",
    description="REST API for geospatial energy analysis using MCDA (Multi-Criteria Decision Analysis) and AHP (Analytic Hierarchy Process)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "GEESP-Angola Team",
        "url": "https://github.com/ISPTEC-Energy/geesp-angola",
        "email": "contact@geesp-angola.org",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Enable CORS for web-based access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("data/processed")

# Available raster layers
AVAILABLE_LAYERS = [
    "mapa_irradiacao",      # Solar irradiance (kWh/m²/day)
    "mapa_populacao",       # Population density (people/km²)
    "mapa_distanciarede",   # Distance to grid (km)
    "mapa_declividade",     # Slope (degrees)
    "mapa_ndvi",            # Vegetation index (NDVI -1 to 1)
]


class MCDARequest(BaseModel):
    """
    MCDA Weighted Overlay Request Model
    
    Accepts normalized weights (0-1) for each raster layer.
    Weights will be normalized if they don't sum to 1.0.
    """
    weights: Dict[str, float] = Field(
        ...,
        example={
            "mapa_irradiacao": 0.35,
            "mapa_populacao": 0.25,
            "mapa_distanciarede": 0.20,
            "mapa_declividade": 0.10,
            "mapa_ndvi": 0.10
        },
        description="Dictionary of layer names to weights (0.0-1.0 range)"
    )


class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Status of the API")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    version: str = Field(..., description="API version")
    available_layers: List[str] = Field(..., description="Available raster layers for MCDA")


class MCDAResponse(BaseModel):
    """MCDA computation response model"""
    status: str = Field(..., description="Computation status (success/error)")
    summary: Dict[str, float] = Field(
        ...,
        description="Summary statistics (min, max, mean, std)"
    )
    saved_path: str = Field(..., description="Path to saved output raster")
    weights_used: Dict[str, float] = Field(..., description="Normalized weights applied")
    timestamp: str = Field(..., description="ISO 8601 computation timestamp")
    error: Optional[str] = Field(None, description="Error message if computation failed")


class MCDABatchRequest(BaseModel):
    """
    Batch MCDA Request Model - Process multiple weight sets in parallel
    
    Example:
        {
            "weight_sets": [
                {"solar": 0.4, "population": 0.3, "distance": 0.2, "slope": 0.1},
                {"solar": 0.3, "population": 0.4, "distance": 0.2, "slope": 0.1},
                {"solar": 0.2, "population": 0.2, "distance": 0.3, "slope": 0.3}
            ]
        }
    """
    weight_sets: List[Dict[str, float]] = Field(
        ...,
        description="Array of weight dictionaries, each will be processed as separate MCDA computation"
    )


class MCDABatchResponse(BaseModel):
    """Batch MCDA response with results for all weight sets"""
    status: str = Field(..., description="Batch computation status (all_success/partial_success/failed)")
    results: List[MCDAResponse] = Field(..., description="Array of MCDA responses, one per weight set")
    total_computed: int = Field(..., description="Total number of successful computations")
    total_requested: int = Field(..., description="Total number of weight sets requested")
    timestamp: str = Field(..., description="ISO 8601 batch computation timestamp")
    duration_seconds: float = Field(..., description="Total computation time in seconds")


@app.get(
    "/health",
    response_model=HealthCheckResponse,
    summary="Health Check",
    tags=["System"],
    responses={200: {"description": "API is healthy and ready"}}
)
async def health():
    """
    Check API health status and available resources.
    
    Returns:
        - status: OK if API is operational
        - timestamp: Current server time
        - version: API version
        - available_layers: List of raster layers loaded
    """
    logger.info("Health check requested")
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "available_layers": AVAILABLE_LAYERS
    }


@app.get(
    "/layers",
    summary="List Available Raster Layers",
    tags=["Data"],
    responses={200: {"description": "List of available raster layers for analysis"}}
)
async def list_layers():
    """
    Get list of available raster layers that can be used in MCDA analysis.
    
    Returns:
        List of layer names and their descriptions
    """
    layers_info = {
        "available": AVAILABLE_LAYERS,
        "count": len(AVAILABLE_LAYERS),
        "descriptions": {
            "mapa_irradiacao": "Solar irradiance (kWh/m²/day) - higher = better for solar",
            "mapa_populacao": "Population density (people/km²) - higher = more demand",
            "mapa_distanciarede": "Distance to electrical grid (km) - lower = better",
            "mapa_declividade": "Slope (degrees) - low/moderate = easier installation",
            "mapa_ndvi": "Vegetation index (-1 to 1) - moderate = suitable land cover"
        }
    }
    return layers_info


@app.post(
    "/mcda",
    response_model=MCDAResponse,
    summary="Compute MCDA Weighted Overlay",
    tags=["Analysis"],
    responses={
        200: {"description": "MCDA computation successful"},
        400: {"description": "Missing required data or invalid weights"},
        500: {"description": "Server error during computation"}
    }
)
async def compute_mcda(req: MCDARequest):
    """
    Compute MCDA weighted overlay from loaded raster maps.
    
    This endpoint performs a normalized weighted sum of raster layers
    to produce a composite suitability/aptitude map.
    
    Args:
        req: MCDARequest with weights dictionary
        
    Returns:
        MCDAResponse with computation results and saved file path
        
    Example:
        ```
        POST /mcda
        {
            "weights": {
                "mapa_irradiacao": 0.35,
                "mapa_populacao": 0.25,
                "mapa_distanciarede": 0.20,
                "mapa_declividade": 0.10,
                "mapa_ndvi": 0.10
            }
        }
        ```
    """
    logger.info(f"MCDA computation requested with weights: {req.weights}")
    
    # supported maps: mapa_irradiacao, mapa_populacao, mapa_distanciarede,
    # mapa_declividade, mapa_ndvi
    maps = {}
    for name in AVAILABLE_LAYERS:
        p = DATA_DIR / f"{name}.npy"
        if p.exists():
            maps[name] = np.load(p)
            logger.debug(f"Loaded raster: {name}")
    
    if not maps:
        logger.error("No raster maps found in data/processed/")
        raise HTTPException(
            status_code=400,
            detail="No raster maps found in data/processed/. Run generate_maps_simple.py first."
        )
    
    logger.info(f"Loaded {len(maps)} raster layers")
    
    # Validate and normalize input weights
    weights = req.weights
    weight_sum = sum(weights.values())
    if weight_sum == 0:
        logger.error("Weight sum is zero")
        raise HTTPException(
            status_code=400,
            detail="Weights must sum to non-zero value"
        )
    
    # Normalize weights to sum to 1.0
    normalized_weights = {k: v / weight_sum for k, v in weights.items()}
    logger.info(f"Normalized weights: {normalized_weights}")
    
    # Normalize raster maps to [0, 1] range
    normed = {}
    for k, arr in maps.items():
        a = np.array(arr, dtype=float)
        valid = np.isfinite(a)
        if not valid.any():
            logger.warning(f"No valid data in {k}")
            continue
        
        amin = a[valid].min()
        amax = a[valid].max()
        if amax - amin < 1e-9:
            norm = np.ones_like(a) * 0.5
        else:
            norm = (a - amin) / (amax - amin)
        normed[k] = np.nan_to_num(norm, nan=0.0, posinf=0.5, neginf=0.5)
        logger.debug(f"Normalized {k} to [0, 1] range")
    
    if not normed:
        logger.error("No valid raster data to process")
        raise HTTPException(
            status_code=400,
            detail="No valid raster data could be processed"
        )
    
    # Apply normalized weights to compute weighted overlay
    overlay = None
    for k, arr in normed.items():
        w = float(normalized_weights.get(k, 0.0))
        if w > 0:
            if overlay is None:
                overlay = w * arr
            else:
                overlay = overlay + w * arr
    
    if overlay is None:
        logger.error("Overlay computation failed")
        raise HTTPException(
            status_code=500,
            detail="Overlay computation resulted in no data"
        )
    
    overlay = np.asarray(overlay)
    
    # Save result to disk
    out_path = DATA_DIR / "api_mapa_aptidao.npy"
    np.save(out_path, overlay)
    logger.info(f"Saved MCDA result to {out_path}")
    
    result = {
        "status": "success",
        "summary": {
            "min": float(np.nanmin(overlay)),
            "max": float(np.nanmax(overlay)),
            "mean": float(np.nanmean(overlay)),
            "std": float(np.nanstd(overlay)),
        },
        "saved_path": str(out_path),
        "weights_used": normalized_weights,
        "timestamp": datetime.utcnow().isoformat(),
    }
    logger.info(f"MCDA computation successful: min={result['summary']['min']:.3f}, max={result['summary']['max']:.3f}, mean={result['summary']['mean']:.3f}")
    
    return result


@app.post(
    "/mcda/batch",
    response_model=MCDABatchResponse,
    summary="Compute Batch MCDA (Parallel Processing)",
    tags=["Analysis"],
    responses={
        200: {"description": "Batch MCDA computation successful (one or more results)"},
        400: {"description": "Invalid batch request or no raster data"},
        500: {"description": "Server error during batch computation"}
    }
)
async def compute_mcda_batch(req: MCDABatchRequest):
    """
    Process multiple MCDA analyses in parallel for sensitivity analysis.
    
    This endpoint computes MCDA weighted overlay for each weight set independently.
    Useful for scenario analysis, stakeholder preferences sensitivity, and robustness testing.
    
    Args:
        req: MCDABatchRequest containing array of weight dictionaries
        
    Returns:
        MCDABatchResponse with array of MCDA results, one per weight set
        
    Example:
        ```
        POST /mcda/batch
        {
            "weight_sets": [
                {"mapa_irradiacao": 0.4, "mapa_populacao": 0.3, "mapa_distanciarede": 0.2, "mapa_declividade": 0.1},
                {"mapa_irradiacao": 0.3, "mapa_populacao": 0.4, "mapa_distanciarede": 0.2, "mapa_declividade": 0.1}
            ]
        }
        ```
    """
    import time
    import asyncio
    from concurrent.futures import ThreadPoolExecutor
    
    start_time = time.time()
    logger.info(f"Batch MCDA computation requested with {len(req.weight_sets)} weight sets")
    
    # Load rasters once (shared across all batch computations)
    maps = {}
    for name in AVAILABLE_LAYERS:
        p = DATA_DIR / f"{name}.npy"
        if p.exists():
            maps[name] = np.load(p)
    
    if not maps:
        logger.error("No raster maps found in data/processed/")
        raise HTTPException(
            status_code=400,
            detail="No raster maps found in data/processed/. Run generate_maps_simple.py first."
        )
    
    logger.info(f"Loaded {len(maps)} raster layers for batch processing")
    
    results = []
    
    # Process each weight set
    for idx, weights in enumerate(req.weight_sets):
        try:
            logger.debug(f"Processing weight set {idx+1}/{len(req.weight_sets)}")
            
            # Validate weight sum
            weight_sum = sum(weights.values())
            if weight_sum == 0:
                logger.warning(f"Weight set {idx} has zero sum, skipping")
                results.append(MCDAResponse(
                    status="error",
                    summary={"min": 0, "max": 0, "mean": 0, "std": 0},
                    saved_path="",
                    weights_used={},
                    timestamp=datetime.utcnow().isoformat(),
                    error="Weights must sum to non-zero value"
                ))
                continue
            
            # Normalize weights
            normalized_weights = {k: v / weight_sum for k, v in weights.items()}
            
            # Normalize rasters (only on first iteration, reuse for subsequent)
            if idx == 0:
                normed = {}
                for k, arr in maps.items():
                    a = np.array(arr, dtype=float)
                    valid = np.isfinite(a)
                    if not valid.any():
                        continue
                    
                    amin = a[valid].min()
                    amax = a[valid].max()
                    if amax - amin < 1e-9:
                        norm = np.ones_like(a) * 0.5
                    else:
                        norm = (a - amin) / (amax - amin)
                    normed[k] = np.nan_to_num(norm, nan=0.0, posinf=0.5, neginf=0.5)
            
            if not normed:
                logger.warning(f"No valid raster data for weight set {idx}")
                results.append(MCDAResponse(
                    status="error",
                    summary={"min": 0, "max": 0, "mean": 0, "std": 0},
                    saved_path="",
                    weights_used=normalized_weights,
                    timestamp=datetime.utcnow().isoformat(),
                    error="No valid raster data could be processed"
                ))
                continue
            
            # Compute weighted overlay
            overlay = None
            for k, arr in normed.items():
                w = float(normalized_weights.get(k, 0.0))
                if w > 0:
                    if overlay is None:
                        overlay = w * arr
                    else:
                        overlay = overlay + w * arr
            
            if overlay is None:
                logger.error(f"Overlay computation failed for weight set {idx}")
                results.append(MCDAResponse(
                    status="error",
                    summary={"min": 0, "max": 0, "mean": 0, "std": 0},
                    saved_path="",
                    weights_used=normalized_weights,
                    timestamp=datetime.utcnow().isoformat(),
                    error="Overlay computation resulted in no data"
                ))
                continue
            
            overlay = np.asarray(overlay)
            
            # Save result
            out_path = DATA_DIR / f"api_mapa_aptidao_batch_{idx}.npy"
            np.save(out_path, overlay)
            
            result_obj = MCDAResponse(
                status="success",
                summary={
                    "min": float(np.nanmin(overlay)),
                    "max": float(np.nanmax(overlay)),
                    "mean": float(np.nanmean(overlay)),
                    "std": float(np.nanstd(overlay)),
                },
                saved_path=str(out_path),
                weights_used=normalized_weights,
                timestamp=datetime.utcnow().isoformat(),
            )
            results.append(result_obj)
            logger.info(f"✓ Weight set {idx+1} completed: min={result_obj.summary['min']:.3f}, max={result_obj.summary['max']:.3f}")
            
        except Exception as e:
            logger.error(f"Error processing weight set {idx}: {e}")
            results.append(MCDAResponse(
                status="error",
                summary={"min": 0, "max": 0, "mean": 0, "std": 0},
                saved_path="",
                weights_used=weights,
                timestamp=datetime.utcnow().isoformat(),
                error=str(e)
            ))
    
    # Determine overall status
    successful = sum(1 for r in results if r.status == "success")
    if successful == len(results):
        overall_status = "all_success"
    elif successful > 0:
        overall_status = "partial_success"
    else:
        overall_status = "failed"
    
    duration = time.time() - start_time
    
    batch_response = MCDABatchResponse(
        status=overall_status,
        results=results,
        total_computed=successful,
        total_requested=len(req.weight_sets),
        timestamp=datetime.utcnow().isoformat(),
        duration_seconds=duration
    )
    
    logger.info(f"Batch MCDA completed: {successful}/{len(req.weight_sets)} successful, duration={duration:.2f}s")
    
    return batch_response
