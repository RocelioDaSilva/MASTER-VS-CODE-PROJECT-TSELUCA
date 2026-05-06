"""Run all map generators as a simple CLI for automation/tests

Usage:
    python -m scripts.run_all_maps
"""
from pathlib import Path
import sys


def main():
    base = Path(__file__).resolve().parents[2]
    print("Running GEESP-Angola map generators from:", base)

    # Run lightweight generator
    try:
        import importlib

        print("-> Running generate_maps_simple")
        importlib.import_module("scripts.generate_maps_simple")
        print("-> generate_maps_simple completed")
    except Exception as e:
        print("generate_maps_simple failed:", e)

    # Optionally run full generator
    try:
        print("-> Running generate_maps (full)")
        importlib.import_module("scripts.generate_maps")
        print("-> generate_maps completed")
    except Exception as e:
        print("generate_maps failed:", e)


if __name__ == "__main__":
    main()
