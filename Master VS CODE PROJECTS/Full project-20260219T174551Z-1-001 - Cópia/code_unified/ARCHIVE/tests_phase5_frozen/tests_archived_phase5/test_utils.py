import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../app_codebase/geesp-angola/backend')))
from utils.helpers import setup_project_paths
setup_project_paths()

import os
import numpy as np
from scripts import utils


def test_save_and_load_npy_fallback(tmp_path):
    fn = tmp_path / "test_raster.npy"
    arr = np.arange(16, dtype=float).reshape((4, 4))
    # save via save_raster (should use npy fallback)
    utils.save_raster(arr, str(fn))
    loaded, meta = utils.load_raster(str(fn))
    assert meta is None or isinstance(meta, dict)
    assert np.allclose(arr, loaded)
    os.remove(fn)


def test_validate_raster_stats():
    a = np.array([[1.0, 2.0], [np.nan, 4.0]])
    stats = utils.validate_raster(a, name="test")
    assert stats["total_pixels"] == 4
    assert stats["valid_pixels"] == 3
    assert stats["min"] == 1.0
    assert stats["max"] == 4.0
