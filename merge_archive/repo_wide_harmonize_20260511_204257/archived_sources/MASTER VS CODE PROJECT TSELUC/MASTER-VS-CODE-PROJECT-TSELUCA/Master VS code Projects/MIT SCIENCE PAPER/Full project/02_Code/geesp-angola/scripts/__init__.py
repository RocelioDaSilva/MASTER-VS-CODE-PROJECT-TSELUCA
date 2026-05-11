"""
scripts package initializer — expose commonly used submodules as package
This helps tests that patch or reference `scripts.<module>` attributes.
"""

__all__ = [
	"gee_extraction",
	"validators",
	"mcda_analysis",
	"lcoe_calculator",
	"performance",
	"config_loader",
	"generate_maps_simple",
	"utils",
	"map_utils",
	"api",
]

# Import submodules lazily but ensure package attributes exist for tests
from importlib import import_module
import logging

logger = logging.getLogger(__name__)

_modules = [
	"gee_extraction",
	"validators",
	"mcda_analysis",
	"lcoe_calculator",
	"performance",
	"config_loader",
	"generate_maps_simple",
	"utils",
	"map_utils",
	"api",
]

for _m in _modules:
	try:
		globals()[_m] = import_module(f".{_m}", package=__name__)
	except Exception as e:
		# Do not fail import of the package if an optional submodule is broken;
		# set attribute to None so tests can patch it safely.
		globals()[_m] = None
		logger.debug(f"Optional submodule scripts.{_m} unavailable: {e}")
