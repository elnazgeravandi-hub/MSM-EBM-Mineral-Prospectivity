import numpy as np

def small(distance, midpoint=1500.0, spread=2.0):
    d = np.asarray(distance, dtype=float)
    if np.any(d < 0): raise ValueError("distance must be nonnegative")
    return 1 / (1 + (d / midpoint) ** spread)

def mslarge(x, mean=None, std=None):
    """Paper Eq. 1, a=b=1: zero below mean; 0.5 at mean+std.
    Raster-wide mean/std must be derived from original complete continuous raster.
    """
    x = np.asarray(x, dtype=float)
    m = float(np.mean(x) if mean is None else mean)
    s = float(np.std(x) if std is None else std)
    if s <= 0: raise ValueError('std must be positive')
    out = np.zeros_like(x, dtype=float)
    mask = x > m
    out[mask] = 1.0 - s / (x[mask] - m + s)
    return out
