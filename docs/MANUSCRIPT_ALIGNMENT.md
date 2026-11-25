# Alignment audit against revised manuscript (Sections 3.1–4.4)

This audit is limited to the supplied manuscript text and associated reviewer response. Original private scripts/data, raw tables/figures, historical GIS logs and actual GitHub CI execution were not supplied or independently verified. **Implemented** means functionality exists for demonstration—not that it reproduces the paper numerically.

| Manuscript requirement | Public implementation | Verification and limitation |
|---|---|---|
| Twelve fixed 0–1 evidence features | `src/schema.py`, `src/synthetic.py` | Synthetic values generated directly; original GIS rasters unavailable |
| 4 MSLarge (a=b=1), 8 Small (midpoint 1500 m, spread 2) | `src/fuzzy.py`, `scripts/demo_fuzzy_membership.py` | Separate illustrative example; NOT wired to synthetic model fitting or original GIS |
| 1500 m fuzzy midpoint selected a priori | README and scientific limitations | Original decision chronology self-reported in manuscript; not verifiable from demo |
| 1500 m positive-cell sampling radius selected a priori; NNA 1487 m only descriptive | Documentation only | Original 101 occurrences/2973 cells cannot be regenerated publicly |
| 824 enrichment cells reserved before positive sampling; shared occurrence inventory | `src/analysis.py` cell overlap check; synthetic holdouts in `src/demo_data.py` | Synthetic enrichment cells chosen randomly, NOT by proximity to real GSI occurrences; no independent external validation |
| 300 m reference grid; 200/500 m retrospective sensitivity | Synthetic 300 m grid | Original 200/500 m sensitivity analysis NOT reproduced |
| Five folds: 6 km spatial blocks, 900 m buffer; same splits for models | `src/spatial_validation/buffered_cv.py` | Fold rule uses 3000 m origin offset, excludes training observations at distance <= buffer; real-space checks need private data |
| Occurrence-exclusion sensitivity | `partitions(..., occurrence_exclusion=True)` | Demonstrative occurrence IDs only; original AUROC/AP shifts NOT reproduced |
| LR, EBM-Raw, CatBoost-Raw, MSM-EBM | `src/models/`, `src/models/factory.py` | Matched EBM parameters; MSM 12 monotone constraints; no pairwise interactions |
| Reported hyperparameters from Table 3 | `configs/manuscript.yaml` | Transcribed reported settings, not validated against historical model objects |
| Limited learning-rate/bin/depth sensitivity, Table 6 | `scripts/run_all.py` | One-at-a-time synthetic tests; not numerical replication |
| Pooled OOF and per-fold metrics including AP (not interpolated AUPRC) | `src/evaluation.py`, `scripts/run_all.py` | Uses `average_precision_score`; synthetic results differ |
| Model-native main-effect importance | `src/interpretation.py` | `eval_terms` mean absolute contributions; no SHAP |
| Figure 10 model-estimated variability band | **NOT reproduced or verified** | Figure 10 synthetic plot omits uncertainty bands; source/meaning of original shading needs separate verification |
| All-four-model descriptive enrichment and DBSCAN sensitivity | `src/analysis.py`, `src/mapping.py` | Demonstration uses withheld synthetic IDs, 10 parameter configurations, not real outcome records |
| Regional calibrated mineral-discovery probabilities | **Not claimed** | Scores are conditional on sampled labels; not absolute discovery probabilities |

**Audit findings addressed:** Prior repository README and `SCIENTIFIC_LIMITATIONS.md` incorrectly said the 1500 m positive sampling radius was informed by NNA; both now match the revised manuscript's a-priori selection chronology. Duplicate model subpackages and empty placeholder pipeline directories were removed. Figure 10 synthetic rendering avoids presenting unverified variability bands.

**Open external checks before citation/submission:** confirm original Tables 1–9 settings against confidential code and outputs, coordinate origin and CRS, tie-handling at percentile cutoffs, 824-cell holdout chronology using real data, Figure 10 uncertainty-band provenance, and actual deployed Python versions / package compatibility.
