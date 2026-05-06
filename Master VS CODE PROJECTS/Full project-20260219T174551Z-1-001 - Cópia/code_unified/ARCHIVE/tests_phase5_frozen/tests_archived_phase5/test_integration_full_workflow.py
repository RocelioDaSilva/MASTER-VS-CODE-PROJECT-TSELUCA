"""Integration test: lightweight full workflow (map generation -> MCDA -> LCOE)

This test runs a small end-to-end flow using the lightweight generators
and core processing functions. Uses temporary directories and small arrays
so it is fast and deterministic for CI.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../app_codebase/geesp-angola/backend')))
from utils.helpers import setup_project_paths
setup_project_paths()

from pathlib import Path
import numpy as np
import tempfile
from scripts.generate_maps_simple import generate_maps
from scripts.map_utils import compute_aptitude


def test_generate_maps_and_compute_aptitude(tmp_path: Path) -> None:
    outdir = tmp_path / "processed"
    outdir.mkdir()

    # Generate maps into tmpdir (should be fast and deterministic)
    generate_maps(output_dir=outdir)

    # Check that aptitude map exists
    apt_path = outdir / "mapa_aptidao_integrada.npy"
    assert apt_path.exists(), "Aptitude map not generated"

    # Load generated rasters and compute aptitude again via shared util
    solar = np.load(outdir / "mapa_irradiacao.npy")
    pop = np.load(outdir / "mapa_populacao.npy")
    dist = np.load(outdir / "mapa_distanciarede.npy")
    slope = np.load(outdir / "mapa_declividade.npy")
    ndvi = np.load(outdir / "mapa_ndvi.npy")

    aptitude = compute_aptitude(solar, pop, dist, slope, ndvi)
    assert aptitude.shape == solar.shape
    assert np.isfinite(aptitude).any()
import numpy as np
from scripts.config_loader import get_map_shape
from scripts.validators import validate_solar_irradiance, validate_population
from scripts.mcda_analysis import MCDAnalyzer


def test_full_workflow_end_to_end():
    shape = get_map_shape()

    # Generate inputs
    solar = np.random.uniform(5.2, 6.8, shape)
    pop = np.random.uniform(10, 1000, shape)

    # Basic validation
    assert validate_solar_irradiance(solar)
    assert validate_population(pop)

    # MCDA: normalize, overlay, classify
    analyzer = MCDAnalyzer()
    analyzer.normalize_raster(solar, "solar_irradiance")
    analyzer.normalize_raster(pop, "population_density")

    aptitude = analyzer.weighted_overlay()
    classified = analyzer.classify_aptitude()

    assert aptitude.shape == tuple(shape)
    assert classified.shape == tuple(shape)
