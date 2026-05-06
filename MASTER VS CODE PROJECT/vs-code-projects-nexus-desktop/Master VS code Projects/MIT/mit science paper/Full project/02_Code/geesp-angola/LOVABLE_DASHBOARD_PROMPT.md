# GEESP-Angola Dashboard - Lovable.dev Generation Prompt

**Copy the entire content below and paste into Lovable.dev to generate the dashboard**

---

## DASHBOARD GENERATION PROMPT FOR LOVABLE

You are creating a **geospatial energy system prioritization dashboard** for GEESP-Angola - a scientific project analyzing optimal locations for solar PV + battery mini-grids in Angola.

### PROJECT CONTEXT

**Objective**: Enable decision-makers to explore, analyze, and recommend electrification zones in Angola using multi-criteria decision analysis (MCDA), financial modeling (LCOE), and real-time field monitoring.

**Users**: Energy analysts, policy makers, field teams  
**Region**: Angola (3 priority provinces: Huambo, Bié, Moxico)  
**Technology**: Solar PV + Battery mini-grids  
**Decision Criteria**: Solar irradiation, electrification demand, accessibility, infrastructure costs

---

## DASHBOARD ARCHITECTURE

Build a **6-page, modular Streamlit dashboard** with the following structure:

### PAGE 1: HOME (Dashboard Overview)
**Purpose**: Introduce project, show key metrics, visualize priority zones

**Components**:
- **Title Section**
  - Title: "🌍 GEESP-Angola: Solar Electrification Prioritization"
  - Subtitle: "Multi-Criteria Decision Analysis for Mini-Grid Site Selection"
  
- **Key Metrics Row** (4 columns)
  - Critérios Avaliados: "5"
  - Zonas Prioritárias: "3"
  - População Potencial: "~48,000"
  - Irradiação Solar: "5.2-5.8 kWh/m²/day"

- **Interactive Map**
  - Folium map centered on Angola (center: -18.0°S, 14.75°E, zoom: 8)
  - Markers for 3 priority zones (Huambo, Bié, Moxico)
  - Color-coded by priority (High=Red, Medium=Orange, Low=Yellow)
  - Click marker to see: Zone name, Community count, Est. Population, Irradiation avg
  - Add layer groups: "Priority Zones", "Communities", "Existing Infrastructure"

- **Quick Stats Cards**
  - Total communities analyzed: 147
  - Average households per community: 325
  - Solar potential (avg): 5.5 kWh/m²/day
  - LCOE potential: USD 0.24-0.28/kWh

- **Navigation Guide**
  - Brief description of each page (Data Exploration, MCDA, Results, LCOE, Monitoring)
  - Use emoji and clear descriptions

---

### PAGE 2: DATA EXPLORATION (Raster & Statistics)
**Purpose**: Explore input geospatial data (rasters) and generate summary statistics

**Components**:
- **File Upload Section**
  - Upload raster files (GeoTIFF, .tif format)
  - Supported: Single-band rasters (irradiance, population density, slope, etc.)
  - File size limits: Max 100MB per file
  - On upload: Extract raster metadata (CRS, resolution, bounds, min/max values)

- **Raster Information Display**
  - Raster name, file format, CRS (coordinate system)
  - Grid resolution (meters)
  - Bounding box (geographic bounds)
  - Data type (float32, etc.)
  - Min/Max/Mean/Std dev values
  - Histogram visualization

- **Statistics Table**
  - Display zonal statistics for each priority zone
  - Columns: Zone, Mean Value, Median, Std Dev, Min, Max, Count
  - Show multiple rasters stacked (irradiance, demand, accessibility, etc.)

- **Visualization**
  - Simple histogram of raster values
  - Statistical summary heatmap

- **Export Options**
  - Download statistics as CSV
  - Download as JSON

---

### PAGE 3: MCDA ANALYSIS (Multi-Criteria Decision Making)
**Purpose**: Configure weights for decision criteria and compute zone rankings

**Components**:
- **Criteria Configuration Section**
  - 5 criteria with weight sliders:
    1. **Irradiação Solar** (Solar Irradiance) - Default: 25%
    2. **Demanda Energética** (Energy Demand) - Default: 20%
    3. **Acessibilidade** (Road Access) - Default: 20%
    4. **Capacidade Financeira** (Financial Capacity) - Default: 20%
    5. **Viabilidade Social** (Social Viability) - Default: 15%
  
  - Each criterion:
    - Slider (0-100%)
    - Real-time sum display ("Total: 95% / 100%")
    - Description and methodology note
    - Lock/unlock toggle

- **Weight Distribution Visualization**
  - Pie chart showing current weight allocation
  - Color-coded by criterion
  - Update in real-time as sliders change

- **Sensitivity Analysis**
  - Select 1-2 criteria to vary (±10%, ±20%, ±30%)
  - Table showing ranking changes with weight variations
  - Highlight criteria with most impact on rankings

- **Compute Rankings Button**
  - Calculate normalized scores for each zone
  - Use formula: Score = Σ (Criterion_Value × Weight) / Σ Weights
  - Display results as table (Zone, Score, Ranking, Confidence)
  - Show confidence interval (±5%)

- **Results Display**
  - Ranked zones table:
    - Columns: Rank, Zone, Score, Confidence, Recommendation
    - Sort by score (descending)
  - Color-coded scores (Green=High, Yellow=Medium, Red=Low)

- **Export Results**
  - Download as CSV
  - Download sensitivity analysis table

---

### PAGE 4: RESULTS VISUALIZATION (Zone Recommendations)
**Purpose**: Display detailed analysis results and zone comparisons

**Components**:
- **Zone Ranking Table**
  - Columns: Rank, Zone Name, Aptitude Score, Est. Communities, Potential Population, LCOE Est., Recommendation Status
  - Interactive sorting (click column headers)
  - Color code rows: Green (Recommended), Yellow (Secondary), Red (Not Recommended)
  - Expandable rows showing detailed metrics:
    - Top 3 criteria for this zone
    - Implementation risks
    - Access considerations
    - Timeline estimate

- **Comparison Charts**
  - Radar chart comparing zones across 5 criteria
  - Bar chart: Population vs Zone Aptitude
  - Scatter plot: LCOE vs Aptitude (bubble size = population)

- **Zone Detail Views** (tabs or expandable)
  - For each of 3 zones:
    - Summary: Zone name, location, priority level
    - Geography: Communities (# and names), Accessibility score, Infrastructure status
    - Energy: Avg irradiation, Demand level, Growth potential
    - Financial: Estimated CAPEX, LCOE range, Subsidy requirements
    - Social: Population demographics, Energy access rate, Local preferences
    - Risk Assessment: Technical, Financial, Social risks with mitigation

- **Confidence & Uncertainty**
  - Display confidence intervals (±5-10%)
  - Note data sources used in analysis
  - Timestamp of last analysis update

- **Export & Sharing**
  - Download full analysis as PDF report
  - Export zone comparison as CSV
  - Generate GeoTIFF aptitude maps (high-res)

---

### PAGE 5: LCOE CALCULATIONS (Financial Viability)
**Purpose**: Calculate Levelized Cost of Electricity (LCOE) for mini-grid scenarios

**Components**:
- **System Configuration Section**
  - **PV System**
    - Capacity (kWp): slider 5-50 kWp, default 10 kWp
    - Module efficiency: 16-22%, default 18%
    - System losses: 5-15%, default 10%
  
  - **Battery Storage**
    - Capacity (kWh): slider 20-200 kWh, default 50 kWh
    - Discharge cycles: 3,000-5,000, default 4,000
    - Round-trip efficiency: 90-95%, default 92%
    - Replacement year (cycle): 10-12, default 10
  
  - **Financial Parameters**
    - Project lifetime: 20 years (fixed)
    - Discount rate (WACC): 5-15%, default 8%
    - Inflation rate: 0-5%, default 2%
    - Operation & Maintenance: 1-3% annual CAPEX, default 2%

- **Cost Components Display**
  - PV system cost: $1,200-1,500/kWp
  - Battery cost: $300-500/kWh (first cycle), $250-400/kWh (replacement)
  - Balance of System: 20-30% additional
  - Installation labor: 10-15% of hardware cost
  - Contingency: 10-15%
  - **Total CAPEX estimate**: Calculated and displayed

- **LCOE Calculation Results**
  - LCOE (USD/kWh): Calculated with formula:
    ```
    LCOE = (CAPEX + PV(O&M) + PV(Degradation) + PV(Battery Replacement)) / PV(Electricity Generation over 20 years)
    ```
  - Components breakdown:
    - PV generation: ~3 MWh/year for 10 kWp system
    - Battery cycles: ~500-600 cycles/year
    - Degradation: -0.5% annually
  - **Result range**: Typically USD 0.24-0.35/kWh depending on config

- **Sensitivity Tornado Chart**
  - Show which parameters most impact LCOE:
    - System capacity (↓ LCOE with size economies)
    - Discount rate (↑ increases LCOE with rate)
    - Battery lifespan (↓ LCOE with longer life)
    - O&M costs (↑ direct impact)

- **Technology Recommendations**
  - Compare 3 scenarios:
    1. "Conservative" (small system, low risk): 5 kWp + 30 kWh, LCOE ~USD 0.35
    2. "Balanced" (medium system): 10 kWp + 50 kWh, LCOE ~USD 0.28
    3. "Growth-Ready" (larger, scalable): 15 kWp + 80 kWh, LCOE ~USD 0.23
  
  - For each show: CAPEX, annual O&M, LCOE, households served, payback period

- **Viability Assessment**
  - Flag if LCOE > local tariff (requires subsidy)
  - Subsidy need: (LCOE - Tariff) × Annual kWh
  - Tariff options: Show local electricity tariff for comparison
  - Break-even analysis: How many households needed for viability?

- **Export & Download**
  - Download detailed LCOE report (PDF)
  - Export parameters as JSON (for reproducibility)
  - Create LCOE sensitivity sheet (Excel)

---

### PAGE 6: REAL-TIME MONITORING (Field Team Portal)
**Purpose**: Track Phase 1 field implementation and baseline data collection

**Components**:
- **Project Overview**
  - Current phase: "Phase 1 Field Validation"
  - Timeline: Expected completion date
  - Key milestones with status (✓ Complete, ⧖ In Progress, ○ Not Started)

- **Zone Status Dashboard**
  - For each of 3 zones (Huambo, Bié, Moxico):
    - Current status: Baseline, Community Engagement, Site Survey, etc.
    - % Completion
    - Communities covered: X/Y
    - Last update: Timestamp
    - Contact person & phone

- **GPS Tracking Map**
  - Show field team locations in real-time (simulated or integrated with GPS API)
  - Markers for surveyed communities
  - Routes between communities
  - Zoom to zone or community level

- **Baseline Data Checklist**
  - For each community, track data collection:
    - ☐ GPS coordinates collected
    - ☐ Household count verified
    - ☐ Energy access status documented
    - ☐ Infrastructure assessment
    - ☐ Community leader interview
    - ☐ Photos taken (site, architecture)
  - Status: Not Started, In Progress, Complete

- **Real-Time Alerts & Notifications**
  - Display latest updates from field teams
  - Format: "Team A: Completed survey in Caála (2 hrs ago)"
  - Alert colors: Green (progress), Yellow (checkpoint), Red (issue)

- **Data Quality Metrics**
  - Communities with complete data: X%
  - Data collection rate: communities/week
  - Photo coverage: X% (with thumbnails)
  - GPS quality: Average accuracy in meters

- **Export Field Reports**
  - Generate daily/weekly progress reports
  - Download baseline data template (CSV)
  - Export zone status summary

---

## TECHNICAL REQUIREMENTS

### Frontend Stack
- **Framework**: Streamlit (Python interactive web app)
- **Mapping**: Folium (interactive maps with markers/layers)
- **Charts**: Plotly (interactive visualizations) + Matplotlib (statistical plots)
- **Data**: Pandas (data manipulation) + NumPy (calculations)
- **Geospatial**: Rasterio (raster reading), GeoPandas (vector data)

### Backend Requirements
- **Language**: Python 3.9+
- **Data Storage**: JSON, CSV, GeoTIFF files
- **Caching**: Streamlit session state (fast page switching)
- **Computations**: NumPy vectorized operations (fast MCDA, LCOE calculations)

### Data Specifications
- **Rasters**: GeoTIFF format, single-band or multi-band, CRS: EPSG:4326 (WGS84)
- **Zones**: GeoJSON or shapefile with properties (Name, Area, Population, etc.)
- **Communities**: CSV with columns: Name, Latitude, Longitude, Households
- **Baseline**: CSV template for field data collection

### Design Guidelines
- **Color Scheme**: 
  - Primary: Deep orange (#FF6B35) for energy/solar theme
  - Secondary: Teal (#004E89) for tech/analysis
  - Success: Green (#06A77D) for positive recommendations
  - Warning: Yellow (#FFB703) for caution
  - Risk: Red (#D62828) for concerns
  
- **Typography**: Sans-serif (Roboto or Inter) for readability
- **Icons**: Use emoji for accessibility and visual clarity
- **Responsive**: Works on desktop (primary), tablet (secondary), mobile (informational only)

### Performance Targets
- **Page Load**: <2 seconds
- **Map Render**: <1 second
- **MCDA Computation**: <500ms
- **LCOE Calculation**: <100ms
- **File Upload**: Handle up to 100MB rasters

### User Experience
- **Navigation**: Sidebar with emoji + text labels for 6 pages
- **Feedback**: Toast notifications for actions (success/error/warning)
- **Input Validation**: Prevent invalid parameter combinations (e.g., weights not summing to 100%)
- **Error Handling**: Show friendly error messages with troubleshooting tips
- **Help Text**: Inline descriptions for all parameters and complex concepts

---

## SAMPLE DATA STRUCTURES

### Priority Zones Data
```json
{
  "zones": [
    {
      "id": 1,
      "name": "Zona A - Huambo",
      "latitude": -12.77,
      "longitude": 15.79,
      "communities": 45,
      "population": 14625,
      "irradiation_avg": 5.6,
      "accessibility_score": 75,
      "financial_capacity": 0.6,
      "social_viability": 0.8,
      "priority_level": "High"
    },
    {
      "id": 2,
      "name": "Zona B - Bié",
      "latitude": -12.43,
      "longitude": 17.83,
      "communities": 52,
      "population": 16900,
      "irradiation_avg": 5.4,
      "accessibility_score": 65,
      "financial_capacity": 0.5,
      "social_viability": 0.7,
      "priority_level": "Medium"
    },
    {
      "id": 3,
      "name": "Zona C - Moxico",
      "latitude": -11.86,
      "longitude": 19.27,
      "communities": 50,
      "population": 16475,
      "irradiation_avg": 5.2,
      "accessibility_score": 55,
      "financial_capacity": 0.45,
      "social_viability": 0.65,
      "priority_level": "Medium"
    }
  ]
}
```

### MCDA Results Format
```json
{
  "analysis_id": "mcda_20260212_001",
  "timestamp": "2026-02-12T14:32:00Z",
  "weights": {
    "irradiation": 0.25,
    "demand": 0.20,
    "accessibility": 0.20,
    "financial": 0.20,
    "social": 0.15
  },
  "results": [
    {
      "rank": 1,
      "zone": "Zona A - Huambo",
      "score": 0.82,
      "confidence": 0.90,
      "recommendation": "Implementar em Fase 1"
    },
    {
      "rank": 2,
      "zone": "Zona B - Bié",
      "score": 0.75,
      "confidence": 0.85,
      "recommendation": "Implementar em Fase 2"
    },
    {
      "rank": 3,
      "zone": "Zona C - Moxico",
      "score": 0.68,
      "confidence": 0.80,
      "recommendation": "Acompanhamento futuro"
    }
  ]
}
```

### LCOE Result Format
```json
{
  "scenario": "Balanced",
  "config": {
    "pv_capacity_kwp": 10,
    "battery_capacity_kwh": 50,
    "project_lifetime_years": 20,
    "discount_rate": 0.08
  },
  "costs": {
    "pv_system": 15000,
    "battery_initial": 15000,
    "battery_replacement": 10500,
    "bos": 9000,
    "installation": 6000,
    "contingency": 4500,
    "total_capex": 60000
  },
  "calculations": {
    "pv_generation_annual_kwh": 3000,
    "lcoe_usd_kwh": 0.28,
    "annual_om_usd": 1200,
    "payback_years": 12
  },
  "viability": {
    "local_tariff_usd_kwh": 0.18,
    "subsidy_required": true,
    "annual_subsidy_need_usd": 300
  }
}
```

---

## DEPLOYMENT OPTIONS

1. **Streamlit Cloud** (Recommended)
   - Free tier available
   - Auto-deploys from GitHub
   - URL: geesp-dashboard.streamlit.app

2. **Docker Container**
   - For local deployment
   - Include in project docker-compose.yml

3. **Self-Hosted Server**
   - Deploy on Linux server with Nginx reverse proxy
   - Manual update process

---

## SUCCESS CRITERIA

- ✅ All 6 pages load and function correctly
- ✅ Maps render smoothly with interactive markers
- ✅ MCDA weights calculate correctly (sum=100%)
- ✅ LCOE calculations match peer-reviewed methods
- ✅ File uploads don't exceed 100MB
- ✅ Export functions generate valid CSV/PDF/GeoTIFF
- ✅ Mobile responsive (tablet accessible)
- ✅ Page load time <2 seconds
- ✅ Intuitive UI with clear navigation
- ✅ Accessible to non-technical users (field teams)

---

## PROJECT CONTEXT - BACKGROUND

**GEESP-Angola** is a scientific research initiative analyzing optimal sites for solar photovoltaic mini-grids in Angola. The project uses:

1. **Geospatial Data**: Solar irradiance maps, population density, infrastructure distance
2. **Multi-Criteria Analysis**: Combines 5 criteria (technical, financial, social) into ranked recommendations
3. **Financial Modeling**: Calculates LCOE (cost per kWh) for each zone
4. **Field Validation**: Phase 1 & 2 field surveys in target zones to validate predictions
5. **Policy Integration**: Recommendations informed by Angola's energy access targets

**Similar Projects**: Similar dashboards exist for electrification (Off-Grid Electric, M-KOPA), but this dashboard is unique for its integration of scientific peer-review methods with actionable decision support for policy makers.

---

## NOTES FOR LOVABLE DEVELOPERS

- **Modular Architecture**: Build as 6 independent pages that can be easily maintained/updated
- **Reusable Components**: Create components for "Metrics Card", "Comparison Table", "Map Viewer" that appear across pages
- **Data Flexibility**: Use JSON/CSV backends to allow easy updates without rebuilding UI
- **Scalability**: Design to handle adding new zones or criteria in future
- **Documentation**: Include comments explaining LCOE formula, MCDA methodology, normalization approaches
- **Testing**: Include sample data for testing all pages without live raster uploads

---

**End of Prompt**

---

# HOW TO USE THIS PROMPT

1. Go to **Lovable.dev** (https://lovable.dev)
2. Click "New Project" 
3. Select "Create from Prompt"
4. Paste the entire text above (from "You are creating a..." to "End of Prompt")
5. Click "Generate"
6. Lovable will create a complete Streamlit dashboard with all 6 pages

**Estimated Generation Time**: 5-10 minutes  
**Output**: Full Python Streamlit app with all components ready to deploy

---

## AFTER GENERATION

Once Lovable generates the dashboard:

1. **Download the Code**
   - Will be in standard Streamlit format
   - Install requirements.txt packages

2. **Add Your Data**
   - Replace sample data with real Angola datasets
   - Update GeoJSON zone boundaries
   - Upload actual raster files (irradiance, demand, etc.)

3. **Customize**
   - Adjust colors/styling
   - Add your logo
   - Update contact information

4. **Deploy**
   - Use Streamlit Cloud (free tier)
   - Or deploy to server with Docker

5. **Testing**
   - Run locally: `streamlit run app.py`
   - Test all 6 pages
   - Verify calculations match your models

---

**Dashboard Ready for Stakeholder Demos**: Show this working dashboard to MINEA, Boston presentation audiences, and field teams!
