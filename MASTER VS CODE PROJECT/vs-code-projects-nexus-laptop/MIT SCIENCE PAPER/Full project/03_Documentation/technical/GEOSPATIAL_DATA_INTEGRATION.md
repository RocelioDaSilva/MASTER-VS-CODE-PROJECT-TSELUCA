# Geospatial Data Integration Guide

## Quick Start: Populate Project with Free Data

The GEESP-Angola project can automatically download and process free geospatial datasets from multiple sources.

### 1. Install Data Integration Tools

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements (including data tools)
pip install -r requirements.txt
pip install earthengine-api google-auth cdsapi sentinelsat
```

### 2. Authenticate for Earth Engine (Optional)

```bash
# Authenticate with Google Earth Engine
earthengine authenticate

# This opens a browser window to authorize the Earth Engine API
# Copy paste the authorization code back into the terminal
```

### 3. Run ETL with Free Datasets

```bash
# Option A: Fetch all available data
python scripts/data_ingestion_etl.py --all-sources --output data/processed

# Option B: Fetch only Earth Engine data
python scripts/data_ingestion_etl.py --earth-engine --output data/processed

# Option C: Fetch only free public datasets (no GEE required)
python scripts/data_ingestion_etl.py --free-datasets --output data/processed
```

### What Gets Downloaded

When you run the ETL with data sources, it automatically fetches:

**From Google Earth Engine:**
- Solar irradiance (NOAA GFS)
- Elevation (SRTM 30m DEM)
- Land cover (Copernicus 100m)
- Vegetation indices (MODIS NDVI)
- Land surface temperature
- Population density

**From Free Public Sources:**
- Solar data from NOAA NSRDB (hourly, 1998-2023)
- Solar atlas from OpenEI (Angola region)
- Elevation from GEBCO (global 500m)
- Population from WorldPop (1km grid)
- Land cover from Copernicus
- Weather from NASA POWER
- Sentinel imagery (optional, requires registration)

## Detailed Integration Examples

### Example 1: Fetch Solar Irradiance for Site Analysis

```python
from scripts.earth_engine_integration import EarthEngineIntegration

# Initialize Earth Engine
ee = EarthEngineIntegration()

# Fetch solar irradiance for Luanda
solar_data = ee.fetch_solar_potential(region='luanda', year=2023)
print(f"Solar irradiance (Luanda): {solar_data['irradiance_mean']} W/m²")

# Fetch elevation data
elevation_data = ee.fetch_dataset(
    dataset_key='elevation',
    region='luanda',
    start_date='2023-01-01',
    end_date='2023-12-31',
    output_file='solar_elevation_luanda.tif'  # Export GeoTIFF
)
```

### Example 2: Assess Environmental Suitability

```python
from scripts.earth_engine_integration import EarthEngineIntegration

ee = EarthEngineIntegration()

# Get vegetation, rainfall, temperature for all of Angola
env_data = ee.fetch_environmental_data(
    region='angola',
    start_date='2023-01-01',
    end_date='2023-12-31'
)

print(f"NDVI (vegetation): {env_data['ndvi_mean']}")
print(f"Precipitation: {env_data['precipitation_mean']} mm")
print(f"Temperature: {env_data['temperature_mean']} K")
```

### Example 3: Download NOAA Solar Data

```python
from scripts.free_datasets_integration import FreeDatasets

# Create instance
datasets = FreeDatasets(cache_dir='data/raw')

# Fetch NOAA NSRDB data (hourly solar, requires API key)
noaa_solar = datasets.fetch_nsrdb_solar_data(
    latitude=-8.84,   # Luanda
    longitude=13.23
)

# Returns hourly solar irradiance data for 25+ years
print(f"NOAA NSRDB data fetched: {len(noaa_solar)} records")
```

### Example 4: Get Population Data

```python
from scripts.free_datasets_integration import FreeDatasets

datasets = FreeDatasets()

# Fetch WorldPop 2020 population grid for Angola
pop_info = datasets.fetch_worldpop_population(country_code='AGO', year=2020)

# Returns download URL and metadata
print(f"Download: {pop_info['url']}")
print(f"Resolution: {pop_info['resolution']}")
```

### Example 5: Integration with MCDA Analysis

```python
from scripts.mcda_analysis import MCDAnalyzer
from scripts.earth_engine_integration import EarthEngineIntegration

# Get Earth Engine data for analysis
ee = EarthEngineIntegration()
elevation = ee.fetch_dataset('elevation', 'angola', '2023-01-01', '2023-12-31')

# Use in MCDA
mcda = MCDAnalyzer(map_shape=(100, 100))

# Incorporate Earth Engine data into criteria
# ... weighted overlay calculations ...
```

## Available Free Datasets Summary

| Source | Dataset | Coverage | Resolution | Format | Setup |
|--------|---------|----------|-----------|--------|-------|
| **Earth Engine** | Solar irradiance | Global | 40km | Tiled | Free account |
| | Elevation (SRTM) | ±60° latitude | 30m | Tiled | Free account |
| | Land cover | Global | 100m | Tiled | Free account |
| | Vegetation (NDVI) | Global | 250m | Tiled | Free account |
| | Temperature | Global | 1km | Tiled | Free account |
| | Population | Global | 1km | Tiled | Free account |
| **NOAA** | Solar (NSRDB) | North/Central America + Angola | Hourly | CSV/NetCDF | API key |
| | Weather (GFS) | Global | ~27km | NetCDF | Free |
| **OpenEI** | Solar atlas | Africa regions | Variable | GeoTIFF | Free download |
| **GEBCO** | Elevation/bathymetry | Global | 500m | NetCDF | Free download |
| **WorldPop** | Population grid | Global | 1km | GeoTIFF | Free download |
| **Copernicus** | Land cover | Global | 100m | GeoTIFF | Free (CDS) |
| | DEM | Global | 30m | GeoTIFF | Free (S3) |
| **USGS** | National Map | North America | Variable | Multiple | Free |
| **NASA POWER** | Solar + weather | Global | Monthly | CSV/JSON | Free (no key) |
| **Sentinel** | Imagery | Global | 10-20m | GeoTIFF | Free (registration) |

## Environment Setup

### Required Environment Variables (Optional)

```bash
# Google Earth Engine (if supported by your cloud environment)
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# NOAA NSRDB API key (free from https://nsrdb.nrel.gov/api)
export NSRDB_API_KEY=your_api_key

# Copernicus CDS API (free from climate.copernicus.eu)
export CDSAPI_URL=https://cds.climate.copernicus.eu/api/v2
export CDSAPI_KEY=your_uid:your_api_key

# Sentinel Hub credentials
export COPERNICUS_USER=your_username
export COPERNICUS_PASSWORD=your_password
```

### Docker Environment

Add to `docker-compose.yml`:

```yaml
environment:
  - NSRDB_API_KEY=${NSRDB_API_KEY}
  - CDSAPI_URL=https://cds.climate.copernicus.eu/api/v2
  - CDSAPI_KEY=${CDSAPI_KEY}
  - GOOGLE_APPLICATION_CREDENTIALS=/app/.secrets/ee-key.json
```

## Workflow Examples

### Complete Analysis Workflow

```bash
# 1. Download all free datasets
python scripts/data_ingestion_etl.py --free-datasets --output data/processed

# 2. Run ETL pipeline to process data
python scripts/data_ingestion_etl.py --communities data/raw/communities.csv --output data/processed

# 3. Run MCDA analysis with populated data
python scripts/mcda_analysis.py --input-communities data/processed/communities.csv

# 4. Run LCOE calculations with environmental data
python scripts/lcoe_calculator.py --elevation-file data/processed/elevation.tif \
                                   --location-file data/processed/communities.csv

# 5. Visualize results
python -c "import streamlit; streamlit.run('Coding parts/geesp-angola/app.py')"
```

### Scheduled Automatic Updates

```bash
# Add to crontab (update daily)
0 2 * * * cd /app && python scripts/data_ingestion_etl.py --free-datasets --output data/processed

# Or with Earth Engine (update weekly)
0 3 * * 0 cd /app && python scripts/data_ingestion_etl.py --all-sources --output data/processed
```

## Troubleshooting

### "Earth Engine not authenticated"

```bash
# Run authentication again
earthengine authenticate

# Or use service account
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

### "requests library not available"

```bash
pip install requests
```

### "NSRDB API key invalid"

```bash
# Get free API key from https://nsrdb.nrel.gov/api
export NSRDB_API_KEY=your_new_key
```

### "netCDF4 not available"

```bash
pip install netCDF4
```

### "Connection timeout"

- Check internet connectivity
- Try reducing the amount of data you're requesting
- Use smaller geographic regions
- Increase timeout values in scripts

## Performance Tips

1. **Cache data locally**: Downloaded datasets are saved to `data/raw/` to avoid re-downloading
2. **Use appropriate resolution**: Higher resolution = slower processing. Use 1km for regional analysis, 30m for local
3. **Filter by date range**: Reducing date ranges speeds up queries
4. **Use regions**: Pre-defined regions (luanda, huambo, benguela) are faster than custom bounds
5. **Batch processing**: Download multiple datasets in one run

## Data Storage

Expected disk space for full Angola dataset:

```
data/raw/
├── communities.csv           ~500 KB
├── energy_data.csv          ~1 MB
├── elevation_angola.tif     ~50 MB   (SRTM 30m)
├── solar_irradiance.tif     ~30 MB   (GFS 40km)
├── land_cover.tif           ~100 MB  (Copernicus 100m)
├── ndvi.tif                 ~40 MB   (MODIS 250m)
└── population.tif           ~50 MB   (WorldPop 1km)

Total: ~270 MB (annual baseline)
```

## Next Steps

1. Run ETL with free datasets: `python scripts/data_ingestion_etl.py --free-datasets`
2. Verify data loaded: Check `data/processed/ingestion_metadata.json`
3. Run full pipeline: `python scripts/data_ingestion_etl.py --all-sources`
4. Analyze results: Use Jupyter notebooks or Streamlit dashboard

## References

- [Earth Engine API Docs](https://developers.google.com/earth-engine)
- [NOAA NSRDB](https://nsrdb.nrel.gov/)
- [OpenEI](https://openei.org/)
- [GEBCO](https://www.gebco.net/)
- [WorldPop](https://www.worldpop.org/)
- [Copernicus](https://climate.copernicus.eu/)
- [NASA POWER](https://power.larc.nasa.gov/)
