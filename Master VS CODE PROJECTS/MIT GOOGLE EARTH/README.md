# Enhanced Solar Feasibility Model for Angola

This comprehensive code implements an **Enhanced Solar Feasibility Model for Angola** in Google Earth Engine. Here's a detailed breakdown of everything it does:

## **OVERALL PURPOSE**
Creates a multi-criteria decision analysis tool to identify optimal solar power plant locations in Angola, considering technical, environmental, infrastructure, and socio-economic factors.

## **KEY SECTIONS & FUNCTIONALITY**

### **1. DATA COLLECTION & PROCESSING**
- **Geographic Scope**: Defines Angola and its provinces as study area
- **Satellite Data Sources**: 
  - Solar radiation: NASA/ORNL/DAYMET_V4 (2000-2020)
  - Weather: ECMWF/ERA5 (wind), ERA5 (temperature/precipitation)
  - Topography: USGS/SRTM (elevation/slope)
  - Soil: ISRIC SoilGrids (soil properties)
  - Water: JRC Global Surface Water (flooding)
  - Vegetation/Fire: MODIS (NDVI, burned areas)
  - Infrastructure: OpenStreetMap (roads, power lines, buildings)
  - Population: WorldPop (2020)
  - Night lights: VIIRS (2023)
  - Land cover: ESA WorldCover

### **2. SOLAR RESOURCE ANALYSIS**
- **GHI (Global Horizontal Irradiance)**: Primary solar energy metric
- **DNI (Direct Normal Irradiation)**: For concentrated solar power suitability
- **DHI (Diffuse Horizontal Irradiation)**: For PV panel performance
- **Solar Consistency Index**: Reliability/variability metric
- **Enhanced Solar Score**: Combines GHI with temperature, wind cooling, aerosol effects

### **3. ENVIRONMENTAL CONSTRAINTS**
- **Terrain Analysis**: Slope (<15° optimal), aspect (south-facing in Southern Hemisphere)
- **Soil Stability**: Clay/sand composition for foundation suitability
- **Flood Risk**: Surface water occurrence and river flood hazards
- **Fire Risk**: Historical fire frequency from MODIS
- **Vegetation Impact**: NDVI for fire fuel load assessment

### **4. INFRASTRUCTURE ANALYSIS**
- **Road Access**: Weighted by road classification (primary > secondary > tertiary)
- **Grid Proximity**: Distance to existing power lines and substations
- **Demand Proximity**: Population centers as energy demand proxies
- **Water Access**: For PV cleaning and potential CSP cooling
- **Line-of-Sight**: Visibility analysis for potential micro-grid connections
- **Infrastructure Conflicts**: Avoids buildings and existing infrastructure

### **5. SOCIO-ECONOMIC FACTORS**
- **Energy Need Index**: Combines population density and low electrification (night lights)
- **Community Infrastructure**: Proximity to schools, health facilities, community centers
- **Regulatory Factors**: 
  - Land tenure complexity (using land cover as proxy)
  - Agricultural land preservation
  - Mining/mineral rights avoidance
  - Population density targeting for off-grid/on-grid

### **6. ANGOLA-SPECIFIC ADJUSTMENTS**
- **Regional Analysis**: Divides Angola into northern, central, southern zones
- **Southern Angola**: High solar but dust from Namib Desert (penalty applied)
- **Central Plateaus**: Good land but water scarcity
- **Northern Regions**: More water but higher humidity and forest constraints
- **Off-Grid Priority**: Identifies un-electrified communities far from grid
- **Regional Solar Adjustments**: Southern (+15%), Central (+5%), Northern (-5%)

### **7. SUITABILITY MODEL INTEGRATION**
- **Hard Constraints**: Binary exclusion of unsuitable areas (steep slopes, floods, protected areas, urban zones)
- **Dynamic Weighting**: Adjustable weights based on project type (off-grid vs grid-connected)
- **Factor Interactions**: Non-linear interactions between variables (wind cooling + temperature)
- **Final Suitability Score**: 0-1 score combining all factors with Angola-specific adjustments
- **Reliability Score**: Data quality and consistency confidence metric

### **8. VISUALIZATION & OUTPUTS**
- **Interactive Map Layers**: ~30 different map layers toggle on/off
- **Statistical Analysis**: Provincial statistics and score distributions
- **Export Functions**:
  - Final suitability map (GeoTIFF)
  - All intermediate analysis layers
  - Provincial statistics (CSV)
  - Hard constraints mask

## **TECHNICAL INNOVATIONS**
1. **Comprehensive Multi-Criteria**: Combines 20+ different factors
2. **Angola-Specific**: Tailored to Angola's geography, climate, and development needs
3. **Dynamic Weighting**: Adjustable for different project goals
4. **Factor Interactions**: Models synergistic/antagonistic effects between variables
5. **Data Quality Integration**: Includes reliability/confidence metrics
6. **Off-Grid Focus**: Special consideration for rural electrification

## **OUTPUTS GENERATED**
1. **Primary Suitability Map**: Final composite score (0-1)
2. **Constraint Maps**: Areas excluded for various reasons
3. **Component Scores**: Individual factor scores for detailed analysis
4. **Regional Analysis**: Angola-specific adjustments and priorities
5. **Statistical Reports**: Provincial averages and distributions

## **PRACTICAL APPLICATIONS**
- **Site Selection**: Identify top candidate locations for solar farms
- **Project Planning**: Understand site-specific challenges/advantages
- **Policy Making**: Inform energy infrastructure development
- **Investment Decisions**: Risk assessment for solar projects
- **Rural Electrification**: Prioritize off-grid solar for unserved communities

The code essentially creates a **complete decision support system** for solar energy development in Angola, balancing technical feasibility with socio-economic priorities.

## **HOW TO USE**

1. **Open in Google Earth Engine**: Copy the code from `INITIAL CODE` into the GEE Code Editor
2. **Run the Script**: Click "Run" to execute the analysis
3. **Explore Layers**: Use the layer panel to toggle different analysis components
4. **Adjust Parameters**: Use the interactive slider to change project type weighting
5. **Export Results**: Check the "Tasks" tab to export maps and statistics
6. **Analyze Statistics**: View provincial statistics and distribution charts in the Console

## **REQUIREMENTS**
- Google Earth Engine account
- Basic understanding of remote sensing and GIS concepts
- Familiarity with JavaScript (for code modifications)

## **DATA SOURCES**
All data is sourced from publicly available satellite datasets in Google Earth Engine:
- NASA/ORNL DAYMET for solar radiation
- ECMWF ERA5 for weather data
- USGS SRTM for topography
- ISRIC SoilGrids for soil properties
- JRC Global Surface Water for hydrology
- MODIS for vegetation and fire data
- OpenStreetMap for infrastructure
- WorldPop for population
- VIIRS for night lights
- ESA WorldCover for land cover

## **CUSTOMIZATION**
The model includes adjustable weights and parameters that can be modified for different project types or regional priorities. Key variables to adjust:
- `projectType`: 0 (off-grid) to 1 (grid-connected)
- Regional adjustment factors
- Weight coefficients in the dynamic weighting section