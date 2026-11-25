# MSM–EBM Mineral Prospectivity Mapping

## Public computational methodology and synthetic demonstration

This repository provides an inspectable Python implementation of four mineral prospectivity models and a synthetic-data demonstration of the computational workflow described in the accompanying manuscript.

> **Scope and reproducibility note.** The public demonstration uses entirely synthetic inputs. It is intended for methodological inspection and software testing; it does **not** numerically reproduce, independently validate, or replace the confidential geological-data analysis reported in the manuscript. The original geological datasets are not distributed here.


## Companion to the revised manuscript

**Research scope:** geologically informed monotonic constraints on EBM main effects for porphyry Cu prospectivity, assessed with 6 km spatial blocks and a 900 m training-exclusion buffer. This is an **executable synthetic companion**, not a public-data reproduction of the published figures or performance numbers.

**Selection chronology:** both the 1,500 m Small-membership midpoint and the separately applied 1,500 m positive-sampling neighborhood were selected **a priori** on geological grounds. The subsequent 1,487 m nearest-neighbor observation is descriptive only. The 824 occurrence-proximity enrichment cells were held out **before** constructing the 2,973 positive labeled cells, and are **not externally independent** because the same inventory of 101 occurrences informs both. These original sample-construction steps are documented, not regenerated, by the public synthetic runner.

**Recommended citation:** cite the final peer-reviewed paper when published; do not cite this synthetic demo as an independent validation study.

See [manuscript alignment audit](docs/MANUSCRIPT_ALIGNMENT.md) for an explicit implemented-vs-not-reproduced matrix.

## 1. Models

Four models are included:

1. **Logistic Regression** — L2-regularized logistic regression in a pipeline with standardization.
2. **EBM-Raw** — Explainable Boosting Machine without monotonic constraints.
3. **CatBoost-Raw** — gradient-boosted tree benchmark.
4. **MSM–EBM** — Explainable Boosting Machine configured with 12 non-decreasing main-effect constraints.

The demonstration uses the same 12 evidence features and common spatial validation partitions for the four models. EBM-Raw and MSM–EBM use the same numerical EBM configuration; their intended implementation difference is the monotonic-constraint vector:

- EBM-Raw: `[0] * 12`
- MSM–EBM: `[1] * 12`

The model settings in `configs/manuscript.yaml` are transcribed from the manuscript's reported configuration (Table 3). This is a transcription of reported settings, not independent proof that this public implementation is identical to the private scripts used to produce the manuscript results.

## 2. Computational Workflow

The public synthetic demonstration is organized into the following stages:

1. **Synthetic data generation:** creation of 12 simulated evidence features and the synthetic labelled dataset.
2. **Spatial validation design:** assignment of five spatial folds and application of buffer-based exclusion to candidate training samples.
3. **Model fitting:** training of Logistic Regression, EBM-Raw, CatBoost-Raw, and MSM–EBM using common spatial validation partitions.
4. **Out-of-fold prediction:** generation of predictions for the shared validation samples across the spatial folds.
5. **Performance evaluation:** calculation of ROC–AUC, Average Precision, MCC, Balanced Accuracy, Recall, and Brier Score.
6. **Additional analyses:** synthetic sensitivity analyses, descriptive occurrence-enrichment demonstrations, and target-delineation procedures where implemented in the public workflow.
7. **Output generation:** saving synthetic tables, figures, predictions, and supporting outputs.

The public synthetic workflow is intended for methodological inspection and software testing. It does not reproduce the original confidential geological-data preparation or the manuscript's numerical results.

### Relationship to the manuscript's data-preparation workflow

The manuscript's Table 1 describes fuzzy-membership transformations of the geological evidence layers. The public synthetic model-training pipeline does **not** reproduce the original GIS/raster preparation. Its synthetic predictors are generated directly as scaled 0–1 features.

A separate illustrative command demonstrates four `MSLarge` and eight `Small` membership functions using fictional raw layer values. This example is not an input-processing stage in the synthetic model-training pipeline and does not reproduce the original ArcGIS raster preparation, raster-wide reference statistics, or distance-scale selection procedure.

## 3. Code Navigation

Use this map to go directly to the implementation relevant to each methodological component.

| Component | File or directory | What to inspect |
|---|---|---|
| Feature names and model names | [`src/schema.py`](src/schema.py) | The 12 input features and four model labels |
| Logistic Regression | [`src/models/logistic.py`](src/models/logistic.py) | Standardization and L2 logistic-regression estimator |
| EBM-Raw | [`src/models/ebm_raw.py`](src/models/ebm_raw.py) | EBM construction with unconstrained main effects |
| CatBoost-Raw | [`src/models/catboost_raw.py`](src/models/catboost_raw.py) | CatBoost estimator construction |
| MSM–EBM | [`src/models/msm_ebm.py`](src/models/msm_ebm.py) | EBM construction with 12 non-decreasing constraints |
| Model selection/factory | [`src/models/factory.py`](src/models/factory.py) | Maps model names and configurations to estimators |
| Spatial fold assignment and buffer exclusion | [`src/spatial_validation/buffered_cv.py`](src/spatial_validation/buffered_cv.py) | Fold IDs, validation partitions and training-buffer exclusion |
| Spatial compatibility imports | [`src/spatial.py`](src/spatial.py) | Public imports for spatial partition functions |
| Performance metrics | [`src/evaluation.py`](src/evaluation.py) | ROC–AUC, AP, MCC, balanced accuracy, recall and Brier score |
| Spatial ranking and target delineation | [`src/mapping.py`](src/mapping.py) | Percentile ranks, redistribution and DBSCAN target groups |
| Additional analyses | [`src/analysis.py`](src/analysis.py) | Descriptive enrichment and target sensitivity analyses |
| Fuzzy membership functions | [`src/fuzzy.py`](src/fuzzy.py) | `mslarge` and `small` transformations |
| Model configuration | [`configs/manuscript.yaml`](configs/manuscript.yaml) | Manuscript-transcribed model and spatial settings |
| Fast demonstration configuration | [`configs/demo.yaml`](configs/demo.yaml) | Lightweight software-demo settings |
| Synthetic data construction | [`src/synthetic.py`](src/synthetic.py), [`src/demo_data.py`](src/demo_data.py) | Simulated labelled subset and full-area grid |
| Main workflow | [`scripts/run_all.py`](scripts/run_all.py) | End-to-end synthetic execution and output generation |
| Synthetic data generation entry point | [`scripts/generate_synthetic_data.py`](scripts/generate_synthetic_data.py) | Synthetic-data generation utility |
| Illustrative fuzzy example | [`scripts/demo_fuzzy_membership.py`](scripts/demo_fuzzy_membership.py) | Example use of four `MSLarge` and eight `Small` functions |
| Automated tests | [`tests/`](tests/) | Unit, pipeline, repository-layout and scientific-contract tests |
| CI workflow | [`.github/workflows/tests.yml`](.github/workflows/tests.yml) | Automated test and synthetic-pipeline execution |

### Where to inspect manuscript-related analyses

The README maps the relevant analysis code to the following files. The presence of a file reference is a navigation aid; the exact correspondence between each manuscript table and a particular function should be checked against the implementation and generated outputs.

| Manuscript component | Relevant code location in this repository |
|---|---|
| Table 1 — fuzzy membership functions | `src/fuzzy.py`; illustrative runner: `scripts/demo_fuzzy_membership.py` |
| Table 3 — model settings | `configs/manuscript.yaml`; model constructors under `src/models/` |
| Table 4 — spatial validation settings | `configs/manuscript.yaml`; `src/spatial_validation/buffered_cv.py` |
| Tables 5–7 — model comparisons and OOF evaluation | `scripts/run_all.py`; `src/evaluation.py`; `src/analysis.py` |
| Table 8 — descriptive occurrence-enrichment analysis | `src/analysis.py` |
| Table 9 — target delineation and sensitivity analysis | `src/mapping.py`; `src/analysis.py` |

The public synthetic workflow does not reproduce the original confidential data preparation or the published numerical tables. These references identify code areas for inspection, not proof of numerical reproduction.

### Recommended inspection order for reviewers

1. Start with [`configs/manuscript.yaml`](configs/manuscript.yaml) to inspect the reported model settings.
2. Inspect the four model constructors under [`src/models/`](src/models/).
3. Inspect [`src/spatial_validation/buffered_cv.py`](src/spatial_validation/buffered_cv.py) for spatial fold assignment and buffer-based training exclusion.
4. Inspect [`src/evaluation.py`](src/evaluation.py) for the performance metrics.
5. Follow [`scripts/run_all.py`](scripts/run_all.py) to see how the components are assembled into the synthetic workflow.
6. Inspect [`src/analysis.py`](src/analysis.py) and [`src/mapping.py`](src/mapping.py) for the additional analysis and target-delineation code.
7. Review [`tests/`](tests/) and [`.github/workflows/tests.yml`](.github/workflows/tests.yml) for software checks and continuous integration.

## 4. Installation

Python 3.11 is used in the automated workflow and is recommended.

```bash
python -m pip install -r requirements.txt
```

## 5. Running the Demonstration

### Quick model smoke test

```bash
python -m scripts.smoke_available_models
```

This is a lightweight check that the available model implementations can be constructed and exercised.

### Full synthetic spatial-validation workflow

```bash
python -m scripts.run_all --data synthetic --config configs/manuscript.yaml
```

This runs the synthetic workflow using the manuscript-transcribed model configuration and the spatial configurations recorded in that file. The command below uses the lightweight demo configuration by default and should not be confused with the manuscript-transcribed configuration:

```bash
python -m scripts.run_all
```

All inputs to the public runner are synthetic. The public runner intentionally does not load the confidential geological datasets.

### Separate illustrative fuzzy-membership example

```bash
python -m scripts.demo_fuzzy_membership
```

This command creates fictional raw layer values and illustrates four `MSLarge` and eight `Small` functions. It is **not** part of the synthetic model-training input pipeline, which supplies already-scaled 0–1 predictors. It does not reproduce the original ArcGIS raster preparation, raster-wide reference statistics, or the study's distance-scale selection procedure. See [`docs/SCIENTIFIC_LIMITATIONS.md`](docs/SCIENTIFIC_LIMITATIONS.md).

## 6. Synthetic Dataset

The synthetic dataset is generated using nonlinear, non-decreasing contributions from 12 simulated evidence layers to the outcome-generating probability, together with stochastic labels and a spatial component. This design illustrates a setting in which monotonic modeling assumptions are relevant; it does not guarantee that MSM–EBM will outperform the other models.

Synthetic performance comparisons must not be interpreted as independent evidence of the published model's superiority. No confidential geological observations, real occurrence locations, or private study coordinates are included. The synthetic dataset is independently generated and is not a statistical privacy-preserving transformation of the original research data.

## 7. Spatial Validation and Evaluation

The reference spatial-validation configuration uses:

- Five spatial folds.
- 6 km spatial blocks.
- A 900 m exclusion buffer around validation samples.
- Shared training and validation partitions across the four models.
- Pooled out-of-fold (OOF) predictions for overall performance metrics.

The configuration file also specifies additional block-size and buffer combinations for the synthetic sensitivity analysis.

The reported performance measures calculated by the evaluation module are:

- ROC–AUC
- Average Precision (AP)
- Matthews Correlation Coefficient (MCC)
- Balanced Accuracy
- Recall
- Brier Score

## 8. Automated Testing and Continuous Integration

The repository includes a GitHub Actions workflow that runs:

- Automated tests (`pytest`).
- Four-model synthetic smoke testing.
- Workflow schematic generation.
- Monotonic-constraint and demonstration checks.
- The full five-fold synthetic pipeline using `configs/manuscript.yaml`.
- Upload of the generated synthetic outputs as a workflow artifact.

A successful workflow run demonstrates that the specified software checks and synthetic pipeline completed in the GitHub Actions environment. It does not establish scientific equivalence with the original confidential analysis or reproduce the manuscript's numerical results.

To inspect generated outputs from a successful run:

1. Open the repository's **Actions** tab.
2. Select the successful `unit-and-synthetic-smoke` run.
3. Open the run summary.
4. Download the `synthetic-pipeline-results` artifact.

## 9. Generated Outputs

The synthetic pipeline writes its outputs under:

```text
outputs/synthetic_demo/
```

These include synthetic performance tables, fold-level metrics, spatial sensitivity summaries, OOF predictions, synthetic maps and supporting figures, and target-sensitivity outputs. Output filenames are marked with `SYNTHETIC` where applicable. They must not be confused with the manuscript's results from the original geological datasets.

## Two distinct 1500 m settings in the reported study

The manuscript uses **1500 m in two different contexts**:

- **Small fuzzy-membership midpoint:** The eight proximity evidence layers use a midpoint of 1500 m and a spread of 2. The manuscript and reviewer responses report that these fuzzy settings were selected *a priori* as geological modeling assumptions, independently of known Cu-occurrence locations. This repository follows those **reported settings**; it cannot independently verify the historical parameter-selection process.
- **Positive-class sampling radius:** A separate 1500 m neighborhood radius was also specified **a priori** on geological grounds. The subsequent nearest-neighbor analysis (NNA) of 101 known Cu occurrences (mean nearest-neighbor distance approximately 1487 m) was a **descriptive consistency check**, not the basis for selecting or modifying this radius. The radius defines deposit-associated sampling neighborhoods, not the Small membership midpoint.

The same numerical value is used for two distinct purposes and does not imply that their roles are interchangeable. The repository cannot independently authenticate the historical selection chronology; that requires the research team’s original analysis records.

The public synthetic pipeline generates 0–1 features directly. `scripts/demo_fuzzy_membership.py` illustrates the reported transformations on invented values, rather than reproducing original GIS processing. See [Scientific Limitations](docs/SCIENTIFIC_LIMITATIONS.md).

## 10. Scientific Interpretation and Limitations

The manuscript reports MSM–EBM as having the best pooled out-of-fold point estimates under the reference validation configuration. The synthetic demonstration is provided to test and illustrate the computational workflow, not to reproduce or independently confirm those numerical results. Differences among synthetic model results are reported as obtained, without forcing a predetermined ranking.

Prospectivity scores are relative model outputs and should not be interpreted as calibrated probabilities of mineral discovery. The descriptive occurrence-enrichment analysis is not independent external validation.

Additional methodological limitations and open verification items—including the provenance of the distance scale, coordinate reference system and fold origin, rank-tie convention, and differences between the synthetic runner and private-data preparation—are documented in [`docs/SCIENTIFIC_LIMITATIONS.md`](docs/SCIENTIFIC_LIMITATIONS.md).

## 11. Data Availability

The underlying Geological Survey of Iran (GSI)-derived geological, geochemical, geophysical and Cu-occurrence records are restricted and are not distributed in this repository. The public synthetic data contain no real coordinates, occurrence locations, map raster cells or study-specific scores.

Numerical reproduction of the published results requires authorized access to the original study inputs and a separately verified private-data analysis. See [`docs/DATA_AVAILABILITY.md`](docs/DATA_AVAILABILITY.md) for the data-availability statement and secure private-data integration requirements.

---

**Repository scope:** Executable methodological implementation and synthetic demonstration.

**Reproducibility limitation:** The published numerical results cannot be regenerated from the public synthetic demonstration data alone.
