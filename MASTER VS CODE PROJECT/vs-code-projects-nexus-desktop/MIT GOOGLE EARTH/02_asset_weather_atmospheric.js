// =====================================================================
// 🌤️ CALCULATIONS: WEATHER & ATMOSPHERIC ANALYSIS
// =====================================================================
// This script performs COMPUTATIONALLY EXPENSIVE calculations
// Processes 26,280+ hourly images - VERY EXPENSIVE!
// =====================================================================

// Load setup (same as solar resource script)
var STUDY_AREA = {
  country: ee.FeatureCollection('FAO/GAUL/2015/level0')
              .filter(ee.Filter.eq('ADM0_NAME', 'Angola'))
};

var CONFIG = {
  dataSources: {
    weather: ['2023-01-01', '2025-12-31']
  },
  analysis: {
    scale: 1000,
    maxPixels: 1e9
  },
  assets: {
    basePath: 'users/YOUR_USERNAME/angola_solar/'
  }
};

print('🔄 Computing Weather & Atmospheric Assets...');
print('⏱️ This may take several minutes...');

// =====================================================================
// TEMPERATURE ANALYSIS
// =====================================================================
var temperature = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY')
  .filterDate(CONFIG.dataSources.weather[0], CONFIG.dataSources.weather[1])
  .select('temperature_2m')
  .mean()
  .subtract(273.15)
  .clip(STUDY_AREA.country)
  .rename('temperature');

var tempDailyMax = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR')
  .filterDate(CONFIG.dataSources.weather[0], CONFIG.dataSources.weather[1])
  .select('temperature_2m_max')
  .mean()
  .subtract(273.15)
  .clip(STUDY_AREA.country)
  .rename('temp_max');

var tempDailyMin = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR')
  .filterDate(CONFIG.dataSources.weather[0], CONFIG.dataSources.weather[1])
  .select('temperature_2m_min')
  .mean()
  .subtract(273.15)
  .clip(STUDY_AREA.country)
  .rename('temp_min');

var tempRange = tempDailyMax.subtract(tempDailyMin).rename('temp_range');
var tempEfficiency = temperature.multiply(-0.0045).add(1.0).clamp(0.75, 1.0).rename('temp_efficiency');

// =====================================================================
// WIND ANALYSIS
// =====================================================================
var windU = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY')
  .filterDate(CONFIG.dataSources.weather[0], CONFIG.dataSources.weather[1])
  .select('u_component_of_wind_10m')
  .mean()
  .clip(STUDY_AREA.country);

var windV = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY')
  .filterDate(CONFIG.dataSources.weather[0], CONFIG.dataSources.weather[1])
  .select('v_component_of_wind_10m')
  .mean()
  .clip(STUDY_AREA.country);

var windSpeed = windU.pow(2).add(windV.pow(2)).sqrt().rename('wind_speed');
var windDirection = windV.atan2(windU).multiply(180).divide(Math.PI).add(180).rename('wind_direction');
var windCooling = windSpeed.subtract(2).abs().multiply(-0.15).add(1).clamp(0.85, 1.1).rename('wind_cooling');

// =====================================================================
// HUMIDITY & PRECIPITATION
// =====================================================================
var humidity = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY')
  .filterDate(CONFIG.dataSources.weather[0], CONFIG.dataSources.weather[1])
  .select('dewpoint_temperature_2m')
  .mean()
  .subtract(273.15)
  .clip(STUDY_AREA.country)
  .rename('dewpoint');

var relativeHumidity = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY')
  .filterDate(CONFIG.dataSources.weather[0], CONFIG.dataSources.weather[1])
  .select('relative_humidity_2m')
  .mean()
  .clip(STUDY_AREA.country)
  .rename('relative_humidity');

var precipitation = ee.ImageCollection('ECMWF/ERA5_LAND/HOURLY')
  .filterDate(CONFIG.dataSources.weather[0], CONFIG.dataSources.weather[1])
  .select('total_precipitation_hourly')
  .sum()
  .multiply(1000)
  .clip(STUDY_AREA.country)
  .rename('annual_precipitation');

var precipCleaning = precipitation.subtract(500).abs().multiply(-0.0004).add(1).clamp(0.8, 1.1).rename('precip_cleaning');

// =====================================================================
// COMBINE INTO SINGLE IMAGE
// =====================================================================
var weatherAssets = ee.Image.cat([
  temperature, tempDailyMax, tempDailyMin, tempRange, tempEfficiency,
  windSpeed, windDirection, windCooling,
  humidity, relativeHumidity, precipitation, precipCleaning
]).rename([
  'temperature', 'temp_max', 'temp_min', 'temp_range', 'temp_efficiency',
  'wind_speed', 'wind_direction', 'wind_cooling',
  'dewpoint', 'relative_humidity', 'annual_precipitation', 'precip_cleaning'
]);

// =====================================================================
// EXPORT AS ASSET
// =====================================================================
Export.image.toAsset({
  image: weatherAssets,
  description: 'Angola_Weather_Atmospheric_Assets',
  assetId: CONFIG.assets.basePath + 'weather_atmospheric',
  region: STUDY_AREA.country.geometry(),
  scale: CONFIG.analysis.scale,
  maxPixels: CONFIG.analysis.maxPixels,
  crs: 'EPSG:4326'
});

print('✅ Weather & Atmospheric Assets export task created!');
print('📋 Check Tasks tab to run the export');
print('💡 Asset will be saved at: ' + CONFIG.assets.basePath + 'weather_atmospheric');