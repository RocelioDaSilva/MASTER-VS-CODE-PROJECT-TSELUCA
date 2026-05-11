// =====================================================================
// 📋 SETUP & PRECURSORS - Angola Solar Model
// =====================================================================
// This script contains all setup, configuration, and helper functions
// These are NON-COMPUTATIONALLY EXPENSIVE and can be reused across scripts
// =====================================================================

// =====================================================================
// STUDY AREA DEFINITION
// =====================================================================
var STUDY_AREA = {
  country: ee.FeatureCollection('FAO/GAUL/2015/level0')
              .filter(ee.Filter.eq('ADM0_NAME', 'Angola')),
  provinces: ee.FeatureCollection('FAO/GAUL/2015/level1')
                .filter(ee.Filter.eq('ADM0_NAME', 'Angola')),
  municipalities: ee.FeatureCollection('FAO/GAUL/2015/level2')
                     .filter(ee.Filter.eq('ADM0_NAME', 'Angola'))
};

// =====================================================================
// GLOBAL CONFIGURATION
// =====================================================================
var CONFIG = {
  // Data source time ranges (optimized for 2024-2025 analysis)
  dataSources: {
    solar: ['2023-01-01', '2025-12-31'],        // ERA5-Land (latest available)
    weather: ['2023-01-01', '2025-12-31'],      // ERA5-Land
    aerosol: ['2023-01-01', '2025-12-31'],      // MODIS
    vegetation: ['2023-01-01', '2025-12-31'],   // MODIS
    nightlights: ['2023-01-01', '2025-12-31'],  // VIIRS
    population: 2020                             // WorldPop (latest available)
  },

  // Analysis parameters
  analysis: {
    scale: 1000,           // meters
    maxPixels: 1e9,
    defaultThreshold: 0.7
  },

  // UI styling
  ui: {
    primaryColor: '#FF9800',
    secondaryColor: '#4CAF50',
    accentColor: '#2196F3'
  },

  // Asset paths (UPDATE WITH YOUR USERNAME)
  assets: {
    basePath: 'users/YOUR_USERNAME/angola_solar/',
    solarResource: 'users/YOUR_USERNAME/angola_solar/solar_resource',
    weatherAtmospheric: 'users/YOUR_USERNAME/angola_solar/weather_atmospheric',
    terrainEnvironmental: 'users/YOUR_USERNAME/angola_solar/terrain_environmental',
    infrastructure: 'users/YOUR_USERNAME/angola_solar/infrastructure',
    finalSuitability: 'users/YOUR_USERNAME/angola_solar/final_suitability'
  }
};

// =====================================================================
// HELPER FUNCTIONS
// =====================================================================

/**
 * Compute Euclidean distance (in km) from a binary mask
 * Uses coarser resolution to reduce computation cost
 */
var DIST_SCALE = CONFIG.analysis.scale * 2;

function computeDistanceKm(mask) {
  var coarse = mask
    .unmask(0)
    .reproject({crs: 'EPSG:4326', scale: DIST_SCALE});

  return coarse.fastDistanceTransform()
    .sqrt()
    .multiply(DIST_SCALE / 1000.0); // pixels -> meters -> km
}

// =====================================================================
// EXPORT CONFIGURATION (for use in other scripts)
// =====================================================================
// This script can be loaded into calculation scripts using:
// var setup = require('users/YOUR_USERNAME/angola_solar:00_setup_precursors');
// var STUDY_AREA = setup.STUDY_AREA;
// var CONFIG = setup.CONFIG;
// var computeDistanceKm = setup.computeDistanceKm;

print('✅ Setup & Precursors loaded');
print('📋 Contains: STUDY_AREA, CONFIG, Helper Functions');
print('💡 This script has NO expensive calculations - fast to load');
