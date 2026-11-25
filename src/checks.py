"""Input contract for private runs: deliberately no private loader distributed."""
import numpy as np
from .schema import FEATURES

def validate_grid(df, require_labels=True):
    cols=['cell_id','x','y',*FEATURES]+(['label'] if require_labels else [])
    missing=set(cols)-set(df.columns)
    if missing: raise ValueError(f'missing required columns: {sorted(missing)}')
    if df.cell_id.duplicated().any(): raise ValueError('duplicate cell ids')
    if df[['x','y']].duplicated().any(): raise ValueError('duplicate coordinates')
    data=df[FEATURES].to_numpy(dtype=float)
    if not np.isfinite(data).all(): raise ValueError('non-finite predictors')
    if np.any((data<0)|(data>1)): raise ValueError('fuzzy values outside [0,1]')
    if require_labels and not set(df.label.unique())<= {0,1}: raise ValueError('invalid class labels')
    return True
