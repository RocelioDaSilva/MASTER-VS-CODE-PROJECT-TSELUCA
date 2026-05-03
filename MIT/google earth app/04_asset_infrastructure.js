// =====================================================================
// 🚗 CALCULATIONS: INFRASTRUCTURE ANALYSIS
// =====================================================================
// This script performs COMPUTATIONALLY EXPENSIVE calculations
// Multiple distance transforms - VERY EXPENSIVE operations!
// =====================================================================

var STUDY_AREA = {
  country: ee.FeatureCollection('FAO/GAUL/2015/level0')
              .filter(ee.Filter.eq('ADM0_NAME', 'Angola'))
};

var CONFIG = {
  dataSources: {
    nightlights: ['2023-01-01', '2025-12-31'],
    population: 2020
  },
  analysis: {
    scale: 1000,
    maxPixels: 1e9
  },
  assets: {
    basePath: 'users/YOUR_USERNAME/angola_solar/'
  }
};

var DIST_SCALE = CONFIG.analysis.scale * 2;

function computeDistanceKm(mask) {
  var coarse = mask
    .unmask(0)
    .reproject({crs: 'EPSG:4326', scale: DIST_SCALE});
  return coarse.fastDistanceTransform()
    .sqrt()
    .multiply(DIST_SCALE / 1000.0);
}

print('🔄 Computing Infrastructure Assets...');
print('⏱️ This may take several minutes...');

// =====================================================================
// ACCESSIBILITY & ROADS
// =====================================================================
var accessibility = ee.Image('Oxford/MAP/accessibility_to_cities_2015_v1_0').clip(STUDY_AREA.country);
var roadAccessScore = accessibility.multiply(-0.0001).add(1).clamp(0.1, 1).rename('road_access_score');
var roadConnectivityScore = ee.Image.constant(0.5).clip(STUDY_AREA.country).rename('road_connectivity_score');

// =====================================================================
// GRID INFRASTRUCTURE
// =====================================================================
var gridConnectionScore = accessibility.multiply(-0.00005).add(0.5).clamp(0.1, 1).rename('grid_connection_score');

var majorCities = ee.FeatureCollection('FAO/GAUL/2015/level1')
  .filter(ee.Filter.eq('ADM0_NAME', 'Angola'))
  .filter(ee.Filter.gt('Shape_Area', 1000000000));

var substationMask = ee.Image().byte().paint(majorCities, 1);
var substationProximity = computeDistanceKm(substationMask).clamp(0, 200).rename('substation_distance_km');
var substationAccessScore = substationProximity.multiply(-0.1).add(1).clamp(0.1, 1).rename('substation_access_score');

// =====================================================================
// POPULATION & DEMAND
// =====================================================================
var population = ee.ImageCollection('WorldPop/GP/100m/pop')
  .filter(ee.Filter.eq('country', 'AGO'))
  .filter(ee.Filter.eq('year', 2020))
  .first()
  .clip(STUDY_AREA.country)
  .rename('population');

var populationCenters = population.gt(50);
var demandDistance = computeDistanceKm(populationCenters).clamp(0, 150).rename('demand_distance_km');
var demandProximityScore = demandDistance.multiply(-0.008).add(1).clamp(0.1, 1).rename('demand_proximity_score');

// =====================================================================
// NIGHT LIGHTS & GRID COVERAGE
// =====================================================================
var nightLights = ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG')
  .filterDate(CONFIG.dataSources.nightlights[0], CONFIG.dataSources.nightlights[1])
  .select('avg_rad')
  .median()
  .clip(STUDY_AREA.country)
  .rename('night_lights');

var popNorm = population.unitScale(0, 1000);
var lightsNorm = nightLights.unitScale(0, 30);
var energyNeedIndex = popNorm.multiply(ee.Image(1).subtract(lightsNorm)).rename('energy_need_index');
var gridCoverageProxy = lightsNorm.rename('grid_coverage_proxy');

var gridConnectionPotential = gridConnectionScore
  .multiply(0.4)
  .add(substationAccessScore.multiply(0.3))
  .add(gridCoverageProxy.multiply(0.3))
  .clamp(0, 1)
  .rename('grid_connection_potential');

// =====================================================================
// WATER ACCESSIBILITY
// =====================================================================
var permanentWater = ee.Image('JRC/GSW1_4/GlobalSurfaceWater')
  .select('occurrence')
  .gt(80)
  .clip(STUDY_AREA.country);

var rivers = ee.FeatureCollection('WWF/HydroSHEDS/v1/FreeFlowingRivers')
  .filterBounds(STUDY_AREA.country);
var riverNetwork = ee.Image().byte().paint(rivers, 1);
var waterBodies = permanentWater.or(riverNetwork);
var waterDistance = computeDistanceKm(waterBodies).clamp(0, 100).rename('water_distance_km');
var waterAccessScore = waterDistance.subtract(3).abs().multiply(-0.1).add(1).clamp(0.2, 1).rename('water_access_score');

// =====================================================================
// INFRASTRUCTURE CONFLICT
// =====================================================================
var infrastructureConflictScore = ee.Image.constant(0.8).clip(STUDY_AREA.country).rename('infrastructure_conflict_score');

// =====================================================================
// SETTLEMENT CONNECTIVITY
// =====================================================================
var settlementPoints = ee.FeatureCollection('FAO/GAUL/2015/level2')
  .filterBounds(STUDY_AREA.country);
var settlementMask = ee.Image().byte().paint(settlementPoints, 1);
var settlementDistance = computeDistanceKm(settlementMask).clamp(0, 150).rename('settlement_distance_km');
var losConnectivityScore = settlementDistance.multiply(-0.015).add(1).clamp(0.2, 1).rename('los_connectivity_score');

// =====================================================================
// COMBINE INTO SINGLE IMAGE
// =====================================================================
var infrastructureAssets = ee.Image.cat([
  accessibility, roadAccessScore, roadConnectivityScore,
  gridConnectionScore, gridConnectionPotential, substationProximity, substationAccessScore, gridCoverageProxy,
  population, demandDistance, demandProximityScore,
  nightLights, energyNeedIndex,
  waterDistance, waterAccessScore,
  infrastructureConflictScore,
  settlementDistance, losConnectivityScore
]).rename([
  'accessibility', 'road_access_score', 'road_connectivity_score',
  'grid_connection_score', 'grid_connection_potential', 'substation_distance_km', 'substation_access_score', 'grid_coverage_proxy',
  'population', 'demand_distance_km', 'demand_proximity_score',
  'night_lights', 'energy_need_index',
  'water_distance_km', 'water_access_score',
  'infrastructure_conflict_score',
  'settlement_distance_km', 'los_connectivity_score'
]);

// =====================================================================
// EXPORT AS ASSET
// =====================================================================
Export.image.toAsset({
  image: infrastructureAssets,
  description: 'Angola_Infrastructure_Assets',
  assetId: CONFIG.assets.basePath + 'infrastructure',
  region: STUDY_AREA.country.geometry(),
  scale: CONFIG.analysis.scale,
  maxPixels: CONFIG.analysis.maxPixels,
  crs: 'EPSG:4326'
});

print('✅ Infrastructure Assets export task created!');
print('📋 Check Tasks tab to run the export');
print('💡 Asset will be saved at: ' + CONFIG.assets.basePath + 'infrastructure');