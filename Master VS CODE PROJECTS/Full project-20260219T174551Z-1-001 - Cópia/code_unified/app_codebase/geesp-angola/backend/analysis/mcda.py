"""
GEESP-Angola: MCDA Analysis Module (Re-export Shim)

Canonical implementation lives in scripts/mcda_analysis.py.
This module re-exports for backward compatibility with analysis package imports.
"""
from scripts.mcda_analysis import AHPWeighter, MCDAnalyzer

__all__ = ["AHPWeighter", "MCDAnalyzer"]
