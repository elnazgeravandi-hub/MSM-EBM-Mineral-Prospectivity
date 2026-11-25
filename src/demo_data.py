"""Entirely simulated full-area grid and confidential-data-free labeled subset."""
import numpy as np
from .synthetic import create

def make_demo(seed=42, quick=False):
    full=create(seed=seed, nx=54 if not quick else 44, ny=42 if not quick else 36)
    rng=np.random.default_rng(seed+111)
    # The full grid includes labels only for internal synthetic construction.
    # Public prediction frame has NO labels; all selected labeled rows are separate.
    mask=rng.uniform(size=len(full)) < (.68 if quick else .52)
    labeled=full.loc[mask].copy().reset_index(drop=True)
    if len(labeled)<100: raise ValueError('insufficient synthetic sample')
    grid=full.drop(columns=['label','occurrence_id']).copy()
    # Demo enrichment cells must be withheld from labeled development cells.
    available=np.setdiff1d(full.cell_id.to_numpy(),labeled.cell_id.to_numpy())
    enrich_ids=rng.choice(available,size=min(120,len(available)//2),replace=False)
    assert not set(enrich_ids).intersection(labeled.cell_id)
    return labeled,grid,enrich_ids
