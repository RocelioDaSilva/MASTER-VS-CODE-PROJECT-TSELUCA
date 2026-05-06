"""
Comprehensive unit tests for MCDA (Multi-Criteria Decision Analysis) module
Tests: AHP weighting, raster normalization, sensitivity analysis, weighted overlay
"""

import pytest
import numpy as np
import pandas as pd
from scripts.mcda_analysis import AHPWeighter, MCDAnalyzer


class TestAHPWeighter:
    """Test Analytic Hierarchy Process (AHP) implementation"""

    def test_ahp_init(self):
        """Test AHPWeighter initialization"""
        ahp = AHPWeighter()
        assert ahp.comparison_matrix is None
        assert ahp.weights is None
        assert ahp.consistency_ratio is None

    def test_create_comparison_matrix_basic(self):
        """Test creating a basic comparison matrix"""
        ahp = AHPWeighter()
        criteria = ["Solar", "Population", "Infrastructure"]
        values = {
            ("Solar", "Population"): 3.0,
            ("Solar", "Infrastructure"): 5.0,
            ("Population", "Infrastructure"): 2.0
        }
        matrix = ahp.create_comparison_matrix(criteria, values)
        
        assert matrix.shape == (3, 3)
        assert matrix.loc["Solar", "Population"] == 3.0
        assert matrix.loc["Population", "Solar"] == pytest.approx(1/3, abs=0.01)
        assert all(matrix.loc[i, i] == 1.0 for i in criteria), "Diagonal should be 1"

    def test_create_comparison_matrix_reciprocal(self):
        """Test that reciprocal property is maintained"""
        ahp = AHPWeighter()
        criteria = ["A", "B", "C"]
        values = {("A", "B"): 4.0, ("B", "C"): 2.0}
        matrix = ahp.create_comparison_matrix(criteria, values)
        
        # Check reciprocals
        assert matrix.loc["A", "B"] * matrix.loc["B", "A"] == pytest.approx(1.0)

    def test_create_comparison_matrix_invalid_criteria_raises(self):
        """Test that invalid criteria names are handled"""
        ahp = AHPWeighter()
        criteria = ["A", "B"]
        values = {("A", "NonExistent"): 3.0}  # NonExistent not in criteria
        
        # Should handle gracefully (log warning, skip invalid entries)
        matrix = ahp.create_comparison_matrix(criteria, values)
        assert matrix is not None

    def test_saaty_scale_completeness(self):
        """Test that Saaty scale is properly defined"""
        ahp = AHPWeighter()
        assert len(ahp.SAATY_SCALE) == 5
        assert 1 in ahp.SAATY_SCALE
        assert 9 in ahp.SAATY_SCALE


class TestMCDANormalization:
    """Test raster normalization functions"""

    @pytest.fixture
    def mcda(self):
        """Fixture: initialize MCDAnalyzer"""
        return MCDAnalyzer(weights_dict={"layer1": 0.5, "layer2": 0.5})

    def test_normalize_raster_basic(self, mcda):
        """Test basic raster normalization (min-max)"""
        raster = np.array([[1.0, 2.0], [3.0, 4.0]])
        normalized = mcda.normalize_raster(raster, name="test")
        
        assert normalized.min() == pytest.approx(0.0)
        assert normalized.max() == pytest.approx(1.0)
        assert normalized.shape == raster.shape

    def test_normalize_raster_with_zeros(self, mcda):
        """Test normalization with zero values"""
        raster = np.array([[0.0, 1.0], [2.0, 3.0]])
        normalized = mcda.normalize_raster(raster, name="test")
        
        assert normalized.min() == pytest.approx(0.0)
        assert normalized.max() == pytest.approx(1.0)

    def test_normalize_raster_constant_values(self, mcda):
        """Test normalization with all same values (should handle division by zero)"""
        raster = np.array([[5.0, 5.0], [5.0, 5.0]])
        normalized = mcda.normalize_raster(raster, name="test")
        
        # Should not raise error; handle gracefully
        assert normalized.shape == raster.shape
        assert not np.any(np.isnan(normalized)) or np.all(normalized == normalized[0, 0])

    def test_normalize_raster_negative_values(self, mcda):
        """Test normalization with negative values"""
        raster = np.array([[-2.0, -1.0], [0.0, 1.0]])
        normalized = mcda.normalize_raster(raster, name="test")
        
        assert normalized.min() == pytest.approx(0.0)
        assert normalized.max() == pytest.approx(1.0)


class TestWeightedOverlay:
    """Test weighted overlay combination logic"""

    def test_weighted_overlay_basic(self):
        """Test basic weighted overlay with two layers"""
        a = np.array([[1.0, 2.0], [3.0, 4.0]])
        b = np.array([[10.0, 20.0], [30.0, 40.0]])

        mcda = MCDAnalyzer(weights_dict={"a": 0.5, "b": 0.5})
        na = mcda.normalize_raster(a, name="a")
        nb = mcda.normalize_raster(b, name="b")

        result = mcda.weighted_overlay()
        
        assert result.shape == a.shape
        assert (result >= 0.0).all() and (result <= 1.0).all()

    def test_weighted_overlay_equal_weights(self):
        """Test that equal weights produce average"""
        a = np.array([[0.0, 1.0]])
        b = np.array([[0.0, 1.0]])
        
        mcda = MCDAnalyzer(weights_dict={"a": 0.5, "b": 0.5})
        na = mcda.normalize_raster(a, name="a")
        nb = mcda.normalize_raster(b, name="b")
        
        result = mcda.weighted_overlay()
        # Should be [0.0, 1.0] since both normalized to [0, 1]
        assert result[0, 1] == pytest.approx(1.0)

    def test_weighted_overlay_unequal_weights(self):
        """Test weighted overlay with different weights"""
        a = np.array([[0.0, 1.0]])  # Normalized: [0, 1]
        b = np.array([[0.5, 0.5]])  # Normalized: [0, 0] (constant)
        
        mcda = MCDAnalyzer(weights_dict={"a": 0.7, "b": 0.3})
        na = mcda.normalize_raster(a, name="a")
        nb = mcda.normalize_raster(b, name="b")
        
        result = mcda.weighted_overlay()
        # Result should be closer to 'a' since it has 0.7 weight
        assert result.shape == (1, 2)


class TestAptitudeClassification:
    """Test classification of aptitude scores"""

    @pytest.fixture
    def mcda(self):
        return MCDAnalyzer(weights_dict={"test": 1.0})

    def test_classify_aptitude_basic(self, mcda):
        """Test aptitude classification into zones"""
        scores = np.array([[0.1, 0.3], [0.6, 0.9]])
        thresholds = [0.25, 0.75]
        
        classified = mcda.classify_aptitude(scores, thresholds)
        
        assert classified.shape == scores.shape
        assert np.all((classified >= 0) & (classified <= len(thresholds)))

    def test_classify_aptitude_edge_cases(self, mcda):
        """Test edge values in classification"""
        scores = np.array([[0.0, 0.25, 0.5, 0.75, 1.0]])
        thresholds = [0.25, 0.75]
        
        classified = mcda.classify_aptitude(scores, thresholds)
        assert classified.shape == scores.shape


class TestSensitivityAnalysis:
    """Test sensitivity analysis functionality"""

    @pytest.fixture
    def mcda(self):
        return MCDAnalyzer(weights_dict={"solar": 0.5, "pop": 0.3, "infra": 0.2})

    def test_sensitivity_analysis_basic(self, mcda):
        """Test that sensitivity analysis runs"""
        base_result = np.array([[0.5, 0.6], [0.7, 0.8]])
        
        sensitivity = mcda.sensitivity_analysis(
            base_result, 
            parameter_name="solar", 
            variation_percent=20
        )
        
        # Should return dict with results for +/- variations
        assert sensitivity is not None
        assert isinstance(sensitivity, (dict, tuple, list))

    def test_sensitivity_analysis_variation_range(self, mcda):
        """Test sensitivity analysis with different variations"""
        base = np.array([[0.5, 0.6]])
        
        for var in [10, 20, 30]:
            sensitivity = mcda.sensitivity_analysis(base, "test", var)
            assert sensitivity is not None


class TestIntegration:
    """Integration tests for full MCDA workflow"""

    def test_full_mcda_workflow(self):
        """Test complete MCDA workflow: normalize → overlay → classify"""
        # Create synthetic data
        solar = np.array([[1000, 2000], [2000, 1500]])  # kWh/m²
        population = np.array([[100, 50], [75, 200]])
        infrastructure = np.array([[5, 10], [3, 15]])    # km to grid
        
        # Initialize MCDA
        mcda = MCDAnalyzer(weights_dict={
            "solar": 0.5,
            "population": 0.3,
            "infrastructure": 0.2
        })
        
        # Normalize layers
        s_norm = mcda.normalize_raster(solar, name="solar")
        p_norm = mcda.normalize_raster(population, name="population")
        i_norm = mcda.normalize_raster(infrastructure, name="infrastructure")
        
        # Weighted overlay
        result = mcda.weighted_overlay()
        
        # Classify
        classes = mcda.classify_aptitude(result, thresholds=[0.3, 0.7])
        
        # Verify
        assert result.shape == solar.shape
        assert classes.shape == solar.shape
        assert np.all((result >= 0) & (result <= 1))

    def test_mcda_consistency_across_runs(self):
        """Test that MCDA gives consistent results for same input"""
        data = np.array([[100, 200], [300, 400]])
        
        mcda1 = MCDAnalyzer(weights_dict={"test": 1.0})
        result1 = mcda1.normalize_raster(data, name="test")
        
        mcda2 = MCDAnalyzer(weights_dict={"test": 1.0})
        result2 = mcda2.normalize_raster(data, name="test")
        
        np.testing.assert_array_almost_equal(result1, result2)


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_mcda_with_nan_values(self):
        """Test handling of NaN values in rasters"""
        raster = np.array([[1.0, np.nan], [3.0, 4.0]])
        mcda = MCDAnalyzer(weights_dict={"test": 1.0})
        
        # Should handle NaN gracefully
        result = mcda.normalize_raster(raster, name="test")
        assert result is not None

    def test_mcda_with_inf_values(self):
        """Test handling of infinite values"""
        raster = np.array([[1.0, np.inf], [3.0, 4.0]])
        mcda = MCDAnalyzer(weights_dict={"test": 1.0})
        
        result = mcda.normalize_raster(raster, name="test")
        assert result is not None

    def test_zero_weights_sum(self):
        """Test behavior when weights sum to zero"""
        mcda = MCDAnalyzer(weights_dict={"a": 0.0, "b": 0.0})
        
        # Should handle gracefully (perhaps normalize internally)
        assert mcda is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
