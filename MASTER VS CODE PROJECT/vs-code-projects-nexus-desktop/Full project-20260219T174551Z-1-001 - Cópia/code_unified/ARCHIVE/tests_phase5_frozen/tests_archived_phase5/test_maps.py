import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../app_codebase/geesp-angola/backend')))
from utils.helpers import setup_project_paths
setup_project_paths()

import numpy as np
from scripts import generate_maps_simple


def test_maps_generated_exist():
    # The lightweight generator writes files; check for metadata
    import json, pathlib

    meta = pathlib.Path("data/processed/mapas_metadata.json")
    assert meta.exists()
    with open(meta, "r") as f:
        data = json.load(f)
    assert "mapa_aptidao_integrada" in data
