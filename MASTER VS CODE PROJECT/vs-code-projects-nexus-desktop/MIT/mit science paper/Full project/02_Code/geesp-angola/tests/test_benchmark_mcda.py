"""Performance benchmark-style test for MCDA weighted overlay.

This test is skipped by default unless environment variable `RUN_BENCHMARKS`
is set. It creates a moderate raster (200x200 by default) to measure
performance of the `weighted_overlay` function.
"""
import os
import numpy as np
import pytest

from scripts.mcda_analysis import MCDAnalyzer


@pytest.mark.skipif("RUN_BENCHMARKS" not in os.environ, reason="Benchmarks skipped")
def test_mcda_weighted_overlay_performance() -> None:
    size = (200, 200)
    # Create synthetic normalized rasters
    m = MCDAnalyzer(weights_dict={"a": 0.25, "b": 0.25, "c": 0.25, "d": 0.25})
    for name in ["a", "b", "c", "d"]:
        arr = np.random.random(size).astype(np.float32)
        m.normalized_rasters[name] = arr

    aptitude = m.weighted_overlay()
    assert aptitude.shape == size
    assert np.isfinite(aptitude).any()
