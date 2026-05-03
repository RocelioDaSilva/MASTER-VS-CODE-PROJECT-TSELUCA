// =====================================================================
// 🎯 CALCULATIONS: FINAL SUITABILITY
// =====================================================================
// This script loads pre-computed assets and calculates final suitability
// Run this AFTER all other calculation scripts (01-04) are completed
// =====================================================================

// =====================================================================
// LOAD PRE-COMPUTED ASSETS
// =====================================================================
// Assets are loaded using ee.Image() - they appear in Assets tab after export
// Processing here does NOT alter the original exported assets
// =====================================================================

var ASSET_BASE_PATH = 'users/YOUR_USERNAME/angola_solar/';

// Load assets using ee.Image() - these pull from Assets tab
var solarAssets = ee.Image(ASSET_BASE_PATH + 'solar_resource');
var weatherAssets = ee.Image(ASSET_BASE_PATH + 'weather_atmospheric');
var terrainAssets = ee.Image(ASSET_BASE_PATH + 'terrain_environmental');
var infrastructureAssets = ee.Image(ASSET_BASE_PATH + 'infrastructure');

var STUDY_AREA = {
  country: ee.FeatureCollection('FAO/GAUL/2015/level0')
              .filter(ee.Filter.eq('ADM0_NAME', 'Angola'))
};

var STUDY_AREA = {
  country: ee.FeatureCollection('FAO/GAUL/2015/level0')
              .filter(ee.Filter.eq('ADM0_NAME', 'Angola'))
};

print('🔄 Computing Final Suitability Assets...');
print('⏱️ Loading pre-computed assets...');

// =====================================================================
// EXTRACT ASSETS
// =====================================================================
// Solar
var ghi = solarAssets.select('ghi');
var dni = solarAssets.select('dni');
var solarStability = solarAssets.select('solar_stability');
var tempEfficiency = weatherAssets.select('temp_efficiency');
var windCooling = weatherAssets.select('wind_cooling');
var precipCleaning = weatherAssets.select('precip_cleaning');
var dustScore = solarAssets.select('dust_transmission');

// Terrain
var slopeScore = terrainAssets.select('slope_score');
var aspectScore = terrainAssets.select('aspect_score');
var soilSuitabilityScore = terrainAssets.select('soil_suitability_score');
var floodSafety = terrainAssets.select('flood_safety');
var fireRiskScore = terrainAssets.select('fire_risk_score');
var elevationScore = terrainAssets.select('elevation_score');
var landCoverScore = terrainAssets.select('land_cover_suitability');
var landSuitabilityMask = terrainAssets.select('land_suitable_mask');
var coastScore = terrainAssets.select('coast_score');

// Infrastructure
var roadAccessScore = infrastructureAssets.select('road_access_score');
var gridConnectionScore = infrastructureAssets.select('grid_connection_score');
var demandProximityScore = infrastructureAssets.select('demand_proximity_score');
var waterAccessScore = infrastructureAssets.select('water_access_score');
var infrastructureConflictScore = infrastructureAssets.select('infrastructure_conflict_score');
var losConnectivityScore = infrastructureAssets.select('los_connectivity_score');
var energyNeedIndex = infrastructureAssets.select('energy_need_index');

// =====================================================================
// CALCULATE CATEGORY SCORES
// =====================================================================
var comprehensiveSolarScore = ghi.unitScale(4.0, 7.0).clamp(0, 1).multiply(0.35)
  .add(dni.unitScale(3.0, 6.0).clamp(0, 1).multiply(0.25))
  .add(solarStability.multiply(0.15))
  .add(tempEfficiency.multiply(0.10))
  .add(windCooling.multiply(0.08))
  .add(dustScore.multiply(0.07))
  .clamp(0, 1)
  .rename('comprehensive_solar_score');

var weatherSuitability = comprehensiveSolarScore
  .multiply(tempEfficiency)
  .multiply(windCooling)
  .multiply(precipCleaning)
  .multiply(dustScore)
  .multiply(solarStability)
  .rename('weather_suitability');

var landSuitability = slopeScore
  .multiply(aspectScore)
  .multiply(soilSuitabilityScore)
  .multiply(floodSafety)
  .multiply(fireRiskScore)
  .multiply(elevationScore)
  .rename('land_suitability');

var infrastructureSuitability = roadAccessScore
  .multiply(gridConnectionScore)
  .multiply(demandProximityScore)
  .multiply(waterAccessScore)
  .multiply(infrastructureConflictScore)
  .multiply(losConnectivityScore)
  .rename('infrastructure_suitability');

// =====================================================================
// REGIONAL ADJUSTMENTS
// =====================================================================
var elevation = terrainAssets.select('elevation');
var northernTropical = ee.Image.pixelLonLat().select('latitude').gt(-10.0);
var centralHighlands = ee.Image.pixelLonLat().select('latitude').lte(-10.0)
  .and(ee.Image.pixelLonLat().select('latitude').gt(-15.0))
  .and(elevation.gt(800));
var southernArid = ee.Image.pixelLonLat().select('latitude').lte(-15.0);
var distanceToCoastKm = terrainAssets.select('distance_to_coast_km');
var coastalZone = distanceToCoastKm.lt(50);

var regionalSolarFactor = northernTropical.multiply(1.1).where(northernTropical.eq(0), 1.0)
  .multiply(centralHighlands.multiply(1.05).where(centralHighlands.eq(0), 1.0))
  .multiply(southernArid.multiply(0.95).where(southernArid.eq(0), 1.0))
  .multiply(coastalZone.multiply(0.9).where(coastalZone.eq(0), 1.0))
  .clamp(0.85, 1.15)
  .rename('regional_solar_factor');

var angolaRegionalAdjustment = regionalSolarFactor.pow(0.20)
  .multiply(ee.Image(1).pow(0.15)) // atmospheric
  .multiply(ee.Image(1).pow(0.20)) // water
  .multiply(ee.Image(1).pow(0.25)) // infrastructure
  .multiply(ee.Image(1).pow(0.20)) // development
  .clamp(0.7, 1.3)
  .rename('angola_regional_adjustment');

// =====================================================================
// HARD CONSTRAINTS
// =====================================================================
var slope = terrainAssets.select('slope');
var landCover = terrainAssets.select('land_cover');
var protectedAreas = ee.FeatureCollection('WCMC/WDPA/current/polygons')
  .filterBounds(STUDY_AREA.country);

var slopeConstraint = slope.lt(12);
var floodConstraint = floodSafety.gt(0.4);
var urbanConstraint = landCover.neq(50).and(landCover.neq(95));
var waterConstraint = landCover.neq(80);
var protectedConstraint = ee.Image().float().paint(protectedAreas, 0).gt(0).not();

var hardConstraints = slopeConstraint
  .and(floodConstraint)
  .and(urbanConstraint)
  .and(waterConstraint)
  .and(landSuitabilityMask)
  .and(protectedConstraint)
  .rename('hard_constraints_mask');

// =====================================================================
// FINAL SUITABILITY SCORES
// =====================================================================
var comprehensiveSuitability = ee.Image(1)
  .multiply(weatherSuitability.pow(0.25))
  .multiply(landSuitability.pow(0.30))
  .multiply(infrastructureSuitability.pow(0.25))
  .multiply(ee.Image(1).pow(0.15)) // regulatory
  .multiply(energyNeedIndex.add(0.5).pow(0.05))
  .multiply(hardConstraints)
  .pow(1/0.8)
  .clamp(0, 1)
  .rename('comprehensive_suitability');

var suitabilityScore = comprehensiveSolarScore.multiply(0.18)
  .add(soilSuitabilityScore.multiply(0.06))
  .add(slopeScore.multiply(0.08))
  .add(aspectScore.multiply(0.04))
  .add(floodSafety.multiply(0.08))
  .add(fireRiskScore.multiply(0.05))
  .add(roadAccessScore.multiply(0.05))
  .add(gridConnectionScore.multiply(0.03))
  .add(waterAccessScore.multiply(0.02))
  .add(energyNeedIndex.multiply(0.08))
  .add(coastScore.multiply(0.03))
  .multiply(angolaRegionalAdjustment.pow(0.05))
  .multiply(hardConstraints)
  .pow(1.2)
  .clamp(0, 1)
  .clip(STUDY_AREA.country)
  .rename('final_suitability_score');

// =====================================================================
// COMBINE FINAL ASSETS
// =====================================================================
var finalSuitabilityAssets = ee.Image.cat([
  comprehensiveSuitability,
  suitabilityScore,
  weatherSuitability,
  landSuitability,
  infrastructureSuitability,
  comprehensiveSolarScore,
  hardConstraints,
  angolaRegionalAdjustment
]).rename([
  'comprehensive_suitability',
  'final_suitability_score',
  'weather_suitability',
  'land_suitability',
  'infrastructure_suitability',
  'comprehensive_solar_score',
  'hard_constraints_mask',
  'angola_regional_adjustment'
]);

// =====================================================================
// EXPORT AS ASSET
// =====================================================================
Export.image.toAsset({
  image: finalSuitabilityAssets,
  description: 'Angola_Final_Suitability_Assets',
  assetId: ASSET_BASE_PATH + 'final_suitability',
  region: STUDY_AREA.country.geometry(),
  scale: 1000,
  maxPixels: 1e9,
  crs: 'EPSG:4326'
});

print('✅ Final Suitability Assets export task created!');
print('📋 Check Tasks tab to run the export');
print('💡 This requires all previous assets (01-04) to be completed first');
print('💡 Asset will be saved at: ' + ASSET_BASE_PATH + 'final_suitability');
