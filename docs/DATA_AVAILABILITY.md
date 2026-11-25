# Data availability, confidentiality and demonstration scope

The underlying Geological Survey of Iran geological, geochemical, geophysical and
Cu-occurrence records are restricted and are **not** distributed in this repository.
The public `data/synthetic/` dataset is generated algorithmically without real
coordinates, real occurrence locations, map raster cells, or study-specific scores.
Its purpose is to check software execution, input contracts, outputs and visualization;
**its results cannot reproduce published Table 4–9 values or Figure 2–13 maps.**
The fitted classification output distinguishes deposit-associated sampled cells from
presumed-background sampled cells, not calibrated discovery probability.
The 824 occurrence-proximity cells, where made available privately, are to be used
only for descriptive spatial enrichment, not external validation.

## Secure private-data integration contract (not published)
Supply a tabular full-area grid with `cell_id, x, y` (projected metres) and the
12 0–1 predictor columns defined in `src/schema.py`, plus a separate labelled
subset with binary `label`, unique cell IDs and optionally `occurrence_id`.
Align rows by cell ID, **not by positional order**. Never publish the actual
CSV, derived target coordinates, fitted private models, logs containing paths,
or georeferenced raster exports. Validate origin, CRS, feature order, duplicate
coordinates, NaNs and overlap before execution.

Demo inputs are NOT a statistical privacy-preserving transformation of the real data.
Review data rights and the GSI data-use agreement before sharing any derivative.
