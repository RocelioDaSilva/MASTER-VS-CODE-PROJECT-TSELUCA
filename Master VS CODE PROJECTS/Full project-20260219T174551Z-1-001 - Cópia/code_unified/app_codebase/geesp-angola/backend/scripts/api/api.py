"""
FastAPI REST API for GEESP-Angola MCDA Analysis
Exposes endpoints for health checks, MCDA computation, batch processing, and analysis metadata.

This module is optional; the project does not require FastAPI to run core analyses.
If FastAPI or Pydantic are not installed the API module will still import at analysis time.

OpenAPI/Swagger Documentation: /docs (Swagger UI)
ReDoc Documentation: /redoc

FEATURES:
- Health checks and API status
- Single MCDA computation
- Batch MCDA processing with synchronous results
- Asynchronous job queue for long-running analyses
- Job status tracking and result retrieval
"""

from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta, timezone
import logging
import uuid
import threading
from dataclasses import dataclass, field, asdict

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import numpy as np
from numpy.typing import NDArray

from utils.helpers import setup_project_paths
from utils.logging import setup_logging
from utils.constants import UIConstants, APIConstants, DataPathConstants, TechnicalConstants
from core.config import get_config_value
from .type_annotations import RasterArray

# Initialize paths and logging
setup_project_paths()
logger = setup_logging(__name__, log_file=DataPathConstants.API_LOG_FILE)


# ============================================================================
# BATCH JOB PROCESSING CLASSES
# ============================================================================

class BatchJobConstants:
    """Batch job processing constants"""
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    CLEANUP_AGE_HOURS = 24
    MSG_SUBMITTED_FORMAT = "MCDA job {job_id} submitted for processing"
    MSG_NOT_FOUND_FORMAT = "Job {job_id} not found"
    MSG_NOT_COMPLETED_FORMAT = "Job {job_id} is {status}, not completed"


@dataclass
class MCDAJobData:
    """Represents a single MCDA batch job"""
    job_id: str
    weights: Dict[str, float]
    status: str = BatchJobConstants.STATUS_PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    output_path: Optional[str] = None
    processing_time_seconds: float = 0.0
    result_metadata: Optional[Dict] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON response"""
        return asdict(self)


class MCDABatchProcessor:
    """Process MCDA jobs asynchronously with queue management"""
    
    def __init__(self, max_workers: int = None):
        """Initialize batch processor"""
        self.max_workers = max_workers or 4
        self.jobs: Dict[str, MCDAJobData] = {}
        self.lock = threading.Lock()
        logger.info(f"MCDABatchProcessor initialized with {self.max_workers} workers")

    def submit_job(self, weights: Dict[str, float]) -> str:
        """Submit new MCDA job"""
        job_id = str(uuid.uuid4())[:8]
        job = MCDAJobData(job_id=job_id, weights=weights)
        
        with self.lock:
            self.jobs[job_id] = job
        
        logger.info(f"✓ Submitted MCDA job {job_id}")
        return job_id

    def get_job_status(self, job_id: str) -> Dict:
        """Get status of job"""
        if job_id not in self.jobs:
            raise HTTPException(status_code=404, detail=BatchJobConstants.MSG_NOT_FOUND_FORMAT.format(job_id=job_id))
        
        job = self.jobs[job_id]
        return {
            "job_id": job_id,
            "status": job.status,
            "created_at": job.created_at,
            "started_at": job.started_at,
            "completed_at": job.completed_at,
            "processing_time_seconds": job.processing_time_seconds,
            "error": job.error_message,
            "output_file": job.output_path,
        }

    def list_jobs(self, status: Optional[str] = None) -> List[Dict]:
        """List all jobs with optional status filter"""
        with self.lock:
            jobs = [
                {
                    "job_id": job.job_id,
                    "status": job.status,
                    "created_at": job.created_at,
                    "processing_time": job.processing_time_seconds,
                }
                for job in self.jobs.values()
                if status is None or job.status == status
            ]
        
        return sorted(jobs, key=lambda x: x["created_at"], reverse=True)

    def get_queue_stats(self) -> Dict:
        """Get queue statistics"""
        with self.lock:
            pending = sum(1 for j in self.jobs.values() if j.status == BatchJobConstants.STATUS_PENDING)
            processing = sum(1 for j in self.jobs.values() if j.status == BatchJobConstants.STATUS_PROCESSING)
            completed = sum(1 for j in self.jobs.values() if j.status == BatchJobConstants.STATUS_COMPLETED)
            failed = sum(1 for j in self.jobs.values() if j.status == BatchJobConstants.STATUS_FAILED)
        
        return {
            "total_jobs": len(self.jobs),
            "pending": pending,
            "processing": processing,
            "completed": completed,
            "failed": failed,
        }


_batch_processor: Optional[MCDABatchProcessor] = None
_processor_lock = threading.Lock()


def get_batch_processor() -> MCDABatchProcessor:
    """Get or create global batch processor instance"""
    global _batch_processor
    
    if _batch_processor is None:
        with _processor_lock:
            if _batch_processor is None:
                _batch_processor = MCDABatchProcessor(max_workers=4)
    
    return _batch_processor

# Initialize FastAPI with comprehensive OpenAPI metadata (from centralized constants)
app = FastAPI(
    title=UIConstants.API_TITLE,
    description=UIConstants.API_DESCRIPTION,
    version=UIConstants.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": UIConstants.API_CONTACT_NAME,
        "url": UIConstants.API_CONTACT_URL,
        "email": UIConstants.API_CONTACT_EMAIL,
    },
    license_info={
        "name": UIConstants.API_LICENSE_NAME,
        "url": UIConstants.API_LICENSE_URL,
    },
)

# Enable CORS for web-based access
app.add_middleware(
    CORSMiddleware,
    allow_origins=UIConstants.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=UIConstants.CORS_ALLOW_METHODS,
    allow_headers=UIConstants.CORS_ALLOW_HEADERS,
)

DATA_DIR = Path(DataPathConstants.DATA_PROCESSED_DIR)

# Available raster layers (from centralized constants)
AVAILABLE_LAYERS = APIConstants.AVAILABLE_LAYERS


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
        "status": APIConstants.HTTP_STATUS_OK,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": UIConstants.API_VERSION,
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
        "descriptions": APIConstants.LAYER_DESCRIPTIONS
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
        logger.error(f"No raster maps found in {DataPathConstants.DATA_PROCESSED_DIR}/")
        raise HTTPException(
            status_code=400,
            detail=APIConstants.ERROR_NO_RASTER_DATA
        )
    
    logger.info(f"Loaded {len(maps)} raster layers")
    
    # Validate and normalize input weights
    weights = req.weights
    weight_sum = sum(weights.values())
    if weight_sum == 0:
        logger.error("Weight sum is zero")
        raise HTTPException(
            status_code=400,
            detail=APIConstants.ERROR_WEIGHT_SUM_ZERO
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
        if amax - amin < TechnicalConstants.FLOAT_COMPARISON_TOLERANCE:
            norm = np.ones_like(a) * TechnicalConstants.RASTER_NORMALIZATION_DEFAULT
        else:
            norm = (a - amin) / (amax - amin)
        normed[k] = np.nan_to_num(norm, nan=TechnicalConstants.RASTER_NAN_VALUE, posinf=TechnicalConstants.RASTER_NORMALIZATION_DEFAULT, neginf=TechnicalConstants.RASTER_NORMALIZATION_DEFAULT)
        logger.debug(f"Normalized {k} to [0, 1] range")
    
    if not normed:
        logger.error("No valid raster data to process")
        raise HTTPException(
            status_code=400,
            detail=APIConstants.ERROR_NO_VALID_DATA
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
            detail=APIConstants.ERROR_OVERLAY_FAILED
        )
    
    overlay = np.asarray(overlay)
    
    # Save result to disk
    out_path = DATA_DIR / UIConstants.API_OUTPUT_MCDA
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
        "timestamp": datetime.now(timezone.utc).isoformat(),
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
        logger.error(f"No raster maps found in {DataPathConstants.DATA_PROCESSED_DIR}/")
        raise HTTPException(
            status_code=400,
            detail=APIConstants.ERROR_NO_RASTER_DATA
        )
    
    logger.info(f"Loaded {len(maps)} raster layers for batch processing")

    # Normalize rasters ONCE outside the loop — identical for all weight sets
    normed: Dict[str, np.ndarray] = {}
    for k, arr in maps.items():
        a = np.array(arr, dtype=float)
        valid = np.isfinite(a)
        if not valid.any():
            continue
        amin = a[valid].min()
        amax = a[valid].max()
        if amax - amin < TechnicalConstants.FLOAT_COMPARISON_TOLERANCE:
            normed[k] = np.ones_like(a) * TechnicalConstants.RASTER_NORMALIZATION_DEFAULT
        else:
            normed[k] = np.nan_to_num(
                (a - amin) / (amax - amin),
                nan=TechnicalConstants.RASTER_NAN_VALUE,
                posinf=TechnicalConstants.RASTER_NORMALIZATION_DEFAULT,
                neginf=TechnicalConstants.RASTER_NORMALIZATION_DEFAULT,
            )

    if not normed:
        logger.error("No valid raster data to process")
        raise HTTPException(status_code=400, detail=APIConstants.ERROR_NO_VALID_DATA)

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
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    error=APIConstants.ERROR_WEIGHT_SUM_ZERO
                ))
                continue

            # Normalize weights
            normalized_weights = {k: v / weight_sum for k, v in weights.items()}

            if not normed:
                logger.warning(f"No valid raster data for weight set {idx}")
                results.append(MCDAResponse(
                    status="error",
                    summary={"min": 0, "max": 0, "mean": 0, "std": 0},
                    saved_path="",
                    weights_used=normalized_weights,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    error=APIConstants.ERROR_NO_VALID_DATA
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
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    error=APIConstants.ERROR_OVERLAY_FAILED
                ))
                continue
            
            overlay = np.asarray(overlay)
            
            # Save result
            out_path = DATA_DIR / UIConstants.API_OUTPUT_MCDA_BATCH.format(idx=idx)
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
                timestamp=datetime.now(timezone.utc).isoformat(),
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
                timestamp=datetime.now(timezone.utc).isoformat(),
                error=str(e)
            ))
    
    # Determine overall status
    successful = sum(1 for r in results if r.status == "success")
    if successful == len(results):
        overall_status = APIConstants.HTTP_BATCH_STATUS_ALL_SUCCESS
    elif successful > 0:
        overall_status = APIConstants.HTTP_BATCH_STATUS_PARTIAL_SUCCESS
    else:
        overall_status = APIConstants.HTTP_BATCH_STATUS_FAILED
    
    duration = time.time() - start_time
    
    batch_response = MCDABatchResponse(
        status=overall_status,
        results=results,
        total_computed=successful,
        total_requested=len(req.weight_sets),
        timestamp=datetime.now(timezone.utc).isoformat(),
        duration_seconds=duration
    )
    
    logger.info(f"Batch MCDA completed: {successful}/{len(req.weight_sets)} successful, duration={duration:.2f}s")
    
    return batch_response

# ============================================================================
# ASYNCHRONOUS JOB QUEUE ENDPOINTS
# ============================================================================

@app.post(
    "/mcda/jobs",
    summary="Submit MCDA Job to Async Queue",
    tags=["Batch Jobs"],
    responses={202: {"description": "Job submitted for asynchronous processing"}}
)
async def submit_mcda_job(req: MCDARequest, background_tasks: BackgroundTasks):
    """
    Submit MCDA analysis to asynchronous job queue.
    
    Returns immediately with job ID for status tracking.
    Use /mcda/jobs/{job_id} to check status.
    
    Args:
        req: MCDARequest with weights dictionary
        
    Returns:
        Job submission response with job_id
        
    Example:
        POST /mcda/jobs with weights
        Response: { "job_id": "abc12345", "status": "submitted" }
    """
    try:
        processor = get_batch_processor()
        job_id = processor.submit_job(req.weights)
        
        # Schedule job processing in background
        background_tasks.add_task(_process_mcda_job_async, job_id, req.weights)
        
        logger.info(f"MCDA job {job_id} submitted to queue")
        return {
            "status": "submitted",
            "job_id": job_id,
            "message": BatchJobConstants.MSG_SUBMITTED_FORMAT.format(job_id=job_id)
        }
    except Exception as e:
        logger.error(f"Failed to submit job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/mcda/jobs/{job_id}",
    summary="Get MCDA Job Status",
    tags=["Batch Jobs"],
    responses={200: {"description": "Job status found"}, 404: {"description": "Job not found"}}
)
async def get_job_status(job_id: str):
    """Get status of submitted MCDA job"""
    processor = get_batch_processor()
    return processor.get_job_status(job_id)


@app.get(
    "/mcda/jobs",
    summary="List MCDA Jobs",
    tags=["Batch Jobs"],
    responses={200: {"description": "List of jobs"}}
)
async def list_mcda_jobs(status: Optional[str] = None):
    """List all MCDA batch jobs with optional status filter"""
    processor = get_batch_processor()
    jobs = processor.list_jobs(status=status)
    return {"jobs": jobs, "count": len(jobs)}


@app.get(
    "/mcda/stats",
    summary="Get Batch Processing Statistics",
    tags=["Batch Jobs"],
    responses={200: {"description": "Queue and processing statistics"}}
)
async def get_batch_stats():
    """Get batch processing statistics"""
    processor = get_batch_processor()
    stats = processor.get_queue_stats()
    return {"statistics": stats}


# ============================================================================
# BACKGROUND JOB PROCESSING FUNCTION
# ============================================================================

def _process_mcda_job_async(job_id: str, weights: Dict[str, float]) -> None:
    """Background task: Process MCDA job asynchronously"""
    processor = get_batch_processor()
    job = processor.jobs.get(job_id)
    
    if not job:
        logger.error(f"Job {job_id} not found")
        return
    
    try:
        job.status = BatchJobConstants.STATUS_PROCESSING
        job.started_at = datetime.now().isoformat()
        start_time = datetime.now()
        
        logger.info(f"Processing MCDA job {job_id}")
        
        # Load rasters
        maps = {}
        for name in AVAILABLE_LAYERS:
            p = DATA_DIR / f"{name}.npy"
            if p.exists():
                maps[name] = np.load(p)
        
        if not maps:
            raise ValueError(f"No raster maps found in {DataPathConstants.DATA_PROCESSED_DIR}/")
        
        # Validate weights
        weight_sum = sum(weights.values())
        if weight_sum == 0:
            raise ValueError("Weight sum is zero")
        
        # Normalize weights
        normalized_weights = {k: v / weight_sum for k, v in weights.items()}
        
        # Normalize rasters
        normed = {}
        for k, arr in maps.items():
            a = np.array(arr, dtype=float)
            valid = np.isfinite(a)
            if not valid.any():
                continue
            
            amin = a[valid].min()
            amax = a[valid].max()
            if amax - amin < TechnicalConstants.FLOAT_COMPARISON_TOLERANCE:
                norm = np.ones_like(a) * TechnicalConstants.RASTER_NORMALIZATION_DEFAULT
            else:
                norm = (a - amin) / (amax - amin)
            normed[k] = np.nan_to_num(norm, nan=TechnicalConstants.RASTER_NAN_VALUE)
        
        if not normed:
            raise ValueError("No valid raster data to process")
        
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
            raise ValueError("Overlay computation failed")
        
        overlay = np.asarray(overlay)
        
        # Save result
        out_path = DATA_DIR / f"mcda_job_{job_id}.npy"
        np.save(out_path, overlay)
        
        # Store result metadata
        job.result_metadata = {
            "shape": overlay.shape,
            "dtype": str(overlay.dtype),
            "min": float(np.nanmin(overlay)),
            "max": float(np.nanmax(overlay)),
            "mean": float(np.nanmean(overlay)),
            "valid_pixels": int((~np.isnan(overlay)).sum()),
            "total_pixels": int(overlay.size),
        }
        
        job.output_path = str(out_path)
        job.processing_time_seconds = (datetime.now() - start_time).total_seconds()
        job.status = BatchJobConstants.STATUS_COMPLETED
        job.completed_at = datetime.now().isoformat()
        
        logger.info(f"✓ Completed MCDA job {job_id} in {job.processing_time_seconds:.2f}s")
        
    except Exception as e:
        job.status = BatchJobConstants.STATUS_FAILED
        job.error_message = str(e)
        job.completed_at = datetime.now().isoformat()
        job.processing_time_seconds = (datetime.now() - datetime.fromisoformat(job.started_at or job.created_at)).total_seconds()
        logger.error(f"✗ Job {job_id} failed: {e}")
