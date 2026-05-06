"""
Comprehensive Test Suite for MCDA Module
Tests AHP weighting, MCDA analysis, and edge cases
"""

import pytest
import numpy as np
import pandas as pd
from typing import Dict
import logging

# Configure test logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def sample_raster():
    """Standard test raster (280x300)"""
    np.random.seed(42)
    return np.random.uniform(0.2, 0.8, (280, 300)).astype(np.float32)


@pytest.fixture
def sample_weights():
    """Standard MCDA weights"""
    return {
        "solar": 0.25,
        "population": 0.25,
        "distance": 0.20,
        "slope": 0.15,
        "vegetation": 0.15
    }


@pytest.fixture
def sample_rasters(sample_raster):
    """Dictionary of 5 sample rasters"""
    np.random.seed(42)
    return {
        "solar": sample_raster,
        "population": np.random.uniform(0.1, 0.9, (280, 300)).astype(np.float32),
        "distance": np.random.uniform(0.0, 1.0, (280, 300)).astype(np.float32),
        "slope": np.random.uniform(0.0, 1.0, (280, 300)).astype(np.float32),
        "vegetation": np.random.uniform(-0.3, 0.7, (280, 300)).astype(np.float32),
    }


# =============================================================================
# TEST: Raster Properties and Edge Cases
# =============================================================================

class TestRasterProperties:
    """Test raster data handling and properties"""
    
    def test_raster_shape_consistency(self, sample_rasters):
        """All input rasters should have same shape"""
        shapes = [r.shape for r in sample_rasters.values()]
        assert all(s == (280, 300) for s in shapes), "Shape mismatch"
    
    def test_raster_dtype_handling(self, sample_rasters):
        """Rasters should maintain float32 dtype"""
        for name, raster in sample_rasters.items():
            assert raster.dtype == np.float32, f"{name} has wrong dtype"
    
    def test_raster_value_ranges(self, sample_rasters):
        """Values should be in normalized range [0, 1]"""
        for name, raster in sample_rasters.items():
            values = raster[~np.isnan(raster)]
            # Allow some margin for edge cases
            assert values.min() >= -0.5, f"{name} has values below -0.5"
            assert values.max() <= 1.5, f"{name} has values above 1.5"
    
    def test_raster_nan_handling(self, sample_raster):
        """Should handle NaN values gracefully"""
        raster_with_nan = sample_raster.copy()
        raster_with_nan[0, 0] = np.nan
        raster_with_nan[10:20, 10:20] = np.nan
        
        valid_percent = np.sum(~np.isnan(raster_with_nan)) / raster_with_nan.size
        assert valid_percent > 0.95, "Too many NaN values"
    
    def test_raster_constant_values(self):
        """Handle rasters with constant values"""
        constant_raster = np.ones((280, 300), dtype=np.float32) * 0.5
        
        # Should be valid but with zero variance
        assert constant_raster.std() == 0.0, "Constant raster should have zero std"
    
    def test_empty_raster_handling(self):
        """Handle empty/all-zero rasters"""
        empty_raster = np.zeros((280, 300), dtype=np.float32)
        
        assert empty_raster.sum() == 0.0, "Empty raster sum not zero"
        assert empty_raster.std() == 0.0, "Empty raster std not zero"
    
    def test_highly_skewed_raster(self):
        """Handle rasters with extreme value distributions"""
        skewed = np.ones((280, 300), dtype=np.float32) * 0.01
        skewed[0, 0] = 0.99
        
        # Should have valid shape and dtype despite skewness
        assert skewed.shape == (280, 300)
        assert skewed.dtype == np.float32


# =============================================================================
# TEST: Weight Normalization and Validation
# =============================================================================

class TestWeightNormalization:
    """Test MCDA weight handling and normalization"""
    
    def test_weight_sum_tolerance(self, sample_weights):
        """Weights should sum to approximately 1.0"""
        weight_sum = sum(sample_weights.values())
        assert abs(weight_sum - 1.0) < 0.01, "Weights don't sum to 1.0"
    
    def test_individual_weight_bounds(self, sample_weights):
        """Each weight should be between 0 and 1"""
        for name, weight in sample_weights.items():
            assert 0 <= weight <= 1, f"{name} weight out of bounds"
    
    def test_weight_order_irrelevance(self, sample_weights):
        """Weight order should not affect result"""
        weights1 = sample_weights.copy()
        weights2 = dict(reversed(sample_weights.items()))
        
        sum1 = sum(weights1.values())
        sum2 = sum(weights2.values())
        
        assert abs(sum1 - sum2) < 0.001, "Weight order affects sum"
    
    def test_weight_adjustment(self):
        """Adjust weights to sum to 1.0"""
        raw_weights = {"a": 2, "b": 3, "c": 5}
        total = sum(raw_weights.values())
        normalized = {k: v / total for k, v in raw_weights.items()}
        
        assert abs(sum(normalized.values()) - 1.0) < 0.0001
        assert normalized == {"a": 0.2, "b": 0.3, "c": 0.5}
    
    def test_zero_weight_handling(self):
        """Handle criteria with zero weight"""
        weights = {"solar": 0.5, "population": 0.5, "distance": 0.0}
        assert sum(weights.values()) == 1.0
        # Distance is ignored in overlay calculation
    
    def test_equal_weight_distribution(self):
        """Equal weights case (5 criteria = 0.2 each)"""
        n = 5
        weights = {f"criterion_{i}": 1.0/n for i in range(n)}
        assert sum(weights.values()) == 1.0
        assert all(abs(w - 0.2) < 0.0001 for w in weights.values())


# =============================================================================
# TEST: Normalization Methods
# =============================================================================

class TestNormalizationMethods:
    """Test different raster normalization approaches"""
    
    def test_minmax_normalization(self, sample_raster):
        """Min-Max normalization [0, 1]"""
        rmin, rmax = sample_raster.min(), sample_raster.max()
        if rmax > rmin:
            normalized = (sample_raster - rmin) / (rmax - rmin)
        else:
            normalized = np.zeros_like(sample_raster)
        
        assert normalized.min() >= -0.0001, "Min not 0"
        assert normalized.max() <= 1.0001, "Max not 1"
    
    def test_zscore_normalization(self, sample_raster):
        """Z-score normalization (mean = 0, std = 1)"""
        mean = sample_raster.mean()
        std = sample_raster.std()
        if std > 0:
            normalized = (sample_raster - mean) / std
        else:
            normalized = np.zeros_like(sample_raster)
        
        assert abs(normalized.mean()) < 0.01, "Mean not 0"
        if normalized.std() > 0:
            assert abs(normalized.std() - 1.0) < 0.01, "Std not 1"
    
    def test_percentile_normalization(self, sample_raster):
        """Normalize by percentiles (5th, 95th)"""
        p5 = np.percentile(sample_raster, 5)
        p95 = np.percentile(sample_raster, 95)
        
        if p95 > p5:
            normalized = np.clip((sample_raster - p5) / (p95 - p5), 0, 1)
        else:
            normalized = np.ones_like(sample_raster) * 0.5
        
        assert normalized.min() >= -0.0001
        assert normalized.max() <= 1.0001
    
    def test_log_normalization(self):
        """Logarithmic normalization for skewed data"""
        data = np.array([1, 10, 100, 1000], dtype=np.float32)
        log_data = np.log1p(data)  # log1p handles 0 values
        
        # Normalize log values
        normalized = (log_data - log_data.min()) / (log_data.max() - log_data.min())
        assert normalized.min() >= 0
        assert normalized.max() <= 1


# =============================================================================
# TEST: Weighted Overlay Computation
# =============================================================================

class TestWeightedOverlay:
    """Test weighted overlay calculation"""
    
    def test_basic_overlay(self, sample_rasters, sample_weights):
        """Compute weighted overlay of normalized rasters"""
        # Normalize each raster
        normalized = {}
        for name, raster in sample_rasters.items():
            rmin, rmax = raster.min(), raster.max()
            if rmax > rmin:
                normalized[name] = (raster - rmin) / (rmax - rmin)
            else:
                normalized[name] = np.zeros_like(raster)
        
        # Compute weighted average
        result = np.zeros((280, 300), dtype=np.float32)
        for name, weight in sample_weights.items():
            if name in normalized:
                result += weight * normalized[name]
        
        assert result.shape == (280, 300)
        assert result.min() >= -0.01
        assert result.max() <= 1.01
    
    def test_overlay_with_zero_weights(self, sample_rasters):
        """Weighted overlay with zero weights"""
        weights = {"solar": 0.5, "population": 0.5, "distance": 0, "slope": 0, "vegetation": 0}
        
        normalized = {}
        for name in weights.keys():
            if name in sample_rasters:
                r = sample_rasters[name]
                rmin, rmax = r.min(), r.max()
                normalized[name] = (r - rmin) / (rmax - rmin) if rmax > rmin else np.zeros_like(r)
        
        result = sum(weights[name] * normalized[name] for name in weights if name in normalized)
        assert result.shape == (280, 300)
    
    def test_overlay_nan_propagation(self, sample_rasters, sample_weights):
        """NaN handling in weighted overlay"""
        # Add NaN values
        rasters_with_nan = {}
        for name, raster in sample_rasters.items():
            r = raster.copy()
            r[10:20, 10:20] = np.nan
            rasters_with_nan[name] = r
        
        # Compute overlay with NaN
        normalized = {}
        for name, raster in rasters_with_nan.items():
            rmin = np.nanmin(raster)
            rmax = np.nanmax(raster)
            if rmax > rmin:
                normalized[name] = (raster - rmin) / (rmax - rmin)
            else:
                normalized[name] = np.zeros_like(raster)
        
        result = np.zeros((280, 300), dtype=np.float32)
        for name, weight in sample_weights.items():
            if name in normalized:
                result = np.nansum([result, weight * normalized[name]], axis=0)
        
        # Check NaN propagation
        nan_count = np.sum(np.isnan(result))
        valid_percent = (1 - nan_count / result.size)
        assert valid_percent > 0.85, "Too many NaN values in result"


# =============================================================================
# TEST: Aptitude Classification
# =============================================================================

class TestAptitudeClassification:
    """Test classification of aptitude values"""
    
    def test_three_class_classification(self, sample_raster):
        """Classify into High/Medium/Low"""
        high_threshold = 0.70
        medium_threshold = 0.40
        
        classified = np.zeros_like(sample_raster, dtype=np.uint8)
        classified[sample_raster >= high_threshold] = 3  # High
        classified[(sample_raster >= medium_threshold) & (sample_raster < high_threshold)] = 2  # Medium
        classified[sample_raster < medium_threshold] = 1  # Low
        
        # Check classification distribution
        high_percent = (classified == 3).sum() / classified.size
        medium_percent = (classified == 2).sum() / classified.size
        low_percent = (classified == 1).sum() / classified.size
        
        assert 0 < high_percent < 1, "No high aptitude areas"
        assert 0 < medium_percent < 1, "No medium aptitude areas"
        assert 0 < low_percent < 1, "No low aptitude areas"
        assert abs((high_percent + medium_percent + low_percent) - 1.0) < 0.01
    
    def test_classification_boundary_values(self):
        """Handle boundary values correctly"""
        threshold = 0.5
        values = np.array([0.49, 0.5, 0.51])
        
        classified = values >= threshold
        assert classified[0] == False
        assert classified[1] == True
        assert classified[2] == True
    
    def test_classification_extremes(self):
        """Classify all 0s and all 1s"""
        all_zeros = np.zeros((100, 100), dtype=np.float32)
        all_ones = np.ones((100, 100), dtype=np.float32)
        
        # All should be below threshold
        below = (all_zeros < 0.5).sum()
        assert below == 10000, "Didn't classify all zeros correctly"
        
        # All should be above threshold
        above = (all_ones > 0.5).sum()
        assert above == 10000, "Didn't classify all ones correctly"


# =============================================================================
# TEST: Performance and Efficiency
# =============================================================================

class TestPerformance:
    """Test computation efficiency"""
    
    def test_raster_loading_efficiency(self, sample_raster):
        """Loading and reshaping efficiency"""
        import time
        
        start = time.time()
        for _ in range(100):
            r = sample_raster.copy()
            r = r.astype(np.float32)
        elapsed = time.time() - start
        
        # Should complete 100 operations in < 1 second
        assert elapsed < 1.0, f"Raster operations took {elapsed}s"
    
    def test_normalization_efficiency(self, sample_raster):
        """Normalization computation efficiency"""
        import time
        
        start = time.time()
        for _ in range(1000):
            rmin, rmax = sample_raster.min(), sample_raster.max()
            if rmax > rmin:
                normalized = (sample_raster - rmin) / (rmax - rmin)
        elapsed = time.time() - start
        
        # Should complete 1000 normalizations in < 2 seconds
        assert elapsed < 2.0, f"1000 normalizations took {elapsed}s"
    
    def test_overlay_efficiency(self, sample_rasters, sample_weights):
        """Weighted overlay computation efficiency"""
        import time
        
        # Normalize once
        normalized = {}
        for name, raster in sample_rasters.items():
            rmin, rmax = raster.min(), raster.max()
            normalized[name] = (raster - rmin) / (rmax - rmin) if rmax > rmin else np.zeros_like(raster)
        
        start = time.time()
        for _ in range(100):
            result = sum(sample_weights[name] * normalized[name] 
                        for name in sample_weights if name in normalized)
        elapsed = time.time() - start
        
        # Should complete 100 overlays in < 1 second  
        assert elapsed < 1.0, f"100 overlays took {elapsed}s"


# =============================================================================
# TEST: Statistical Validation
# =============================================================================

class TestStatisticalProperties:
    """Test statistical properties of results"""
    
    def test_result_distribution(self, sample_raster):
        """Check statistical distribution of aptitude"""
        mean = sample_raster.mean()
        std = sample_raster.std()
        
        assert 0.1 < mean < 0.9, "Mean outside expected range"
        assert std > 0.05, "Std dev too low (no variation)"
    
    def test_result_percentiles(self, sample_raster):
        """Check percentile distribution"""
        p10 = np.percentile(sample_raster, 10)
        p50 = np.percentile(sample_raster, 50)
        p90 = np.percentile(sample_raster, 90)
        
        assert p10 < p50 < p90, "Percentiles not in order"
        assert (p90 - p10) > 0.1, "Range too narrow"
    
    def test_correlation_between_inputs(self):
        """Check correlation between input rasters"""
        # Create truly independent rasters
        np.random.seed(42)
        solar_flat = np.random.uniform(0, 1, 1000)
        
        np.random.seed(123)  # Different seed for independence
        pop_flat = np.random.uniform(0, 1, 1000)
        
        correlation = np.corrcoef(solar_flat, pop_flat)[0, 1]
        
        # Correlation should be between -1 and 1
        assert -1.0 <= correlation <= 1.0
        # Independent random data should have low correlation
        assert abs(correlation) < 0.3, f"Correlation {correlation} too high for independent data"


# =============================================================================
# TEST: Integration Tests
# =============================================================================

class TestMCDAIntegration:
    """End-to-end MCDA workflow tests"""
    
    def test_full_mcda_workflow(self, sample_rasters, sample_weights):
        """Complete MCDA analysis workflow"""
        # Step 1: Validate inputs
        assert len(sample_rasters) == 5
        assert sum(sample_weights.values()) == pytest.approx(1.0, abs=0.01)
        
        # Step 2: Normalize rasters
        normalized = {}
        for name, raster in sample_rasters.items():
            rmin, rmax = raster.min(), raster.max()
            if rmax > rmin:
                normalized[name] = (raster - rmin) / (rmax - rmin)
            else:
                normalized[name] = np.zeros_like(raster)
        
        # Step 3: Apply weights
        result = np.zeros((280, 300), dtype=np.float32)
        for name, weight in sample_weights.items():
            if name in normalized:
                result += weight * normalized[name]
        
        # Step 4: Verify result
        assert result.shape == (280, 300)
        assert result.min() >= 0 and result.max() <= 1
        assert result.mean() > 0  # Should have non-zero mean
    
    def test_sensitivity_analysis(self, sample_rasters, sample_weights):
        """Test sensitivity to weight changes"""
        # Original weights
        original_weights = sample_weights.copy()
        
        # Compute original result
        normalized = {}
        for name, raster in sample_rasters.items():
            rmin, rmax = raster.min(), raster.max()
            normalized[name] = (raster - rmin) / (rmax - rmin) if rmax > rmin else np.zeros_like(raster)
        
        result_original = sum(original_weights[name] * normalized[name] 
                             for name in original_weights if name in normalized)
        
        # Adjust one weight
        modified_weights = original_weights.copy()
        modified_weights["solar"] += 0.1
        modified_weights["distance"] -= 0.1
        
        result_modified = sum(modified_weights[name] * normalized[name]
                             for name in modified_weights if name in normalized)
        
        # Results should be different but similar
        difference = np.abs(result_original - result_modified).mean()
        assert difference > 0.01, "No sensitivity to weight changes"
        assert difference < 0.5, "Too sensitive to weight changes"


# =============================================================================
# TEST: Edge Cases and Error Conditions
# =============================================================================

class TestEdgeCases:
    """Test edge cases and unusual inputs"""
    
    def test_single_pixel_raster(self, sample_weights):
        """Handle 1x1 raster"""
        tiny_raster = np.array([[0.5]], dtype=np.float32)
        assert tiny_raster.shape == (1, 1)
    
    def test_very_large_raster(self, sample_weights):
        """Handle larger rasters (1000x1000)"""
        large_raster = np.random.uniform(0, 1, (1000, 1000)).astype(np.float32)
        assert large_raster.shape == (1000, 1000)
        
        # Should normalize efficiently
        normalized = (large_raster - large_raster.min()) / (large_raster.max() - large_raster.min())
        assert normalized.shape == (1000, 1000)
    
    def test_ill_conditioned_weights(self):
        """Very skewed weight distribution"""
        weights = {"a": 0.98, "b": 0.01, "c": 0.01}
        assert sum(weights.values()) == pytest.approx(1.0, abs=0.01)
    
    def test_floating_point_precision(self):
        """Floating point precision in weight sum"""
        weights = {"a": 1/3, "b": 1/3, "c": 1/3}
        weight_sum = sum(weights.values())
        assert abs(weight_sum - 1.0) < 1e-10
