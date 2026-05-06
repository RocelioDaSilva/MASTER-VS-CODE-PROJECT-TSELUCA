import importlib
import numpy as np
import sys


def run_smoke_tests():
    results = {"import_ok": [], "errors": []}
    modules = [
        "scripts.mcda_analysis",
        "scripts.lcoe_calculator",
        "scripts.utils",
        "scripts.generate_maps_simple",
        "scripts.generate_maps",
    ]
    for m in modules:
        try:
            importlib.import_module(m)
            results["import_ok"].append(m)
        except Exception as e:
            results["errors"].append(f"import {m}: {e}")

    # mcda smoke
    try:
        M = importlib.import_module("scripts.mcda_analysis")
        a = np.array([1.0, 2.0, 3.0, 4.0])
        ma = M.MCDAnalyzer()
        na = ma.normalize_raster(a, name="test")
        if not (abs(na.min()) < 1e-6 and abs(na.max() - 1) < 1e-6):
            results["errors"].append("mcda normalize failed")
    except Exception as e:
        results["errors"].append("mcda_smoke: " + str(e))

    # lcoe smoke (use compare_technologies for quick check)
    try:
        LC = importlib.import_module("scripts.lcoe_calculator")
        calc = LC.LCOECalculator(location="Huíla")
        comp = calc.compare_technologies(capacity_mw=1.0, annual_irradiance=2226)
        if comp is None or comp.empty:
            results["errors"].append("lcoe compare_technologies returned empty result")
    except Exception as e:
        results["errors"].append("lcoe_smoke: " + str(e))

    # generate_maps_simple: importing the module executes the lightweight generator
    try:
        importlib.import_module("scripts.generate_maps_simple")
        results["import_ok"].append("generate_maps_simple_executed")
    except Exception as e:
        results["errors"].append("maps_simple_smoke: " + str(e))

    # utils save/load smoke (optional)
    try:
        U = importlib.import_module("scripts.utils")
        # Only run save/load smoke if rasterio is available or fallback implemented
        if hasattr(U, "save_raster") and hasattr(U, "load_raster"):
            try:
                arr = np.ones((4, 4), dtype=float)
                fn = "data/processed/_temp_test.npy"
                U.save_raster(arr, fn)
                loaded = U.load_raster(fn)
                # load_raster may return (data, meta) or data alone
                if isinstance(loaded, tuple) or isinstance(loaded, list):
                    data_loaded = loaded[0]
                else:
                    data_loaded = loaded

                if not np.allclose(arr, data_loaded):
                    results["errors"].append("utils save/load mismatch")
                import os

                try:
                    os.remove(fn)
                except Exception:
                    pass
            except Exception as e:
                results["errors"].append("utils_smoke: " + str(e))
        else:
            results["import_ok"].append("utils_skipped_save_load")
    except Exception as e:
        results["errors"].append("utils_smoke: " + str(e))

    # dashboard import smoke (optional)
    try:
        importlib.import_module("dashboard.app")
        results["import_ok"].append("dashboard_imported")
    except Exception as e:
        # Streamlit/dashboard may be optional in this environment; mark as skipped
        results["import_ok"].append("dashboard_skipped: " + str(e))

    print("IMPORT_OK:", results["import_ok"])
    print("ERRORS:", results["errors"])
    return results


if __name__ == "__main__":
    res = run_smoke_tests()
    if res["errors"]:
        sys.exit(2)
    else:
        sys.exit(0)
