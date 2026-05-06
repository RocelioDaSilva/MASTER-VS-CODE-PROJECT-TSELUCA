"""
Enhanced Google Earth Engine Integration with Batch Processing & Scheduling
Provides async data extraction, batch export, and progress tracking
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
import threading
import time

try:
    import ee
except Exception:
    ee = None

import numpy as np

try:
    from .config_loader import load_config
    from .data_loaders_async import get_progress_tracker
except ImportError:
    from config_loader import load_config
    from data_loaders_async import get_progress_tracker

# Ensure project root on path and load utils.error_handlers (avoid scripts/utils.py shadowing)
import sys as _sys
_geesp_root = Path(__file__).resolve().parent.parent
_root_s = str(_geesp_root)
if _root_s not in _sys.path:
    _sys.path.insert(0, _root_s)
try:
    from utils.error_handlers import retry_on_exception, TimeoutError as GEESPTimeoutError
except (ModuleNotFoundError, AttributeError):
    import importlib.util
    _err_path = _geesp_root / "utils" / "error_handlers.py"
    _spec = importlib.util.spec_from_file_location("utils.error_handlers", _err_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    retry_on_exception = _mod.retry_on_exception
    GEESPTimeoutError = _mod.TimeoutError

logger = logging.getLogger(__name__)


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class ExportTask:
    """Represents a single GEE batch export task"""
    task_id: str
    dataset_name: str  # e.g., 'solar_radiation', 'ndvi', 'elevation'
    aoi_bounds: Tuple[float, float, float, float]  # (west, south, east, north)
    bands: List[str]
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD
    output_filename: str
    status: str = "pending"  # pending, processing, completed, failed
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    gee_task_id: Optional[str] = None
    scale: int = 30  # Resolution in meters
    crs: str = "EPSG:32733"  # Angola projection
    retry_count: int = 0
    max_retries: int = 3
    output_path: Optional[str] = None
    checksums: Dict[str, str] = field(default_factory=dict)  # For manifest validation

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        # Filter out non-serializable fields
        data['checksums'] = str(self.checksums)
        return data
    
    def can_retry(self) -> bool:
        """Check if task can be retried"""
        return self.retry_count < self.max_retries and self.status == "failed"


@dataclass
class ExportBatch:
    """Represents a batch of export tasks"""
    batch_id: str
    tasks: List[ExportTask] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "pending"  # pending, processing, completed, partial, failed

    def add_task(self, task: ExportTask) -> None:
        """Add task to batch"""
        self.tasks.append(task)

    def get_status_summary(self) -> Dict:
        """Get summary of batch status"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.status == "completed")
        failed = sum(1 for t in self.tasks if t.status == "failed")
        processing = sum(1 for t in self.tasks if t.status == "processing")

        return {
            "total_tasks": total,
            "completed": completed,
            "failed": failed,
            "processing": processing,
            "pending": total - completed - failed - processing,
            "completion_percentage": (completed / total * 100) if total > 0 else 0,
        }


# ============================================================================
# ENHANCED GEE EXTRACTOR WITH BATCH/ASYNC
# ============================================================================

class EnhancedGEEExtractor:
    """
    Enhanced Google Earth Engine extractor with:
    - Batch export scheduling
    - Progress tracking
    - Robust error handling
    - Async integration
    """

    def __init__(self, project_id: Optional[str] = None):
        """Initialize GEE with error handling"""
        self.project_id = project_id
        self.config = load_config()
        self.progress_tracker = get_progress_tracker()
        self.batches: Dict[str, ExportBatch] = {}
        self.export_dir = Path("data/gee_exports")
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.export_manifest = self.export_dir / "export_manifest.json"

        # Load existing batches on startup
        self._load_manifest()

        # Try to initialize Earth Engine
        self._initialize_gee()

    def _initialize_gee(self) -> bool:
        """Initialize GEE with error handling"""
        if ee is None:
            logger.warning("⚠️ Earth Engine SDK not available (test environment)")
            return False

        try:
            ee.Initialize()
            logger.info("✓ Google Earth Engine initialized")
            return True
        except Exception as e:
            logger.error(f"✗ GEE initialization failed: {e}")
            return False

    def _load_manifest(self) -> None:
        """Load existing export batches from manifest"""
        if not self.export_manifest.exists():
            return

        try:
            with open(self.export_manifest, "r") as f:
                data = json.load(f)
                for batch_id, batch_data in data.items():
                    batch = ExportBatch(batch_id=batch_id)
                    for task_data in batch_data.get("tasks", []):
                        task = ExportTask(**task_data)
                        batch.add_task(task)
                    self.batches[batch_id] = batch
            logger.info(f"✓ Loaded {len(self.batches)} export batches from manifest")
        except Exception as e:
            logger.warning(f"⚠️ Could not load manifest: {e}")

    def _save_manifest(self) -> None:
        """Save export batches to manifest"""
        try:
            manifest_data = {}
            for batch_id, batch in self.batches.items():
                manifest_data[batch_id] = {
                    "batch_id": batch.batch_id,
                    "created_at": batch.created_at,
                    "status": batch.status,
                    "tasks": [t.to_dict() for t in batch.tasks],
                }

            with open(self.export_manifest, "w") as f:
                json.dump(manifest_data, f, indent=2)
            logger.debug("✓ Export manifest saved")
        except Exception as e:
            logger.error(f"✗ Could not save manifest: {e}")

    def create_export_batch(self, batch_id: str) -> ExportBatch:
        """Create new export batch"""
        batch = ExportBatch(batch_id=batch_id)
        self.batches[batch_id] = batch
        self._save_manifest()
        logger.info(f"✓ Created batch {batch_id}")
        return batch

    def add_export_task(
        self,
        batch_id: str,
        dataset_name: str,
        aoi_bounds: Tuple[float, float, float, float],
        bands: List[str],
        start_date: str,
        end_date: str,
        output_filename: Optional[str] = None,
    ) -> ExportTask:
        """Add task to batch"""
        if batch_id not in self.batches:
            self.create_export_batch(batch_id)

        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{dataset_name}_{timestamp}.tif"

        task = ExportTask(
            task_id=f"{batch_id}_{len(self.batches[batch_id].tasks)}",
            dataset_name=dataset_name,
            aoi_bounds=aoi_bounds,
            bands=bands,
            start_date=start_date,
            end_date=end_date,
            output_filename=str(self.export_dir / output_filename),
        )

        self.batches[batch_id].add_task(task)
        self._save_manifest()
        logger.info(f"✓ Added task {task.task_id} to batch {batch_id}")
        return task

    def process_batch_async(
        self,
        batch_id: str,
        max_workers: int = 2,
    ) -> Dict:
        """Process batch of exports asynchronously with retry logic"""
        if batch_id not in self.batches:
            return {"status": "failed", "error": f"Batch {batch_id} not found"}

        batch = self.batches[batch_id]
        batch.status = "processing"
        self._save_manifest()

        # Start progress tracking
        self.progress_tracker.start(batch_id, total_steps=len(batch.tasks))

        processed = 0
        failed = 0
        retried = 0

        try:
            for idx, task in enumerate(batch.tasks):
                if task.status not in ("pending", "failed"):
                    continue

                # Skip if max retries exceeded
                if task.status == "failed" and not task.can_retry():
                    logger.warning(f"Skipping {task.task_id}: max retries exceeded")
                    failed += 1
                    continue

                task.status = "processing"
                if task.started_at is None:
                    task.started_at = datetime.now().isoformat()

                try:
                    # Process with retry logic
                    self._export_with_retry(task)
                    
                    # Validate manifest after successful export
                    if self._validate_manifest(task):
                        task.status = "completed"
                        task.completed_at = datetime.now().isoformat()
                        processed += 1
                        logger.info(f"✓ Completed & Validated: {task.dataset_name}")
                    else:
                        raise RuntimeError("Manifest validation failed")

                except Exception as e:
                    task.error_message = str(e)
                    task.retry_count += 1
                    
                    if task.can_retry():
                        task.status = "failed"  # Will be retried
                        retried += 1
                        logger.warning(
                            f"⚠ Export failed (retry {task.retry_count}/{task.max_retries}): "
                            f"{task.dataset_name} - {e}"
                        )
                    else:
                        task.status = "failed"
                        failed += 1
                        logger.error(f"✗ Final failure: {task.dataset_name} - {e}")

                # Update progress
                self.progress_tracker.update(batch_id, current_step=idx + 1)

            # Update batch status
            if failed == 0:
                batch.status = "completed"
            elif processed == 0:
                batch.status = "failed"
            else:
                batch.status = "partial"

            self._save_manifest()
            self.progress_tracker.complete(batch_id)

            return {
                "status": batch.status,
                "batch_id": batch_id,
                "summary": batch.get_status_summary(),
                "details": {
                    "processed": processed,
                    "failed": failed,
                    "retried": retried,
                }
            }

        except Exception as e:
            batch.status = "failed"
            self._save_manifest()
            logger.error(f"✗ Batch processing failed: {e}")
            return {"status": "failed", "error": str(e)}

    def get_batch_status(self, batch_id: str) -> Dict:
        """Get status of batch"""
        if batch_id not in self.batches:
            return {"status": "not_found"}

        batch = self.batches[batch_id]
        return {
            "batch_id": batch_id,
            "status": batch.status,
            "created_at": batch.created_at,
            "summary": batch.get_status_summary(),
            "tasks": [
                {
                    "task_id": t.task_id,
                    "dataset": t.dataset_name,
                    "status": t.status,
                    "error": t.error_message,
                }
                for t in batch.tasks
            ],
        }

    def list_batches(self) -> List[Dict]:
        """List all batches with status"""
        return [
            {
                "batch_id": batch_id,
                "status": batch.status,
                "task_count": len(batch.tasks),
                "summary": batch.get_status_summary(),
            }
            for batch_id, batch in self.batches.items()
        ]

    def cleanup_old_batches(self, days: int = 7) -> int:
        """Remove batches older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_iso = cutoff_date.isoformat()

        removed = 0
        batch_ids_to_remove = []

        for batch_id, batch in self.batches.items():
            if batch.created_at < cutoff_iso and batch.status == "completed":
                batch_ids_to_remove.append(batch_id)
                removed += 1

        for batch_id in batch_ids_to_remove:
            del self.batches[batch_id]

        if removed > 0:
            self._save_manifest()
            logger.info(f"✓ Cleaned up {removed} old batches")

        return removed

    def _export_to_geotiff(self, task: ExportTask) -> str:
        """Export GEE image to GeoTIFF (placeholder for actual GEE export)"""
        if ee is None:
            # Simulation for testing
            logger.debug(f"[TEST MODE] Would export {task.dataset_name} to {task.output_filename}")
            return task.output_filename

        try:
            # Real GEE export logic would go here
            logger.info(f"Exporting {task.dataset_name} to {task.output_filename}")
            return task.output_filename
        except Exception as e:
            raise RuntimeError(f"Export failed: {e}")

    @retry_on_exception(retries=3, delay_seconds=2.0, backoff=2.0)
    def _export_with_retry(self, task: ExportTask) -> str:
        """Export with exponential backoff retry logic"""
        logger.info(f"📤 Processing export task: {task.dataset_name} (attempt {task.retry_count + 1})")
        
        try:
            output_path = self._export_to_geotiff(task)
            task.output_path = output_path
            logger.info(f"✓ Export successful: {task.dataset_name}")
            return output_path
        except Exception as e:
            logger.error(f"✗ Export failed: {task.dataset_name} - {e}")
            raise

    def _validate_manifest(self, task: ExportTask) -> bool:
        """Validate exported manifest and checksums
        
        Args:
            task: ExportTask with output_path set
            
        Returns:
            True if manifest valid, False otherwise
        """
        if not task.output_path:
            logger.error(f"No output path for task {task.task_id}")
            return False
        
        try:
            # Verify output file exists
            output_file = Path(task.output_path)
            if not output_file.exists():
                logger.error(f"Output file not found: {task.output_path}")
                return False
            
            # Verify file size > 0
            if output_file.stat().st_size == 0:
                logger.error(f"Output file is empty: {task.output_path}")
                return False
            
            # Calculate and store checksum
            import hashlib
            sha256_hash = hashlib.sha256()
            with open(output_file, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            task.checksums["sha256"] = sha256_hash.hexdigest()
            logger.info(f"✓ Manifest validated: {task.dataset_name} (SHA256: {task.checksums['sha256'][:8]}...)")
            return True
            
        except Exception as e:
            logger.error(f"✗ Manifest validation failed: {e}")
            return False

    def rollback_export(self, task: ExportTask) -> bool:
        """Rollback failed export by removing output file
        
        Args:
            task: ExportTask to rollback
            
        Returns:
            True if rollback successful
        """
        if not task.output_path:
            return True
        
        try:
            output_file = Path(task.output_path)
            if output_file.exists():
                output_file.unlink()
                logger.info(f"✓ Rolled back: {task.output_path}")
            return True
        except Exception as e:
            logger.error(f"✗ Rollback failed: {e}")
            return False


# ============================================================================
# SINGLETON & CONVENIENCE FUNCTIONS
# ============================================================================

_extractor_instance: Optional[EnhancedGEEExtractor] = None
_extractor_lock = threading.Lock()


def get_gee_extractor(project_id: Optional[str] = None) -> EnhancedGEEExtractor:
    """Get or create singleton GEE extractor instance"""
    global _extractor_instance

    if _extractor_instance is None:
        with _extractor_lock:
            if _extractor_instance is None:
                _extractor_instance = EnhancedGEEExtractor(project_id=project_id)

    return _extractor_instance


def create_batch(batch_id: str) -> ExportBatch:
    """Convenience function to create batch"""
    return get_gee_extractor().create_export_batch(batch_id)


def add_task(
    batch_id: str,
    dataset_name: str,
    aoi_bounds: Tuple[float, float, float, float],
    bands: List[str],
    start_date: str,
    end_date: str,
    output_filename: Optional[str] = None,
) -> ExportTask:
    """Convenience function to add task to batch"""
    return get_gee_extractor().add_export_task(
        batch_id, dataset_name, aoi_bounds, bands, start_date, end_date, output_filename
    )


def process_batch(batch_id: str) -> Dict:
    """Convenience function to process batch"""
    return get_gee_extractor().process_batch_async(batch_id)


def get_batch_status(batch_id: str) -> Dict:
    """Convenience function to check batch status"""
    return get_gee_extractor().get_batch_status(batch_id)


if __name__ == "__main__":
    # Example usage
    extractor = get_gee_extractor()

    # Create batch
    batch = create_batch("angola_solar_2024")

    # Add multiple export tasks
    aoi = (14.0, -18.5, 15.5, -17.0)  # Huíla region

    add_task(
        "angola_solar_2024",
        "solar_radiation",
        aoi,
        ["ALLSKY_SFC_SW_DWN"],
        "2023-01-01",
        "2023-12-31",
        "solar_radiation_2023.tif",
    )

    add_task(
        "angola_solar_2024",
        "ndvi",
        aoi,
        ["NDVI"],
        "2023-06-01",
        "2023-08-31",
        "ndvi_2023_summer.tif",
    )

    add_task(
        "angola_solar_2024",
        "elevation",
        aoi,
        ["elevation"],
        "2022-01-01",
        "2022-01-01",
        "elevation_srtm.tif",
    )

    # Process batch
    print("Processing batch...")
    result = process_batch("angola_solar_2024")
    print(f"Batch status: {result['status']}")
    print(f"Summary: {result.get('summary', {})}")

    # Check status
    print("\nBatch details:")
    status = get_batch_status("angola_solar_2024")
    print(json.dumps(status, indent=2))
