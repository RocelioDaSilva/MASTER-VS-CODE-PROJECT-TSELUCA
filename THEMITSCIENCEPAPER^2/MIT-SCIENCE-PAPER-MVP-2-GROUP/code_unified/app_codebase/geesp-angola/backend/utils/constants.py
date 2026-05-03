"""
GEESP-Angola: Centralized Constants and Configuration
Eliminates magic numbers and centralizes all configuration values
"""

from enum import Enum
from typing import Dict, List, Tuple
from dataclasses import dataclass

# ============================================================================
# MCDA & AHP Constants
# ============================================================================

class MCDAConstants:
    """Multi-Criteria Decision Analysis constants"""

    # Aptitude classification thresholds
    APTITUDE_THRESHOLDS = [0.25, 0.75]  # Low/Medium/High
    APTITUDE_LOW = 0.25
    APTITUDE_MEDIUM = 0.75
    APTITUDE_HIGH = 1.0

    # AHP (Analytic Hierarchy Process)
    AHP_CONSISTENCY_THRESHOLD = 0.10  # Max acceptable CR (Consistency Ratio)
    AHP_SAATY_SCALE = {
        1: "Equally important",
        3: "Moderately more important",
        5: "Strongly more important",
        7: "Very strongly more important",
        9: "Absolutely more important",
    }
    
    # Saaty Random Index Table (for consistency ratio calculation)
    AHP_RANDOM_INDEX = {
        1: 0.0,
        2: 0.0,
        3: 0.58,
        4: 0.90,
        5: 1.12,
        6: 1.24,
        7: 1.32,
        8: 1.41,
        9: 1.45,
        10: 1.49,
    }

    # Normalization
    NORMALIZATION_MIN = 0.0
    NORMALIZATION_MAX = 100.0
    NORMALIZATION_NAN_VALUE = 0.0

    # Default criteria weights (if not provided by user)
    # NOTE: 6 criteria as specified in manuscript SOL.tex (lines 64, 136, 152)
    DEFAULT_WEIGHTS = {
        "Irradiação Solar": 0.25,
        "Densidade Populacional": 0.20,
        "Acesso (Distância Rede)": 0.20,
        "Infraestrutura (Declividade)": 0.10,
        "Uso do Solo (NDVI)": 0.15,
        "Luminosidade Noturna (VIIRS)": 0.10,
    }

    # Weight adjustment ranges for UI sliders
    WEIGHT_MIN = 0
    WEIGHT_MAX = 100
    
    # Raster normalization ranges for specific layers (min, max for each criterion)
    RASTER_WEIGHTS = {
        "irradiacao": 0.25,
        "populacao": 0.20,
        "distancia_rede": 0.20,
        "declividade": 0.10,
        "ndvi": 0.15,
        "luminosidade_noturna": 0.10,
    }
    
    # Normalization ranges for raster data [min, max]
    RASTER_NORMALIZATION_RANGES = {
        "solar_irradiance": (5.5, 6.4),      # kWh/m²/day
        "population_density": (10, 95),       # people/km²
        "grid_distance": (0, 45),             # km
        "slope": (0, 30),                     # degrees
        "ndvi": (-0.2, 0.7),                  # dimensionless
        "nighttime_lights": (0, 50),          # nanoWatts/cm²/sr (VIIRS DNB)
    }
    
    # Alternative raster weights with English keys
    RASTER_WEIGHTS_ENGLISH = {
        "solar_irradiance": 0.25,
        "population_density": 0.20,
        "grid_distance": 0.20,
        "slope": 0.10,
        "vegetation_ndvi": 0.15,
        "nighttime_lights": 0.10,
    }

    # Sensitivity analysis parameters
    SENSITIVITY_DEFAULT_RANGE = 20  # ±20%
    SENSITIVITY_DEFAULT_STEPS = 5   # 5% increments


class GeoConstants:
    """Geospatial data constants"""

    # Raster resolution
    RASTER_RESOLUTION_KM = 1
    RASTER_RESOLUTION_M = RASTER_RESOLUTION_KM * 1000

    # CRS (Coordinate Reference System)
    DEFAULT_CRS = "EPSG:32734"  # UTM Zone 34S (Angola)
    WGS84_CRS = "EPSG:4326"

    # Clipping buffer
    CLIP_BUFFER_KM = 5
    CLIP_BUFFER_PIXELS = CLIP_BUFFER_KM // RASTER_RESOLUTION_KM

    # Scaling for visualization
    RESCALE_FACTOR = 0.5  # Reduce memory for web display

    # Null/no-data values
    NODATA_VALUE = -9999
    VALID_DATA_THRESHOLD = 0.8  # 80% valid pixels required

    # Angola geographic bounds (approximate)
    ANGOLA_BOUNDS = {
        "lat_min": -18.0,
        "lat_max": -4.38,
        "lon_min": 11.67,
        "lon_max": 24.82
    }
    
    # Data validation ranges for spatial criteria
    SOLAR_IRRADIANCE_MIN = 0  # kWh/m²/day (global minimum)
    SOLAR_IRRADIANCE_MAX = 10  # kWh/m²/day (global maximum)
    SOLAR_IRRADIANCE_TYPICAL_MIN = 5  # Angola typical minimum
    SOLAR_IRRADIANCE_TYPICAL_MAX = 7  # Angola typical maximum
    
    POPULATION_DENSITY_MIN = 0  # people/km²
    POPULATION_DENSITY_MAX = 50000  # people/km² (extreme maximum)
    POPULATION_DENSITY_WARNING_THRESHOLD = 10000  # people/km² (very high)
    
    NDVI_MIN = -1.0  # Normalized Difference Vegetation Index minimum
    NDVI_MAX = 1.0  # NDVI maximum
    NDVI_WATER_THRESHOLD = -0.1  # Values < this indicate water
    NDVI_BARREN_THRESHOLD = 0.1  # Values < this indicate barren/rock
    NDVI_GRASS_THRESHOLD = 0.3  # Values < this indicate grass/shrub
    
    DISTANCE_TO_GRID_MIN = 0  # km (at grid location)
    DISTANCE_TO_GRID_MAX = 500  # km (maximum meaningful distance)
    DISTANCE_TO_GRID_TYPICAL_MAX = 200  # km (typical service area)
    
    SLOPE_MIN = 0  # degrees
    SLOPE_MAX = 90  # degrees (maximum)
    SLOPE_PRACTICAL_MAX = 30  # degrees (practical installation limit)

    # Export task retry configuration
    MAX_EXPORT_RETRIES = 3  # Maximum attempts for failed exports
    EXPORT_TIMEOUT_SECONDS = 3600  # 1 hour timeout per export


class SolarConstants:
    """Solar energy specific constants"""

    # Solar irradiance ranges (kWh/m²/day)
    GHI_EXCELLENT = 6.5
    GHI_GOOD = 6.0
    GHI_ACCEPTABLE = 5.5
    GHI_POOR = 5.0

    # Solar irradiance data sources
    NASA_POWER_BAND = "ALLSKY_SFC_SW_DWN"  # Downwelling shortwave radiation
    MODIS_BAND = "LST_Day_1km"

    # Panel efficiency
    PANEL_EFFICIENCY_MIN = 0.16  # 16%
    PANEL_EFFICIENCY_MAX = 0.22  # 22%
    PANEL_EFFICIENCY_DEFAULT = 0.18  # 18%

    # Temperature derating
    TEMPERATURE_COEFFICIENT = -0.004  # -0.4% per °C


class PopulationConstants:
    """Population and demand constants"""

    # Viable community size thresholds
    MIN_VIABLE_POP = 100  # Minimum for mini-grid
    OPTIMAL_MINI_GRID_POP = 500
    MAX_FOR_SHS = 200  # SHS = Solar Home System

    # Population density (people/km²)
    DENSE = 1000
    MODERATE = 300
    SPARSE = 100


class InfrastructureConstants:
    """Infrastructure related constants"""

    # Grid distances (km)
    ISOLATED_THRESHOLD = 8  # >8km = off-grid
    PROXIMITY_THRESHOLD = 5  # <5km = can integrate with grid
    FEASIBLE_MAX_DISTANCE = 50  # Absolute maximum distance considered

    # Access roads
    MIN_ROAD_DISTANCE = 2  # km from village access road

    # Water availability (critical for hybrid systems)
    HAS_WATER = 1
    NO_WATER = 0


class LCOEConstants:
    """Levelized Cost of Energy (LCOE) constants"""

    # Financial parameters (all in USD)
    PROJECT_LIFETIME_YEARS = 20
    PROJECT_LIFETIME_MIN = 10
    PROJECT_LIFETIME_MAX = 40
    DEFAULT_DISCOUNT_RATE = 0.08  # 8%
    DISCOUNT_RATE = 0.08  # 8%
    DISCOUNT_RATE_MIN = 1  # 1%
    DISCOUNT_RATE_MAX = 15  # 15%

    # Solar irradiance
    DEFAULT_ANNUAL_IRRADIANCE = 2226  # kWh/m²/year for Angola
    IRRADIANCE_MIN_ANNUAL = 1000
    IRRADIANCE_MAX_ANNUAL = 3000

    # CAPEX estimates by technology ($/Wp for PV)
    PV_CAPEX_MIN = 0.8  # Optimistic
    PV_CAPEX_TYPICAL = 1.1  # Typical
    PV_CAPEX_HIGH = 1.5  # Conservative

    # Battery costs ($/kWh)
    BATTERY_CAPEX_LI_ION = 250  # $/kWh (improving rapidly)
    BATTERY_CAPEX_LEAD_ACID = 150  # $/kWh (cheaper but shorter life)

    # OPEX (% of CAPEX annually)
    OPEX_PERCENTAGE = 0.02  # 2% per year
    MAINTENANCE_ANNUAL = 0.01  # 1% for maintenance

    # Fuel costs
    DIESEL_PRICE_PER_LITER = 1.50  # USD
    DIESEL_FUEL_EFFICIENCY = 0.33  # kWh per liter

    # LCOE targets for viability
    LCOE_THRESHOLD_VIABLE = 0.35  # USD/kWh
    LCOE_THRESHOLD_EXCELLENT = 0.25  # USD/kWh

    # Load factors
    SOLAR_CAPACITY_FACTOR = 0.18  # 18% average
    DIESEL_CAPACITY_FACTOR = 0.40  # 40% average

    # System-level parameters
    SYSTEM_EFFICIENCY_PV = 0.18  # 18% typical PV efficiency
    ANNUAL_DEGRADATION_RATE = 0.5  # 0.5% per year
    OPEX_INFLATION_RATE = 0.02  # 2% annual increase
    OPEX_MAINTENANCE_RATE = 0.03  # 3% annual maintenance
    AREA_PER_KW_SQM = 7.5  # Standard PV footprint
    WARRANTY_YEARS = 10  # Standard warranty period

    # Technology-specific CAPEX (USD/kW)
    TECHNOLOGY_COSTS = {
        "PV_Fixed": {
            "name": "PV Fixo",
            "pv_module": 170,
            "inverter": 80,
            "bop": 80,  # Balance of Plant
            "installation": 150,
            "total_capex": 880,
        },
        "PV_Tracker": {
            "name": "PV com Rastreador de Eixo Único",
            "pv_module": 200,
            "tracker": 150,  # Single-axis tracking system
            "inverter": 80,
            "bop": 120,
            "installation": 170,
            "total_capex": 920,
        },
        "Hybrid_Solar_Diesel": {
            "name": "Híbrido Solar + Diesel + Baterias",
            "pv_module": 200,
            "diesel_gen": 300,  # Diesel generator (USD/kW)
            "battery": 200,
            "inverter": 120,
            "bop": 150,
            "installation": 200,
            "total_capex": 1170,
        },
    }

    # Technology-specific OPEX (% CAPEX/year, USD/MWh)
    TECHNOLOGY_OPEX = {
        "PV_Fixed": {"fixed": 1.5, "variable": 5.0},
        "PV_Tracker": {"fixed": 2.0, "variable": 6.0},
        "Hybrid_Solar_Diesel": {"fixed": 3.0, "variable": 25.0},
    }


class EnvironmentalConstants:
    """Environmental and land-use constants"""

    # NDVI ranges
    NDVI_VEGETATION_MIN = 0.3  # Minimum for vegetation
    NDVI_GOOD = 0.5  # Good vegetation
    NDVI_DEGRADED = 0.3  # Degraded vegetatione

    # Slope (degrees)
    SLOPE_OPTIMAL_MAX = 10  # Degrees
    SLOPE_ACCEPTABLE_MAX = 20  # Degrees
    SLOPE_POOR_MIN = 30  # >30° is problematic

    # Land-use compatibility
    COMPATIBLE_LAND_TYPES = ["grassland", "shrubland", "cropland", "bare_ground"]


class FinancialConstants:
    """Financial report and analysis constants"""

    # Report visualization colors (hex codes)
    COLOR_PRIMARY = '#2E86AB'
    COLOR_SECONDARY = '#A23B72'
    COLOR_SUCCESS = '#06A77D'
    COLOR_WARNING = '#F18F01'
    COLOR_DANGER = '#C73E1D'
    COLOR_LIGHT_GRAY = '#F0F0F0'
    COLOR_DARK_GRAY = '#333333'
    
    COLOR_PALETTE = {
        'primary': COLOR_PRIMARY,
        'secondary': COLOR_SECONDARY,
        'success': COLOR_SUCCESS,
        'warning': COLOR_WARNING,
        'danger': COLOR_DANGER,
        'light_gray': COLOR_LIGHT_GRAY,
        'dark_gray': COLOR_DARK_GRAY,
    }

    # Financial analysis parameters
    PROJECT_LIFETIME_DEFAULT = 25  # years
    DISCOUNT_RATE_INIT = 0.1  # Initial rate for Newton-Raphson (10%)
    IRR_MAX_ITERATIONS = 100  # Newton-Raphson iterations for IRR calculation
    IRR_TOLERANCE = 1e-6  # Convergence tolerance

    # Report generation
    SENSITIVITY_SAMPLE_SIZE = 13  # Number of sensitivity analysis samples
    SENSITIVITY_RANGE_PERCENT = 30  # ±30% variation for sensitivity


class OperationalConstants:
    """Operational and automation constants"""

    # Cron/scheduling timeouts
    ETL_PIPELINE_TIMEOUT_SECONDS = 600  # 10 minutes for ETL pipeline
    EARTH_ENGINE_TIMEOUT_SECONDS = 1800  # 30 minutes for Earth Engine operations
    DATABASE_BACKUP_TIMEOUT_SECONDS = 300  # 5 minutes for database backup

    # Earth Engine regions (pre-defined bounds as (west, south, east, north))
    EE_REGION_ANGOLA = [-5.92, 11.20, 24.10, -4.38]
    EE_REGION_LUANDA = [13.20, 8.80, 13.60, 8.40]
    EE_REGION_HUAMBO = [15.70, 12.90, 16.20, 12.40]
    EE_REGION_BENGUELA = [13.20, 13.60, 14.40, 12.20]

    # Earth Engine dataset configurations
    EE_DATASET_SOLAR_COLLECTION = 'NOAA/GFSANL'
    EE_DATASET_SOLAR_BAND = 'DSWRF_surface'
    EE_DATASET_ELEVATION_COLLECTION = 'USGS/SRTMGL1_Ellip/SRTM30'
    EE_DATASET_ELEVATION_BAND = 'elevation'
    EE_DATASET_LANDCOVER_COLLECTION = 'COPERNICUS/Lc100/LCQS/timmulticov'
    EE_DATASET_LANDCOVER_BAND = 'lc'
    EE_DATASET_NDVI_COLLECTION = 'MODIS/061/MOD13Q1'
    EE_DATASET_NDVI_BAND = 'NDVI'
    EE_DATASET_LST_COLLECTION = 'MODIS/061/MOD11A2'
    EE_DATASET_LST_BAND = 'LST_Day_1km'
    EE_DATASET_POPULATION_COLLECTION = 'CIESIN/GPWv411/GPW_Population_Count'
    EE_DATASET_POPULATION_BAND = 'population_count'

    # ETL batch settings
    ETL_BATCH_SIZE = 1000  # Records per batch
    ETL_LOG_FILE = 'data_ingestion.log'


class ValidationConstants:
    """Validation parameter ranges and thresholds"""
    
    # Weight validation tolerance
    WEIGHTS_TOLERANCE = 0.01  # ±1% deviation from 1.0
    WEIGHTS_TOLERANCE_STRICT = 0.001  # ±0.1% (strict)
    
    # Solar capacity (MW)
    CAPACITY_MW_MIN = 0.1  # Minimum viable solar installation
    CAPACITY_MW_MAX = 500  # Maximum considered size
    
    # Annual irradiance (kWh/m²/year)
    IRRADIANCE_ANNUAL_MIN = 500  # Minimum viable
    IRRADIANCE_ANNUAL_MAX = 3500  # Maximum realistic
    IRRADIANCE_ANNUAL_TYPICAL_MIN = 1500  # Typical Angola minimum
    IRRADIANCE_ANNUAL_TYPICAL_MAX = 2500  # Typical Angola maximum
    
    # Discount rate (%)
    DISCOUNT_RATE_MIN = -100  # Allow negative (unusual)
    DISCOUNT_RATE_MAX = 100  # Allow very high
    DISCOUNT_RATE_WARNING_THRESHOLD = 25  # Warn if > 25%
    DISCOUNT_RATE_TYPICAL_MIN = 5  # Typical range for EMs
    DISCOUNT_RATE_TYPICAL_MAX = 12  # Typical range for EMs
    
    # Project lifetime (years)
    PROJECT_LIFETIME_MIN = 5  # Minimum considered
    PROJECT_LIFETIME_MAX = 50  # Maximum considered
    PROJECT_LIFETIME_TYPICAL = 20  # Standard for solar PV
    
    # Probability array bounds
    PROBABILITY_MIN = 0.0
    PROBABILITY_MAX = 1.0
    
    # Raster shape defaults (height, width pixels)
    RASTER_SHAPE_DEFAULT = (280, 300)
    RASTER_SHAPE_MIN = (50, 50)  # Minimum usable resolution
    RASTER_SHAPE_MAX = (5000, 5000)  # Maximum for performance


class MapGenerationConstants:
    """Synthetic map generation parameters for GEESP demonstration"""
    
    # Raster dimensions
    MAP_WIDTH_PIXELS = 300
    MAP_HEIGHT_PIXELS = 280
    MAP_SHAPE = (MAP_HEIGHT_PIXELS, MAP_WIDTH_PIXELS)
    
    # UTM coordinate system
    MAP_CRS = "EPSG:32733"  # UTM Zone 33S
    
    # UTM bounds for Huíla region (meters)
    MAP_WEST_UTM = 500000
    MAP_SOUTH_UTM = 8000000
    MAP_EAST_UTM = 530000
    MAP_NORTH_UTM = 8078500
    
    # Solar radiation parameters
    SOLAR_MAX = 6.4      # kWh/m²/day
    SOLAR_MIN = 5.5      # kWh/m²/day
    SOLAR_NOISE_AMP = 0.3  # Amplitude of sinusoidal noise
    SOLAR_SINE_MULT = 3  # Sine wave multiplier for east-west variation
    SOLAR_COSINE_MULT = 4  # Cosine wave multiplier for north-south variation
    SOLAR_GAUSSIAN_SIGMA = 2  # Smoothing kernel width
    
    # Population density parameters
    POP_CENTER_1_Y = 0.25  # Caçula (fraction of height)
    POP_CENTER_1_X = 0.45  # Caçula (fraction of width)
    POP_CENTER_2_Y = 0.75  # Humpata (fraction of height)
    POP_CENTER_2_X = 0.65  # Humpata (fraction of width)
    POP_CENTER_3_Y = 0.55  # Quilengues (fraction of height)
    POP_CENTER_3_X = 0.30  # Quilengues (fraction of width)
    POP_INTENSITY_1 = 45   # Caçula intensity
    POP_INTENSITY_2 = 60   # Humpata intensity
    POP_INTENSITY_3 = 55   # Quilengues intensity
    POP_POISSON_LAMBDA = 5  # Poisson noise parameter
    POP_GAUSSIAN_SIGMA = 3  # Smoothing kernel width
    POP_GAUSSIAN_CENTER = 1500  # Gaussian center spread
    POP_MIN = 10           # Minimum population value
    POP_MAX = 95           # Maximum population value
    POP_SCALE_RANGE = 85   # Scaling range (max - min)
    
    # Distance to grid parameters
    DISTANCE_GRID_ROW_FRAC = 0.3   # Horizontal grid line position
    DISTANCE_GRID_COL_FRAC = 0.4   # Vertical grid line position
    DISTANCE_DIAGONAL_SLOPE = 0.18  # Diagonal transmission line slope
    DISTANCE_MIN = 0               # Minimum distance (km)
    DISTANCE_MAX = 45              # Maximum distance (km)
    
    # Slope parameters
    SLOPE_X_RANGE = 3                # X coordinate range for DEM
    SLOPE_Y_RANGE = 3                # Y coordinate range for DEM
    SLOPE_ELEVATION_BASE = 2000      # Base elevation (meters)
    SLOPE_SINE_AMP = 200             # Sine amplitude for elevation
    SLOPE_COSINE_AMP = 150           # Cosine amplitude for elevation
    SLOPE_NOISE_STD = 50             # Standard deviation of elevation noise
    SLOPE_MIN = 0                    # Minimum slope (degrees)
    SLOPE_MAX = 30                   # Maximum slope (degrees)
    
    # NDVI parameters
    NDVI_X_RANGE = 1                 # X coordinate range
    NDVI_Y_RANGE = 1                 # Y coordinate range
    NDVI_BASE_VALUE = 0.3            # Base NDVI value
    NDVI_Y_COEFFICIENT = 0.35        # Y-direction coefficient
    NDVI_AMPLITUDE = 0.1             # Noise amplitude
    NDVI_SINE_MULT = 4               # Sine wave multiplier
    NDVI_COSINE_MULT = 3             # Cosine wave multiplier
    NDVI_GAUSSIAN_SIGMA = 2          # Smoothing kernel width
    NDVI_MIN = -0.2                  # Minimum NDVI
    NDVI_MAX = 0.7                   # Maximum NDVI
    
    # Visualization parameters
    VIZ_FIGSIZE = (12, 10)           # Figure size (inches)
    VIZ_DPI_DISPLAY = 100            # Display DPI
    VIZ_DPI_SAVE = 150               # Save DPI for PNG
    VIZ_COLORBAR_FRACTION = 0.046    # Colorbar width fraction
    VIZ_COLORBAR_PAD = 0.04          # Colorbar padding
    VIZ_TITLE_FONTSIZE = 16          # Title font size
    VIZ_LABEL_FONTSIZE = 12          # Axis label font size
    VIZ_GRID_ALPHA = 0.3             # Grid transparency
    
    # Page and annotation defaults for PDF generation
    MARGIN_MM = 10                    # Page margin in millimeters
    SCALE_BAR_LENGTH_PX = 200         # Default visual length of scale bar in pixels
    SCALE_BAR_HEIGHT = 10             # Scale bar height in pixels
    COMPASS_SIZE = 80                 # Compass rose size (px radius)
    LEGEND_WIDTH = 300                # Legend image width (px)
    LEGEND_HEIGHT = 150               # Legend image height (px)
    DEFAULT_FONT_SIZE = 12            # Default annotation font size
    SMALL_FONT_SIZE = 10              # Secondary small font size
    
    # Output
    OUTPUT_DIR_DEFAULT = "data/processed"
    OUTPUT_GEOTIFF_COMPRESS = "lzw"
    OUTPUT_GEOTIFF_NODATA = -9999


class DataPathConstants:
    """File paths and directories"""

    # Data directories
    DATA_RAW_DIR = "data/raw"
    DATA_PROCESSED_DIR = "data/processed"
    DATA_OUTPUTS_DIR = "data/outputs"
    LOGS_DIR = "logs"
    TEMP_DIR = "tmp"

    # File naming conventions
    RASTER_EXTENSION = ".tif"
    VECTOR_EXTENSION = ".shp"
    NUMPY_EXTENSION = ".npy"
    COMMUNITIES_FILE = "communities_45.csv"
    CONFIG_FILE = "config.json"

    # GEE export names
    GEE_EXPORT_BUCKET = "geesp-angola-exports"
    
    # API output file names
    API_LOG_FILE = "logs/geesp_api.log"
    API_OUTPUT_DIR = "data/processed"  # Where API saves results


class TechnicalConstants:
    """Technical/computational constants"""

    # Performance thresholds
    COMPUTATION_TIMEOUT_SECONDS = 60
    API_TIMEOUT_SECONDS = 30
    DATA_LOADING_TIMEOUT_SECONDS = 30  # Timeout for async data loading
    MAX_WORKERS_PARALLEL = 4

    # Memory limits
    MAX_RASTER_SIZE_GB = 2
    CHUNK_SIZE_PIXELS = 1000 * 1000  # 1M pixels per chunk
    ASYNC_CACHE_MAX_SIZE_MB = 1000  # Max cache size for async data loaders

    # Numerical precision
    FLOAT_PRECISION = 1e-10
    WEIGHT_SUM_TOLERANCE = 0.01  # Weights sum to 1.0 ±1%
    
    # Normalization defaults
    NORMALIZATION_MIN_DEFAULT = 0.0
    NORMALIZATION_MAX_DEFAULT = 1.0
    
    # Outlier detection
    OUTLIER_Z_SCORE_THRESHOLD = 3.0  # Standard deviations for outlier detection
    
    # Array statistics thresholds
    FLOAT_COMPARISON_TOLERANCE = 1e-9  # For safe division and comparisons
    RASTER_NAN_VALUE = 0.0  # Default NaN replacement value
    RASTER_NORMALIZATION_DEFAULT = 0.5  # Default normalization midpoint
    FLOAT_COMPARISON_TOLERANCE = 1e-9  # Tolerance for min/max comparison in normalization
    RASTER_NAN_VALUE = 0.0  # Default value for NaN in normalized rasters
    RASTER_NORMALIZATION_DEFAULT = 0.5  # Default normalized value when min==max

    # Validation constraints
    MIN_CRITERIA = 3
    MAX_CRITERIA = 10
    WEIGHT_RANGE = (0.0, 1.0)


class UIConstants:
    """UI/Dashboard constants"""

    # Streamlit configuration
    PAGE_TITLE = "GEESP-Angola Dashboard"
    PAGE_ICON = "☀️"
    LAYOUT = "wide"
    DASHBOARD_TITLE = "GEESP-Angola Dashboard"
    DASHBOARD_ICON = "☀️"
    DASHBOARD_LAYOUT = "wide"
    SIDEBAR_STATE = "expanded"

    # Map display
    MAP_CENTER_LAT = -17.5
    MAP_CENTER_LON = 14.75
    MAP_ZOOM = 8
    MAP_ZOOM_OVERVIEW = 8
    MAP_ZOOM_DETAIL = 12
    MAP_TILE_LAYER = "OpenStreetMap"
    MAP_TILES = "OpenStreetMap"

    # Color schemes
    COLOR_HIGH = "#00AA00"  # Green
    COLOR_MEDIUM = "#FFAA00"  # Orange
    COLOR_LOW = "#AA0000"  # Red
    COLOR_ZONES = {
        "Cacula": "#1f77b4",
        "Humpata": "#ff7f0e",
        "Quilengues": "#2ca02c",
    }

    # Display settings
    DECIMAL_PLACES_LCOE = 3
    DECIMAL_PLACES_PERCENTAGE = 1
    DECIMAL_PLACES_DISTANCE = 2

    # API/REST Configuration
    API_TITLE = "GEESP-Angola Energy Suitability API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "REST API for geospatial energy analysis using MCDA (Multi-Criteria Decision Analysis) and AHP (Analytic Hierarchy Process)"
    API_CONTACT_NAME = "GEESP-Angola Team"
    API_CONTACT_URL = "https://github.com/ISPTEC-Energy/geesp-angola"
    API_CONTACT_EMAIL = "contact@geesp-angola.org"
    API_LICENSE_NAME = "MIT License"
    API_LICENSE_URL = "https://opensource.org/licenses/MIT"
    CORS_ALLOW_ORIGINS = ["*"]  # Restrict in production
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

    # API Output Filenames
    API_OUTPUT_MCDA = "api_mapa_aptidao.npy"
    API_OUTPUT_MCDA_BATCH = "api_mapa_aptidao_batch_{idx}.npy"


class MessageConstants:
    """User-facing messages and labels"""

    # Success messages
    SUCCESS_ANALYSIS = "✅ Analysis completed successfully"
    SUCCESS_EXPORT = "✅ File exported successfully"

    # Error messages
    ERROR_NO_DATA = "❌ No data available for analysis"
    ERROR_INVALID_WEIGHTS = "❌ Weights do not sum to 1.0"
    ERROR_INSUFFICIENT_DATA = "❌ Insufficient data for analysis"

    # Info messages
    INFO_PROCESSING = "⏳ Processing data..."
    INFO_LOADING = "📊 Loading data..."

    # Zone descriptions
    ZONE_DESCRIPTIONS = {
        "Cacula": "High solar potential, moderate population, isolated from grid",
        "Humpata": "Very high solar potential, good road access, suitable land use",
        "Quilengues": "Good solar potential, high population density, agricultural communities",
    }


class APIConstants:
    """API/REST endpoint constants"""

    # Available raster layers for MCDA analysis
    AVAILABLE_LAYERS = [
        "mapa_irradiacao",      # Solar irradiance (kWh/m²/day)
        "mapa_populacao",       # Population density (people/km²)
        "mapa_distanciarede",   # Distance to grid (km)
        "mapa_declividade",     # Slope (degrees)
        "mapa_ndvi",            # Vegetation index (NDVI -1 to 1)
    ]

    # Layer descriptions for API documentation
    LAYER_DESCRIPTIONS = {
        "mapa_irradiacao": "Solar irradiance (kWh/m²/day) - higher = better for solar",
        "mapa_populacao": "Population density (people/km²) - higher = more demand",
        "mapa_distanciarede": "Distance to electrical grid (km) - lower = better",
        "mapa_declividade": "Slope (degrees) - low/moderate = easier installation",
        "mapa_ndvi": "Vegetation index (-1 to 1) - moderate = suitable land cover"
    }

    # HTTP Response status messages
    HTTP_STATUS_OK = "ok"
    HTTP_BATCH_STATUS_ALL_SUCCESS = "all_success"
    HTTP_BATCH_STATUS_PARTIAL_SUCCESS = "partial_success"
    HTTP_BATCH_STATUS_FAILED = "failed"
    
    # Error detail messages
    ERROR_NO_RASTER_DATA = "No raster maps found in data/processed/. Run generate_maps_simple.py first."
    ERROR_NO_VALID_DATA = "No valid raster data could be processed"
    ERROR_OVERLAY_FAILED = "Overlay computation resulted in no data"
    ERROR_WEIGHT_SUM_ZERO = "Weights must sum to non-zero value"


class ExportTaskConstants:
    """Google Earth Engine export task constants"""
    
    # Export task status values
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_PARTIAL = "partial"
    
    # Batch status values (different from task status)
    BATCH_STATUS_PENDING = "pending"
    BATCH_STATUS_PROCESSING = "processing"
    BATCH_STATUS_COMPLETED = "completed"
    BATCH_STATUS_PARTIAL = "partial"
    BATCH_STATUS_FAILED = "failed"
    
    # Error message templates
    MSG_TASK_NOT_FOUND = "Export task {} not found"
    MSG_TASK_FAILED = "Export task {} failed: {}"
    MSG_BATCH_EMPTY = "Batch cannot be empty when submitted"
    MSG_EXPORT_TIMEOUT = "Export did not complete within {} seconds"


class ConfigLoaderConstants:
    """Configuration loader constants and defaults"""
    
    # Project metadata
    PROJECT_NAME = "GEESP-Angola"
    PROJECT_VERSION = "3.0.0"
    
    # Logging defaults
    LOG_LEVEL_DEFAULT = "INFO"
    LOG_FORMAT_DEFAULT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE_DEFAULT = "logs/geesp.log"
    LOG_MAX_BYTES = 10485760  # 10 MB
    LOG_BACKUP_COUNT = 5
    
    # Config file discovery paths
    CONFIG_PATHS = [
        "../config.json",  # ../config.json
        "./config.json",   # ./config.json
        "~/.geesp/config.json",  # ~/.geesp/config.json
    ]
    
    # Map generation defaults
    MAP_OUTPUT_SHAPE_DEFAULT = (280, 300)  # (height, width)
    MAP_FORMAT_DEFAULT = "npy"
    MAP_RESOLUTION_M_DEFAULT = 1000
    MAP_NODATA_VALUE = -9999
    MAP_DTYPE_DEFAULT = "float32"
    
    # MCDA defaults
    MCDA_CONSISTENCY_THRESHOLD = 0.1
    MCDA_MIN_WEIGHT = 0.05
    MCDA_MAX_WEIGHT = 0.50
    MCDA_WEIGHTS_SUM_TOLERANCE = 0.01
    MCDA_CLASSIFICATION_HIGH = 0.70
    MCDA_CLASSIFICATION_MEDIUM = 0.40
    MCDA_CLASSIFICATION_LOW = 0.0
    
    # MCDA normalization ranges (min, max)
    MCDA_NORMALIZATION_RANGES = {
        "solar_irradiance": (5.5, 6.4),
        "population_density": (10, 95),
        "grid_distance": (0, 45),
        "slope": (0, 30),
        "vegetation_ndvi": (-0.2, 0.7)
    }
    
    # Default MCDA weights
    DEFAULT_MCDA_WEIGHTS = {
        "solar_irradiance": 0.25,
        "population_density": 0.25,
        "grid_distance": 0.20,
        "slope": 0.15,
        "vegetation_ndvi": 0.15
    }
    
    # LCOE defaults
    LCOE_DEFAULT_CAPACITY_MW = 1.0
    LCOE_DEFAULT_DISCOUNT_RATE_PERCENT = 8.0
    LCOE_DEFAULT_PROJECT_LIFETIME_YEARS = 25
    LCOE_DEFAULT_WARRANTY_YEARS = 10
    LCOE_DEFAULT_DEGRADATION_RATE_PERCENT = 0.5
    LCOE_AREA_PER_KW_SQM = 7.5
    LCOE_OPEX_PERCENT_OF_CAPEX = 2.0
    LCOE_DECOMMISSIONING_PERCENT_OF_CAPEX = 0.5
    LCOE_CAPACITY_FACTOR_PERCENT = 20.0
    LCOE_IRRADIANCE_HOURS_PER_YEAR = 1825
    
    # LCOE technology costs (USD)
    LCOE_PV_MODULE_USD_PER_KW = 200
    LCOE_INVERTER_USD_PER_KW = 80
    LCOE_BATTERY_USD_PER_KWH = 150
    LCOE_INSTALLATION_LABOR_PERCENT = 15
    
    # Solar data range expectations
    SOLAR_IRRADIANCE_EXPECTED_RANGE = (4.5, 7.5)
    SOLAR_IRRADIANCE_ABSOLUTE_MIN = 0
    SOLAR_IRRADIANCE_ABSOLUTE_MAX = 10
    
    POPULATION_DENSITY_EXPECTED_RANGE = (50, 5000)
    POPULATION_DENSITY_ABSOLUTE_MIN = 0
    POPULATION_DENSITY_ABSOLUTE_MAX = 50000
    
    GRID_DISTANCE_EXPECTED_RANGE = (0, 50)
    GRID_DISTANCE_UNIT = "km"
    GRID_DISTANCE_ABSOLUTE_MAX = 500
    
    SLOPE_EXPECTED_RANGE = (0, 30)
    SLOPE_UNIT = "degrees"
    SLOPE_ABSOLUTE_MAX = 90
    
    NDVI_EXPECTED_RANGE = (-0.2, 0.7)
    NDVI_ABSOLUTE_MIN = -1.0
    NDVI_ABSOLUTE_MAX = 1.0
    
    # Caching defaults
    CACHE_TTL_SECONDS = 300
    CACHE_MAX_SIZE_MB = 1000
    ENABLE_CACHING_DEFAULT = True
    
    # Monitoring defaults
    REFRESH_INTERVAL_SECONDS = 60
    MAX_DATAPOINTS = 1000
    
    # Google Earth Engine defaults
    GEE_TIMEOUT_SECONDS = 300
    GEE_MAX_RETRIES = 3
    GEE_BATCH_SIZE = 10
    GEE_EXPORT_RESOLUTION_M = 1000
    
    # API defaults
    API_HOST_DEFAULT = "0.0.0.0"
    API_PORT_DEFAULT = 8000
    API_DEBUG_DEFAULT = False
    API_CORS_ORIGINS_DEFAULT = ["*"]
    API_RATE_LIMIT_REQUESTS = 100
    API_RATE_LIMIT_SECONDS = 60
    
    # Dashboard defaults
    DASHBOARD_PAGE_TITLE = "GEESP-Angola"
    DASHBOARD_PAGE_ICON = "☀️"
    DASHBOARD_LAYOUT = "wide"
    DASHBOARD_SIDEBAR_STATE = "expanded"
    DASHBOARD_THEME = "light"
    
    # Performance defaults
    NUM_WORKERS_DEFAULT = 4
    BATCH_PROCESSING_ENABLED = True
    
    # Validation defaults
    STRICT_MODE_DEFAULT = True
    WARN_ON_INVALID_DEFAULT = True
    MAX_ARRAY_SIZE_MB = 500
    
    # Data storage defaults
    DATA_STORAGE_BACKEND = "local"  # local, s3, gcs
    DATA_DIR_DEFAULT = "data"
    OUTPUT_DIR_DEFAULT = "output"
    LOGS_DIR_DEFAULT = "logs"
    CACHE_DIR_DEFAULT = ".cache"


# ============================================================================
# Utility: Get all constants as dictionary
# ============================================================================

def get_all_constants() -> Dict[str, Dict]:
    """Get all constants organized by category"""
    return {
        "mcda": {k: v for k, v in MCDAConstants.__dict__.items() if not k.startswith("_")},
        "geo": {k: v for k, v in GeoConstants.__dict__.items() if not k.startswith("_")},
        "solar": {k: v for k, v in SolarConstants.__dict__.items() if not k.startswith("_")},
        "population": {k: v for k, v in PopulationConstants.__dict__.items() if not k.startswith("_")},
        "infrastructure": {k: v for k, v in InfrastructureConstants.__dict__.items() if not k.startswith("_")},
        "lcoe": {k: v for k, v in LCOEConstants.__dict__.items() if not k.startswith("_")},
        "environmental": {k: v for k, v in EnvironmentalConstants.__dict__.items() if not k.startswith("_")},
        "financial": {k: v for k, v in FinancialConstants.__dict__.items() if not k.startswith("_")},
        "operational": {k: v for k, v in OperationalConstants.__dict__.items() if not k.startswith("_")},
        "validation": {k: v for k, v in ValidationConstants.__dict__.items() if not k.startswith("_")},
        "map_generation": {k: v for k, v in MapGenerationConstants.__dict__.items() if not k.startswith("_")},
        "data_paths": {k: v for k, v in DataPathConstants.__dict__.items() if not k.startswith("_")},
        "technical": {k: v for k, v in TechnicalConstants.__dict__.items() if not k.startswith("_")},
        "ui": {k: v for k, v in UIConstants.__dict__.items() if not k.startswith("_")},
        "messages": {k: v for k, v in MessageConstants.__dict__.items() if not k.startswith("_")},
        "api": {k: v for k, v in APIConstants.__dict__.items() if not k.startswith("_")},
        "export_task": {k: v for k, v in ExportTaskConstants.__dict__.items() if not k.startswith("_")},
        "config_loader": {k: v for k, v in ConfigLoaderConstants.__dict__.items() if not k.startswith("_")},
    }
