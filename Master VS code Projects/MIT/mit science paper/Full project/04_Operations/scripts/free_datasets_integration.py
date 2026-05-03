#!/usr/bin/env python3
"""
Free Datasets Integration for GEESP-Angola
Downloads from public sources: NOAA, OpenEI, GEBCO, WorldPop, etc.

Usage:
  python scripts/free_datasets_integration.py \
    --source noaa \
    --dataset solar_irradiance \
    --region angola \
    --output data/raw/noaa_irradiance.csv
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import argparse
import json

# Data handling
import numpy as np

# HTTP requests
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Optional: netCDF4 for advanced data handling
try:
    import netCDF4 as nc
    HAS_NETCDF = True
except ImportError:
    HAS_NETCDF = False

# Optional: rasterio for geospatial
try:
    import rasterio
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FreeDatasets:
    """Access free geospatial and climate datasets"""
    
    def __init__(self, cache_dir: str = "data/raw"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    # ========================================================================
    # NOAA - Solar Irradiance, Weather, Climate
    # ========================================================================
    
    def fetch_nsrdb_solar_data(self, latitude: float, longitude: float) -> Dict:
        """
        Fetch hourly solar irradiance from NOAA NSRDB (1998-2023)
        Free tier: 4 requests/hour
        
        Args:
            latitude, longitude: Location coordinates
        
        Returns:
            Solar irradiance data (GHI, DHI, DNI)
        """
        logger.info(f"Fetching NSRDB solar data for ({latitude}, {longitude})")
        
        # NSRDB API endpoint (requires API key from https://nsrdb.nrel.gov/api)
        api_endoint = 'https://nsrdb.nrel.gov/api/v2/solar/nsrdb-data.json'
        
        params = {
            'wkt': f'POINT({longitude} {latitude})',
            'names': 'TMY',  # Typical Meteorological Year
            'leap_day': 'true',
            'interval': '60',
            'utc': 'false',
            'email': 'your_email@example.com',
            'api_key': os.getenv('NSRDB_API_KEY', 'DEMO_KEY')
        }
        
        try:
            if not HAS_REQUESTS:
                logger.warning("requests library not available")
                return {}
            
            response = requests.get(api_endoint, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✓ NSRDB data fetched: {len(data.get('outputs', {}).get('solar_resource', []))} records")
            
            return data
        
        except Exception as e:
            logger.error(f"Error fetching NSRDB: {e}")
            return {}
    
    # ========================================================================
    # OpenEI - Solar, Wind, Load Data
    # ========================================================================
    
    def fetch_openei_solar_atlas(self, region: str) -> Dict:
        """
        Fetch solar atlas data from OpenEI
        Free annual solar irradiance maps for Africa
        
        Args:
            region: Region name (e.g., 'Angola', 'Southern_Africa')
        
        Returns:
            Solar atlas metadata and download URLs
        """
        logger.info(f"Fetching OpenEI solar atlas for {region}")
        
        openei_url = 'https://data.openei.org/api/3/action/'
        
        datasets = {
            'Angola': 'IRENA-GSAP-Angola-Solar-Atlas-2015',
            'East_Africa': 'East-Africa-Solar-Resource-Dataset',
            'Sub_Saharan': 'Sub-Saharan-Africa-Solar-Resource'
        }
        
        if region not in datasets:
            logger.warning(f"Region {region} not available")
            return {}
        
        dataset_id = datasets[region]
        
        try:
            if not HAS_REQUESTS:
                return {}
            
            # Query OpenEI package info
            url = f"{openei_url}package_show?id={dataset_id}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()['result']
            logger.info(f"✓ OpenEI dataset found: {data['title']}")
            
            # Return dataset metadata and file URLs
            return {
                'title': data['title'],
                'description': data['notes'],
                'files': [{'url': r['url'], 'name': r['name']} for r in data.get('resources', [])],
                'license': data.get('license_id', 'CC-BY-4.0')
            }
        
        except Exception as e:
            logger.error(f"Error fetching OpenEI: {e}")
            return {}
    
    # ========================================================================
    # GEBCO - Global Bathymetry and Topography
    # ========================================================================
    
    def fetch_gebco_elevation(self, west: float, south: float, east: float, north: float) -> Dict:
        """
        Fetch elevation data from GEBCO (General Bathymetric Chart of the Oceans)
        Global 15 arc-second (~500m) resolution DEM
        """
        logger.info(f"Fetching GEBCO elevation for bounds ({west},{south},{east},{north})")
        
        gebco_url = 'https://www.gebco.net/data/gridded_bathymetry_data/'
        file_url = f"{gebco_url}gebco_2023.nc"
        
        try:
            if not HAS_REQUESTS:
                logger.warning("requests library not available")
                return {'url': file_url, 'resolution': '15 arc-seconds', 'format': 'NetCDF'}
            
            # Check file exists
            response = requests.head(file_url, timeout=10)
            if response.status_code == 200:
                logger.info(f"✓ GEBCO available: {response.headers.get('content-length', 'N/A')} bytes")
                
                return {
                    'url': file_url,
                    'resolution': '15 arc-seconds (~500m)',
                    'extent': [west, south, east, north],
                    'coverage': 'Global',
                    'format': 'NetCDF',
                    'note': 'Download via GEBCO website or wget'
                }
            
        except Exception as e:
            logger.warning(f"GEBCO check failed: {e}")
        
        return {'url': file_url, 'note': 'Manual download required from https://www.gebco.net/'}
    
    # ========================================================================
    # WorldPop - Population Data
    # ========================================================================
    
    def fetch_worldpop_population(self, country_code: str = 'AGO', year: int = 2020) -> Dict:
        """
        Fetch population density from WorldPop
        1km resolution global population grid
        
        Args:
            country_code: ISO-3 country code (e.g., 'AGO' for Angola)
            year: Year (2000-2020)
        """
        logger.info(f"Fetching WorldPop population for {country_code} ({year})")
        
        # WorldPop FTP server
        ftp_base = 'ftp://ftp.worldpop.org.uk/GIS/Population/'
        
        # Construct file path
        filename = f'{country_code.lower()}_ppp_{year}_1km_Aggregated.tif'
        file_url = f"{ftp_base}{country_code}/{year}/AGO/{filename}"
        
        logger.info(f"WorldPop dataset: {file_url}")
        
        return {
            'url': file_url,
            'country': country_code,
            'year': year,
            'resolution': '1km',
            'format': 'GeoTIFF',
            'note': 'Download from WorldPop FTP: ftp.worldpop.org.uk'
        }
    
    # ========================================================================
    # Copernicus - Land Cover, Emissions, Climate
    # ========================================================================
    
    def fetch_copernicus_land_cover(self, year: int = 2020) -> Dict:
        """
        Fetch Copernicus Land Cover Map (Discrete Classification)
        100m resolution, 23 land cover classes
        
        Args:
            year: Year (2015, 2017, 2018, 2019, 2020)
        """
        logger.info(f"Fetching Copernicus Land Cover Map {year}")
        
        # Copernicus Climate Data Store (CDS) API
        cds_url = 'https://cds.climate.copernicus.eu/'
        
        # Dataset ID
        dataset_id = f'lc-globcover/{year}'
        
        return {
            'url': 'https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-land-cover',
            'resolution': '100m',
            'year': year,
            'format': 'GeoTIFF',
            'classes': 23,
            'note': 'Register for free CDS access at climate.copernicus.eu',
            'download_note': 'Use CDS API or web interface'
        }
    
    def fetch_copernicus_dem(self) -> Dict:
        """Fetch Copernicus DEM (global 30m DEM)"""
        logger.info("Fetching Copernicus DEM")
        
        return {
            'url': 'http://copernicus-dem-30m.s3.amazonaws.com/',
            'resolution': '30m',
            'coverage': 'Global',
            'format': 'GeoTIFF',
            'bucket': 'copernicus-dem-30m (AWS S3)',
            'note': 'Access via AWS S3 or Copernicus portal'
        }
    
    # ========================================================================
    # USGS - National Map, Geology
    # ========================================================================
    
    def fetch_usgs_dem(self, filename: str = 'SRTM30m.zip') -> Dict:
        """
        Fetch USGS 3DEP (3D Elevation Program) data
        Multiple resolutions: 1/3 arc-second (~10m), 1 arc-second (~30m)
        """
        logger.info("Fetching USGS 3DEP DEM")
        
        return {
            'url': 'https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/SRTM_GL30/SRTM_GL30_srtm/',
            'resolution': '30m (SRTM GL30)',
            'coverage': 'Global',
            'format': 'GeoTIFF',
            'accessing': 'OpenTopography (registration free)',
            'note': 'Also available via USGS Earth Explorer'
        }
    
    # ========================================================================
    # NASA POWER - Solar, Weather Data
    # ========================================================================
    
    def fetch_nasa_power_solar(self, latitude: float, longitude: float) -> Dict:
        """
        Fetch NASA POWER solar and meteorological data (1984-present)
        Free, no API key required
        
        Args:
            latitude, longitude: Location coordinates
        """
        logger.info(f"Fetching NASA POWER for ({latitude}, {longitude})")
        
        api_url = 'https://power.larc.nasa.gov/api/v1/point'
        
        params = {
            'parameters': 'ALLSKY_SFC_SW_DWN,T2M,RH2M,WS10M,PRECTOT',
            'start': '1984',
            'end': datetime.now().year,
            'latitude': latitude,
            'longitude': longitude,
            'format': 'JSON'
        }
        
        try:
            if not HAS_REQUESTS:
                logger.warning("requests library not available")
                return {'url': api_url}
            
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✓ NASA POWER data fetched: {len(data.get('properties', {}).get('parameter', {}))} parameters")
            
            return data
        
        except Exception as e:
            logger.error(f"Error fetching NASA POWER: {e}")
            return {}
    
    # ========================================================================
    # Sentinel Data - Imagery and SAR (via Copernicus Scihub)
    # ========================================================================
    
    def fetch_sentinel_metadata(self, region: str, start_date: str, end_date: str) -> Dict:
        """
        Query Sentinel satellite imagery metadata
        Requires registration at scihub.copernicus.eu
        """
        logger.info(f"Querying Sentinel data for {region} ({start_date} to {end_date})")
        
        scihub_url = 'https://scihub.copernicus.eu/dhus'
        
        return {
            'url': scihub_url,
            'note': 'Register free at https://scihub.copernicus.eu/dhus/#/self-registration',
            'available_missions': ['Sentinel-1', 'Sentinel-2', 'Sentinel-3', 'Sentinel-5P'],
            'documentation': 'https://scihub.copernicus.eu/twiki/do/view/SciHubUserGuide',
            'access': 'API available for automated downloads via Python (sentinelsat library)'
        }
    
    # ========================================================================
    # Summary and Discovery
    # ========================================================================
    
    def list_available_datasets(self) -> Dict:
        """List all available free datasets"""
        return {
            'solar_data': {
                'NSRDB': 'NOAA/NREL hourly solar (1998-2023)',
                'OpenEI': 'Solar atlas data for Africa',
                'NASA_POWER': 'Monthly solar data (1984-present)'
            },
            'elevation': {
                'GEBCO': 'Global bathymetry/topography (500m)',
                'SRTM30': 'USGS 3DEP 30m DEM',
                'Copernicus': 'Global 30m DEM'
            },
            'land_cover': {
                'Copernicus': '100m LC map (23 classes)',
                'GEDI': 'NASA forest canopy height (GEDI L2B)',
                'Sentinel-1/2': 'Optical and SAR imagery'
            },
            'population': {
                'WorldPop': '1km population density grid'
            },
            'weather': {
                'NASA_POWER': 'Temperature, rainfall, wind, RH',
                'NOAA_GFSANL': 'Historical weather analysis'
            }
        }
    
    def download_dataset(self, source: str, dataset: str, crop_bounds: Optional[tuple] = None) -> str:
        """
        Generic download function for available datasets
        Saves to data/raw/
        """
        logger.info(f"Preparing download: {source}/{dataset}")
        
        if source == 'noaa':
            method = getattr(self, 'fetch_nsrdb_solar_data', None)
        elif source == 'openei':
            method = getattr(self, 'fetch_openei_solar_atlas', None)
        elif source == 'gebco':
            method = getattr(self, 'fetch_gebco_elevation', None)
        elif source == 'worldpop':
            method = getattr(self, 'fetch_worldpop_population', None)
        elif source == 'copernicus':
            method = getattr(self, 'fetch_copernicus_land_cover', None)
        elif source == 'nasa_power':
            method = getattr(self, 'fetch_nasa_power_solar', None)
        else:
            raise ValueError(f"Unknown source: {source}")
        
        if not method:
            raise ValueError(f"Dataset {dataset} not found for source {source}")
        
        # Call appropriate method
        result = method(dataset) if source in ['openei', 'worldpop', 'copernicus'] else method()
        
        logger.info(json.dumps(result, indent=2))
        
        return str(self.cache_dir)


def main():
    parser = argparse.ArgumentParser(description='Free Datasets Integration')
    parser.add_argument('--source', help='Data source (noaa, openei, gebco, worldpop, copernicus, nasa_power)')
    parser.add_argument('--dataset', help='Dataset name')
    parser.add_argument('--region', help='Region (Angola, Angola_Luanda, etc.)')
    parser.add_argument('--list', action='store_true', help='List available datasets')
    parser.add_argument('--output', help='Output directory')
    
    args = parser.parse_args()
    
    try:
        datasets = FreeDatasets(cache_dir=args.output or 'data/raw')
        
        if args.list:
            print(json.dumps(datasets.list_available_datasets(), indent=2))
            return 0
        
        if args.source and args.dataset:
            datasets.download_dataset(args.source, args.dataset)
            return 0
        
        parser.print_help()
        return 1
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
