# Technical Summary: GEESP-Angola Methodology & Validation Framework
**Version**: 1.0 | **Classification**: Peer Review | **Length**: 1 page equivalent

---

## 1. Method Overview

**Framework**: Multicriteria Geospatial Analysis for Equity-Focused Solar Planning

**Workflow** (4-step cascade):
1. **Data Integration**: Collect 6 raster layers (1 km resolution, 2020 baseline)
   - Solar: NASA POWER GHI (30-year climatology 1984–2014)
   - Demand: VIIRS nighttime lights (proxy for electrification/consumption)
   - Infrastructure: OpenStreetMap distance to transmission, roads
   - Terrain: SRTM elevation → slope, aspect
   - LULC: Sentinel-2 NDVI (available land, vegetation)
   - Population: WorldPop grid (age-adjusted demographic density)

2. **MCDA Weighting**: Analytic Hierarchy Process (Saaty 1980, validated)
   - 5 pairwise comparison matrices across 6 criteria
   - Stakeholder panel: 5 experts (GIS, energy, community, finance, policy)
   - Consistency validation: CR = 0.0847 (within Saaty's <0.10 threshold)
   - Final weights: GHI 25.6%, Population 23.5%, Distance-network 19.8%, NDVI 16.2%, Slope 14.9%

3. **Spatial Analysis**: Weighted Overlay + reclassification
   - Min-max normalization of all 6 layers to 0–100 scale
   - Weighted sum: Aptitude = Σ(normalized value × weight)
   - Output: Continuous 0–100 grid; reclassified to 5 aptitude classes (very low to very high)

4. **Technology Matching** & Validation
   - Rule-based system: If (aptitude > 75) AND (GHI > 5.6) THEN recommend PV-fixed + battery
   - LCOE calculation (NREL method): CapEx, OpEx, interest, degradation → USD/kWh over 20 years
   - Sensitivity: Vary all weights ±20% → 42 scenarios → confirm ranking stability

---

## 2. Validation Framework

### **In-Situ Measurement Protocol** (Months 0–6 before deployment)

| Component | Method | Duration | Accuracy | Cost |
|-----------|--------|----------|----------|------|
| **Solar Irradiance** | Pyranometer array (4 stations/zone) | 6 months continuous | ±5% vs NASA POWER | USD 8K/zone |
| **Population Mobility** | Mobile-based surveys (500 households/zone) | 3 months | ±10 (actual settlement pattern) | USD 5K/zone |
| **Grid Distance Accuracy** | GPS + network audit | 2 months | ±100 m validation | USD 2K/zone |
| **Slope/Soil** | Field survey + borehole samples | 2 weeks | Foundation adequacy check | USD 3K/zone |
| **Community Acceptance** | Focus groups + willingness-to-pay study | 2 months | Social risk assessment | USD 4K/zone |

**Total Validation Cost**: USD 60K (included in Phase 1 budget)  
**Output**: Refined MCDA model incorporating real data; field-corrected LCOE

### **Model Performance Metrics**

After 12 months of pilot operation:
- **Root Mean Square Error (RMSE)** of predicted vs actual solar generation: Target <15%
- **Community satisfaction survey**: Target >80% favorable
- **Technical uptime**: Target >95% (battery + inverter + monitoring)
- **Financial targets**: Collect 85%+ of tariff fees; demonstrate cost recovery trajectory

---

## 3. Key Technical Innovations

| Innovation | Advantage | Novelty vs Prior Work |
|-----------|-----------|----------------------|
| **Community-scale focus** | Technologies sized 5–25 kW (locally managed) vs utility-scale MW | Nassar (Iraq, MW+), Li (macro-regional) both miss community level |
| **Equity weighting** | 25% of score from population density + VIIRS (development proxy) | Standard MCDA ignores social equity |
| **Adaptive learning system** | Validation protocol feeds real data back to model → continuous refinement | Most analyses static; GEESP iterates |
| **Open-source reproducibility** | GitHub + Zenodo + Docker → <30 min replication anywhere | Competitors often proprietary/opaque |
| **3-technology comparison** | LCOE provided for 3 options per site; decision-maker picks per context | "Optimal" often assumes wrong cost structure |

---

## 4. Data Quality & Limitations

| Data Input | Resolution | Temporal | Limitation | Mitigation |
|-----------|-----------|----------|-----------|-----------|
| **NASA POWER GHI** | 0.5° (~55 km) aggregated to 1 km | 1984–2014 climatology | Coarse; doesn't capture local shading | In-situ pyranometer 6 months |
| **Sentinel-2 NDVI** | 10 m (resampled to 1 km) | 2020 composite | One-year snapshot; misses seasonal variation | Re-run analysis with 2024-2025 data |
| **VIIRS Nightlights** | 375 m | 2020 average | Can't resolve villages <1 km²; may overweight roads | Corroborate with WorldPop + census |
| **World Pop** | 100 m (resampled to 1 km) | 2020 estimate | Census 2014 + modeling; +4% annual growth not captured | Planned recount (2025 Angola census) |
| **OpenStreetMap Distances** | Vector; inherent error ±50 m | Current snapshot | May exclude informal/future roads | Community consultation on accessibility |

**Mitigation Strategy**: Validation Phase 1 includes field survey of all <5 priority communities to reconcile model vs ground truth

---

## 5. LCOE Calculation Details

**Inputs** (Angola 2023–2024 market rates):
- **PV Panel Cost**: USD 0.25/Wp (includes installation labor, tracking, wiring)
- **Battery (Li-ion)**: USD 140/kWh (6-hour system, 10-year warranty, 2000 cycles)
- **Balance of System** (inverter, breakers, combiner, monitoring): USD 0.75/Wp
- **Installation Labor**: USD 0.30/Wp (local technician rates)
- **Total CapEx**: USD 2.50/Wp + Battery cost separate

**Outputs**:
- **PV-Fixed 10 kW + 30 kWh battery**: USD 0.18–0.20/kWh (Zone A, best irradiance)
- **PV-Tracker 10 kW + 30 kWh battery**: USD 0.22–0.25/kWh (±10% higher cost, ±25% more generation)
- **Diesel Baseline (5 kW generator, fuel cost USD 1.20/L, 4L/hour)**: USD 0.40–0.45/kWh

**Sensitivity** (±20% parameter variation):
- If CapEx rises 20% → LCOE rises ~USD 0.04/kWh (still <USD 0.24, beats diesel)
- If battery cost drops 20% → LCOE drops ~USD 0.04/kWh (to USD 0.14–0.16)
- If interest rate rises 5% (8%→13%) → LCOE rises ~USD 0.02/kWh

**Conclusion**: Even pessimistic scenarios (cost up 20%, rate up 5%) still beat diesel baseline (USD 0.40+/kWh)

---

## 6. Reproducibility Checklist

- ✅ **Code**: Python (MCDA, LCOE, GEE extraction) on GitHub, MIT license, 12/12 tests passing
- ✅ **Data**: NASA POWER (public), Sentinel-2 (ESA open), SRTM (USGS), VIIRS (NOAA), OpenStreetMap (ODbL)
- ✅ **Compute**: Google Earth Engine (free tier sufficient for 55 hours/month)
- ✅ **Documentation**: README.md + Jupyter notebooks + Docker image (automated environment)
- ✅ **Dataset**: Zenodo DOI (pending publication; will include processed rasters + QGIS project file)
- ✅ **Replication Time**: <30 minutes from data download to final map output (on 4-core laptop)

---

## 7. Next Steps: From Research to Implementation

| Phase | Duration | Output | Funding |
|-------|----------|--------|---------|
| **1. Validation** | 3 months | Field data + refined model + stakeholder MOUs | USD 500K (grants) |
| **2. Pilot** | 6 months | 12.5 MWp operational, 4K households connected | USD 12.5M (AfDB loan) |
| **3. Monitoring** | 3 months | Impact report + model update | USD 1M (grants) |
| **4. Scale** | 6 months | 27 MWp additional (Zones B–C) | USD 37M (private + soft loans) |

---

## Citation & Preprint

**Planned Publication**: Energy Policy, Applied Energy, or Journal of Cleaner Production

**Preprint**: Available on request from corresponding author (r.dasilva@isptec.ao)

**Contact for Technical Details**: Alexandre Dos Santos (a.dossantos@isptec.ao, GEE & Python expert)
