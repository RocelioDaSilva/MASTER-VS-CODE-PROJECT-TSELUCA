# GeoestatÃ­stica

**Ano:** 3Âº | **Semestre:** 2Âº | **Sector:** Upstream (Reservoir, Exploration)

---

## What You Learned

Spatial statistics: variograms, kriging (simple, ordinary, universal), sequential Gaussian simulation, conditional simulation, and geostatistical modeling of spatially distributed data. You learned to estimate values at unsampled locations using spatial correlation.

## Where This Subject Is Used in Industry

- **Reservoir Property Mapping:** Wells are expensive â€” typically 5â€“30 wells per reservoir. But the reservoir extends over square kilometres. How do you estimate porosity, permeability, and saturation between wells? Geostatistics. Kriging interpolates properties between wells using a variogram that captures the spatial continuity of the geological property.
- **Geological Modeling:** PETREL ([SLB](../../../data/company-directory/slb.md)) and Geoscience SKUA-GOCAD use geostatistical algorithms (Sequential Gaussian Simulation, Sequential Indicator Simulation) to populate 3D geological models with rock properties. These models are the input to reservoir simulators.
- **Uncertainty Quantification:** By running multiple realizations of a geostatistical model (each equally probable), you quantify the uncertainty in STOIIP and production forecasts â€” essential for investment decisions.
- **Ore Body / Resource Estimation:** Though this is oil & gas focused, the same geostatistical techniques are used in mining â€” a potential alternative career path in Angola (diamonds, iron ore).

## Angola-Specific Context

Angola's turbidite reservoirs have complex heterogeneity â€” channels, lobes, and shale drapes that separate reservoir compartments. Mapping this heterogeneity between wells requires geostatistics. The geological models for Girassol, Dalia, and Kaombo were built using geostatistical simulation in PETREL. Reservoir engineers use these models every day.

## ðŸ” Your Reflection Task

*"If I have porosity measurements from 10 wells across a Block 17 reservoir, and I need to estimate porosity at a location 2 km from the nearest well, how does kriging use the variogram to weight the contributions of each well's data?"*

---
*Courses, books, free software: [Learning Resources](../../../docs/learning-resources.md)*
