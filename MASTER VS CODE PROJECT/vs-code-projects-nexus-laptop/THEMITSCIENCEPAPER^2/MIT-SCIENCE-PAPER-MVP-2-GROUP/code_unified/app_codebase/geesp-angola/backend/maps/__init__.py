"""
GEESP-Angola Maps Module

Consolidated map generation, export, and orchestration utilities.
"""

# Generator module: MapGenerator class and generate_all_maps
from .generator import MapGenerator, generate_all_maps

# Exporters module: PDF and image export functions
from .exporters import (
    process_png_to_styled_pdf,
    enhance_image_contrast,
    enhance_colorfulness,
    boost_brightness,
    add_compass_rose,
    add_scale_bar,
    add_coordinate_grid,
    create_legend,
)

__all__ = [
    "MapGenerator",
    "generate_all_maps",
    "process_png_to_styled_pdf",
    "enhance_image_contrast",
    "enhance_colorfulness",
    "boost_brightness",
    "add_compass_rose",
    "add_scale_bar",
    "add_coordinate_grid",
    "create_legend",
    "run_all_maps",
    "prepare_map_data",
]
