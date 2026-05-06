// =====================================================================
// ☀️ CALCULATIONS: SOLAR RESOURCE ANALYSIS
// =====================================================================
// This script performs COMPUTATIONALLY EXPENSIVE calculations and exports
// results as Earth Engine assets for fast loading in display script
// =====================================================================
// 
// WORKFLOW:
// 1. Loads setup/precursors (configuration, study area, helpers)
// 2. Performs expensive calculations (image collection processing)
// 3. Exports results as assets using Export.image.toAsset()
// 4. Assets appear in Assets tab and can be loaded with ee.Image()
// =====================================================================

// =====================================================================
// LOAD SETUP & PRECURSORS
// =====================================================================
// Option 1: If setup script is saved as an asset/module, load it:
// var setup = require('users/YOUR_USERNAME/angola_solar:00_setup_precursors');

// Option 2: Include setup directly (for standalone execution):
var STUDY_AREA = {
  country: ee.FeatureCollection('FAO/GAUL/2015/level0')
              .filter(ee.Filter.eq('ADM0_NAME', 'Angola'))
};

var CONFIG = {
  dataSources: {
    solar: ['2023-01-01', '2025-12-31'],
    weather: ['2023-01-01', '2025-12-31'],
    aerosol: ['2023-01-01', '2025-12-31']
  },
  analysis: {
    scale: 1000,
    maxPixels: 1e9
  },
  assets: {
    basePath: 'users/YOUR_USERNAME/angola_solar/'
  }
};

print('🔄 Computing Solar Resource Assets...');
print('⏱️ This may take several minutes...');

// =====================================================================
// SOLAR IRRADIANCE DATA
// =====================================================================
var ghi = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR')
  .filterDate(CONFIG.dataSources.solar[0], CONFIG.dataSources.solar[1])
  .select('surface_solar_radiation_downwards_sum')
  .mean()
  .divide(3600000)
  .clip(STUDY_AREA.country)
  .rename('GHI');

var ghiAnnual = ghi.multiply(365).rename('GHI_annual');

var clearnessIndex = ghi.divide(8.5);
var dniFraction = clearnessIndex.multiply(0.8).add(0.2);
var dni = ghi.multiply(dniFraction).clamp(0, 10).rename('DNI');
var dhi = ghi.subtract(dni).clamp(0, 10).rename('DHI');

var irradiationClass = ee.Image(0)
  .where(ghiAnnual.lt(1500), 1)
  .where(ghiAnnual.gte(1500).and(ghiAnnual.lt(1800)), 2)
  .where(ghiAnnual.gte(1800).and(ghiAnnual.lt(2000)), 3)
  .where(ghiAnnual.gte(2000), 4)
  .rename('irradiation_class');

// =====================================================================
// SOLAR VARIABILITY & STABILITY
// =====================================================================
var solarVariability = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR')
  .filterDate(CONFIG.dataSources.solar[0], CONFIG.dataSources.solar[1])
  .select('surface_solar_radiation_downwards_sum');

var solarMean = solarVariability.mean().divide(3600000);
var solarStdDev = solarVariability.reduce(ee.Reducer.stdDev());
var solarCV = solarStdDev.divide(solarMean.add(0.1));
var solarStability = ee.Image(1)
  .subtract(solarCV.unitScale(0, 0.5))
  .clamp(0, 1)
  .rename('solar_stability');

// =====================================================================
// AEROSOL ANALYSIS
// =====================================================================
var aerosol = ee.ImageCollection('MODIS/061/MCD19A2_GRANULES')
  .filterDate(CONFIG.dataSources.aerosol[0], CONFIG.dataSources.aerosol[1])
  .select('Optical_Depth_047')
  .mean()
  .clip(STUDY_AREA.country)
  .rename('aerosol_optical_depth');

var dustScore = aerosol.multiply(-0.6).add(1).clamp(0.6, 1.0).rename('dust_transmission');

// =====================================================================
// COMBINE INTO SINGLE IMAGE
// =====================================================================
var solarResourceAssets = ee.Image.cat([
  ghi, ghiAnnual, dni, dhi, irradiationClass,
  solarStability, aerosol, dustScore
]).rename([
  'ghi', 'ghi_annual', 'dni', 'dhi', 'irradiation_class',
  'solar_stability', 'aerosol_optical_depth', 'dust_transmission'
]);

// =====================================================================
// EXPORT AS ASSET
// =====================================================================
// Using Export.image.toAsset() to save processed data
// Docs: https://developers.google.com/earth-engine/guides/export
// 
// IMPORTANT:
// - Exported assets appear in Assets tab
// - Assets can be loaded with: ee.Image('asset/path')
// - Processing in new script does NOT alter original exported asset
// =====================================================================

Export.image.toAsset({
  image: solarResourceAssets,
  description: 'Angola_Solar_Resource_Assets',
  assetId: CONFIG.assets.basePath + 'solar_resource',
  region: STUDY_AREA.country.geometry(),
  scale: CONFIG.analysis.scale,
  maxPixels: CONFIG.analysis.maxPixels,
  crs: 'EPSG:4326'
});

print('✅ Solar Resource Assets export task created!');
print('📋 Check Tasks tab to run the export');
print('💡 After export completes:');
print('   1. Asset will appear in Assets tab');
print('   2. Can be loaded with: ee.Image("' + CONFIG.assets.basePath + 'solar_resource")');
print('   3. Processing in display script does NOT alter this asset');
