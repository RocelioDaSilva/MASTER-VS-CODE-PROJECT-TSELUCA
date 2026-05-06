GEESP-Angola — FAQ

Q: What data sources are required to reproduce results?
A: Processed rasters (irradiation, population, distance-to-grid, slope, NDVI) saved in `data/processed` plus the `mapas_metadata.json`. Code in `scripts/` reproduces maps; `generate_maps_simple.py` creates synthetic examples.

Q: How do you choose AHP weights?
A: We use a small expert panel (n=5) representing MINEA, ISPTEC, EDA, PNUD, and an NGO. Pairwise comparisons are documented in Appendix A; sensitivity analysis across 42 scenarios confirms rank stability.

Q: Is the code reproducible within 30 minutes?
A: Yes. Create the virtual environment, install `requirements.txt`, run `generate_maps_simple.py`, then `scripts/mcda_analysis.py` to reproduce aptitude maps.

Q: How are vulnerable populations protected?
A: Risk screening checklist (see `RISK_SCREENING_CHECKLIST.md`) defines exclusion criteria and safeguards. Community consent and grievance mechanisms are required before any pilot.

Q: What is needed for field validation?
A: Piranometer, data logger, GPS, technician training. See Appendix B for equipment list, coordinates, and daily procedures.

Q: Who owns the code and data?
A: Code is open-source under the LICENSE in the repo. Data generated in pilots follow MOUs with MINEA and community consent.

Q: How to request intervention if implementation fails?
A: Use the grievance channel documented in Appendix C; escalate to PNUD/ISPTEC and MINEA if unresolved after 14 days.
