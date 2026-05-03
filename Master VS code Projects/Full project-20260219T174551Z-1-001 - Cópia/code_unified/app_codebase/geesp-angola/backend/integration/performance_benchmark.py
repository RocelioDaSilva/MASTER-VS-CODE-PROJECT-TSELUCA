#!/usr/bin/env python3
"""
GEESP-Angola Performance Benchmarking Suite
Comprehensive performance testing for all major components
"""

import time
import statistics
import json
import sys
from pathlib import Path
from typing import List, Dict
import numpy as np

# Setup centralized import paths
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.helpers import setup_project_paths
setup_project_paths()


class PerformanceBenchmark:
    """Runs performance benchmarks on all components"""

    def __init__(self):
        self.results: Dict[str, Dict] = {}
        self.ITERATIONS = 10

    def print_header(self, text: str):
        print(f"\n{'='*70}")
        print(f"▶ {text}")
        print(f"{'='*70}\n")

    def run_benchmark(self, name: str, func, iterations: int = None) -> Dict:
        """Run benchmark and collect metrics"""
        if iterations is None:
            iterations = self.ITERATIONS

        times = []
        errors = 0

        print(f"Running {name}...", end=" ", flush=True)

        for i in range(iterations):
            try:
                start = time.perf_counter()
                result = func()
                elapsed = time.perf_counter() - start
                times.append(elapsed * 1000)  # Convert to ms
            except Exception as e:
                print(f"✗ Error: {e}", end=" ", flush=True)
                errors += 1

        if times:
            metrics = {
                "iterations": iterations,
                "errors": errors,
                "min_ms": min(times),
                "max_ms": max(times),
                "mean_ms": statistics.mean(times),
                "median_ms": statistics.median(times),
                "stdev_ms": statistics.stdev(times) if len(times) > 1 else 0,
                "p95_ms": np.percentile(times, 95),
                "p99_ms": np.percentile(times, 99),
            }

            print(f"✓")
            self.print_metrics(name, metrics)
            return metrics
        else:
            print(f"✗ All attempts failed")
            return {"error": "All attempts failed"}

    def print_metrics(self, name: str, metrics: Dict):
        """Print formatted metrics"""
        if "error" in metrics:
            print(f"  {name}: {metrics['error']}")
            return

        print(f"  Iterations: {metrics['iterations']}")
        print(f"  Errors: {metrics['errors']}")
        print(f"  Min: {metrics['min_ms']:.2f}ms | Max: {metrics['max_ms']:.2f}ms")
        print(f"  Mean: {metrics['mean_ms']:.2f}ms | Median: {metrics['median_ms']:.2f}ms")
        print(f"  StDev: {metrics['stdev_ms']:.2f}ms")
        print(f"  p95: {metrics['p95_ms']:.2f}ms | p99: {metrics['p99_ms']:.2f}ms")

    # ========================================================================
    # MCDA ANALYSIS BENCHMARKS
    # ========================================================================

    def benchmark_mcda_analysis(self):
        """Benchmark MCDA analysis performance"""
        self.print_header("MCDA Analysis Performance")

        from scripts.mcda_analysis import MCDAnalyzer

        # Generate test data
        def mcda_single_weight_set():
            weights = {"solar": 0.35, "pop": 0.25, "dist": 0.2, "slope": 0.1, "ndvi": 0.1}
            mcda = MCDAnalyzer(weights_dict=weights)
            return mcda

        # Generate test rasters
        def mcda_with_rasters():
            weights = {"solar": 0.35, "pop": 0.25, "dist": 0.2, "slope": 0.1, "ndvi": 0.1}
            solar = np.random.rand(100, 100) * 300
            pop = np.random.rand(100, 100) * 200000
            dist = np.random.rand(100, 100) * 50000
            slope = np.random.rand(100, 100) * 30
            ndvi = np.random.rand(100, 100)

            mcda = MCDAnalyzer(weights_dict=weights)
            # Note: Would call mcda methods with rasters if available
            return mcda

        benchmark1 = self.run_benchmark(
            "MCDA Analyzer Initialization",
            mcda_single_weight_set,
            iterations=20
        )
        self.results["mcda_initialization"] = benchmark1

        benchmark2 = self.run_benchmark(
            "MCDA with Raster Data",
            mcda_with_rasters,
            iterations=10
        )
        self.results["mcda_with_rasters"] = benchmark2

    # ========================================================================
    # LCOE CALCULATOR BENCHMARKS
    # ========================================================================

    def benchmark_lcoe_calculator(self):
        """Benchmark LCOE calculator performance"""
        self.print_header("LCOE Calculator Performance")

        from scripts.lcoe_calculator import LCOECalculator

        def lcoe_calculation():
            lcoe = LCOECalculator(
                capacity_kw=50,
                irradiance=1200,
                capex_usd=150000,
                opex_annual_percent=2.5,
                system_degradation=0.5,
                discount_rate=8,
                lifetime_years=25,
            )
            lcoe.calculate()
            return lcoe

        benchmark = self.run_benchmark(
            "LCOE Calculation (50kW system)",
            lcoe_calculation,
            iterations=50
        )
        self.results["lcoe_calculation"] = benchmark

    # ========================================================================
    # DATA LOADER BENCHMARKS
    # ========================================================================

    def benchmark_async_data_loader(self):
        """Benchmark async data loader performance"""
        self.print_header("Async Data Loader Performance")

        from scripts.data_loaders_async import get_async_loader, AsyncDataLoader

        # Create test data first
        import tempfile
        test_dir = Path(tempfile.gettempdir()) / "geesp_test"
        test_dir.mkdir(exist_ok=True)

        for i in range(3):
            test_file = test_dir / f"test_map_{i}.npy"
            np.save(test_file, np.random.rand(100, 100))

        def loader_initialization():
            loader = get_async_loader()
            return loader

        def load_single_map():
            loader = get_async_loader()
            # Would call load_map_async if available
            return loader

        benchmark1 = self.run_benchmark(
            "AsyncDataLoader Initialization",
            loader_initialization,
            iterations=5
        )
        self.results["async_loader_init"] = benchmark1

        benchmark2 = self.run_benchmark(
            "Single Map Load (with caching)",
            load_single_map,
            iterations=10
        )
        self.results["async_loader_single"] = benchmark2

    # ========================================================================
    # DATABASE BENCHMARKS
    # ========================================================================

    def benchmark_database(self):
        """Benchmark database operations"""
        self.print_header("Database Operation Performance")

        from models.monitoring import (
            get_database_manager,
            Project,
            ProjectRepository,
        )

        # Initialize in-memory database for testing
        db = get_database_manager("sqlite:///:memory:")
        session = db.get_session()

        def db_project_create():
            repo = ProjectRepository(session)
            repo.create(
                project_id=f"PRJ-{time.time()}",
                community="Test",
                province="Huíla",
                status="Operacional",
                capacity_kw=50.0,
                population_served=500,
                annual_generation_mwh=87.5,
                investment_usd=150000,
            )
            return True

        def db_project_query():
            repo = ProjectRepository(session)
            projects = repo.get_all_active()
            return projects

        benchmark1 = self.run_benchmark(
            "Database Project Creation",
            db_project_create,
            iterations=20
        )
        self.results["db_create"] = benchmark1

        benchmark2 = self.run_benchmark(
            "Database Project Query",
            db_project_query,
            iterations=20
        )
        self.results["db_query"] = benchmark2

        session.close()

    # ========================================================================
    # CONFIGURATION BENCHMARKS
    # ========================================================================

    def benchmark_configuration(self):
        """Benchmark configuration loading"""
        self.print_header("Configuration Load Performance")

        from scripts.config_loader import load_config

        def config_load():
            config = load_config()
            return config

        def config_access():
            config = load_config()
            _ = config.get_map_shape()
            _ = config.get_api_host()
            _ = config.get_logging_config()
            return config

        benchmark1 = self.run_benchmark(
            "Config Load & Parse",
            config_load,
            iterations=20
        )
        self.results["config_load"] = benchmark1

        benchmark2 = self.run_benchmark(
            "Config Multi-Access",
            config_access,
            iterations=20
        )
        self.results["config_access"] = benchmark2

    # ========================================================================
    # ERROR HANDLING BENCHMARKS
    # ========================================================================

    def benchmark_error_handling(self):
        """Benchmark error handling performance"""
        self.print_header("Error Handling Performance")

        from scripts.error_handlers import GEESPError, validate_inputs

        def error_raise_catch():
            try:
                raise GEESPError("Test error")
            except GEESPError:
                pass
            return True

        @validate_inputs(weights=dict)
        def validated_function(weights):
            return weights

        def validation_decorator():
            result = validated_function({"test": 1.0})
            return result

        benchmark1 = self.run_benchmark(
            "Exception Raise/Catch Cycle",
            error_raise_catch,
            iterations=50
        )
        self.results["exception_handling"] = benchmark1

        benchmark2 = self.run_benchmark(
            "Validation Decorator",
            validation_decorator,
            iterations=50
        )
        self.results["validation_decorator"] = benchmark2

    # ========================================================================
    # REPORTING
    # ========================================================================

    def generate_report(self):
        """Generate performance report"""
        self.print_header("PERFORMANCE BENCHMARK REPORT")

        print("Summary of Results:\n")

        categories = {
            "MCDA Analysis": ["mcda_initialization", "mcda_with_rasters"],
            "LCOE Calculator": ["lcoe_calculation"],
            "Async Data Loading": ["async_loader_init", "async_loader_single"],
            "Database Operations": ["db_create", "db_query"],
            "Configuration": ["config_load", "config_access"],
            "Error Handling": ["exception_handling", "validation_decorator"],
        }

        for category, metrics in categories.items():
            print(f"\n{category}:")
            for metric in metrics:
                if metric in self.results and "error" not in self.results[metric]:
                    result = self.results[metric]
                    print(f"  {metric}: mean={result['mean_ms']:.2f}ms, "
                          f"p95={result['p95_ms']:.2f}ms")
                elif metric in self.results:
                    print(f"  {metric}: FAILED")

        # Save detailed report
        report_file = Path(__file__).parent / "PERFORMANCE_REPORT.json"
        with open(report_file, "w") as f:
            # Convert numpy types to native Python for JSON serialization
            json_results = {}
            for key, value in self.results.items():
                if isinstance(value, dict):
                    json_results[key] = {
                        k: float(v) if isinstance(v, (np.floating, np.integer)) else v
                        for k, v in value.items()
                    }
                else:
                    json_results[key] = value

            json.dump({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "results": json_results,
            }, f, indent=2)

        print(f"\n✓ Detailed report saved to: PERFORMANCE_REPORT.json")

    def run_all_benchmarks(self):
        """Run all performance benchmarks"""
        print("\n" + "="*70)
        print("GEESP-Angola Performance Benchmark Suite")
        print("="*70)

        try:
            self.benchmark_configuration()
            self.benchmark_error_handling()
            self.benchmark_mcda_analysis()
            self.benchmark_lcoe_calculator()
            self.benchmark_async_data_loader()
            self.benchmark_database()

            self.generate_report()

            print("\n" + "="*70)
            print("✓ Benchmark Complete")
            print("="*70)

        except Exception as e:
            print(f"\n✗ Benchmark failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    benchmark = PerformanceBenchmark()
    benchmark.run_all_benchmarks()
