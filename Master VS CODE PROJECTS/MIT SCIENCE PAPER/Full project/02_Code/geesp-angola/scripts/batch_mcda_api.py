"""
Batch MCDA API Endpoint
Provides asynchronous batch processing of MCDA analysis with job queue and status tracking
"""

import uuid
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
from pathlib import Path
import threading

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

try:
    # Package-relative imports when used as part of the geesp-angola package
    from .config_loader import load_config
    from .data_loaders_async import get_async_loader
    from .mcda_analysis import MCDAnalyzer
except ImportError:
    # Fallback for running as a standalone script
    from config_loader import load_config
    from data_loaders_async import get_async_loader
    from mcda_analysis import MCDAnalyzer

from utils.error_handlers import ValidationError, APIError, TimeoutError as GEESPTimeoutError

logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

class MCDAInputs(BaseModel):
    """Input parameters for MCDA analysis"""
    solar_filename: str
    population_filename: str
    distance_filename: str
    slope_filename: str
    ndvi_filename: str
    weights: Optional[Dict[str, float]] = None
    output_filename: Optional[str] = None


@dataclass
class MCDAJob:
    """Represents a single MCDA batch job"""
    job_id: str
    inputs: MCDAInputs
    status: str = "pending"  # pending, processing, completed, failed
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
    
    def __init__(self, max_workers: int = 4):
        """Initialize batch processor
        
        Args:
            max_workers: Maximum concurrent jobs
        """
        self.max_workers = max_workers
        self.jobs: Dict[str, MCDAJob] = {}
        self.job_queue: List[str] = []
        self.lock = threading.Lock()
        self.async_loader = get_async_loader()
        self.analyzer = MCDAnalyzer()
        self.config = load_config()
        
        logger.info(f"MCDABatchProcessor initialized with {max_workers} workers")

    def submit_job(self, inputs: MCDAInputs) -> str:
        """Submit new MCDA job to queue
        
        Args:
            inputs: MCDA analysis parameters
            
        Returns:
            Job ID
        """
        job_id = str(uuid.uuid4())[:8]
        
        # Create output filename if not provided
        if not inputs.output_filename:
            inputs.output_filename = f"mcda_result_{job_id}.npy"
        
        job = MCDAJob(job_id=job_id, inputs=inputs)
        
        with self.lock:
            self.jobs[job_id] = job
            self.job_queue.append(job_id)
        
        logger.info(f"✓ Submitted MCDA job {job_id}")
        return job_id

    def get_job_status(self, job_id: str) -> Dict:
        """Get status of job
        
        Args:
            job_id: Job ID to query
            
        Returns:
            Job status dictionary
            
        Raises:
            HTTPException: If job not found
        """
        if job_id not in self.jobs:
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
        
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

    def get_job_result(self, job_id: str) -> Optional[Dict]:
        """Get result of completed job
        
        Args:
            job_id: Job ID
            
        Returns:
            Result metadata dictionary or None
            
        Raises:
            HTTPException: If job not found or not completed
        """
        if job_id not in self.jobs:
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        
        if job.status != "completed":
            raise HTTPException(
                status_code=400,
                detail=f"Job {job_id} is {job.status}, not completed"
            )
        
        return job.result_metadata

    def list_jobs(self, status: Optional[str] = None) -> List[Dict]:
        """List all jobs with optional status filter
        
        Args:
            status: Filter by status (optional)
            
        Returns:
            List of job summaries
        """
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
        """Get queue statistics
        
        Returns:
            Queue statistics dictionary
        """
        with self.lock:
            pending = sum(1 for j in self.jobs.values() if j.status == "pending")
            processing = sum(1 for j in self.jobs.values() if j.status == "processing")
            completed = sum(1 for j in self.jobs.values() if j.status == "completed")
            failed = sum(1 for j in self.jobs.values() if j.status == "failed")
        
        return {
            "total_jobs": len(self.jobs),
            "pending": pending,
            "processing": processing,
            "completed": completed,
            "failed": failed,
            "queue_length": len(self.job_queue),
        }

    def process_job(self, job_id: str) -> None:
        """Process a single job (runs in background)
        
        Args:
            job_id: Job ID to process
        """
        job = self.jobs.get(job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return
        
        try:
            job.status = "processing"
            job.started_at = datetime.now().isoformat()
            
            logger.info(f"Processing MCDA job {job_id}")
            start_time = datetime.now()
            
            # Load input maps asynchronously
            try:
                solar = self.async_loader.load_map_async(job.inputs.solar_filename)
                population = self.async_loader.load_map_async(job.inputs.population_filename)
                distance = self.async_loader.load_map_async(job.inputs.distance_filename)
                slope = self.async_loader.load_map_async(job.inputs.slope_filename)
                ndvi = self.async_loader.load_map_async(job.inputs.ndvi_filename)
                
                if any(x is None for x in [solar, population, distance, slope, ndvi]):
                    raise ValueError("Failed to load one or more input maps")
                
                logger.info(f"✓ Loaded all input maps for job {job_id}")
                
            except Exception as e:
                raise ValidationError(f"Failed to load input maps: {e}")
            
            # Compute MCDA analysis
            try:
                aptitude = self.analyzer.calculate_weighted_overlay(
                    solar=solar,
                    population=population,
                    distance=distance,
                    slope=slope,
                    ndvi=ndvi,
                    weights=job.inputs.weights
                )
                
                logger.info(f"✓ Computed aptitude map for job {job_id}")
                
            except Exception as e:
                raise APIError(f"MCDA computation failed: {e}", status_code=500)
            
            # Save result
            try:
                output_path = Path("output") / job.inputs.output_filename
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                import numpy as np
                np.save(output_path, aptitude)
                
                job.output_path = str(output_path)
                logger.info(f"✓ Saved result to {output_path}")
                
            except Exception as e:
                raise APIError(f"Failed to save result: {e}", status_code=500)
            
            # Compute metrics
            job.result_metadata = {
                "shape": aptitude.shape,
                "dtype": str(aptitude.dtype),
                "min": float(aptitude.min()),
                "max": float(aptitude.max()),
                "mean": float(aptitude.mean()),
                "valid_pixels": int((~np.isnan(aptitude)).sum()),
                "total_pixels": int(aptitude.size),
            }
            
            # Calculate processing time
            job.processing_time_seconds = (datetime.now() - start_time).total_seconds()
            job.status = "completed"
            job.completed_at = datetime.now().isoformat()
            
            logger.info(
                f"✓ Completed MCDA job {job_id} in {job.processing_time_seconds:.2f}s"
            )
            
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.now().isoformat()
            job.processing_time_seconds = (datetime.now() - datetime.fromisoformat(job.started_at)).total_seconds()
            logger.error(f"✗ Job {job_id} failed: {e}")

    def cleanup_old_jobs(self, hours: int = 24) -> int:
        """Remove completed jobs older than specified hours
        
        Args:
            hours: Age threshold in hours
            
        Returns:
            Number of jobs removed
        """
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(hours=hours)
        cutoff_iso = cutoff_date.isoformat()
        
        removed = 0
        job_ids_to_remove = []
        
        with self.lock:
            for job_id, job in self.jobs.items():
                if job.completed_at and job.completed_at < cutoff_iso and job.status == "completed":
                    job_ids_to_remove.append(job_id)
                    removed += 1
            
            for job_id in job_ids_to_remove:
                del self.jobs[job_id]
        
        if removed > 0:
            logger.info(f"✓ Cleaned up {removed} old jobs")
        
        return removed


# ============================================================================
# GLOBAL BATCH PROCESSOR INSTANCE
# ============================================================================

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


# ============================================================================
# FASTAPI ROUTER
# ============================================================================

router = APIRouter(prefix="/mcda/batch", tags=["batch_mcda"])


@router.post("/jobs", response_model=Dict)
async def submit_mcda_job(
    inputs: MCDAInputs,
    background_tasks: BackgroundTasks
) -> Dict:
    """Submit new MCDA batch job
    
    Args:
        inputs: MCDA analysis parameters
        background_tasks: FastAPI background task queue
        
    Returns:
        Job submission response with job_id
    """
    try:
        processor = get_batch_processor()
        job_id = processor.submit_job(inputs)
        
        # Schedule job processing in background
        background_tasks.add_task(processor.process_job, job_id)
        
        return {
            "status": "submitted",
            "job_id": job_id,
            "message": f"MCDA job {job_id} submitted for processing"
        }
    except Exception as e:
        logger.error(f"Failed to submit job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str) -> Dict:
    """Get status of MCDA job
    
    Args:
        job_id: Job ID to query
        
    Returns:
        Job status dictionary
    """
    processor = get_batch_processor()
    return processor.get_job_status(job_id)


@router.get("/jobs/{job_id}/result")
async def get_job_result(job_id: str) -> Dict:
    """Get result of completed MCDA job
    
    Args:
        job_id: Job ID
        
    Returns:
        Job result metadata
    """
    processor = get_batch_processor()
    result = processor.get_job_result(job_id)
    return {"job_id": job_id, "result": result}


@router.get("/jobs")
async def list_mcda_jobs(status: Optional[str] = None) -> Dict:
    """List all MCDA batch jobs
    
    Args:
        status: Optional filter by status
        
    Returns:
        List of jobs with metadata
    """
    processor = get_batch_processor()
    jobs = processor.list_jobs(status=status)
    return {"jobs": jobs, "count": len(jobs)}


@router.get("/stats")
async def get_batch_stats() -> Dict:
    """Get batch processing statistics
    
    Returns:
        Queue and processing statistics
    """
    processor = get_batch_processor()
    stats = processor.get_queue_stats()
    return {"statistics": stats}


if __name__ == "__main__":
    # Example usage
    processor = get_batch_processor()
    
    # Create sample inputs
    sample_inputs = MCDAInputs(
        solar_filename="mapa_irradiacao.npy",
        population_filename="mapa_populacao.npy",
        distance_filename="mapa_distancia_rede.npy",
        slope_filename="mapa_declividade.npy",
        ndvi_filename="mapa_ndvi.npy",
        weights={
            "solar_irradiance": 0.25,
            "population_density": 0.25,
            "grid_distance": 0.20,
            "slope": 0.15,
            "vegetation_ndvi": 0.15
        }
    )
    
    # Submit job
    job_id = processor.submit_job(sample_inputs)
    print(f"Submitted job: {job_id}")
    
    # Get stats
    stats = processor.get_queue_stats()
    print(f"Queue stats: {json.dumps(stats, indent=2)}")
