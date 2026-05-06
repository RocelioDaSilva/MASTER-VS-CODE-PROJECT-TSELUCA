#!/usr/bin/env python3
"""
DEPRECATED: Use backend/geospatial/earth_engine_integration.py instead.
This is an older/simpler version kept for reference only.

Google Earth Engine Integration for GEESP-Angola
Fetch geospatial datasets for solar analysis, land cover, elevation, etc.

Setup:
  1. pip install google-auth earthengine-api
  2. earthengine authenticate
  3. See EARTH_ENGINE_SETUP.md for full instructions

Usage:
  python scripts/earth_engine_integration.py \
    --collection COPERNICUS/S5P/OFFL/L2__NO2 \
    --region angola \
    --start-date 2023-01-01 \
    --end-date 2023-12-31
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse
import json

# Google Earth Engine
try:
    import ee
    HAS_EE = True
except ImportError:
    HAS_EE = False
    print("Warning: earthengine-api not installed. Install with: pip install earthengine-api")

import numpy as np

# Constants
proj_root = Path(__file__).parent.parent.parent
if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))
try:
    from logging_config import get_script_logger
except ImportError:
    from .logging_config import get_script_logger
from utils.constants import OperationalConstants

logger = get_script_logger(__name__)


class EarthEngineIntegration:
    """Google Earth Engine data extraction for GEESP-Angola"""
    
    # Pre-defined regions using OperationalConstants bounds (as [west, south, east, north])
    REGIONS = {
        'angola': {
            'bounds': ee.Geometry.Rectangle(OperationalConstants.EE_REGION_ANGOLA),
            'region_name': 'Angola',
            'description': 'Angola national boundary'
        },
        'luanda': {
            'bounds': ee.Geometry.Rectangle(OperationalConstants.EE_REGION_LUANDA),
            'region_name': 'Luanda Province',
            'description': 'Luanda Province'
        },
        'huambo': {
            'bounds': ee.Geometry.Rectangle(OperationalConstants.EE_REGION_HUAMBO),
            'region_name': 'Huambo Province',
            'description': 'Huambo Province'
        },
        'benguela': {
            'bounds': ee.Geometry.Rectangle(OperationalConstants.EE_REGION_BENGUELA),
            'region_name': 'Benguela Province',
            'description': 'Benguela Province'
        }
    }
    
    # Pre-defined datasets
    DATASETS = {
        'solar_irradiance': {
            'collection': OperationalConstants.EE_DATASET_SOLAR_COLLECTION,
            'band': OperationalConstants.EE_DATASET_SOLAR_BAND,
            'description': 'Global Forecast System solar irradiance'
        },
        'elevation': {
            'collection': OperationalConstants.EE_DATASET_ELEVATION_COLLECTION,
            'band': OperationalConstants.EE_DATASET_ELEVATION_BAND,
            'description': 'SRTM 30m DEM - Elevation'
        },
        'land_cover': {
            'collection': OperationalConstants.EE_DATASET_LANDCOVER_COLLECTION,
            'band': OperationalConstants.EE_DATASET_LANDCOVER_BAND,
            'description': 'Copernicus Land Cover 100m annual'
        },
        'ndvi': {
            'collection': OperationalConstants.EE_DATASET_NDVI_COLLECTION,
            'band': OperationalConstants.EE_DATASET_NDVI_BAND,
            'description': 'MODIS Vegetation Index (16-day, 250m)'
        },
        'lst': {
            'collection': OperationalConstants.EE_DATASET_LST_COLLECTION,
            'band': OperationalConstants.EE_DATASET_LST_BAND,
            'description': 'MODIS Land Surface Temperature (8-day, 1km)'
        },
        'population': {
            'collection': OperationalConstants.EE_DATASET_POPULATION_COLLECTION,
            'band': OperationalConstants.EE_DATASET_POPULATION_BAND,
            'description': 'Gridded Population of the World v4.11'
        },
        'nightlights': {
            'collection': 'NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG',
            'band': 'avg_rad',
            'description': 'VIIRS Nighttime Lights (monthly)'
        },
        'rainfall': {
            'collection': 'JAXA/GPM_L3/GSMaP_v6/operational',
            'band': 'precipitationCal',
            'description': 'GPM Global Satellite Mapping of Precipitation'
        }
    }
    
    def __init__(self, project_id: Optional[str] = None, auth_path: Optional[str] = None):
        """Initialize Earth Engine integration"""
        if not HAS_EE:
            raise ImportError("earthengine-api required. Install: pip install earthengine-api")
        
        try:
            # Authenticate with Earth Engine
            if auth_path:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = auth_path
            
            ee.Initialize()
            logger.info("✓ Earth Engine authenticated successfully")
            
            # Set project if provided
            if project_id:
                ee.data.setDefaultProject(project_id)
            
        except Exception as e:
            logger.error(f"Earth Engine authentication failed: {e}")
            logger.info("Run: earthengine authenticate")
            raise
    
    def get_region_bounds(self, region_name: str) -> ee.Geometry:
        """Get geometry for a named region"""
        if region_name not in self.REGIONS:
            raise ValueError(f"Unknown region: {region_name}. Available: {list(self.REGIONS.keys())}")
        
        return self.REGIONS[region_name]['bounds']
    
    def fetch_dataset(
        self,
        dataset_key: str,
        region: str,
        start_date: str,
        end_date: str,
        output_file: Optional[str] = None
    ) -> Dict:
        """
        Fetch a dataset for a region and date range
        Returns statistics and saves to GeoTIFF if output_file specified
        """
        logger.info(f"Fetching {dataset_key} for {region} ({start_date} to {end_date})")
        
        if dataset_key not in self.DATASETS:
            raise ValueError(f"Unknown dataset: {dataset_key}")
        
        dataset_info = self.DATASETS[dataset_key]
        bounds = self.get_region_bounds(region)
        
        # Load collection and filter
        collection = ee.ImageCollection(dataset_info['collection'])
        filtered = (collection
                   .filterDate(start_date, end_date)
                   .filterBounds(bounds))
        
        # Reduce (mean) for the time period
        image = filtered.mean().clip(bounds)
        
        # Extract band
        band = dataset_info['band']
        if band in image.bandNames().getInfo():
            data = image.select(band)
        else:
            logger.warning(f"Band {band} not found. Using first band.")
            data = image.select(0)
        
        # Calculate statistics
        stats = data.reduceRegion(
            ee.Reducer.mean().combine(
                ee.Reducer.stdDev(), "", True
            ).combine(
                ee.Reducer.minMax(), "", True
            ),
            bounds,
            scale=30  # 30m default
        ).getInfo()
        
        logger.info(f"Statistics: {stats}")
        
        result = {
            'dataset': dataset_key,
            'region': region,
            'start_date': start_date,
            'end_date': end_date,
            'description': dataset_info['description'],
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        }
        
        # Export to GeoTIFF if requested
        if output_file:
            self._export_geotiff(data, bounds, output_file, dataset_key)
            result['output_file'] = output_file
        
        return result
    
    def _export_geotiff(self, image: ee.Image, bounds: ee.Geometry, output_file: str, filename_base: str):
        """Export image to GeoTIFF"""
        logger.info(f"Exporting to {output_file}")
        
        task = ee.batch.Export.image.toDrive(
            image=image,
            description=f"geesp_{filename_base}_{datetime.now().strftime('%Y%m%d')}",
            folder='geesp-earth-engine-exports',
            fileNamePrefix=filename_base,
            region=bounds,
            scale=30,
            format="GeoTIFF"
        )
        
        task.start()
        logger.info(f"Export task started: {task.id}")
        logger.info("Check Google Drive: geesp-earth-engine-exports/")
    
    def fetch_solar_potential(self, region: str, year: int = 2023) -> Dict:
        """
        Fetch solar irradiance and derived metrics for a region
        Uses multiple datasets (irradiance, elevation, cloud cover)
        """
        logger.info(f"Computing solar potential for {region} ({year})")
        
        bounds = self.get_region_bounds(region)
        
        # Solar irradiance from NOAA GFS
        irradiance = ee.ImageCollection('NOAA/GFSANL').filterDate(
            f'{year}-01-01', f'{year}-12-31'
        ).filterBounds(bounds).mean().clip(bounds).select('DSWRF_surface')
        
        # Elevation from SRTM
        elevation = ee.Image('USGS/SRTMGL1_Ellip/SRTM30').clip(bounds).select('elevation')
        
        # Cloud cover from Sentinel-5P
        clouds = ee.ImageCollection('COPERNICUS/S5P/OFFL/L2__CLOUD').filterDate(
            f'{year}-01-01', f'{year}-12-31'
        ).filterBounds(bounds).mean().clip(bounds)
        
        # Calculate combined metrics
        combined = ee.Image.cat([irradiance, elevation, clouds])
        
        stats = combined.reduceRegion(
            ee.Reducer.mean(),
            bounds,
            scale=1000
        ).getInfo()
        
        result = {
            'region': region,
            'year': year,
            'irradiance_mean': stats.get('DSWRF_surface'),
            'elevation_mean': stats.get('elevation'),
            'cloud_fraction': stats.get('cloud_fraction'),
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def fetch_environmental_data(self, region: str, start_date: str, end_date: str) -> Dict:
        """
        Fetch environmental data: NDVI, precipitation, temperature
        Useful for assessing land suitability
        """
        logger.info(f"Fetching environmental data for {region}")
        
        bounds = self.get_region_bounds(region)
        
        # NDVI (vegetation)
        ndvi = ee.ImageCollection('MODIS/061/MOD13Q1').filterDate(
            start_date, end_date
        ).filterBounds(bounds).mean().clip(bounds).select('NDVI')
        
        # Precipitation
        precip = ee.ImageCollection('JAXA/GPM_L3/GSMaP_v6/operational').filterDate(
            start_date, end_date
        ).filterBounds(bounds).mean().clip(bounds).select('precipitationCal')
        
        # Land Surface Temperature
        lst = ee.ImageCollection('MODIS/061/MOD11A2').filterDate(
            start_date, end_date
        ).filterBounds(bounds).mean().clip(bounds).select('LST_Day_1km')
        
        stats = ee.Image.cat([ndvi, precip, lst]).reduceRegion(
            ee.Reducer.mean(),
            bounds,
            scale=1000
        ).getInfo()
        
        return {
            'region': region,
            'period': f'{start_date} to {end_date}',
            'ndvi_mean': stats.get('NDVI'),
            'precipitation_mean': stats.get('precipitationCal'),
            'temperature_mean': stats.get('LST_Day_1km'),
            'timestamp': datetime.now().isoformat()
        }
    
    def list_available_datasets(self) -> Dict:
        """List all available datasets"""
        return {
            'datasets': {k: v['description'] for k, v in self.DATASETS.items()},
            'regions': {k: v['description'] for k, v in self.REGIONS.items()}
        }


def main():
    parser = argparse.ArgumentParser(description='Google Earth Engine data extraction for GEESP-Angola')
    parser.add_argument('--collection', help='Dataset key (see --list for available)')
    parser.add_argument('--region', default='angola', help='Region name')
    parser.add_argument('--start-date', default=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
    parser.add_argument('--end-date', default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('--output', help='Output GeoTIFF file')
    parser.add_argument('--list', action='store_true', help='List available datasets')
    parser.add_argument('--solar-potential', action='store_true', help='Compute solar potential')
    parser.add_argument('--environmental', action='store_true', help='Fetch environmental data')
    parser.add_argument('--project-id', help='Google Cloud project ID')
    parser.add_argument('--auth-path', help='Path to service account JSON')
    
    args = parser.parse_args()
    
    try:
        ee_integration = EarthEngineIntegration(
            project_id=args.project_id,
            auth_path=args.auth_path
        )
        
        if args.list:
            print(json.dumps(ee_integration.list_available_datasets(), indent=2))
            return 0
        
        if args.solar_potential:
            result = ee_integration.fetch_solar_potential(args.region)
            print(json.dumps(result, indent=2))
            return 0
        
        if args.environmental:
            result = ee_integration.fetch_environmental_data(
                args.region, args.start_date, args.end_date
            )
            print(json.dumps(result, indent=2))
            return 0
        
        if args.collection:
            result = ee_integration.fetch_dataset(
                args.collection, args.region, args.start_date, args.end_date, args.output
            )
            print(json.dumps(result, indent=2))
            return 0
        
        parser.print_help()
        return 1
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
