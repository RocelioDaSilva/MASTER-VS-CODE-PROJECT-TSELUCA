# 📊 Angola Solar Model - Asset-Based Architecture

## 🎯 Overview

This codebase has been optimized to separate **computationally expensive calculations** from **fast visualization**. The model is split into:

1. **Asset Generation Scripts** (01-05): Compute and export expensive operations as Earth Engine assets
2. **Display Script** (00): Loads pre-computed assets for fast visualization

---

## ⏱️ Computationally Expensive Sections

### **Section 1: Solar Resource Analysis** (`01_asset_solar_resource.js`)
**Computation Time:** ~5-15 minutes  
**Why Expensive:**
- Processes 3 years of ERA5-Land daily data (2023-2025)
- Calculates statistical measures (mean, stdDev) across time series
- Processes MODIS aerosol data collection
- Multiple image collection reductions

**Exports:**
- GHI (daily and annual)
- DNI and DHI
- Solar stability scores
- Aerosol optical depth
- Irradiation classification

---

### **Section 2: Weather & Atmospheric Analysis** (`02_asset_weather_atmospheric.js`)
**Computation Time:** ~10-20 minutes  
**Why Expensive:**
- Processes 3 years of ERA5-Land HOURLY data (26,280+ images)
- Multiple collection reductions (mean, sum)
- Temperature, wind, humidity, precipitation calculations
- Multiple band selections and conversions

**Exports:**
- Temperature (mean, min, max, range)
- Wind speed and direction
- Humidity and dewpoint
- Annual precipitation
- Temperature efficiency scores
- Wind cooling benefits

---

### **Section 3: Terrain & Environmental Analysis** (`03_asset_terrain_environmental.js`)
**Computation Time:** ~8-15 minutes  
**Why Expensive:**
- NASADEM elevation processing (30m resolution)
- Terrain derivatives (slope, aspect, TPI)
- ISRIC SoilGrids processing (multiple bands)
- MODIS vegetation collection processing
- MODIS fire collection processing (10 years)
- Land cover classification
- Distance transforms for coastal analysis

**Exports:**
- Elevation, slope, aspect
- Terrain complexity scores
- Soil suitability scores
- Flood safety scores
- Fire risk scores
- Vegetation density
- Land cover suitability
- Coastal distance scores

---

### **Section 4: Infrastructure Analysis** (`04_asset_infrastructure.js`)
**Computation Time:** ~10-18 minutes  
**Why Expensive:**
- Multiple distance transforms (computationally intensive)
- Population data processing
- VIIRS night lights collection processing
- Feature collection painting operations
- Multiple accessibility calculations

**Exports:**
- Road access scores
- Grid connection scores and potential
- Substation proximity
- Population and demand proximity
- Water accessibility
- Energy need index
- Night lights data

---

### **Section 5: Final Suitability Calculations** (`05_asset_final_suitability.js`)
**Computation Time:** ~3-8 minutes  
**Why Expensive:**
- Loads and combines all previous assets
- Complex weighted calculations
- Regional adjustment factors
- Hard constraints application
- Multiple suitability score calculations

**Exports:**
- Comprehensive suitability score
- Final suitability score
- Weather suitability
- Land suitability
- Infrastructure suitability
- Hard constraints mask
- Regional adjustments

---

## 🚀 Usage Instructions

### **Step 1: Generate Assets** (Run Once)

1. **Update Asset Paths**: In each script (01-05), replace `YOUR_USERNAME` with your Earth Engine username:
   ```javascript
   assetId: 'users/YOUR_USERNAME/angola_solar/solar_resource'
   ```

2. **Run Asset Generation Scripts** (in order):
   - `01_asset_solar_resource.js` → Wait for export to complete
   - `02_asset_weather_atmospheric.js` → Wait for export to complete
   - `03_asset_terrain_environmental.js` → Wait for export to complete
   - `04_asset_infrastructure.js` → Wait for export to complete
   - `05_asset_final_suitability.js` → Wait for export to complete

3. **Monitor Exports**: Check the **Tasks** tab in Earth Engine Code Editor
   - Each export may take 10-30 minutes depending on server load
   - Wait for each task to complete before running the next

### **Step 2: Display Results** (Fast - No Computation)

1. **Update Asset Path**: In `00_display_main.js`:
   ```javascript
   var ASSET_BASE_PATH = 'users/YOUR_USERNAME/angola_solar/';
   ```

2. **Run Display Script**: `00_display_main.js`
   - ⚡ **Fast loading** - no computation required!
   - All layers load instantly from pre-computed assets
   - Interactive controls and dashboard work immediately

---

## 📁 File Structure

```
├── 00_display_main.js              ← Main display script (FAST)
├── 01_asset_solar_resource.js      ← Solar calculations (SLOW)
├── 02_asset_weather_atmospheric.js ← Weather calculations (SLOW)
├── 03_asset_terrain_environmental.js ← Terrain calculations (SLOW)
├── 04_asset_infrastructure.js      ← Infrastructure calculations (SLOW)
├── 05_asset_final_suitability.js   ← Final calculations (MEDIUM)
└── README_ASSET_STRUCTURE.md       ← This file
```

---

## 💡 Benefits of This Architecture

### **Before (Original Script):**
- ⏱️ **Total Runtime:** 30-60+ minutes
- 🔄 **Every Run:** Recalculates everything
- 💻 **Resource Intensive:** High CPU/memory usage
- ⚠️ **Timeout Risk:** May exceed Earth Engine limits

### **After (Asset-Based):**
- ⚡ **Display Runtime:** < 1 minute (instant loading)
- 🔄 **One-Time Setup:** Generate assets once
- 💾 **Efficient:** Pre-computed results stored
- ✅ **Reliable:** No timeout issues
- 🎨 **Fast Iteration:** Quick visualization changes

---

## 🔧 Troubleshooting

### **Issue: Assets Not Found**
- **Solution:** Ensure all asset generation scripts have completed
- Check Tasks tab for export status
- Verify asset paths match your username

### **Issue: Export Fails**
- **Solution:** 
  - Reduce `maxPixels` if export fails
  - Increase `scale` (e.g., 2000m instead of 1000m)
  - Check Earth Engine quotas

### **Issue: Display Script Errors**
- **Solution:**
  - Verify asset paths are correct
  - Ensure all 5 asset generation scripts completed successfully
  - Check asset names match exactly

---

## 📊 Asset Storage

Assets are stored in your Earth Engine account at:
```
users/YOUR_USERNAME/angola_solar/
├── solar_resource
├── weather_atmospheric
├── terrain_environmental
├── infrastructure
└── final_suitability
```

**Storage Cost:** ~500MB - 2GB total (depending on resolution)

---

## 🎯 When to Regenerate Assets

Regenerate assets when:
- ✅ Data sources are updated (new years available)
- ✅ Analysis parameters change significantly
- ✅ Study area changes
- ✅ Algorithm improvements are made

**Otherwise:** Use the display script for fast visualization!

---

## 📝 Notes

- **Asset Generation:** Run scripts 01-05 sequentially, waiting for each to complete
- **Display:** Run script 00 anytime for instant visualization
- **Updates:** Modify asset generation scripts to update calculations
- **Sharing:** Share asset paths with collaborators for fast access

---

## ✅ Summary

| Script | Purpose | Runtime | Frequency |
|--------|---------|---------|-----------|
| 01-05 | Generate Assets | 30-60 min | Once |
| 00 | Display Results | < 1 min | Anytime |

**Total Setup Time:** ~1 hour (one-time)  
**Subsequent Use:** Instant! ⚡
