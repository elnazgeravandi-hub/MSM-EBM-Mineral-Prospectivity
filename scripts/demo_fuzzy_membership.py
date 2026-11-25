"""Standalone synthetic Table 1 fuzzy-membership example (not manuscript data).

Run: python -m scripts.demo_fuzzy_membership
This is independent from the 0–1 feature generator used by scripts.run_all.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from src.fuzzy import mslarge, small

# The order and meanings of the 12 features match src.schema.FEATURES.
INCREASING = ('f1_cu_pb_zn', 'f3_cu_mo', 'rtp', 'fault_density')
DECREASING = ('granitoid', 'fault_n', 'fault_e', 'fault_nw', 'fault_ne',
              'phyllic', 'argillic', 'fe_oxide')


def example_table(n=30, seed=42):
    """Return fictional raw inputs alongside transformed favorability scores."""
    rng = np.random.default_rng(seed)
    raw = pd.DataFrame(index=range(n))
    for col in INCREASING:
        raw[col] = rng.normal(loc=5, scale=2, size=n)
    for col in DECREASING:
        raw[col] = rng.uniform(0, 4000, size=n)
    membership = pd.DataFrame(index=raw.index)
    for col in INCREASING:
        # Demonstration only: full synthetic vector supplies reference statistics.
        membership[col] = mslarge(raw[col].to_numpy(), mean=raw[col].mean(),
                                  std=raw[col].std(ddof=0))
    for col in DECREASING:
        membership[col] = small(raw[col].to_numpy(), midpoint=1500, spread=2)
    assert ((membership >= 0) & (membership <= 1)).all().all()
    return raw, membership


def main():
    raw, membership = example_table()
    output = Path('outputs/fuzzy_example')
    output.mkdir(parents=True, exist_ok=True)
    raw.to_csv(output / 'raw_invented_values.csv', index=False)
    membership.to_csv(output / 'transformed_invented_memberships.csv', index=False)
    print(f'Wrote synthetic fuzzy example to {output.resolve()}')


if __name__ == '__main__':
    main()
