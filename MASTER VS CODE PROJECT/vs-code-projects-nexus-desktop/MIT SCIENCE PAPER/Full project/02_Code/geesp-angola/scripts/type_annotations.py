"""
Type Annotations for GEESP-Angola Core Modules
Comprehensive type hints for better IDE support and code clarity
"""

from typing import (
    Dict, List, Tuple, Optional, Union, Any, Callable,
    NamedTuple, TypeVar, Sequence
)
import numpy as np
import pandas as pd
from numpy.typing import NDArray

# Type aliases for common patterns
RasterArray = NDArray[np.float32]  # 2D float array (280, 300)
WeightsDict = Dict[str, float]     # {"criterion": weight}
BoundsType = Tuple[float, float, float, float]  # (minx, miny, maxx, maxy)


class SolarParameters(NamedTuple):
    """Solar installation parameters for LCOE calculation"""
    capacity_mw: float
    capex_dict: Dict[str, float]
    opex_fixed: float
    opex_variable: float
    annual_irradiance: float
    system_efficiency: float
    degradation_rate: float
    discount_rate: float
    project_lifetime: int
    warranty_years: int
    location: str = "Angola"


class MCDAWeights(NamedTuple):
    """MCDA criterion weights"""
    solar_irradiance: float
    population_density: float
    grid_distance: float
    slope: float
    vegetation: float
    
    def to_dict(self) -> WeightsDict:
        """Convert to dictionary format"""
        return {
            "irradiacao": self.solar_irradiance,
            "populacao": self.population_density,
            "distancia_rede": self.grid_distance,
            "declividade": self.slope,
            "ndvi": self.vegetation
        }


class LCOEResult(NamedTuple):
    """LCOE calculation result"""
    lcoe_usd_per_mwh: float
    lcoe_usd_per_kwh: float
    capex_total_usd: float
    annual_opex_usd: float
    annual_generation_mwh: float
    discount_rate: float
    project_lifetime: int


class MCDAResult(NamedTuple):
    """MCDA weighted overlay result"""
    aptitude_map: RasterArray
    min_value: float
    max_value: float
    mean_value: float
    std_value: float
    valid_percent: float


# ============================================================================
# MCDA MODULE TYPE HINTS
# ============================================================================

class AHPWeighter:
    """Analytic Hierarchy Process for criterion weighting
    
    Type-annotated version with explicit parameter and return types
    """
    
    comparison_matrix: Optional[pd.DataFrame]
    weights: Optional[np.ndarray]
    consistency_ratio: Optional[float]
    
    def create_comparison_matrix(
        self,
        criteria_names: List[str],
        values: Dict[Tuple[str, str], float]
    ) -> pd.DataFrame:
        """Create AHP comparison matrix"""
        ...
    
    def calculate_weights_from_matrix(self) -> np.ndarray:
        """Calculate normalized weights from matrix"""
        ...
    
    def get_weights_df(self) -> pd.DataFrame:
        """Return weights as DataFrame"""
        ...


class MCDAnalyzer:
    """Multi-Criteria Decision Analysis with Weighted Overlay"""
    
    weights: WeightsDict
    normalized_rasters: Dict[str, RasterArray]
    aptitude_map: Optional[RasterArray]
    
    def normalize_raster(
        self,
        raster_array: RasterArray,
        name: str,
        minimum: float = 0,
        maximum: float = 1
    ) -> RasterArray:
        """Normalize raster to [minimum, maximum]"""
        ...
    
    def weighted_overlay(self) -> RasterArray:
        """Compute weighted overlay of normalized rasters"""
        ...
    
    def classify_aptitude(
        self,
        high_threshold: float = 0.70,
        low_threshold: float = 0.40
    ) -> NDArray[np.uint8]:
        """Classify aptitude into 3 classes"""
        ...


# ============================================================================
# LCOE MODULE TYPE HINTS
# ============================================================================

class LCOECalculator:
    """LCOE calculation for solar technologies"""
    
    TECHNOLOGY_COSTS: Dict[str, Dict[str, float]]
    TECHNOLOGY_OPEX: Dict[str, Dict[str, float]]
    location: str
    results: Dict[str, Any]
    
    def calculate_lcoe(self, params: SolarParameters) -> Dict[str, Any]:
        """Calculate LCOE for given parameters"""
        ...
    
    def compare_technologies(
        self,
        capacity_mw: float,
        annual_irradiance: float,
        discount_rate: float = 8,
        lifetime: int = 25
    ) -> pd.DataFrame:
        """Compare LCOE across technologies"""
        ...
    
    def financial_analysis(
        self,
        capacity_mw: float,
        annual_irradiance: float,
        system_cost_usd: float,
        annual_revenue_usd: float
    ) -> Dict[str, Union[float, int]]:
        """Detailed financial analysis"""
        ...


# ============================================================================
# MAP GENERATION MODULE TYPE HINTS
# ============================================================================

def generate_map_simple(
    name: str,
    intensity: float = 1.0,
    output_shape: Tuple[int, int] = (280, 300),
    seed: Optional[int] = 42
) -> RasterArray:
    """Generate synthetic map data"""
    ...


def compute_irradiance(
    output_shape: Tuple[int, int] = (280, 300),
    base_irradiance: float = 6.0
) -> RasterArray:
    """Compute solar irradiance map"""
    ...


def compute_population(
    output_shape: Tuple[int, int] = (280, 300),
    num_clusters: int = 3
) -> RasterArray:
    """Compute population density map"""
    ...


def compute_distance(
    output_shape: Tuple[int, int] = (280, 300)
) -> RasterArray:
    """Compute distance to grid map"""
    ...


def compute_slope(
    output_shape: Tuple[int, int] = (280, 300)
) -> RasterArray:
    """Compute terrain slope map"""
    ...


def compute_ndvi(
    output_shape: Tuple[int, int] = (280, 300)
) -> RasterArray:
    """Compute NDVI vegetation map"""
    ...


# ============================================================================
# UTILITY MODULE TYPE HINTS
# ============================================================================

def normalize_for_visualization(
    data: RasterArray,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None
) -> RasterArray:
    """Normalize raster for visualization"""
    ...


def save_raster(
    data: RasterArray,
    filename: str,
    format: str = "npy"
) -> None:
    """Save raster to file"""
    ...


def load_raster(
    filename: str,
    memmap: bool = False
) -> Union[RasterArray, Any]:
    """Load raster from file"""
    ...


def build_metadata(
    maps: Dict[str, RasterArray],
    weights: Optional[WeightsDict] = None,
    location: str = "Angola"
) -> Dict[str, Any]:
    """Build metadata dictionary"""
    ...


# ============================================================================
# PERFORMANCE MODULE TYPE HINTS
# ============================================================================

def timer(func: Callable) -> Callable:
    """Decorator to measure and log execution time"""
    ...


def vectorized_npv(
    annual_cf: float,
    discount_rate: float,
    years: int
) -> float:
    """Vectorized NPV calculation"""
    ...


def normalize_array(
    data: RasterArray,
    handle_constant: bool = True
) -> RasterArray:
    """Fast vectorized normalization"""
    ...


def parallel_map(
    func: Callable[[Any], Any],
    items: Sequence[Any],
    max_workers: int = 4
) -> List[Any]:
    """Apply function to items in parallel"""
    ...


# ============================================================================
# VALIDATORS MODULE TYPE HINTS
# ============================================================================

def validate_solar_irradiance(
    data: RasterArray,
    name: str = "solar_irradiance"
) -> bool:
    """Validate solar irradiance data"""
    ...


def validate_weights(
    weights: WeightsDict,
    tolerance: float = 0.01
) -> bool:
    """Validate MCDA weights"""
    ...


def validate_capacity_mw(
    capacity: float,
    min_val: float = 0.1,
    max_val: float = 500
) -> bool:
    """Validate capacity parameter"""
    ...


def validate_all_inputs(
    solar: RasterArray,
    population: RasterArray,
    distance: RasterArray,
    slope: RasterArray,
    ndvi: RasterArray,
    weights: WeightsDict,
    capacity_mw: float,
    irradiance: float,
    discount_rate: float,
    expected_shape: Tuple[int, int] = (280, 300)
) -> bool:
    """Comprehensive batch validation"""
    ...


# ============================================================================
# API MODULE TYPE HINTS (FastAPI/Pydantic) - Optional: only if pydantic installed
# ============================================================================

try:
    from pydantic import BaseModel, Field

    class MCDARequest(BaseModel):
        """MCDA computation request"""
        weights: WeightsDict = Field(..., description="MCDA criterion weights")
        location: str = Field(default="Angola", description="Location name")

        class Config:
            schema_extra = {
                "example": {
                    "weights": {
                        "solar": 0.25,
                        "population": 0.25,
                        "distance": 0.20,
                        "slope": 0.15,
                        "vegetation": 0.15
                    }
                }
            }

    class LCOERequest(BaseModel):
        """LCOE computation request"""
        capacity_mw: float = Field(..., gt=0.1, lt=500, description="Capacity in MW")
        annual_irradiance: float = Field(..., ge=500, le=3500, description="kWh/m²/year")
        discount_rate: float = Field(default=8.0, ge=-100, le=100, description="Discount rate %")
        project_lifetime: int = Field(default=25, ge=5, le=50, description="Years")

        class Config:
            schema_extra = {
                "example": {
                    "capacity_mw": 1.0,
                    "annual_irradiance": 2226,
                    "discount_rate": 8.0,
                    "project_lifetime": 25
                }
            }

    class MCDAResponse(BaseModel):
        """MCDA computation response"""
        status: str
        aptitude_stats: Dict[str, float]
        message: Optional[str] = None

    class LCOEResponse(BaseModel):
        """LCOE computation response"""
        status: str
        technologies: List[Dict[str, Any]]
        best_technology: str
        message: Optional[str] = None

except ImportError:
    # Stub classes when pydantic not installed (e.g. minimal test env)
    BaseModel = type("BaseModel", (), {})  # type: ignore
    MCDARequest = type("MCDARequest", (BaseModel,), {})  # type: ignore
    LCOERequest = type("LCOERequest", (BaseModel,), {})  # type: ignore
    MCDAResponse = type("MCDAResponse", (BaseModel,), {})  # type: ignore
    LCOEResponse = type("LCOEResponse", (BaseModel,), {})  # type: ignore


if __name__ == "__main__":
    print("✓ Type annotations module loaded successfully")
    print(f"  - RasterArray: {RasterArray}")
    print(f"  - WeightsDict: {WeightsDict}")
    print(f"  - SolarParameters: {SolarParameters}")
    print(f"  - MCDAWeights: {MCDAWeights}")
    print(f"  - LCOEResult: {LCOEResult}")
    print(f"  - MCDAResult: {MCDAResult}")
