"""
Kubernetes Custom Metrics for GEESP-Angola
Implements Prometheus metrics and custom scaling indicators for HPA
"""

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import deque
from threading import Lock

try:
    from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry, generate_latest
except ImportError:
    logging.warning("prometheus_client not installed")

logger = logging.getLogger(__name__)


# ============================================================================
# METRICS DEFINITIONS
# ============================================================================

@dataclass
class MetricWindow:
    """Time window for metric collection"""
    window_size_seconds: int = 60
    max_samples: int = 120
    samples: deque = field(default_factory=deque)
    lock: Lock = field(default_factory=Lock)

    def add_sample(self, value: float) -> None:
        """Add sample to window"""
        with self.lock:
            self.samples.append((time.time(), value))
            
            # Keep only samples within window
            cutoff_time = time.time() - self.window_size_seconds
            while self.samples and self.samples[0][0] < cutoff_time:
                self.samples.popleft()

    def get_stats(self) -> Dict[str, float]:
        """Get statistics for window"""
        with self.lock:
            if not self.samples:
                return {"count": 0, "mean": 0, "min": 0, "max": 0}
            
            values = [v for _, v in self.samples]
            return {
                "count": len(values),
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "sum": sum(values),
            }


class GEESPMetricsCollector:
    """Collect and expose metrics for Kubernetes scaling"""

    def __init__(self, registry: Optional["CollectorRegistry"] = None):
        """Initialize metrics collector
        
        Args:
            registry: Prometheus registry (uses default if None)
        """
        try:
            self.registry = registry or CollectorRegistry()
            
            # Define Prometheus metrics
            self.mcda_requests = Counter(
                "geesp_mcda_requests_total",
                "Total MCDA analysis requests",
                ["status"],
                registry=self.registry,
            )
            
            self.mcda_duration = Histogram(
                "geesp_mcda_computation_seconds",
                "MCDA computation duration",
                buckets=[5, 10, 30, 60, 120, 300],
                registry=self.registry,
            )
            
            self.gee_exports = Counter(
                "geesp_gee_exports_total",
                "Total GEE export requests",
                ["dataset", "status"],
                registry=self.registry,
            )
            
            self.queue_length = Gauge(
                "geesp_job_queue_length",
                "Current job queue length",
                registry=self.registry,
            )
            
            self.active_jobs = Gauge(
                "geesp_active_jobs",
                "Currently active jobs",
                registry=self.registry,
            )
            
            self.api_requests = Counter(
                "geesp_api_requests_total",
                "Total API requests",
                ["method", "endpoint", "status"],
                registry=self.registry,
            )
            
            self.api_latency = Histogram(
                "geesp_api_latency_seconds",
                "API endpoint latency",
                ["endpoint"],
                buckets=[0.1, 0.5, 1.0, 2.0, 5.0],
                registry=self.registry,
            )
            
            self.memory_usage = Gauge(
                "geesp_memory_usage_bytes",
                "Process memory usage",
                registry=self.registry,
            )
            
            self.cache_hits = Counter(
                "geesp_cache_hits_total",
                "Cache hits",
                ["cache_type"],
                registry=self.registry,
            )
            
            self.cache_misses = Counter(
                "geesp_cache_misses_total",
                "Cache misses",
                ["cache_type"],
                registry=self.registry,
            )
            
            logger.info("✓ Prometheus metrics initialized")
            self.enabled = True
            
        except Exception as e:
            logger.warning(f"Prometheus not available: {e}")
            self.enabled = False

    # ============================================================================
    # MCDA METRICS
    # ============================================================================

    def record_mcda_request(self, success: bool = True) -> None:
        """Record MCDA request"""
        if not self.enabled:
            return
        
        status = "success" if success else "failure"
        self.mcda_requests.labels(status=status).inc()

    def record_mcda_computation(self, duration_seconds: float) -> None:
        """Record MCDA computation duration"""
        if not self.enabled:
            return
        
        self.mcda_duration.observe(duration_seconds)

    # ============================================================================
    # GEE METRICS
    # ============================================================================

    def record_gee_export(self, dataset: str, success: bool = True) -> None:
        """Record GEE export request"""
        if not self.enabled:
            return
        
        status = "success" if success else "failure"
        self.gee_exports.labels(dataset=dataset, status=status).inc()

    # ============================================================================
    # QUEUE METRICS
    # ============================================================================

    def update_queue_length(self, length: int) -> None:
        """Update job queue length"""
        if not self.enabled:
            return
        
        self.queue_length.set(length)

    def update_active_jobs(self, count: int) -> None:
        """Update active job count"""
        if not self.enabled:
            return
        
        self.active_jobs.set(count)

    # ============================================================================
    # API METRICS
    # ============================================================================

    def record_api_request(self, method: str, endpoint: str, status_code: int) -> None:
        """Record API request"""
        if not self.enabled:
            return
        
        status = "success" if 200 <= status_code < 300 else "error"
        self.api_requests.labels(method=method, endpoint=endpoint, status=status).inc()

    def record_api_latency(self, endpoint: str, duration_seconds: float) -> None:
        """Record API request latency"""
        if not self.enabled:
            return
        
        self.api_latency.labels(endpoint=endpoint).observe(duration_seconds)

    # ============================================================================
    # SYSTEM METRICS
    # ============================================================================

    def update_memory_usage(self, bytes_used: int) -> None:
        """Update memory usage metric"""
        if not self.enabled:
            return
        
        self.memory_usage.set(bytes_used)

    def record_cache_hit(self, cache_type: str) -> None:
        """Record cache hit"""
        if not self.enabled:
            return
        
        self.cache_hits.labels(cache_type=cache_type).inc()

    def record_cache_miss(self, cache_type: str) -> None:
        """Record cache miss"""
        if not self.enabled:
            return
        
        self.cache_misses.labels(cache_type=cache_type).inc()

    # ============================================================================
    # METRICS EXPORT
    # ============================================================================

    def get_metrics(self) -> bytes:
        """Get metrics in Prometheus exposition format"""
        if not self.enabled:
            return b""
        
        return generate_latest(self.registry)


# ============================================================================
# CUSTOM HPA METRICS
# ============================================================================

class HPAScalingMetrics:
    """Custom metrics for Kubernetes HPA scaling decisions"""

    def __init__(self, window_size_seconds: int = 60):
        """Initialize HPA metrics
        
        Args:
            window_size_seconds: Window for averaging metrics
        """
        self.requests_per_second = MetricWindow(window_size_seconds)
        self.analysis_duration = MetricWindow(window_size_seconds)
        self.queue_length_window = MetricWindow(window_size_seconds)
        self.error_rate_window = MetricWindow(window_size_seconds)
        
        logger.info(f"HPAScalingMetrics initialized with {window_size_seconds}s window")

    def add_request(self) -> None:
        """Record incoming request"""
        self.requests_per_second.add_sample(1)

    def add_analysis_duration(self, duration: float) -> None:
        """Record analysis duration"""
        self.analysis_duration.add_sample(duration)

    def add_queue_length(self, length: int) -> None:
        """Record queue length"""
        self.queue_length_window.add_sample(float(length))

    def add_error(self) -> None:
        """Record error occurrence"""
        self.error_rate_window.add_sample(1)

    def get_scaling_metric(self) -> Dict[str, float]:
        """Calculate scaling metric for HPA
        
        Returns:
            Scaling indicator (0-100 scale):
            - <30: Scale down
            - 30-70: Scale stable
            - >70: Scale up
        """
        rps_stats = self.requests_per_second.get_stats()
        duration_stats = self.analysis_duration.get_stats()
        queue_stats = self.queue_length_window.get_stats()
        error_stats = self.error_rate_window.get_stats()

        # Calculate utilization score
        rps = rps_stats.get("mean", 0)
        avg_duration = duration_stats.get("mean", 0)
        queue_length = queue_stats.get("mean", 0)
        error_rate = error_stats.get("mean", 0) if error_stats.get("count", 0) > 0 else 0

        # Weighted scoring (0-100)
        score = 0
        
        # Request rate contribution (max 40%)
        if rps > 0:
            score += min(40, rps * 5)
        
        # Queue length contribution (max 40%)
        if queue_length > 0:
            score += min(40, queue_length * 2)
        
        # Analysis duration contribution (max 20%)
        if avg_duration > 10:  # If avg analysis > 10s
            score += min(20, (avg_duration / 60) * 20)

        # Error rate penalty
        if error_rate > 0:
            score = max(score * (1 - error_rate), 0)

        return {
            "scaling_score": score,
            "requests_per_second": rps,
            "average_analysis_duration": avg_duration,
            "queue_length": queue_length,
            "error_rate": error_rate,
            "should_scale_up": score > 70,
            "should_scale_down": score < 30,
        }

    def get_detailed_metrics(self) -> Dict:
        """Get all scaling metrics details"""
        return {
            "requests_per_second": self.requests_per_second.get_stats(),
            "analysis_duration_seconds": self.analysis_duration.get_stats(),
            "queue_length": self.queue_length_window.get_stats(),
            "error_rate": self.error_rate_window.get_stats(),
            "scaling_decision": self.get_scaling_metric(),
        }


# ============================================================================
# GLOBAL INSTANCES
# ============================================================================

_metrics_collector: Optional[GEESPMetricsCollector] = None
_hpa_metrics: Optional[HPAScalingMetrics] = None


def get_metrics_collector() -> GEESPMetricsCollector:
    """Get or create global metrics collector"""
    global _metrics_collector
    
    if _metrics_collector is None:
        _metrics_collector = GEESPMetricsCollector()
    
    return _metrics_collector


def get_hpa_metrics() -> HPAScalingMetrics:
    """Get or create global HPA metrics"""
    global _hpa_metrics
    
    if _hpa_metrics is None:
        _hpa_metrics = HPAScalingMetrics()
    
    return _hpa_metrics


# ============================================================================
# FASTAPI INTEGRATION
# ============================================================================

from fastapi import APIRouter

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/prometheus")
async def get_prometheus_metrics() -> str:
    """Expose metrics in Prometheus format
    
    Returns:
        Prometheus exposition format metrics
    """
    collector = get_metrics_collector()
    return collector.get_metrics().decode("utf-8")


@router.get("/scaling")
async def get_scaling_metrics() -> Dict:
    """Get custom HPA scaling metrics
    
    Returns:
        HPA scaling decision metrics
    """
    hpa = get_hpa_metrics()
    return hpa.get_detailed_metrics()


# ============================================================================
# EXAMPLE USAGE & TESTING
# ============================================================================

if __name__ == "__main__":
    # Example usage
    metrics = get_metrics_collector()
    hpa = get_hpa_metrics()
    
    # Simulate workload
    import random
    
    print("Simulating workload...")
    
    for i in range(100):
        # Record MCDA requests
        success = random.random() > 0.1
        metrics.record_mcda_request(success=success)
        
        if success:
            duration = random.uniform(5, 120)
            metrics.record_mcda_computation(duration)
            hpa.add_analysis_duration(duration)
        
        # Record API requests
        endpoint = random.choice(["/analyze", "/batch", "/status"])
        status = random.choice([200, 200, 200, 400, 500])
        metrics.record_api_request("POST", endpoint, status)
        metrics.record_api_latency(endpoint, random.uniform(0.1, 2.0))
        
        # Update queue
        queue_length = random.randint(0, 50)
        metrics.update_queue_length(queue_length)
        hpa.add_queue_length(queue_length)
        
        # Record requests for HPA
        hpa.add_request()
        
        if not success:
            hpa.add_error()
        
        time.sleep(0.1)
    
    # Print scaling metrics
    scaling = hpa.get_scaling_metric()
    print(f"\nScaling Metrics:")
    print(f"  Score: {scaling['scaling_score']:.1f}/100")
    print(f"  RPS: {scaling['requests_per_second']:.2f}")
    print(f"  Avg Duration: {scaling['average_analysis_duration']:.2f}s")
    print(f"  Queue: {scaling['queue_length']:.1f}")
    print(f"  Scale Up: {scaling['should_scale_up']}")
    print(f"  Scale Down: {scaling['should_scale_down']}")
    
    # Print Prometheus metrics sample
    print(f"\nPrometheus Metrics (first 500 chars):")
    print(metrics.get_metrics()[:500].decode("utf-8"))
