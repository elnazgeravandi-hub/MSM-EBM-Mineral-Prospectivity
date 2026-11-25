import numpy as np
from scripts.demo_fuzzy_membership import example_table, INCREASING, DECREASING
from src.fuzzy import mslarge, small
from src.schema import FEATURES


def test_table1_evidence_coverage_and_bounded_outputs():
    assert set(INCREASING).isdisjoint(DECREASING)
    assert set(INCREASING) | set(DECREASING) == set(FEATURES)
    raw, transformed = example_table()
    assert list(raw.columns) == list(transformed.columns)
    assert np.isfinite(transformed.to_numpy()).all()
    assert ((transformed >= 0) & (transformed <= 1)).all().all()


def test_table1_favorable_direction():
    x = np.array([-4., -2., 0., 2., 4.])
    increasing = mslarge(x, mean=0., std=1.)
    assert np.all(np.diff(increasing) >= 0)
    distances = np.array([0., 500., 1500., 3000.])
    decreasing = small(distances, midpoint=1500, spread=2)
    assert np.all(np.diff(decreasing) <= 0)
    assert decreasing[2] == 0.5
