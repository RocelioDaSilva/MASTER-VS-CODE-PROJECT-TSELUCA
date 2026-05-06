# Dashboard pages package (stubs for tests)
from .home import render as home_render
from .data_explore import render as data_explore_render
from .mcda import render as mcda_render
from .results import render as results_render
from .lcoe import render as lcoe_render
__all__ = ["home_render", "data_explore_render", "mcda_render", "results_render", "lcoe_render"]
