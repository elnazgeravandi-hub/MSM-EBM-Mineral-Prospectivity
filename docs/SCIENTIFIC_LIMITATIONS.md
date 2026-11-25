# Scientific scope and open verification items

This repository demonstrates an executable *synthetic-data* implementation, not the regeneration of the manuscript's numerical results. No published metrics have been substituted into execution outputs.

## Fuzzy transformation settings and distinct 1500 m roles

Four MSLarge layers (F1, F3, RTP magnetic anomaly, fault/lineament density) use mean and standard-deviation multipliers of 1. Eight Small distance-membership layers use a midpoint of **1500 m** and spread of **2**. Larger transformed values mean *assigned* geological favorability, not measured discovery probabilities.

**Fuzzy Small midpoint (as reported):** Section 3.1 of the supplied manuscript and the reviewer responses describe this midpoint as an *a priori* geological modeling assumption selected independently of known Cu occurrences, held fixed across spatial-validation folds. This repository reproduces the **reported numerical settings**, but cannot independently authenticate the chronology of the original GIS and parameter-selection decisions.

**Positive-sample radius (separate use):** The study also uses a **1500 m** radius around occurrences to construct positive modeling cells. This sampling radius was also specified **a priori**, on geological grounds. The subsequent NNA of 101 Cu occurrences yielded an observed mean nearest-neighbor distance of about **1487 m**; it served as a descriptive check and did **not** determine or modify the radius. It is not the fuzzy midpoint. Shared numerical values do not prove that the two settings have the same origin.

**Independent provenance limitation:** The manuscript and reviewer responses report both 1500 m settings as a priori. These historical choices cannot be independently authenticated from a synthetic code demonstration. The research team should retain original GIS logs and notes supporting the chronology. The synthetic runner does not test alternative original fuzzy midpoints or sampling radii.

The synthetic pipeline supplies scaled 0–1 evidence directly. `scripts/demo_fuzzy_membership.py` is an illustrative exercise, not the original geological-data preprocessing.

## Other verification limitations

- The synthetic generator directly supplies 12 scaled 0–1 evidence features; it does not load original raster layers. `scripts/demo_fuzzy_membership.py` separately illustrates the Table 1 transformations on invented raw values.
- The supplied manuscript Methods specify a common 300 × 300 m grid and a deterministic fold origin offset of 3000 m. These settings are represented in the public demonstration, but coordinate-system alignment and original grid geometry cannot be independently verified without the restricted inputs.
- Rank ties use mean percentile ranks in `src/mapping.py`. Threshold-based selection at an exact percentile boundary can include a different number of cells than a strict `ceil(N*fraction)` top-N rule (even for distinct scores). The manuscript does not define a tie/boundary convention; the demonstration's convention is disclosed and should not be claimed to replicate unpublished selection details.
- Published metrics in Tables 4–9 are not reconstructed from confidential data. The original data are required for numerical replication.
- Simulated enrichment cells are withheld from model fitting but are not independent external geological evidence; likewise the manuscript's 824 occurrence-proximity cells should only be treated as descriptive spatial concordance as stated in Table 8.
- A passing test suite validates specific software behaviors, not identity with the original private training workflow. EBM's runtime API and native monotonic shapes should be validated in the target environment.
- Production-ready private raster ingestion, original stratified sampling, and the manuscript's 200 m/500 m grid-resolution sensitivity assessment are outside the public runner.
