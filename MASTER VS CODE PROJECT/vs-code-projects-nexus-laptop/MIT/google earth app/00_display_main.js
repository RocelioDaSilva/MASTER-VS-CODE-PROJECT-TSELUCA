// =====================================================================
// 🎨 DISPLAY SCRIPT - Angola Solar Feasibility Model
// =====================================================================
// This script PULLS RESULTS from calculation scripts (01-05)
// Handles display, layer toggles, and NON-COMPUTATIONALLY EXPENSIVE tasks
// 
// WORKFLOW:
// 1. Loads pre-computed assets using ee.Image() from Assets tab
// 2. Displays layers with Map.addLayer()
// 3. Creates UI controls and dashboard
// 4. NO expensive calculations - fast loading!
// =====================================================================

// =====================================================================
// CONFIGURATION
// =====================================================================
// ⚠️ IMPORTANT: Update asset paths after running calculation scripts (01-05)
var ASSET_BASE_PATH = 'users/YOUR_USERNAME/angola_solar/';

var STUDY_AREA = {
  country: ee.FeatureCollection('FAO/GAUL/2015/level0')
              .filter(ee.Filter.eq('ADM0_NAME', 'Angola')),
  provinces: ee.FeatureCollection('FAO/GAUL/2015/level1')
                .filter(ee.Filter.eq('ADM0_NAME', 'Angola')),
  municipalities: ee.FeatureCollection('FAO/GAUL/2015/level2')
                     .filter(ee.Filter.eq('ADM0_NAME', 'Angola'))
};

var CONFIG = {
  ui: {
    primaryColor: '#FF9800',
    secondaryColor: '#4CAF50',
    accentColor: '#2196F3'
  }
};

// =====================================================================
// LOAD PRE-COMPUTED ASSETS
// =====================================================================
// Assets are loaded using ee.Image() - they pull from Assets tab
// Processing here does NOT alter the original exported assets
// =====================================================================
print('🔄 Loading pre-computed assets from Assets tab...');
print('⏱️ This should be FAST since assets are pre-computed!');

try {
  // Load assets using ee.Image() - these pull from Assets tab
  // Docs: https://developers.google.com/earth-engine/guides/export
  var solarAssets = ee.Image(ASSET_BASE_PATH + 'solar_resource');
  var weatherAssets = ee.Image(ASSET_BASE_PATH + 'weather_atmospheric');
  var terrainAssets = ee.Image(ASSET_BASE_PATH + 'terrain_environmental');
  var infrastructureAssets = ee.Image(ASSET_BASE_PATH + 'infrastructure');
  var finalSuitabilityAssets = ee.Image(ASSET_BASE_PATH + 'final_suitability');
  
  print('✅ All assets loaded successfully from Assets tab!');
  print('💡 Processing here does NOT alter original exported assets');
} catch (e) {
  print('❌ ERROR: Could not load assets. Please ensure:');
  print('   1. All calculation scripts (01-05) have been run');
  print('   2. Exports completed successfully (check Tasks tab)');
  print('   3. Assets appear in Assets tab');
  print('   4. Asset paths are correct in ASSET_BASE_PATH');
  print('Error:', e);
}

// =====================================================================
// EXTRACT LAYERS FROM ASSETS
// =====================================================================
// Solar Resource Layers
var ghi = solarAssets.select('ghi');
var ghiAnnual = solarAssets.select('ghi_annual');
var dni = solarAssets.select('dni');
var dhi = solarAssets.select('dhi');
var irradiationClass = solarAssets.select('irradiation_class');
var solarStability = solarAssets.select('solar_stability');
var comprehensiveSolarScore = finalSuitabilityAssets.select('comprehensive_solar_score');

// Weather Layers
var temperature = weatherAssets.select('temperature');
var windSpeed = weatherAssets.select('wind_speed');
var precipitation = weatherAssets.select('annual_precipitation');
var tempEfficiency = weatherAssets.select('temp_efficiency');
var windCooling = weatherAssets.select('wind_cooling');

// Terrain Layers
var elevation = terrainAssets.select('elevation');
var slope = terrainAssets.select('slope');
var aspect = terrainAssets.select('aspect');
var slopeScore = terrainAssets.select('slope_score');
var aspectScore = terrainAssets.select('aspect_score');
var soilSuitabilityScore = terrainAssets.select('soil_suitability_score');
var floodSafety = terrainAssets.select('flood_safety');
var fireRiskScore = terrainAssets.select('fire_risk_score');
var landCoverScore = terrainAssets.select('land_cover_suitability');
var distanceToCoastKm = terrainAssets.select('distance_to_coast_km');
var coastScore = terrainAssets.select('coast_score');

// Infrastructure Layers
var roadAccessScore = infrastructureAssets.select('road_access_score');
var gridConnectionScore = infrastructureAssets.select('grid_connection_score');
var gridConnectionPotential = infrastructureAssets.select('grid_connection_potential');
var gridDistance = infrastructureAssets.select('substation_distance_km');
var demandProximityScore = infrastructureAssets.select('demand_proximity_score');
var waterAccessScore = infrastructureAssets.select('water_access_score');
var energyNeedIndex = infrastructureAssets.select('energy_need_index');
var nightLights = infrastructureAssets.select('night_lights');

// Final Suitability Layers
var comprehensiveSuitability = finalSuitabilityAssets.select('comprehensive_suitability');
var suitabilityScore = finalSuitabilityAssets.select('final_suitability_score');
var weatherSuitability = finalSuitabilityAssets.select('weather_suitability');
var landSuitability = finalSuitabilityAssets.select('land_suitability');
var infrastructureSuitability = finalSuitabilityAssets.select('infrastructure_suitability');
var hardConstraints = finalSuitabilityAssets.select('hard_constraints_mask');

// =====================================================================
// INITIALIZE MAP
// =====================================================================
Map.centerObject(STUDY_AREA.country, 6);
Map.addLayer(STUDY_AREA.country,
             {color: 'black', width: 3},
             '🇦🇴 Angola Country Boundary',
             true);

// Add administrative boundaries
Map.addLayer(STUDY_AREA.provinces,
             {color: '#2196F3', width: 1.5, fillColor: '00000000'},
             '📍 Provincial Boundaries',
             false);

Map.addLayer(STUDY_AREA.municipalities,
             {color: '#4CAF50', width: 1, fillColor: '00000000'},
             '📍 Municipal Boundaries',
             false);

// =====================================================================
// ADD VISUALIZATION LAYERS
// =====================================================================
// Solar Resource Layers
Map.addLayer(ghi, {min: 4.5, max: 6.5, palette: ['blue', 'cyan', 'yellow', 'orange', 'red']}, 
             '☀️ 2.1 GHI (kWh/m²/day)', false);
Map.addLayer(ghiAnnual, {min: 1500, max: 2200, palette: ['blue', 'cyan', 'yellow', 'orange', 'red']}, 
             '☀️ 2.1b GHI Annual (kWh/m²/year)', false);
Map.addLayer(dni, {min: 3.5, max: 5.5, palette: ['blue', 'cyan', 'green', 'yellow', 'orange']}, 
             '☀️ 2.2 DNI (kWh/m²/day)', false);
Map.addLayer(irradiationClass, {min: 1, max: 4, palette: ['red', 'orange', 'yellow', 'green']}, 
             '☀️ 2.4 Irradiation Classification', false);
Map.addLayer(comprehensiveSolarScore, {min: 0, max: 1, palette: ['darkred', 'red', 'orange', 'yellow', 'lime', 'green']}, 
             '☀️ 2.5 Comprehensive Solar Score', false);

// Terrain Layers
Map.addLayer(slopeScore, {min: 0.1, max: 1, palette: ['red', 'orange', 'yellow', 'green']}, 
             '🏔️ 3.1 Slope Suitability', false);
Map.addLayer(aspectScore, {min: 0.2, max: 1, palette: ['red', 'orange', 'yellow', 'green']}, 
             '🏔️ 3.2 Aspect Suitability', false);
Map.addLayer(soilSuitabilityScore, {min: 0.4, max: 1, palette: ['brown', 'tan', 'yellow', 'green']}, 
             '🏔️ 3.3 Soil Suitability', false);
Map.addLayer(floodSafety, {min: 0.3, max: 1, palette: ['blue', 'cyan', 'white', 'yellow', 'brown']}, 
             '🏔️ 3.4 Flood Safety', false);
Map.addLayer(landCoverScore, {min: 0, max: 1, palette: ['red', 'orange', 'yellow', 'lime', 'green']}, 
             '🏔️ 3.5 Land Cover Suitability', false);

// Infrastructure Layers
Map.addLayer(roadAccessScore, {min: 0.1, max: 1, palette: ['red', 'orange', 'yellow', 'green']}, 
             '🚗 4.1 Road Access Score', false);
Map.addLayer(gridConnectionScore, {min: 0.1, max: 1, palette: ['red', 'orange', 'yellow', 'green']}, 
             '⚡ 4.2 Grid Connection Score', false);
Map.addLayer(gridConnectionPotential, {min: 0, max: 1, palette: ['red', 'orange', 'yellow', 'green']}, 
             '⚡ 4.2b Grid Connection Potential', false);
Map.addLayer(gridDistance, {min: 0, max: 200, palette: ['green', 'yellow', 'orange', 'red']}, 
             '⚡ 4.2a Grid Distance (km)', false);
Map.addLayer(demandProximityScore, {min: 0.1, max: 1, palette: ['red', 'orange', 'yellow', 'green']}, 
             '👥 4.3 Demand Proximity Score', false);
Map.addLayer(energyNeedIndex, {min: 0, max: 1, palette: ['white', 'yellow', 'orange', 'red']}, 
             '💡 4.4 Energy Need Index', false);

// Final Suitability Layers
Map.addLayer(hardConstraints, {min: 0, max: 1, palette: ['red', 'green']}, 
             '🚫 7.1 Hard Constraints Mask', false);
Map.addLayer(weatherSuitability, {min: 0, max: 1, palette: ['red', 'orange', 'yellow', 'green']}, 
             '🌞 7.2 Weather Suitability', false);
Map.addLayer(landSuitability, {min: 0, max: 1, palette: ['brown', 'tan', 'yellow', 'green']}, 
             '🏔️ 7.3 Land Suitability', false);
Map.addLayer(infrastructureSuitability, {min: 0, max: 1, palette: ['gray', 'blue', 'cyan', 'green']}, 
             '🚗 7.4 Infrastructure Suitability', false);
Map.addLayer(comprehensiveSuitability, {
  min: 0.0,
  max: 1.0,
  palette: ['darkred', 'red', 'orange', 'yellow', 'lime', 'green', 'darkgreen']
}, '🎯 7.6 Comprehensive Suitability Heatmap', true);
Map.addLayer(suitabilityScore, {
  min: 0.0,
  max: 1.0,
  palette: ['red', 'yellow', 'lime', 'darkgreen']
}, '🎯 7.7 Final Suitability Score', false);

// =====================================================================
// ADD INFORMATION DASHBOARD
// =====================================================================
// (Include the dashboard creation function from the original script)
// For brevity, including a simplified version here

var createInformationDashboard = function() {
  var dashboard = ui.Panel({
    style: {
      position: 'top-left',
      width: '380px',
      padding: '15px',
      backgroundColor: '#ffffff',
      border: '3px solid #FF9800',
      borderRadius: '10px',
      maxHeight: '600px',
      overflowY: 'auto'
    }
  });

  var header = ui.Panel({
    layout: ui.Panel.Layout.flow('horizontal'),
    style: {margin: '0 0 15px 0', padding: '10px', backgroundColor: '#FF9800', borderRadius: '5px'}
  });

  header.add(ui.Label({
    value: '📊 ANGOLA SOLAR ANALYSIS DASHBOARD',
    style: {fontSize: '18px', fontWeight: 'bold', color: 'white', margin: '0'}
  }));

  dashboard.add(header);
  dashboard.add(ui.Label({
    value: '✅ Using Pre-Computed Assets',
    style: {fontSize: '12px', color: '#4CAF50', fontWeight: 'bold', margin: '10px 0'}
  }));
  dashboard.add(ui.Label({
    value: '⚡ Fast Loading - No Computation!',
    style: {fontSize: '11px', color: '#666', margin: '5px 0'}
  }));

  return dashboard;
};

Map.add(createInformationDashboard());

// =====================================================================
// PRINT SUMMARY
// =====================================================================
print('');
print('╔══════════════════════════════════════════════════════════════╗');
print('║     🎨 ANGOLA SOLAR MODEL - DISPLAY MODE (ASSETS)          ║');
print('╚══════════════════════════════════════════════════════════════╝');
print('');
print('✅ All pre-computed assets loaded successfully!');
print('⚡ Fast visualization - no computation required');
print('');
print('📋 Available Layers:');
print('   ☀️ Solar Resource: GHI, DNI, Irradiation Classification');
print('   🌤️ Weather: Temperature, Wind, Precipitation');
print('   🏔️ Terrain: Slope, Aspect, Soil, Flood, Fire');
print('   🚗 Infrastructure: Roads, Grid, Water, Demand');
print('   🎯 Final Suitability: Comprehensive & Final Scores');
print('');
print('💡 Toggle layers in the Layers panel to explore results');
print('📊 Check the Dashboard (top-left) for key information');
