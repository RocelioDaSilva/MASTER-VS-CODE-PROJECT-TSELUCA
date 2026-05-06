"""
GEESP-Angola: LCOE Analysis Module (Re-export Shim)

Canonical implementation lives in scripts/lcoe_calculator.py.
This module re-exports for backward compatibility with analysis package imports.
"""
from scripts.lcoe_calculator import LCOECalculator, SolarParameters

__all__ = ["LCOECalculator", "SolarParameters"]
