# Free and Open Geospatial Datasets Setup Guide

## Overview

GEESP-Angola integrates with multiple free geospatial data sources:
- **Google Earth Engine**: Curated satellite imagery, weather, climate
- **NOAA**: Solar irradiance (NSRDB), weather analysis
- **OpenEI**: Solar atlas data, energy datasets
- **GEBCO**: Global elevation and bathymetry
- **WorldPop**: Population density grids
- **Copernicus**: Land cover, digital elevation, air quality
- **USGS**: National Map, geological data
- **NASA POWER**: Solar and meteorological data
- **Sentinel**: High-resolution satellite imagery

## Installation

### Core Requirements

```bash
# Basic geospatial tools
pip install numpy pandas geopandas rasterio shapely

# Earth Engine (Google)
pip install google-auth earthengine-api

# Data access
pip install requests netCDF4 xarray dask

# Optional: Geospatial visualization
pip install folium matplotlib cartopy
```

## Google Earth Engine Setup

### 1. Create Google Cloud Project

```bash
# Go to Google Cloud Console
# https://console.cloud.google.com/

# Create new project: geesp-angola
# Enable Earth Engine API
# Create service account (or use personal account)
```

### 2. Authenticate

```bash
# Option A: Personal account (interactive)
earthengine authenticate

# Option B: Service account (automated)
earthengine authenticate --auth_mode=service_account

# Verify authentication
python -c "import ee; ee.Initialize(); print('✓ Authenticated')"
```

### 3. Use Earth Engine in Code

```python
import ee
from scripts.earth_engine_integration import EarthEngineIntegration

# Initialize
ee_data = EarthEngineIntegration(project_id='your-project-id')

# Fetch solar potential
solar = ee_data.fetch_solar_potential('angola', year=2023)
print(solar)

# Export to GeoTIFF
results = ee_data.fetch_dataset(
    'solar_irradiance',
    region='luanda',
    start_date='2023-01-01',
    end_date='2023-12-31',
    output_file='solar_irradiance_2023.tif'
)
```

### Available Earth Engine Datasets

| Dataset | Key | Resolution | Coverage |
|---------|-----|-----------|----------|
| Solar Irradiance | `solar_irradiance` | 40km | Global |
| Elevation (SRTM) | `elevation` | 30m | ±60° latitude |
| Land Cover | `land_cover` | 100m | Global |
| NDVI (Vegetation) | `ndvi` | 250m | Global |
| Land Temp (LST) | `lst` | 1km | Global |
| Population | `population` | 1km | Global |
| Nightlights | `nightlights` | 500m | Global |
| Rainfall | `rainfall` | 11km | 65°N-65°S |

### Pre-configured Regions

- `angola` — Full country
- `luanda` — Luanda Province (headquarters)
- `huambo` — Huambo Province (regional)
- `benguela` — Benguela Province (field station)

## NSRDB Solar Data (NOAA/NREL)

Free hourly solar irradiance data (1998-2023) for any location.

### Step 1: Register for API Key

```bash
# Go to https://nsrdb.nrel.gov/api
# Email activation may be required
# Copy your API key
```

### Step 2: Set Environment Variable

```bash
export NSRDB_API_KEY="your_api_key_here"
```

### Step 3: Query Data

```python
from scripts.earth_engine_integration import EarthEngineIntegration

ee_data = EarthEngineIntegration()
solar_data = ee_data.fetch_nsrdb_solar_data(
    latitude=-8.84,   # Luanda
    longitude=13.23
)
```

## OpenEI Solar Data

Pre-computed solar atlas for Africa regions.

### Available Datasets

```python
from scripts.free_datasets_integration import FreeDatasets

datasets = FreeDatasets()

# Angola solar atlas
angola_solar = datasets.fetch_openei_solar_atlas('Angola')
print(angola_solar['files'])  # Download URLs
```

### Manual Download

1. Go to [https://data.openei.org/](https://data.openei.org/)
2. Search: "IRENA GSAP Angola Solar Atlas"
3. Download GeoTIFF files
4. Save to `data/raw/openei/`

## GEBCO Elevation Data

Global bathymetry and topography (500m resolution).

### Automated Download

```python
from scripts.free_datasets_integration import FreeDatasets

datasets = FreeDatasets()

# Get download info
gebco_info = datasets.fetch_gebco_elevation(
    west=13.0, south=-8.8,
    east=14.0, north=-8.7
)

print(gebco_info['url'])  # Direct download URL
```

### Manual Download

```bash
# Download via wget
wget https://www.gebco.net/data/gebco_2023/gebco_2023.nc

# Or via curl
curl -O https://www.gebco.net/data/gebco_2023/gebco_2023.nc

# Extract elevation for Angola
python scripts/extract_gebco_region.py --bounds 5:24:11:-4 --output data/raw/elevation.tif
```

## WorldPop Population Data

1km resolution population density maps.

### Download

```python
from scripts.free_datasets_integration import FreeDatasets

datasets = FreeDatasets()

# Get Angola 2020 population data
pop = datasets.fetch_worldpop_population(country_code='AGO', year=2020)
print(pop['url'])
```

### Via FTP

```bash
# Download Angola 2020 population
wget ftp://ftp.worldpop.org.uk/GIS/Population/AGO/2020/AGO/ago_ppp_2020_1km_Aggregated.tif

# Move to data/raw/
mv ago_ppp_2020_1km_Aggregated.tif data/raw/worldpop_2020.tif
```

## Copernicus Land Cover

100m resolution land cover classification (23 classes).

### Access via Climate Data Store

1. Register free at [climate.copernicus.eu](https://climate.copernicus.eu)
2. Install CDS API:
   ```bash
   pip install cdsapi
   ```
3. Download data:
   ```bash
   cds request 'satellite-land-cover' \
     year=2020 \
     month=1 \
     version='v2.1.1'
   ```

### Direct Download (AWS S3)

```bash
# Copernicus has datasets on AWS S3 (anonymous access)
aws s3 ls s3://copernicus-dem-30m/ --no-sign-request

# Download Angola region
aws s3 cp s3://copernicus-dem-30m/cog/ data/raw/ \
  --recursive \
  --no-sign-request \
  --exclude "*" \
  --include "*_N10_*" --include "*_S10_*"
```

## NASA POWER Solar Data

Monthly solar and meteorological data (1984-present), no API key required.

### Usage

```python
from scripts.free_datasets_integration import FreeDatasets

datasets = FreeDatasets()

# Fetch for Luanda
nasa_data = datasets.fetch_nasa_power_solar(
    latitude=-8.84,
    longitude=13.23
)

# Get specific parameters:
# ALLSKY_SFC_SW_DWN = Solar irradiance
# T2M = Temperature at 2m
# RH2M = Relative humidity
# WS10M = Wind speed at 10m
# PRECTOT = Total precipitation
```

### Web Interface

Visit [power.larc.nasa.gov](https://power.larc.nasa.gov/) for interactive downloads.

## Sentinel Satellite Data

High-resolution optical (Sentinel-2) and SAR (Sentinel-1) imagery.

### Setup

```bash
# Install sentinelsat for automated downloads
pip install sentinelsat

# Register free at https://scihub.copernicus.eu/dhus
```

### Download Script

```python
from sentinelsat import SentinelAPI

api = SentinelAPI('username', 'password', 'https://apihub.copernicus.eu/apihub')

# Search for Sentinel-2 imagery (Angola, recent)
products = api.query(
    wkt='POLYGON((10 -15, 25 -15, 25 -4, 10 -4, 10 -15))',
    producttype='S2MSI1C',
    date=('2023-01-01', '2023-12-31'),
    cloudcoverpercentage=(0, 30)
)

# Download (will be ~1GB per scene)
api.download_all(products, directory_path='data/raw/sentinel2/')
```

## Integrate with ETL Pipeline

Update `scripts/data_ingestion_etl.py` to fetch from these sources:

```python
from scripts.earth_engine_integration import EarthEngineIntegration
from scripts.free_datasets_integration import FreeDatasets

# In ETL class
def fetch_from_earth_engine(self, dataset_key: str, region: str) -> dict:
    """Fetch from Google Earth Engine"""
    ee_integration = EarthEngineIntegration()
    return ee_integration.fetch_dataset(
        dataset_key, region,
        start_date='2023-01-01',
        end_date='2023-12-31',
        output_file=f'data/raw/{dataset_key}_{region}.tif'
    )

def fetch_from_free_sources(self, source: str, dataset: str) -> dict:
    """Fetch from free public sources"""
    datasets = FreeDatasets()
    return datasets.download_dataset(source, dataset)

# In run_etl_pipeline
if sources.get('earth_engine'):
    earth_engine_data = self.fetch_from_earth_engine(
        'solar_irradiance', 'angola'
    )

if sources.get('free_datasets'):
    nasa_data = self.fetch_from_free_sources('nasa_power', 'solar')
```

## Docker Compose Environment Variables

Add to `.env`:

```env
# Google Earth Engine
GOOGLE_APPLICATION_CREDENTIALS=/app/secrets/earth-engine-key.json

# NOAA NSRDB
NSRDB_API_KEY=your_api_key_here

# Copernicus CDS
CDSAPI_URL=https://cds.climate.copernicus.eu/api/v2
CDSAPI_KEY=your_uid:your_api_key

# Sentinel/Copernicus Hub
COPERNICUS_USER=your_username
COPERNICUS_PASSWORD=your_password

# AWS (for anonymous public data)
AWS_REQUEST_PAYER=requester  # Only if accessing requester-pays buckets
```

## Data Volume Estimates

| Source | Domain | Size (Angola) | Cost |
|--------|--------|---------------|------|
| Earth Engine | All | On-demand | Free |
| NSRDB | Solar hourly | ~500MB | Free |
| OpenEI | Solar atlas | ~50MB | Free |
| GEBCO | Elevation | ~200MB | Free |
| WorldPop | Population | ~50MB | Free |
| Copernicus | Land Cover | ~100MB | Free |
| Sentinel-1/2 | Raw imagery | 100GB+ | Free |
| NASA POWER | Weather monthly | ~10MB | Free |

**Total:** ~11GB for comprehensive baseline dataset (annual coverage)

## Scheduling Automated Downloads

Use Cron (Linux) or Task Scheduler (Windows) to keep data fresh:

```bash
# Daily NASA POWER update
0 2 * * * cd /app && python scripts/free_datasets_integration.py --source nasa_power --dataset solar

# Weekly Earth Engine extraction
0 3 * * 0 cd /app && python scripts/earth_engine_integration.py --collection elevation --region angola

# Monthly Sentinel download
0 4 1 * * cd /app && python scripts/sentinel_downloader.py --region angola
```

## References

- [Google Earth Engine Docs](https://developers.google.com/earth-engine)
- [NSRDB Documenta](https://nsrdb.nrel.gov/)
- [OpenEI Datasets](https://openei.org/datasets)
- [GEBCO Bathymetry](https://www.gebco.net/)
- [WorldPop Project](https://www.worldpop.org/)
- [Copernicus Data Hub](https://scihub.copernicus.eu/)
- [NASA POWER](https://power.larc.nasa.gov/docs/)
- [Sentinel Hub](https://www.sentinel-hub.com/)
