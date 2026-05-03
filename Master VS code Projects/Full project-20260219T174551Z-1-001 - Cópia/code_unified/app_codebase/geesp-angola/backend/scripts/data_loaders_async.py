"""
Async Data Loaders for GEESP-Angola Dashboard
Non-blocking data loading using ThreadPoolExecutor for improved UI responsiveness
"""

import numpy as np
from pathlib import Path
from typing import Optional, Dict, Callable, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import atexit
import time

from utils.logging import setup_logging
from utils.constants import TechnicalConstants, DataPathConstants

logger = setup_logging(__name__)

# Global thread pool for data operations
_executor = ThreadPoolExecutor(max_workers=TechnicalConstants.MAX_WORKERS_PARALLEL)
atexit.register(_executor.shutdown, wait=False)  # prevent thread leak on process exit


class AsyncDataLoader:
    """Non-blocking data loader for raster maps and computations"""
    
    def __init__(self, data_dir: str = None, max_workers: int = None):
        """
        Initialize async data loader
        
        Args:
            data_dir: Path to data directory (default from DataPathConstants)
            max_workers: Maximum number of concurrent worker threads (default from TechnicalConstants)
        """
        if data_dir is None:
            data_dir = DataPathConstants.DATA_PROCESSED_DIR
        if max_workers is None:
            max_workers = TechnicalConstants.MAX_WORKERS_PARALLEL
            
        self.data_dir = Path(data_dir)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._cache: Dict[str, Any] = {}
        self._loading: Dict[str, Any] = {}
        logger.info(f"AsyncDataLoader initialized with {max_workers} workers")
    
    def load_map_async(self, filename: str) -> Optional[np.ndarray]:
        """
        Load raster map asynchronously with caching
        
        Args:
            filename: Raster filename (e.g., "mapa_irradiacao.npy")
            
        Returns:
            Numpy array if successful, None otherwise
        """
        # Check cache first
        if filename in self._cache:
            logger.debug(f"Cache hit: {filename}")
            return self._cache[filename]
        
        # Check if already loading
        if filename in self._loading:
            logger.debug(f"Loading in progress: {filename}")
            return self._loading[filename].result(timeout=TechnicalConstants.DATA_LOADING_TIMEOUT_SECONDS)
        
        # Submit to executor
        logger.debug(f"Loading asynchronously: {filename}")
        future = self.executor.submit(self._load_map_sync, filename)
        self._loading[filename] = future
        
        try:
            result = future.result(timeout=TechnicalConstants.DATA_LOADING_TIMEOUT_SECONDS)
            self._cache[filename] = result
            del self._loading[filename]
            return result
        except TimeoutError:
            logger.error(f"Timeout loading {filename} after {TechnicalConstants.DATA_LOADING_TIMEOUT_SECONDS}s")
            if filename in self._loading:
                del self._loading[filename]
            return None
        except FileNotFoundError:
            logger.warning(f"File not found: {filename}")
            if filename in self._loading:
                del self._loading[filename]
            return None
        except Exception as e:
            logger.error(f"Unexpected error loading {filename}: {e}")
            if filename in self._loading:
                del self._loading[filename]
            return None
    
    def load_maps_parallel(self, filenames: list) -> Dict[str, Optional[np.ndarray]]:
        """
        Load multiple maps in parallel
        
        Args:
            filenames: List of map filenames
            
        Returns:
            Dictionary mapping filename to numpy array (or None if failed)
        """
        logger.info(f"Loading {len(filenames)} maps in parallel")
        results = {}
        futures = {}
        
        # Submit all loads
        for filename in filenames:
            if filename in self._cache:
                results[filename] = self._cache[filename]
            else:
                futures[filename] = self.executor.submit(self._load_map_sync, filename)
        
        # Wait for completion
        for filename, future in futures.items():
            try:
                result = future.result(timeout=TechnicalConstants.DATA_LOADING_TIMEOUT_SECONDS)
                results[filename] = result
                self._cache[filename] = result
            except Exception as e:
                logger.error(f"Failed to load {filename}: {e}")
                results[filename] = None
        
        logger.info(f"Parallel load complete: {len([r for r in results.values() if r is not None])}/{len(filenames)} successful")
        return results
    
    def _load_map_sync(self, filename: str) -> Optional[np.ndarray]:
        """Synchronous map loading (runs in thread pool)"""
        try:
            map_path = self.data_dir / filename
            if map_path.exists():
                logger.debug(f"Loading from disk: {map_path}")
                return np.load(str(map_path))
            else:
                logger.warning(f"File not found: {map_path}")
                return None
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return None
    
    def clear_cache(self, filename: Optional[str] = None) -> None:
        """
        Clear cache for specific file or all files
        
        Args:
            filename: Specific file to clear (None = clear all)
        """
        if filename is None:
            self._cache.clear()
            logger.info("Cache cleared (all)")
        else:
            if filename in self._cache:
                del self._cache[filename]
                logger.info(f"Cache cleared: {filename}")
    
    def get_cache_size(self) -> Dict[str, Any]:
        """Get cache statistics"""
        size_mb = sum(
            arr.nbytes / (1024 * 1024)
            for arr in self._cache.values()
            if isinstance(arr, np.ndarray)
        )
        return {
            "files_cached": len(self._cache),
            "size_mb": size_mb,
            "max_size_mb": TechnicalConstants.ASYNC_CACHE_MAX_SIZE_MB
        }
    
    def compute_mcda_async(self, solar: np.ndarray, population: np.ndarray, distance: np.ndarray,
                           slope: np.ndarray, ndvi: np.ndarray, weights: Optional[Dict] = None,
                           timeout: float = None) -> Optional[np.ndarray]:
        """Compute MCDA analysis asynchronously
        
        Args:
            solar, population, distance, slope, ndvi: Input raster arrays
            weights: MCDA weights dictionary
            timeout: Computation timeout in seconds (default from TechnicalConstants)
            
        Returns:
            Aptitude map array or None if failed
        """
        if timeout is None:
            timeout = TechnicalConstants.COMPUTATION_TIMEOUT_SECONDS
            
        logger.info("Submitting MCDA computation to thread pool")
        future = self.executor.submit(
            self._compute_mcda_sync, solar, population, distance, slope, ndvi, weights
        )
        
        try:
            result = future.result(timeout=timeout)
            logger.info(f"MCDA computation completed")
            return result
        except TimeoutError:
            logger.error(f"MCDA computation timed out after {timeout:.1f}s")
            return None
        except Exception as e:
            logger.error(f"MCDA computation failed: {e}")
            return None
    
    def _compute_mcda_sync(self, solar, population, distance, slope, ndvi, weights):
        """Synchronous MCDA computation (runs in thread pool)"""
        try:
            from mcda_analysis import MCDAnalyzer
            from utils.constants import MCDAConstants

            default_weights = MCDAConstants.DEFAULT_WEIGHTS if weights is None else weights

            analyzer = MCDAnalyzer(weights_dict=default_weights)

            # Normalize each input raster and store in analyzer
            raster_map = {
                "solar": solar,
                "population": population,
                "distance": distance,
                "slope": slope,
                "ndvi": ndvi,
            }
            for name, arr in raster_map.items():
                if arr is not None:
                    analyzer.normalize_raster(arr, name=name)

            # Compute weighted overlay
            aptitude = analyzer.weighted_overlay()
            return aptitude
        except Exception as e:
            logger.error(f"MCDA sync computation error: {e}")
            raise
    
    def shutdown(self) -> None:
        """Shutdown thread pool"""
        self.executor.shutdown(wait=True)
        logger.info("AsyncDataLoader shutdown complete")


class ComputationProgressTracker:
    """Track progress of long-running computations"""
    
    def __init__(self):
        """Initialize progress tracker"""
        self.progress: Dict[str, Dict[str, Any]] = {}
    
    def start(self, task_id: str, total_steps: int) -> None:
        """Start tracking a computation"""
        self.progress[task_id] = {
            "total": total_steps,
            "current": 0,
            "start_time": time.time(),
            "status": "running"
        }
        logger.info(f"Started tracking: {task_id}")
    
    def update(self, task_id: str, current_step: int) -> None:
        """Update progress"""
        if task_id in self.progress:
            self.progress[task_id]["current"] = current_step
    
    def complete(self, task_id: str) -> Dict[str, Any]:
        """Mark computation as complete"""
        if task_id in self.progress:
            self.progress[task_id]["status"] = "complete"
            self.progress[task_id]["duration"] = time.time() - self.progress[task_id]["start_time"]
            logger.info(f"Completed: {task_id} ({self.progress[task_id]['duration']:.2f}s)")
            return self.progress[task_id]
        return {}
    
    def get_progress(self, task_id: str) -> Dict[str, Any]:
        """Get current progress"""
        return self.progress.get(task_id, {})
    
    def get_percentage(self, task_id: str) -> float:
        """Get progress percentage"""
        if task_id in self.progress:
            p = self.progress[task_id]
            if p["total"] > 0:
                return (p["current"] / p["total"]) * 100
        return 0.0


# Global instances
_data_loader = None
_progress_tracker = None


def get_async_loader() -> AsyncDataLoader:
    """Get or create global async data loader"""
    global _data_loader
    if _data_loader is None:
        _data_loader = AsyncDataLoader()
    return _data_loader


def get_progress_tracker() -> ComputationProgressTracker:
    """Get or create global progress tracker"""
    global _progress_tracker
    if _progress_tracker is None:
        _progress_tracker = ComputationProgressTracker()
    return _progress_tracker


# Convenience functions for Streamlit integration
def async_load_map(filename: str) -> Optional[np.ndarray]:
    """Load map with automatic caching"""
    loader = get_async_loader()
    return loader.load_map_async(filename)


def async_load_maps(filenames: list) -> Dict[str, Optional[np.ndarray]]:
    """Load multiple maps in parallel"""
    loader = get_async_loader()
    return loader.load_maps_parallel(filenames)


def async_compute_mcda(solar: np.ndarray, population: np.ndarray, distance: np.ndarray,
                       slope: np.ndarray, ndvi: np.ndarray, weights: Optional[Dict] = None,
                       timeout: float = None) -> Optional[np.ndarray]:
    """Compute MCDA analysis asynchronously"""
    loader = get_async_loader()
    if timeout is None:
        timeout = TechnicalConstants.COMPUTATION_TIMEOUT_SECONDS
    return loader.compute_mcda_async(solar, population, distance, slope, ndvi, weights, timeout)


def get_computation_status(task_id: str) -> Optional[Dict[str, Any]]:
    """Get status of a running computation"""
    tracker = get_progress_tracker()
    return tracker.get_progress(task_id)


if __name__ == "__main__":
    # Test async loader
    loader = AsyncDataLoader()
    
    # Test single load
    result = loader.load_map_async("mapa_irradiacao.npy")
    print(f"Single load: {result.shape if result is not None else 'None'}")
    
    # Test parallel load
    results = loader.load_maps_parallel([
        "mapa_irradiacao.npy",
        "mapa_populacao.npy",
        "mapa_declividade.npy"
    ])
    
    print(f"Parallel load: {len([r for r in results.values() if r is not None])} successful")
    print(f"Cache stats: {loader.get_cache_size()}")
    
    loader.shutdown()
