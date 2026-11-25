# Manuscript-output traceability

All `SYNTHETIC` outputs are operational demonstrations, not reproduced results.

| Manuscript item | Public implementation | Status/qualification |
|---|---|---|
| Table 1 fuzzy functions | `src/fuzzy.py`, `configs/manuscript.yaml`, Methods | Standalone fictional raw-input fuzzy example and unit tests; raster ArcGIS extraction cannot be verified without restricted GIS layers |
| Table 2 model architecture | `src/models/`, `src/schema.py` | Model design captured |
| Table 3 locked hyperparameters | `configs/manuscript.yaml` | Transcribed, private-data equivalence not independently verified |
| Table 4 class-specific spatial counts | `src/spatial.py`, `scripts/run_all.py` | Synthetic counts differ from paper |
| Table 5 five spatial-design fold metrics | `scripts/run_all.py` | Implemented; real-data reproduction not independently verified |
| Table 6 hyperparameter sensitivity | `scripts/run_all.py` | Implemented nine reference/alternative configurations; real-data reproduction not independently verified |
| Table 7 pooled OOF metrics | `src/evaluation.py` | Synthetic only; distinguish pooled from fold means |
| Table 8 descriptive capture | `src/analysis.py` | Simulated withheld enrichment cells; not external validation |
| Table 9 DBSCAN sensitivity | `src/analysis.py` | 10 configurations; numeric differences expected |
| Figure 1 study area geology | not distributed | Real geographical map cannot be recreated with anonymous synthetic data |
| Figure 2 spatial integrity | `src/figures_extra.py` | Fold-wise sensitivity implemented; EBM integration pending |
| Figure 3 workflow | `scripts/make_workflow.py` | Standalone methodological schematic |
| Figures 4–6 maps and OOF curves | `src/figures.py` | Synthetic example only |
| Figures 7–9 rank changes, consensus, decision-space | `src/figures_extra.py` | Synthetic example only |
| Figures 10–11 EBM shape/importance | `src/interpretation.py`, `src/figures_extra.py` | Requires interpret-core; model-native contributions, not SHAP |
| Figure 12 decile capture | `src/figures_extra.py` | Simulated descriptive enrichment only |
| Figure 13 target maps and ranking | `src/figures_extra.py` | Synthetic coordinate scatter; no genuine georeferenced map |

**Required secure-side independent audit:** verify real sample construction, original Table 4 counts, per-fold predictions against source analysis, predictor raster alignment, fold IDs, score rank ties, and expected Table 5–9 metrics. The private data and its derived coordinates must never be committed.
