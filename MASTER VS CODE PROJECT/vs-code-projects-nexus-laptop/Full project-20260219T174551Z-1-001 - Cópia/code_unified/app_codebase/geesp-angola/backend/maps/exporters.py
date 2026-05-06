"""
Enhanced PDF Map Generation with Styling, Metadata, and Cartographic Elements

This module converts PNG map images to Professional PDF files with:
- Map title and metadata (date, CRS, resolution)
- Color-enhanced styling (histogram equalization, contrast boost)
- Compass rose (N/S/E/W indicator)
- Scale bar with measurements
- Legend with data layer information
- Coordinate grid overlay
- Copyright/attribution footer

Usage:
    python enhanced_maps_to_pdf.py
    
Output:
    Saves enhanced PDFs to data/processed/ with matching PNG basenames
"""

import os
import sys
from pathlib import Path
from datetime import datetime

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties
from utils.constants import MapGenerationConstants
from utils.logging import setup_logging


# ============================================================================
# CONFIGURATION
# ============================================================================

INPUT_DIR = Path(MapGenerationConstants.OUTPUT_DIR_DEFAULT)
OUTPUT_DIR = INPUT_DIR
RESOLUTION_DPI = MapGenerationConstants.VIZ_DPI_SAVE
MARGIN_MM = MapGenerationConstants.MARGIN_MM  # Page margins

# Map styling parameters
STYLE_CONFIG = {
    "mapa_irradiacao": {
        "title": "Solar Irradiance Map",
        "units": "kWh/m²/day",
        "color_scheme": "YlOrRd",
        "is_numeric": True,
        "enhance_contrast": True,
        "enhance_colorfulness": 1.3,
    },
    "mapa_populacao": {
        "title": "Population Density Map",
        "units": "people/km²",
        "color_scheme": "Reds",
        "is_numeric": True,
        "enhance_contrast": True,
        "enhance_colorfulness": 1.2,
    },
    "mapa_distanciarede": {
        "title": "Distance to Electrical Grid",
        "units": "kilometers",
        "color_scheme": "Blues_r",
        "is_numeric": True,
        "enhance_contrast": True,
        "enhance_colorfulness": 1.1,
    },
    "mapa_declividade": {
        "title": "Terrain Slope Map",
        "units": "degrees",
        "color_scheme": "RdYlGn_r",
        "is_numeric": True,
        "enhance_contrast": False,
        "enhance_colorfulness": 1.0,
    },
    "mapa_ndvi": {
        "title": "Vegetation Index (NDVI)",
        "units": "-1.0 to +1.0",
        "color_scheme": "RdYlGn",
        "is_numeric": True,
        "enhance_contrast": True,
        "enhance_colorfulness": 1.2,
    },
    "mapa_aptidao": {
        "title": "Site Suitability Index (MCDA Overlay)",
        "units": "0.0 to 1.0",
        "color_scheme": "viridis",
        "is_numeric": True,
        "enhance_contrast": True,
        "enhance_colorfulness": 1.4,
    },
}

# ============================================================================
# LOGGING SETUP
# ============================================================================

logger = setup_logging(__name__)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def enhance_image_contrast(image: Image.Image) -> Image.Image:
    """Apply histogram equalization for better visibility.
    
    Args:
        image: PIL Image object to enhance
        
    Returns:
        Enhanced PIL Image with improved contrast
    """
    # Convert to numpy array
    img_array: np.ndarray = np.array(image.convert("RGB"))

    # Apply histogram equalization per channel
    for i in range(3):
        hist, bins = np.histogram(img_array[:, :, i].flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * (255 / cdf.max())
        img_array[:, :, i] = np.interp(
            img_array[:, :, i].flatten(), bins[:-1], cdf_normalized
        ).reshape(img_array[:, :, i].shape)

    return Image.fromarray(np.uint8(img_array))


def enhance_colorfulness(image: Image.Image, factor: float = 1.2) -> Image.Image:
    """Increase color saturation and vibrancy.
    
    Args:
        image: PIL Image to enhance
        factor: Enhancement factor (>1.0 increases saturation)
        
    Returns:
        Enhanced PIL Image with increased color saturation
    """
    enhancer: ImageEnhance.Color = ImageEnhance.Color(image)
    return enhancer.enhance(factor)


def boost_brightness(image: Image.Image, factor: float = 1.1) -> Image.Image:
    """Increase brightness slightly.
    
    Args:
        image: PIL Image to enhance
        factor: Brightness factor (>1.0 increases brightness)
        
    Returns:
        Enhanced PIL Image with increased brightness
    """
    enhancer: ImageEnhance.Brightness = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def _resolve_font(bold: bool = False, size: int = 12) -> ImageFont.FreeTypeFont:
    """Resolve a TrueType font cross-platform, falling back to PIL default."""
    candidates = [
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        # Windows
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def add_compass_rose(draw: ImageDraw.ImageDraw, x: int, y: int, size: int = MapGenerationConstants.COMPASS_SIZE) -> None:
    """Draw a compass rose (N/S/E/W indicator) on the map.
    
    Args:
        draw: ImageDraw object for drawing
        x: X coordinate of compass center
        y: Y coordinate of compass center
        size: Compass rose size in pixels
    """
    # Outer circle
    draw.ellipse([x - size, y - size, x + size, y + size], outline="black", width=2)  # type: ignore

    # Cardinal directions
    font_size = max(MapGenerationConstants.SMALL_FONT_SIZE, size // 4)
    font = _resolve_font(bold=True, size=font_size)

    offset = int(size * 0.2) + 15

    # N (north - top, red)
    draw.text((x, y - size - offset), "N", fill="red", font=font, anchor="mm")
    draw.line([(x, y - size), (x, y - size + offset)], fill="red", width=3)

    # S (south - bottom)
    draw.text((x, y + size + offset), "S", fill="black", font=font, anchor="mm")
    draw.line([(x, y + size), (x, y + size - offset)], fill="black", width=2)

    # E (east - right)
    draw.text((x + size + offset, y), "E", fill="black", font=font, anchor="mm")
    draw.line([(x + size, y), (x + size - offset, y)], fill="black", width=2)

    # W (west - left)
    draw.text((x - size - offset, y), "W", fill="black", font=font, anchor="mm")
    draw.line([(x - size, y), (x - size + offset, y)], fill="black", width=2)


def add_scale_bar(draw: ImageDraw.ImageDraw, x: int, y: int, scale_km: float = 50) -> None:
    """Draw a scale bar with distance labels.
    
    Args:
        draw: ImageDraw object for drawing
        x: X coordinate of scale bar start
        y: Y coordinate of scale bar baseline
        scale_km: Scale in kilometers
    """
    # Scale bar dimensions
    bar_length_px = MapGenerationConstants.SCALE_BAR_LENGTH_PX
    bar_height = MapGenerationConstants.SCALE_BAR_HEIGHT

    pad = 10

    # Background rectangle
    draw.rectangle(
        [x - pad, y - bar_height - pad, x + bar_length_px + pad, y + pad],
        fill="white",
        outline="black",
        width=2,
    )

    # Scale bar line
    draw.rectangle([x, y - bar_height // 2, x + bar_length_px, y + bar_height // 2], fill="black")

    # Tick marks (4 segments)
    n_ticks = 4
    tick_step = max(1, bar_length_px // n_ticks)
    for i in range(0, bar_length_px + 1, tick_step):
        draw.line([(x + i, y - bar_height), (x + i, y + bar_height)], fill="black", width=2)

    # Labels
    font = _resolve_font(bold=False, size=MapGenerationConstants.SMALL_FONT_SIZE)

    draw.text((x, y + pad + 5), "0 km", font=font, anchor="lt", fill="black")
    draw.text((x + bar_length_px, y + pad + 5), f"{scale_km} km", font=font, anchor="rt", fill="black")


def add_coordinate_grid(
    image: Image.Image, num_gridlines: int = 4, grid_color: tuple = (200, 200, 200), width: int = 1
) -> Image.Image:
    """Add coordinate grid overlay.
    
    Args:
        image: PIL Image to overlay grid on
        num_gridlines: Number of gridlines in each direction
        grid_color: RGB color tuple for gridlines
        width: Line width in pixels
        
    Returns:
        Modified PIL Image with grid overlay
    """
    draw = ImageDraw.Draw(image, "RGBA")
    width_px, height_px = image.size

    alpha = int(255 * MapGenerationConstants.VIZ_GRID_ALPHA)

    # Vertical gridlines
    for i in range(1, num_gridlines):
        x = int(width_px * i / num_gridlines)
        draw.line([(x, 0), (x, height_px)], fill=(*grid_color, alpha), width=width)

    # Horizontal gridlines
    for i in range(1, num_gridlines):
        y = int(height_px * i / num_gridlines)
        draw.line([(0, y), (width_px, y)], fill=(*grid_color, alpha), width=width)

    return image


def create_legend(layer_name: str, config: dict) -> Image.Image:
    """Create a legend box showing data range and units.
    
    Args:
        layer_name: Name of the data layer (e.g., 'mapa_irradiacao')
        config: Configuration dictionary with title, units, range info
        
    Returns:
        PIL Image object containing the legend
    """
    legend_width = MapGenerationConstants.LEGEND_WIDTH
    legend_height = MapGenerationConstants.LEGEND_HEIGHT

    # Create legend image with white background
    legend_img = Image.new("RGB", (legend_width, legend_height), color="white")
    draw = ImageDraw.Draw(legend_img)

    # Border
    draw.rectangle([0, 0, legend_width - 1, legend_height - 1], outline="black", width=2)

    # Title
    title_font = _resolve_font(bold=True, size=MapGenerationConstants.DEFAULT_FONT_SIZE)
    text_font = _resolve_font(bold=False, size=MapGenerationConstants.SMALL_FONT_SIZE)

    pad = 10
    line_height = 30

    title = config["title"]
    draw.text((pad, pad), title, fill="black", font=title_font)

    # Units and metadata
    units = config["units"]
    draw.text((pad, pad + line_height), f"Units: {units}", fill="black", font=text_font)

    # Color scheme indicator
    draw.text((pad, pad + line_height * 2), f"Scheme: {config['color_scheme']}", fill="black", font=text_font)

    # Generated timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    draw.text((pad, pad + line_height * 3), f"Generated: {timestamp}", fill="gray", font=text_font)

    return legend_img


def add_metadata_footer(
    draw: ImageDraw.ImageDraw, width: int, height: int, layer_name: str, config: dict
):
    """Add metadata footer to map."""
    font = _resolve_font(bold=False, size=MapGenerationConstants.SMALL_FONT_SIZE)

    footer_pad = MapGenerationConstants.MARGIN_MM * 2
    footer_y = height - footer_pad
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    footer_text = (
        f"{config['title']} | {config['units']} | Generated: {timestamp} | "
        f"CRS: EPSG:4326 | Resolution: {RESOLUTION_DPI} DPI"
    )

    # Background rectangle for footer
    draw.rectangle(
        [0, footer_y - 15, width, height],
        fill=(240, 240, 240),
    )

    pad = MapGenerationConstants.MARGIN_MM
    draw.text((pad, footer_y - 10), footer_text, fill="black", font=font)
    draw.text((width - 150, footer_y - 10), "© GEESP-Angola 2026", fill="gray", font=font)


def process_png_to_styled_pdf(png_path: Path) -> bool:
    """
    Convert PNG map to enhanced PDF with styling, metadata, and cartographic elements.

    Args:
        png_path: Path to PNG file

    Returns:
        bool: True if successful, False otherwise
    """
    pdf_path = png_path.with_suffix(".pdf")
    layer_name = png_path.stem

    logger.info(f"Processing: {png_path.name}")

    # Get configuration for this layer
    config = STYLE_CONFIG.get(layer_name, {
        "title": layer_name.replace("_", " ").title(),
        "units": "unknown",
        "color_scheme": "viridis",
        "is_numeric": True,
        "enhance_contrast": True,
        "enhance_colorfulness": 1.2,
    })

    try:
        # Step 1: Load image
        img = Image.open(png_path).convert("RGB")
        original_size = img.size
        logger.info(f"  Loaded: {original_size} pixels")

        # Step 2: Enhance image
        if config.get("enhance_contrast"):
            img = enhance_image_contrast(img)
            logger.info("  ✓ Contrast enhanced")

        if config.get("enhance_colorfulness", 1.0) > 1.0:
            img = enhance_colorfulness(img, config["enhance_colorfulness"])
            logger.info("  ✓ Colorfulness enhanced")

        # Slight brightness boost
        img = boost_brightness(img, 1.05)

        # Step 3: Add cartographic elements
        overlay = img.copy()
        draw = ImageDraw.Draw(overlay, "RGBA")

        width, height = overlay.size
        grid_lines = 5
        grid_color_rgb = (150, 150, 150)

        # Add coordinate grid (subtle)
        overlay = add_coordinate_grid(overlay, num_gridlines=grid_lines, grid_color=grid_color_rgb, width=1)
        logger.info("  ✓ Coordinate grid added")

        # Add compass rose (top-right)
        compass_margin = MapGenerationConstants.MARGIN_MM * 5
        compass_y_offset = compass_margin
        add_compass_rose(draw, width - compass_margin, compass_y_offset, size=MapGenerationConstants.COMPASS_SIZE)
        logger.info("  ✓ Compass rose added")

        # Add scale bar (bottom-left)
        scale_margin = MapGenerationConstants.MARGIN_MM * 3
        scale_y_offset = height - (MapGenerationConstants.MARGIN_MM * 6)
        add_scale_bar(draw, scale_margin, scale_y_offset, scale_km=50)
        logger.info("  ✓ Scale bar added")

        # Add metadata footer
        add_metadata_footer(draw, width, height, layer_name, config)
        logger.info("  ✓ Metadata footer added")

        # Step 4: Create figure with map and legend
        fig_width, fig_height = 11, 14  # A4 size (inches)
        fig = plt.figure(figsize=(fig_width, fig_height))
        gs = fig.add_gridspec(10, 10, hspace=0.3, wspace=0.2)

        # Map (main area)
        ax_map = fig.add_subplot(gs[0:8, 0:8])
        ax_map.imshow(overlay)
        ax_map.axis("off")
        ax_map.set_title(config["title"], fontsize=MapGenerationConstants.VIZ_TITLE_FONTSIZE, fontweight="bold", pad=10)

        # Legend (right side)
        ax_legend = fig.add_subplot(gs[0:4, 8:10])
        legend_img = create_legend(layer_name, config)
        ax_legend.imshow(legend_img)
        ax_legend.axis("off")

        # Metadata table (bottom-right)
        ax_metadata = fig.add_subplot(gs[5:8, 8:10])
        ax_metadata.axis("off")

        metadata_text = f"""
        Layer: {layer_name}
        Units: {config['units']}
        CRS: EPSG:4326
        Res: {RESOLUTION_DPI} DPI
        Date: {datetime.now().strftime('%Y-%m-%d')}
        """

        ax_metadata.text(0.05, 0.95, metadata_text, transform=ax_metadata.transAxes,
                        fontsize=MapGenerationConstants.SMALL_FONT_SIZE, verticalalignment="top", family="monospace",
                        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

        # Step 5: Save as PDF
        fig.savefig(pdf_path, format="pdf", dpi=RESOLUTION_DPI, bbox_inches="tight", 
                   facecolor="white", edgecolor="none")
        plt.close(fig)
        
        file_size_kb = pdf_path.stat().st_size / 1024
        logger.info(f"  ✓ PDF created: {pdf_path.name} ({file_size_kb:.1f} KB)")

        return True

    except Exception as e:
        logger.error(f"  ✗ Failed: {e}", exc_info=True)
        return False


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def main():
    """Main entry point."""
    logger.info("=" * 70)
    logger.info("Enhanced Map PDF Generation Started")
    logger.info(f"Input directory: {INPUT_DIR}")
    logger.info(f"Output directory: {OUTPUT_DIR}")
    logger.info(f"Resolution: {RESOLUTION_DPI} DPI")
    logger.info("=" * 70)
    logger.info("")

    # Find all PNG files
    png_files = sorted(INPUT_DIR.glob("*.png"))

    if not png_files:
        logger.warning(f"No PNG files found in {INPUT_DIR}")
        return 1

    logger.info(f"Found {len(png_files)} PNG files to process")
    logger.info("")

    # Process each PNG
    success_count = 0
    for png_file in png_files:
        if process_png_to_styled_pdf(png_file):
            success_count += 1
        logger.info("")

    # Summary
    logger.info("=" * 70)
    logger.info(f"Processing Complete: {success_count}/{len(png_files)} successful")
    logger.info("=" * 70)

    return 0 if success_count == len(png_files) else 1


if __name__ == "__main__":
    sys.exit(main())
