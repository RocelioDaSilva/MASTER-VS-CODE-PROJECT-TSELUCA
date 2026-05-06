# IMAGE SOURCES & LITERATURE — Recommended replacements for placeholders
Date: 2026-04-18

Purpose: centralize recommended openly-licensed images, data sources, and authoritative literature to replace placeholders in `figures/` and to strengthen the manuscript argumentation. Each entry includes a suggested local filename, a direct link (when available), the license/attribution text to place in the manuscript or captions, and a note on how the image supports the paper.

---

## Figure placeholders inventory (recommended replacements)

1) `mapa_aptidao_integrada` (integrated suitability map)
   - Recommendation: Use your generated MCDA raster export (GeoTIFF/PNG) as the canonical figure (best provenance).
   - If you need an illustrative external map: Global Solar Atlas (World Bank / Solargis) — export area map or PVOUT raster for Angola.
   - URL (site): https://globalsolaratlas.info/
   - License / attribution: "Global Solar Atlas — World Bank Group, Solargis" (see site Terms of Use). Include dataset citation in caption.
   - Suggested filename: `mapa_aptidao_integrada.png`

2) `mapa_irradiacao` (irradiance map)
   - Recommendation: Generate map from NASA POWER or Global Solar Atlas for chosen study extent and export PNG.
   - NASA POWER: https://power.larc.nasa.gov/ (public domain — cite NASA POWER)
   - Global Solar Atlas: https://globalsolaratlas.info/
   - Suggested filename: `mapa_irradiacao.png`
   - Caption attribution example: "Irradiance based on NASA POWER (NASA/LaRC) or Global Solar Atlas (World Bank/ESMAP/Solargis)."

3) `mapa_populacao` (population map)
   - Source: WorldPop (high-resolution population rasters for Angola). Use the WorldPop country download for Angola and render the appropriate extent.
   - URL: https://www.worldpop.org/
   - License / attribution: See WorldPop data terms; include "WorldPop (University of Southampton)" in caption.
   - Suggested filename: `mapa_populacao.png`

4) `mapa_distanciarede` (distance-to-grid)
   - Recommended approach: derive from OpenStreetMap power layer (overpass/Geofabrik) and compute Euclidean distance in QGIS or GDAL; export PNG for figure.
   - OSM / Overpass: https://overpass-turbo.eu/
   - If you need a ready image: consider OpenInfraMap or an OSM export screenshot (check tile licensing and attribute OpenStreetMap contributors).
   - Suggested filename: `mapa_distanciarede.png`

5) Mini-grid photograph(s) (replace or supplement `solartainer_mali.jpg`)
   - Wikimedia Commons candidates (check license on each file page):
     - Solartainer in Cinzana, Mali — https://commons.wikimedia.org/wiki/File:Solartainer_in_Cinzana-Gare_(Segou-region)_Mali.jpg (CC BY‑SA 4.0)
     - Mini-Grid Bayelsa (Nigeria) — https://commons.wikimedia.org/wiki/File:Mini-Grid_Bayelsa.jpg (check license on file page)
   - Suggested filename(s): `photo_solartainer_mali.jpg`, `photo_minigrid_bayelsa.jpg`
   - Caption attribution example: "Photo: [Author], Wikimedia Commons, CC BY‑SA 4.0" (place full credit on the figure caption or list of figure credits).

6) IoT protocol stack / architecture (`iot_protocol_stack.png`)
   - Option A: Recreate a clean vector diagram in diagrams.net (draw.io) and export as `iot_protocol_stack.svg/png` (preferred for clarity and license control).
   - Option B: Use an openly-licensed Wikimedia diagram if available. Search: https://commons.wikimedia.org
   - Suggested filename: `iot_protocol_stack.png`

7) Climate scenarios / RCP irradiance projection (`climate_scenarios.png`)
   - Best practice: generate your own projection figure using NASA POWER baseline + CMIP6-derived irradiance anomalies (or use published IPCC/IRENA visuals if license allows).
   - Useful resources: IPCC AR6 figures (may be copyrighted), IRENA climate/renewables briefs, NASA POWER.
   - Suggested filename: `climate_scenarios_irradiance.png`

8) Köppen climate classification (`koppen_climate.png`)
   - Wikimedia Commons has Koppen maps (search "Köppen map" on Commons). Example wiki page: https://en.wikipedia.org/wiki/K%C3%B6ppen_climate_classification (then follow figure file link and check license).
   - Suggested filename: `koppen_climate.png`

---

## How to download and place files (recommended)

1. Preferred workflow: create or export maps locally (QGIS) from raw rasters (WorldPop, NASA POWER, your MCDA outputs) to keep provenance. Export as PNG at 300 DPI for publication.

2. Example PowerShell commands to download a Wikimedia Commons image (adjust URL and filename):

```powershell
# Example: download Solartainer image
$url = 'https://upload.wikimedia.org/wikipedia/commons/..../Solartainer_in_Cinzana-Gare_(Segou-region)_Mali.jpg'
Invoke-WebRequest -Uri $url -OutFile 'manuscript_unified/science_manuscript/manuscript/figures/photo_solartainer_mali.jpg'
```

3. For dataset downloads (WorldPop, NASA POWER, Global Solar Atlas) follow the providers' data portals and cite datasets according to their instructions.

4. Add images to LaTeX where placeholders exist using the `figures/` path. Example snippet to insert in `SOL.tex`:

```tex
\begin{figure}[ht]
  \centering
  \includegraphics[width=0.95\linewidth]{figures/photo_solartainer_mali.jpg}
  \caption{Example mini-grid (Solartainer). Photo: Klimakrieger / Wikimedia Commons (CC BY‑SA 4.0).}
  \label{fig:solartainer}
\end{figure}
```

---

## Curated literature & data sources (use to strengthen manuscript sections)

### Core datasets (open / authoritative)
- NASA POWER: meteorological & solar resource time series (public domain) — https://power.larc.nasa.gov/
- Global Solar Atlas (World Bank / Solargis): irradiance maps and PVOUT — https://globalsolaratlas.info/
- WorldPop: high-resolution population rasters (Angola) — https://www.worldpop.org/
- VIIRS Nighttime Lights (Earth Observation Group / Colorado School of Mines): socio-economic proxy — https://eogdata.mines.edu/
- OpenStreetMap / Overpass (power network data): https://overpass-turbo.eu/

### Key academic references (recommended citations)
- Malczewski, J. (2006). GIS‑based multicriteria decision analysis: a survey. International Journal of Geographical Information Science. DOI:10.1080/13658810600661508 — Use in Methods (GIS‑MCDA justification).
- Saaty, T. L. (1980 / 1987). Analytic Hierarchy Process (AHP) — Use when justifying weight elicitation and consistency ratios.
- Ester, M., Kriegel, H.-P., Sander, J., & Xu, X. (1996). A density‑based algorithm for discovering clusters in large spatial databases with noise. KDD 1996 — Cite for DBSCAN clustering rationale.
- Ahlborg, H., & Hammar, L. (2014). Comparative mini‑grid case studies (Tanzania) — Use to support participatory design and sustainability claims.
- IEA (2022). Africa Energy Outlook 2022 — policy and investment context (use figures and numbers with citation): https://iea.blob.core.windows.net/assets/220b2862-33a6-47bd-81e9-00e586f4d384/AfricaEnergyOutlook2022.pdf
- Zeiselmair, A.; Köppl, S. (2021). Constrained Optimization as the Allocation Method in Local Flexibility Markets. Energies, 14, 3932. DOI:10.3390/en14133932 — useful for optimization and constrained allocation comparisons.
- IRENA country and technical reports (Angola-specific zoning & PV economics) — https://www.irena.org/

### Mapping literature to manuscript sections (short suggestions)
- **Introduction / Policy**: cite IEA 2022 and IRENA Angola reports for investment and electrification targets.
- **Methods / MCDA**: cite Malczewski (GIS‑MCDA) and Saaty (AHP). Add a short paragraph justifying weight elicitation and reporting the consistency ratio threshold (CR < 0.1 recommended).
- **Data / Inputs**: cite WorldPop (population), NASA POWER (irradiance), VIIRS (nighttime lights) and state pre-processing (normalization to 0–100) with provenance.
- **Clustering & Extraction**: cite Ester et al. (DBSCAN) for the agglomeration approach and provide parameter selection rationale (eps/minPts) plus sensitivity results.
- **Economics**: cite IRENA and NREL cost reports for LCOE and sample payback calculations.
- **Validation**: cite project case studies (Ahlborg 2014) and outline the field validation protocol (baseline, 6‑month operational monitoring, control-treatment evaluation) with reference.

---

## Next steps (suggested)
1. Confirm whether you want me to download selected Wikimedia images into `figures/` (I will keep each file's license metadata in a text file next to the image). (RECOMMENDED: yes for Commons images.)
2. If you prefer, I can also generate LaTeX figure blocks to replace current placeholders and open a follow-up patch that inserts them into `SOL.tex` (requires confirming caption text and figure order).
3. I can map each curated literature item into exact manuscript locations and propose 1–2 sentence rewrites with citations.

---

If you want me to proceed with actual downloads and LaTeX edits, reply "Download images" (I will fetch Commons images and add them) or "Insert citations" to proceed with integrating literature into manuscript sections.
