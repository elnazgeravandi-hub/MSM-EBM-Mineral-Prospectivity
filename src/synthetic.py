
"""Synthetic demonstration with nonlinear monotonic relationships.

No confidential geological data are included.
This scenario is designed to illustrate monotonic inductive bias,
not to reproduce or independently validate manuscript results.
"""
import numpy as np
import pandas as pd
from .schema import FEATURES


def create(seed=42, nx=48, ny=36, step=300):
    rng = np.random.default_rng(seed)

    gx, gy = np.meshgrid(np.arange(nx), np.arange(ny))
    x = (gx.ravel() + 10) * step + 3000
    y = (gy.ravel() + 10) * step + 3000
    n = len(x)

    # Twelve synthetic evidence layers on a 0-1 scale.
    raw = rng.normal(size=(n, 12))
    spatial = np.sin(x / 2900) + np.cos(y / 2700)

    vals = 1 / (
        1 + np.exp(-(0.75 * raw + 0.15 * spatial[:, None]))
    )

    # Nonlinear, non-decreasing contributions from all 12 layers.
    weights = np.array([
        1.2, 1.1, 1.0, 0.9, 0.85, 1.1,
        1.3, 1.2, 0.95, 1.15, 1.0, 0.9
    ])

    nonlinear = (
        0.50 * vals**2
        + 0.30 * vals**4
        + 0.20 * np.maximum(vals - 0.45, 0)**2
    )

    signal = (nonlinear - nonlinear.mean(axis=0)) @ weights

    # Stochastic labels: no model predictions are used.
    logit = -0.1 + 2.0 * signal + 0.12 * spatial
    prob = 1 / (1 + np.exp(-np.clip(logit, -20, 20)))
    labels = rng.binomial(1, prob)

    df = pd.DataFrame(vals, columns=FEATURES)
    df.insert(0, "cell_id", np.arange(n))
    df["x"] = x.astype(float)
    df["y"] = y.astype(float)
    df["label"] = labels

    positive = np.flatnonzero(labels == 1)
    df["occurrence_id"] = -1
    df.loc[positive, "occurrence_id"] = (
        (x[positive] // 1500) * 10000
        + (y[positive] // 1500)
    ).astype(int)

    return df
