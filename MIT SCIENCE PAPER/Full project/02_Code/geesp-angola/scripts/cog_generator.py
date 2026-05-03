"""
Cloud-Optimized GeoTIFF (COG) Generator
Converts GEESP numpy arrays to web-optimized GeoTIFF format with STAC metadata
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple
import numpy as np
from dataclasses import dataclass, asdict

try:
    import rasterio
    from rasterio.crs import CRS
    from rasterio.enums import Resampling
    from rasterio.vrt import WarpedVRT
    from rasterio.io import MemoryFile
except ImportError:
    rasterio = None

logger = logging.getLogger(__name__)


# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

# Default Angola geospatial bounds (Huíla province)
DEFAULT_BOUNDS = {
    "west": 13.5,
    "south": -18.5,
    "east": 25.1,
    "north": -4.4
}

# Tile sizes for COG optimization
COG_TILE_SIZE = 512
COG_COMPRESSION = "deflate"


@dataclass
class COGMetadata:
    """Metadata for Cloud-Optimized GeoTIFF"""
    dataset_name: str
    description: str
    source_file: str
    output_file: str
    created_at: str
    bounds: Dict[str, float]
    crs: str
    resolution: float
    data_type: str
    nodata_value: Optional[float]
    bands: int
    width: int
    height: int
    statistics: Dict[str, float]

    def to_stac(self) -> Dict:
        """Convert to STAC Item format"""
        return {
            "type": "Feature",
            "stac_version": "1.0.0",
            "id": f"{self.dataset_name}_{self.created_at.split('T')[0]}",
            "description": self.description,
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [self.bounds["west"], self.bounds["south"]],
                    [self.bounds["east"], self.bounds["south"]],
                    [self.bounds["east"], self.bounds["north"]],
                    [self.bounds["west"], self.bounds["north"]],
                    [self.bounds["west"], self.bounds["south"]],
                ]]
            },
            "properties": {
                "datetime": self.created_at,
                "start_datetime": self.created_at,
                "end_datetime": self.created_at,
                "platform": "geesp-angola",
                "instruments": ["analysis"],
            },
            "links": [
                {
                    "rel": "self",
                    "href": self.output_file,
                    "type": "image/tiff; application=geotiff"
                }
            ],
            "assets": {
                "data": {
                    "href": self.output_file,
                    "type": "image/tiff; application=geotiff",
                    "title": self.dataset_name,
                    "roles": ["data"],
                }
            }
        }


class COGGenerator:
    """Generate Cloud-Optimized GeoTIFFs from numpy arrays"""

    def __init__(
        self,
        bounds: Optional[Dict[str, float]] = None,
        crs: str = "EPSG:32733",  # Angola zone
        resolution: float = 1000.0,  # meters
    ):
        """Initialize COG generator
        
        Args:
            bounds: Geographic bounds (west, south, east, north)
            crs: Coordinate Reference System
            resolution: Pixel resolution in meters
        """
        if rasterio is None:
            logger.warning("Rasterio not available - COG generation will be limited")
        
        self.bounds = bounds or DEFAULT_BOUNDS
        self.crs = CRS.from_string(crs) if rasterio else None
        self.resolution = resolution
        logger.info(f"COGGenerator initialized with CRS {crs} and {resolution}m resolution")

    def create_cog(
        self,
        data: np.ndarray,
        output_path: str,
        dataset_name: str = "dataset",
        description: str = "",
        nodata_value: Optional[float] = np.nan,
        cmap: Optional[str] = "viridis",
    ) -> Optional[COGMetadata]:
        """Create Cloud-Optimized GeoTIFF from numpy array
        
        Args:
            data: Input numpy array (2D or 3D)
            output_path: Path to save COG
            dataset_name: Name of dataset
            description: Dataset description
            nodata_value: Value to treat as no-data
            cmap: Colormap name for visualization
            
        Returns:
            COGMetadata object or None if failed
        """
        if rasterio is None:
            logger.error("Rasterio not installed - cannot create COG")
            return None
        
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Ensure 3D array (bands, height, width)
            if data.ndim == 2:
                data = data[np.newaxis, :, :]
            
            bands, height, width = data.shape
            
            logger.info(f"Creating COG: {dataset_name} ({width}x{height}x{bands})")
            
            # Calculate georeferencing
            transform = self._calculate_transform(width, height)
            
            # Prepare profile for GeoTIFF
            profile = {
                "driver": "GTiff",
                "dtype": data.dtype,
                "nodata": nodata_value,
                "width": width,
                "height": height,
                "count": bands,
                "crs": self.crs,
                "transform": transform,
                "compress": COG_COMPRESSION,
                "tiled": True,
                "blockxsize": COG_TILE_SIZE,
                "blockysize": COG_TILE_SIZE,
            }
            
            # Write COG
            with rasterio.open(output_file, "w", **profile) as dst:
                for i in range(bands):
                    dst.write(data[i], i + 1)
                
                # Add overviews for zoom levels
                dst.build_overviews([2, 4, 8, 16], Resampling.nearest)
            
            logger.info(f"✓ COG created: {output_file}")
            
            # Calculate statistics
            valid_data = data[~np.isnan(data)]
            stats = {
                "min": float(np.nanmin(data)),
                "max": float(np.nanmax(data)),
                "mean": float(np.nanmean(data)),
                "std": float(np.nanstd(data)),
                "valid_pixels": int((~np.isnan(data)).sum()),
            }
            
            # Create metadata
            metadata = COGMetadata(
                dataset_name=dataset_name,
                description=description,
                source_file="numpy_array",
                output_file=str(output_file),
                created_at=datetime.now().isoformat(),
                bounds=self.bounds,
                crs=str(self.crs),
                resolution=self.resolution,
                data_type=str(data.dtype),
                nodata_value=nodata_value,
                bands=bands,
                width=width,
                height=height,
                statistics=stats,
            )
            
            return metadata
            
        except Exception as e:
            logger.error(f"✗ COG creation failed: {e}")
            return None

    def create_cogs_from_dict(
        self,
        data_dict: Dict[str, np.ndarray],
        output_dir: str = "output/cogs",
        descriptions: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Optional[COGMetadata]]:
        """Create multiple COGs from dictionary of arrays
        
        Args:
            data_dict: Dictionary of {name: array}
            output_dir: Output directory for COGs
            descriptions: Optional descriptions for each dataset
            
        Returns:
            Dictionary of {name: metadata}
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        for name, data in data_dict.items():
            output_file = output_path / f"{name}.tif"
            description = descriptions.get(name, "") if descriptions else ""
            
            metadata = self.create_cog(
                data,
                str(output_file),
                dataset_name=name,
                description=description,
            )
            
            results[name] = metadata
        
        return results

    def create_stac_catalog(
        self,
        metadata_list: list[COGMetadata],
        catalog_dir: str = "output/stac",
        catalog_name: str = "geesp-cogs",
    ) -> bool:
        """Create STAC catalog for COGs
        
        Args:
            metadata_list: List of COGMetadata objects
            catalog_dir: Output directory for catalog
            catalog_name: Name of catalog
            
        Returns:
            True if successful
        """
        try:
            catalog_path = Path(catalog_dir)
            catalog_path.mkdir(parents=True, exist_ok=True)
            
            # Create catalog JSON
            catalog = {
                "stac_version": "1.0.0",
                "type": "Catalog",
                "id": catalog_name,
                "description": f"GEESP-Angola Cloud-Optimized GeoTIFFs - {datetime.now().strftime('%Y-%m-%d')}",
                "links": [],
            }
            
            # Add item links
            for metadata in metadata_list:
                item = metadata.to_stac()
                item_file = catalog_path / f"{metadata.dataset_name}.json"
                
                with open(item_file, "w") as f:
                    json.dump(item, f, indent=2)
                
                catalog["links"].append({
                    "rel": "item",
                    "href": str(item_file.relative_to(catalog_path)),
                    "title": metadata.dataset_name,
                })
            
            # Save catalog
            catalog_file = catalog_path / "catalog.json"
            with open(catalog_file, "w") as f:
                json.dump(catalog, f, indent=2)
            
            logger.info(f"✓ STAC catalog created: {catalog_file}")
            return True
            
        except Exception as e:
            logger.error(f"✗ STAC catalog creation failed: {e}")
            return False

    def _calculate_transform(self, width: int, height: int) -> "rasterio.transform.Affine":
        """Calculate geotransform from bounds and dimensions
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            
        Returns:
            Affine transform
        """
        if rasterio is None:
            return None
        
        from rasterio.transform import from_bounds
        
        return from_bounds(
            self.bounds["west"],
            self.bounds["south"],
            self.bounds["east"],
            self.bounds["north"],
            width,
            height,
        )

    def validate_cog(self, cog_path: str) -> bool:
        """Validate that file is a proper Cloud-Optimized GeoTIFF
        
        Args:
            cog_path: Path to COG file
            
        Returns:
            True if valid COG
        """
        if rasterio is None:
            logger.warning("Cannot validate COG without rasterio")
            return True
        
        try:
            with rasterio.open(cog_path) as src:
                # Check for tiling
                if src.profile.get("tiled"):
                    logger.info(f"✓ {cog_path} has tiling enabled")
                else:
                    logger.warning(f"⚠ {cog_path} does not have tiling")
                
                # Check for overviews
                if src.overviews(1):
                    logger.info(f"✓ {cog_path} has overviews: {src.overviews(1)}")
                else:
                    logger.warning(f"⚠ {cog_path} does not have overviews")
                
                return True
                
        except Exception as e:
            logger.error(f"✗ COG validation failed: {e}")
            return False


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_cog_from_array(
    data: np.ndarray,
    output_path: str,
    dataset_name: str = "dataset",
) -> Optional[COGMetadata]:
    """Convenience function to create single COG
    
    Args:
        data: Input numpy array
        output_path: Output file path
        dataset_name: Name of dataset
        
    Returns:
        COGMetadata or None
    """
    generator = COGGenerator()
    return generator.create_cog(data, output_path, dataset_name=dataset_name)


def create_cogs_from_geesp_output(
    output_dir: str = "output/cogs",
) -> Dict[str, Optional[COGMetadata]]:
    """Create COGs from standard GEESP output files
    
    Args:
        output_dir: Output directory for COGs
        
    Returns:
        Dictionary of created COGs
    """
    import glob
    
    generator = COGGenerator()
    data_dict = {}
    
    # Load all .npy files
    for npy_file in glob.glob("data/processed/*.npy"):
        name = Path(npy_file).stem
        try:
            data = np.load(npy_file)
            data_dict[name] = data
            logger.info(f"Loaded {name}: {data.shape}")
        except Exception as e:
            logger.error(f"Failed to load {npy_file}: {e}")
    
    # Create COGs
    return generator.create_cogs_from_dict(data_dict, output_dir=output_dir)


if __name__ == "__main__":
    # Example usage
    generator = COGGenerator()
    
    # Create sample data
    sample_data = np.random.rand(280, 300)
    
    # Create COG
    metadata = generator.create_cog(
        sample_data,
        "output/sample_cog.tif",
        dataset_name="sample_aptitude",
        description="Sample aptitude map for testing",
    )
    
    if metadata:
        print(f"Created COG: {metadata.output_file}")
        print(f"Statistics: min={metadata.statistics['min']:.3f}, "
              f"max={metadata.statistics['max']:.3f}, "
              f"mean={metadata.statistics['mean']:.3f}")
        
        # Validate
        if generator.validate_cog(metadata.output_file):
            print("✓ COG validation passed")
        
        # Create STAC item
        print(f"STAC Item: {json.dumps(metadata.to_stac(), indent=2)}")
