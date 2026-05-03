"""
Pytest configuration and shared fixtures for GEESP-Angola tests.
Ensures project root is first so 'utils' resolves to the utils package (not scripts/utils.py),
then scripts so that 'import mcda_analysis' etc. find scripts/mcda_analysis.py.

Provides unified fixtures for:
- Unit tests: Isolated component testing
- Integration tests: Multiple components interaction
- E2E tests: Full workflow testing
- Performance tests: Benchmarking
"""
import sys
import pytest
import numpy as np
from pathlib import Path
from typing import Dict, Any
from _path_setup import ensure_backend_paths

_root_s, _scripts_s = ensure_backend_paths()


def pytest_configure(config):
    """Run path setup again when pytest starts (before collection)."""
    ensure_backend_paths()


# ============================================================================
# SHARED FIXTURES
# ============================================================================


@pytest.fixture
def sample_array_2d():
    """Sample 2D numpy array for testing"""
    return np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])


@pytest.fixture
def sample_array_with_nan():
    """Sample 2D numpy array with NaN values"""
    arr = np.array([[1.0, 2.0, np.nan], [4.0, np.nan, 6.0], [7.0, 8.0, 9.0]])
    return arr


@pytest.fixture
def sample_raster_data():
    """Sample realistic raster data for geospatial tests"""
    np.random.seed(42)
    return np.random.uniform(0, 255, (100, 100)).astype(np.float32)


@pytest.fixture
def test_data_dir():
    """Return path to test data directory"""
    return Path(__file__).parent / "data"


@pytest.fixture
def temp_dir(tmp_path):
    """Provide temporary directory for test outputs"""
    return tmp_path


# ============================================================================
# UNIT TEST FIXTURES
# ============================================================================

@pytest.fixture
def unit_test_timeout():
    """Timeout for unit tests (should be very fast)"""
    return 5  # seconds


# ============================================================================
# INTEGRATION TEST FIXTURES
# ============================================================================

@pytest.fixture
def integration_test_timeout():
    """Timeout for integration tests"""
    return 30  # seconds


@pytest.fixture
def mock_config():
    """Provide mock configuration for integration tests"""
    return {
        "database": "sqlite:///:memory:",
        "cache_enabled": True,
        "logging_level": "INFO"
    }
