import numpy as np
from scripts.mcda_analysis import MCDAnalyzer


def test_normalize_and_weighted_overlay():
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([[10.0, 20.0], [30.0, 40.0]])

    ma = MCDAnalyzer(weights_dict={"a": 0.5, "b": 0.5})
    na = ma.normalize_raster(a, name="a")
    nb = ma.normalize_raster(b, name="b")

    assert np.isclose(na.min(), 0.0, atol=1e-6) and np.isclose(na.max(), 1.0, atol=1e-6)
    assert np.isclose(nb.min(), 0.0, atol=1e-6) and np.isclose(nb.max(), 1.0, atol=1e-6)

    result = ma.weighted_overlay()
    assert result.shape == a.shape
    assert (result >= 0).all() and (result <= 1).all()
