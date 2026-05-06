#!/usr/bin/env python3
"""
ETL/Data Ingestion Automation for GEESP-Angola
Populates data/processed/ from raw data sources
Usage: python scripts/data_ingestion_etl.py [--source TYPE] [--output DIR]
"""

import os
import sys
import json
import csv
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_ingestion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class SurveyLocation:
    """Survey location data model"""
    location_id: str
    name: str
    latitude: float
    longitude: float
    province: str
    district: str
    population: int = 0
    solar_potential: float = 0.0  # kWh/m²/day
    poverty_rate: float = 0.0  # percentage


class DataIngestionETL:
    """Main ETL processor for GEESP-Angola"""
    
    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data = {}
        logger.info(f"ETL initialized with output directory: {self.output_dir}")
    
    def ingest_community_survey_data(self, source_file: str) -> List[Dict[str, Any]]:
        """
        Ingest community survey data from CSV
        Expected columns: location_id, name, latitude, longitude, province, district, population
        """
        logger.info(f"Ingesting community survey data from {source_file}")
        
        communities = []
        if not Path(source_file).exists():
            logger.warning(f"Source file not found: {source_file}")
            return communities
        
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        location = SurveyLocation(
                            location_id=row.get('location_id', ''),
                            name=row.get('name', ''),
                            latitude=float(row.get('latitude', 0)),
                            longitude=float(row.get('longitude', 0)),
                            province=row.get('province', ''),
                            district=row.get('district', ''),
                            population=int(row.get('population', 0)),
                            solar_potential=float(row.get('solar_potential', 0.0)),
                            poverty_rate=float(row.get('poverty_rate', 0.0))
                        )
                        communities.append(location.__dict__)
                    except (ValueError, TypeError) as e:
                        logger.error(f"Error parsing row {row}: {e}")
                        continue
            
            logger.info(f"Successfully ingested {len(communities)} communities")
            return communities
        
        except Exception as e:
            logger.error(f"Error ingesting survey data: {e}")
            return communities
    
    def ingest_geospatial_raster_data(self, source_dir: str) -> Dict[str, str]:
        """
        Ingest geospatial raster files (GeoTIFF, NetCDF)
        Expects directory structure: source_dir/[irradiance|elevation|land_use]/...
        """
        logger.info(f"Ingesting geospatial raster data from {source_dir}")
        
        raster_files = {}
        source_path = Path(source_dir)
        
        if not source_path.exists():
            logger.warning(f"Raster source directory not found: {source_dir}")
            return raster_files
        
        try:
            # Find all GeoTIFF and NetCDF files
            for raster_type in ['irradiance', 'elevation', 'land_use']:
                type_dir = source_path / raster_type
                if type_dir.exists():
                    files = list(type_dir.glob('*.tif')) + list(type_dir.glob('*.nc'))
                    for file in files:
                        # Copy to processed directory (or link)
                        output_file = self.output_dir / f"{raster_type}_{file.name}"
                        if not output_file.exists():
                            # In production, would do actual copying
                            logger.info(f"Would process: {file} -> {output_file}")
                        raster_files[f"{raster_type}:{file.stem}"] = str(output_file)
            
            logger.info(f"Found {len(raster_files)} raster files")
            return raster_files
        
        except Exception as e:
            logger.error(f"Error ingesting raster data: {e}")
            return raster_files
    
    def ingest_energy_data(self, source_file: str) -> List[Dict[str, Any]]:
        """Ingest energy consumption and generation data"""
        logger.info(f"Ingesting energy data from {source_file}")
        
        energy_records = []
        if not Path(source_file).exists():
            logger.warning(f"Energy source file not found: {source_file}")
            return energy_records
        
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        record = {
                            'location_id': row.get('location_id', ''),
                            'year': int(row.get('year', 0)),
                            'consumption_kwh': float(row.get('consumption_kwh', 0)),
                            'generation_kwh': float(row.get('generation_kwh', 0)),
                            'grid_availability_hours': int(row.get('grid_availability_hours', 0))
                        }
                        energy_records.append(record)
                    except (ValueError, TypeError) as e:
                        logger.error(f"Error parsing energy row {row}: {e}")
                        continue
            
            logger.info(f"Successfully ingested {len(energy_records)} energy records")
            return energy_records
        
        except Exception as e:
            logger.error(f"Error ingesting energy data: {e}")
            return energy_records
    
    def transform_and_validate(self, data: Dict[str, Any]) -> bool:
        """Data quality checks and transformations"""
        logger.info("Validating and transforming data")
        
        try:
            # Validate communities
            if 'communities' in data:
                communities = data['communities']
                logger.info(f"Validating {len(communities)} communities...")
                
                # Check for required fields
                for i, community in enumerate(communities):
                    if not all(k in community for k in ['location_id', 'latitude', 'longitude']):
                        logger.warning(f"Community {i} missing required fields")
                        communities[i]['valid'] = False
                
                # Filter out invalid communities
                valid_communities = [c for c in communities if c.get('valid', True)]
                data['communities'] = valid_communities
                logger.info(f"{len(valid_communities)} communities passed validation")
            
            # Validate energy data
            if 'energy' in data:
                energy_records = data['energy']
                logger.info(f"Validating {len(energy_records)} energy records...")
                
                valid_energy = []
                for record in energy_records:
                    try:
                        # Validate numeric ranges
                        if record.get('consumption_kwh', 0) >= 0 and record.get('generation_kwh', 0) >= 0:
                            valid_energy.append(record)
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Invalid energy record: {record} - {e}")
                
                data['energy'] = valid_energy
                logger.info(f"{len(valid_energy)} energy records passed validation")
            
            return True
        
        except Exception as e:
            logger.error(f"Error during transformation: {e}")
            return False
    
    def load_to_csv(self, data: Dict[str, Any]) -> bool:
        """Load processed data to CSV files in data/processed/"""
        logger.info("Loading data to CSV files")
        
        try:
            # Write communities
            if 'communities' in data:
                communities_file = self.output_dir / 'communities.csv'
                communities = data['communities']
                
                if communities:
                    keys = communities[0].keys()
                    with open(communities_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=keys)
                        writer.writeheader()
                        writer.writerows(communities)
                    logger.info(f"Wrote {len(communities)} communities to {communities_file}")
            
            # Write energy data
            if 'energy' in data:
                energy_file = self.output_dir / 'energy_data.csv'
                energy_records = data['energy']
                
                if energy_records:
                    keys = energy_records[0].keys()
                    with open(energy_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=keys)
                        writer.writeheader()
                        writer.writerows(energy_records)
                    logger.info(f"Wrote {len(energy_records)} energy records to {energy_file}")
            
            # Write metadata
            metadata = {
                'timestamp': datetime.now().isoformat(),
                'source': 'geesp_etl_automation',
                'record_counts': {
                    'communities': len(data.get('communities', [])),
                    'energy_records': len(data.get('energy', []))
                }
            }
            
            metadata_file = self.output_dir / 'ingestion_metadata.json'
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            logger.info(f"Wrote metadata to {metadata_file}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error loading data to CSV: {e}")
            return False
    
    def fetch_from_earth_engine(self, dataset_key: str, region: str = 'angola') -> Dict[str, Any]:
        """
        Fetch data from Google Earth Engine
        Requires authentication: earthengine authenticate
        """
        logger.info(f"Fetching from Earth Engine: {dataset_key} for {region}")
        
        try:
            from scripts.earth_engine_integration import EarthEngineIntegration
            
            ee_integration = EarthEngineIntegration()
            result = ee_integration.fetch_dataset(
                dataset_key=dataset_key,
                region=region,
                start_date='2023-01-01',
                end_date='2023-12-31'
            )
            
            logger.info(f"✓ Earth Engine data fetched: {result}")
            return result
        
        except ImportError:
            logger.warning("earthengine-api not installed. Skipping Earth Engine.")
        except Exception as e:
            logger.error(f"Error fetching from Earth Engine: {e}")
        
        return {}
    
    def fetch_from_free_datasets(self, source: str, dataset: str) -> Dict[str, Any]:
        """
        Fetch data from free public sources
        Supported sources: noaa, openei, gebco, worldpop, copernicus, nasa_power
        """
        logger.info(f"Fetching from {source}: {dataset}")
        
        try:
            from scripts.free_datasets_integration import FreeDatasets
            
            free_data = FreeDatasets(cache_dir='data/raw')
            
            if source == 'noaa_nsrdb':
                # Solar irradiance from NSRDB (requires NSRDB_API_KEY env var)
                result = free_data.fetch_nsrdb_solar_data(-8.84, 13.23)  # Luanda coords
            elif source == 'openei':
                result = free_data.fetch_openei_solar_atlas(dataset)
            elif source == 'gebco':
                result = free_data.fetch_gebco_elevation(-6, 11, 24, -4)  # Angola bounds
            elif source == 'worldpop':
                result = free_data.fetch_worldpop_population(dataset or 'AGO', 2020)
            elif source == 'copernicus':
                if dataset == 'land_cover':
                    result = free_data.fetch_copernicus_land_cover(2020)
                elif dataset == 'dem':
                    result = free_data.fetch_copernicus_dem()
                else:
                    result = {}
            elif source == 'nasa_power':
                result = free_data.fetch_nasa_power_solar(-8.84, 13.23)  # Luanda coords
            else:
                logger.warning(f"Unknown source: {source}")
                result = {}
            
            logger.info(f"✓ Free dataset info retrieved: {source}/{dataset}")
            return result
        
        except Exception as e:
            logger.error(f"Error fetching from free datasets: {e}")
            return {}
    
    def save_dataset_metadata(self, datasets_info: List[Dict[str, Any]]) -> bool:
        """Save information about fetched datasets to metadata file"""
        logger.info("Saving dataset metadata")
        
        try:
            metadata_file = self.output_dir / 'datasets_metadata.json'
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'description': 'Metadata about geospatial datasets used in analysis',
                    'datasets': datasets_info
                }, f, indent=2)
            
            logger.info(f"Saved dataset metadata to {metadata_file}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
            return False
    
    def run_etl_pipeline(self, sources: Dict[str, str], fetch_earth_engine: bool = False, 
                        fetch_free_datasets: bool = False) -> bool:
        """
        Execute full ETL pipeline with optional external data sources
        
        Args:
            sources: Dict with paths to local data sources
            fetch_earth_engine: Fetch from Google Earth Engine
            fetch_free_datasets: Fetch from free public sources
        """
        logger.info("Starting ETL pipeline")
        
        try:
            # EXTRACT
            data = {
                'communities': self.ingest_community_survey_data(
                    sources.get('communities', 'data/raw/communities.csv')
                ),
                'energy': self.ingest_energy_data(
                    sources.get('energy', 'data/raw/energy_data.csv')
                ),
                'rasters': self.ingest_geospatial_raster_data(
                    sources.get('rasters', 'data/raw/rasters')
                )
            }
            
            # Optional: Fetch external data
            datasets_info = []
            if fetch_earth_engine:
                logger.info("Fetching data from Google Earth Engine...")
                for dataset in ['elevation', 'solar_irradiance', 'land_cover']:
                    info = self.fetch_from_earth_engine(dataset, 'angola')
                    if info:
                        datasets_info.append(info)
            
            if fetch_free_datasets:
                logger.info("Fetching data from free public sources...")
                for source, dataset in [('noaa_nsrdb', None), ('copernicus', 'land_cover'), 
                                       ('worldpop', 'AGO'), ('nasa_power', None)]:
                    info = self.fetch_from_free_datasets(source, dataset)
                    if info:
                        datasets_info.append(info)
            
            if datasets_info:
                self.save_dataset_metadata(datasets_info)
            
            # TRANSFORM
            if not self.transform_and_validate(data):
                logger.error("Transform/validate step failed")
                return False
            
            # LOAD
            if not self.load_to_csv(data):
                logger.error("Load step failed")
                return False
            
            logger.info("ETL pipeline completed successfully")
            return True
        
        except Exception as e:
            logger.error(f"ETL pipeline error: {e}")
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='GEESP-Angola Data Ingestion ETL')
    parser.add_argument('--communities', default='data/raw/communities.csv',
                        help='Path to communities survey CSV')
    parser.add_argument('--energy', default='data/raw/energy_data.csv',
                        help='Path to energy data CSV')
    parser.add_argument('--rasters', default='data/raw/rasters',
                        help='Path to raster data directory')
    parser.add_argument('--output', default='data/processed',
                        help='Output directory for processed data')
    parser.add_argument('--earth-engine', action='store_true',
                        help='Fetch data from Google Earth Engine (requires authentication)')
    parser.add_argument('--free-datasets', action='store_true',
                        help='Fetch data from free public sources (NOAA, Copernicus, etc.)')
    parser.add_argument('--all-sources', action='store_true',
                        help='Fetch from all available sources')
    
    args = parser.parse_args()
    
    etl = DataIngestionETL(output_dir=args.output)
    
    sources = {
        'communities': args.communities,
        'energy': args.energy,
        'rasters': args.rasters
    }
    
    fetch_ee = args.earth_engine or args.all_sources
    fetch_free = args.free_datasets or args.all_sources
    
    success = etl.run_etl_pipeline(sources, fetch_earth_engine=fetch_ee, 
                                    fetch_free_datasets=fetch_free)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
