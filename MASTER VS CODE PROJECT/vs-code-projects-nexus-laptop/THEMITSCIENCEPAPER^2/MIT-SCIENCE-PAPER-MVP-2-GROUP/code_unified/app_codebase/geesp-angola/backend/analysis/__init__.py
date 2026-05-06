"""
GEESP-Angola analysis engines module.

Re-exports canonical implementations from backend/scripts/:
- LCOECalculator, SolarParameters from scripts/lcoe_calculator.py
- AHPWeighter, MCDAnalyzer from scripts/mcda_analysis.py
- Validation from analysis/validation_base.py
- Base classes from analysis/base.py
"""

try:
    from .base import AnalysisEngine, AnalysisResult, Component, RasterProcessor, Validator
except ImportError:
    # Allow partial imports if some modules are not yet migrated.
    pass

try:
    from .lcoe import LCOECalculator, SolarParameters
except ImportError:
    pass

try:
    from .mcda import AHPWeighter, MCDAnalyzer
except ImportError:
    pass

try:
    from .validation_base import ValidationPipeline, ValidationResult
except ImportError:
    pass

_EXPORT_CANDIDATES = [
    "AnalysisEngine",
    "AnalysisResult",
    "Component",
    "RasterProcessor",
    "Validator",
    "LCOECalculator",
    "SolarParameters",
    "AHPWeighter",
    "MCDAnalyzer",
    "ValidationPipeline",
    "ValidationResult",
]

__all__ = [name for name in _EXPORT_CANDIDATES if name in globals()]
