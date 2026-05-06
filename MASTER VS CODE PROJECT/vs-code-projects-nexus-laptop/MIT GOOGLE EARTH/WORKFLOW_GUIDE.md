# 🔄 Angola Solar Model - Workflow Guide

## 📋 Code Separation Strategy

This project follows a **clear separation** between:
1. **Setup/Precursors** (non-computationally expensive)
2. **Calculations** (computationally expensive - exported as assets)
3. **Display** (pulls results from assets - fast)

---

## 📁 File Structure

```
├── 00_setup_precursors.js          ← Setup, config, helper functions (FAST)
├── 01_calculations_solar.js        ← Solar calculations (SLOW - exports asset)
├── 02_calculations_weather.js      ← Weather calculations (SLOW - exports asset)
├── 03_calculations_terrain.js      ← Terrain calculations (SLOW - exports asset)
├── 04_calculations_infrastructure.js ← Infrastructure calculations (SLOW - exports asset)
├── 05_calculations_final.js        ← Final suitability (MEDIUM - exports asset)
└── 00_display_main.js              ← Display script (FAST - loads assets)
```

---

## 🎯 Workflow Steps

### **Step 1: Setup & Precursors** (Fast - < 1 minute)

**File:** `00_setup_precursors.js`

**Contains:**
- Study area definition (Angola boundaries)
- Global configuration (data sources, analysis parameters)
- Helper functions (computeDistanceKm, etc.)
- UI styling configuration

**Purpose:** 
- Non-computationally expensive setup
- Can be reused across all calculation scripts
- Contains no heavy image processing

**Run:** Once (or include in each calculation script)

---

### **Step 2: Run Calculation Scripts** (Slow - 30-60 minutes total)

**Files:** `01_calculations_solar.js` through `05_calculations_final.js`

**Each script:**
1. **Loads setup/precursors** (or includes them directly)
2. **Performs expensive calculations:**
   - Image collection processing
   - Statistical reductions
   - Distance transforms
   - Complex mathematical operations
3. **Exports results as assets** using `Export.image.toAsset()`

**Export Process:**
```javascript
Export.image.toAsset({
  image: processedData,
  description: 'Task_Name',
  assetId: 'users/YOUR_USERNAME/angola_solar/asset_name',
  region: STUDY_AREA.country.geometry(),
  scale: 1000,
  maxPixels: 1e9,
  crs: 'EPSG:4326'
});
```

**After Export:**
- ✅ Asset appears in **Assets tab** in Earth Engine
- ✅ Can be loaded with: `ee.Image('asset/path')`
- ✅ Processing in display script does **NOT** alter original asset

**Run Order:**
1. `01_calculations_solar.js` → Wait for export
2. `02_calculations_weather.js` → Wait for export
3. `03_calculations_terrain.js` → Wait for export
4. `04_calculations_infrastructure.js` → Wait for export
5. `05_calculations_final.js` → Wait for export (depends on 01-04)

---

### **Step 3: Display Results** (Fast - < 1 minute)

**File:** `00_display_main.js`

**This script:**
1. **Pulls results** from calculation scripts using `ee.Image()`
2. **Handles display:**
   - Map visualization
   - Layer toggles
   - UI controls
   - Dashboard
3. **NO expensive calculations** - just loads and displays

**Asset Loading:**
```javascript
// Load assets from Assets tab
var solarAssets = ee.Image('users/YOUR_USERNAME/angola_solar/solar_resource');
var weatherAssets = ee.Image('users/YOUR_USERNAME/angola_solar/weather_atmospheric');
// ... etc
```

**Key Points:**
- ⚡ **Fast loading** - no computation required
- 🔄 **Can run anytime** after assets are generated
- 🎨 **Full visualization** - all layers, controls, dashboard
- 💾 **Original assets unchanged** - processing here doesn't alter exports

---

## 📊 Asset Management

### **Creating Assets**

1. **Run calculation script** (e.g., `01_calculations_solar.js`)
2. **Check Tasks tab** - export task appears
3. **Run export task** - click "Run" button
4. **Wait for completion** - check task status
5. **Asset appears** in Assets tab

### **Loading Assets**

```javascript
// Load asset using ee.Image()
var myAsset = ee.Image('users/YOUR_USERNAME/angola_solar/asset_name');

// Select specific bands
var ghi = myAsset.select('ghi');

// Use in calculations (doesn't alter original)
var ghiScaled = ghi.multiply(2);
```

### **Important Notes**

- ✅ **Assets are permanent** - stored in your Earth Engine account
- ✅ **Processing doesn't alter assets** - original export remains unchanged
- ✅ **Assets can be shared** - share asset paths with collaborators
- ✅ **Assets can be updated** - re-run calculation script to regenerate

---

## 🔍 Key Concepts

### **1. Setup vs. Calculations**

**Setup (Precursors):**
- Configuration
- Study area definition
- Helper functions
- **Fast to load** - no heavy processing

**Calculations:**
- Image collection processing
- Statistical reductions
- Complex operations
- **Slow to compute** - export as assets

### **2. Export Function**

**Purpose:** Save processed data/images as reusable assets

**Parameters:**
- `image`: The processed image to export
- `description`: Task name (appears in Tasks tab)
- `assetId`: Where to save (appears in Assets tab)
- `region`: Geographic extent
- `scale`: Resolution (meters)
- `maxPixels`: Maximum pixels to process
- `crs`: Coordinate reference system

**Result:** Asset appears in Assets tab, can be loaded with `ee.Image()`

### **3. Asset Loading**

**Method:** `ee.Image('asset/path')`

**Benefits:**
- Fast loading (pre-computed)
- No computation required
- Original asset unchanged
- Can be used in new calculations

---

## ✅ Checklist

### **Initial Setup:**
- [ ] Update `YOUR_USERNAME` in all scripts
- [ ] Run `00_setup_precursors.js` (optional - can be included in each script)
- [ ] Run `01_calculations_solar.js` → Wait for export
- [ ] Run `02_calculations_weather.js` → Wait for export
- [ ] Run `03_calculations_terrain.js` → Wait for export
- [ ] Run `04_calculations_infrastructure.js` → Wait for export
- [ ] Run `05_calculations_final.js` → Wait for export
- [ ] Verify all assets appear in Assets tab

### **Display:**
- [ ] Update asset paths in `00_display_main.js`
- [ ] Run `00_display_main.js`
- [ ] Verify all layers load correctly
- [ ] Test UI controls and dashboard

---

## 🎯 Summary

| Script Type | Purpose | Runtime | Frequency |
|-------------|---------|---------|-----------|
| **Setup** | Configuration, helpers | < 1 min | Once |
| **Calculations** | Expensive processing | 30-60 min | Once |
| **Display** | Load & visualize assets | < 1 min | Anytime |

**Total Setup Time:** ~1 hour (one-time)  
**Subsequent Use:** Instant! ⚡

---

## 💡 Best Practices

1. **Run calculations sequentially** - wait for each export to complete
2. **Verify assets** - check Assets tab before running display script
3. **Update paths** - ensure asset paths match your username
4. **Share assets** - share asset paths with team members
5. **Regenerate when needed** - update calculation scripts when data/parameters change

---

## 📚 References

- **Export Documentation:** https://developers.google.com/earth-engine/guides/export
- **Asset Management:** Assets tab in Earth Engine Code Editor
- **ee.Image():** https://developers.google.com/earth-engine/guides/image_overview
