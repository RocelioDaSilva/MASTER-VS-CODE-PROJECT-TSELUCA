import numpy as np
from scripts.validators import (
    validate_solar_irradiance, validate_population, validate_ndvi
)
from scripts.mcda_analysis import MCDAnalyzer
from scripts.config_loader import get_map_shape, get_mcda_weights


def test_mcda_pipeline_basic():
    shape = get_map_shape()
    solar = np.random.uniform(5.0, 7.0, shape)
    pop = np.random.uniform(0.0, 500.0, shape)
    ndvi = np.random.uniform(-0.2, 0.6, shape)

    assert validate_solar_irradiance(solar) is True
    assert validate_population(pop) is True
    assert validate_ndvi(ndvi) is True

    weights = get_mcda_weights()
    analyzer = MCDAnalyzer(weights_dict=weights)

    analyzer.normalize_raster(solar, "solar_irradiance")
    analyzer.normalize_raster(pop, "population_density")
    analyzer.normalize_raster(ndvi, "vegetation_ndvi")

    aptitude = analyzer.weighted_overlay()
    assert aptitude.shape == tuple(shape)

    classified = analyzer.classify_aptitude()
    assert classified.dtype == np.uint8
