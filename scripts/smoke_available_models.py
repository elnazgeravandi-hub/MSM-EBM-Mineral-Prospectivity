
"""Smoke-test all four manuscript models on synthetic data.

This test verifies that each model can be fitted and evaluated
using the same spatial training/validation split.

Synthetic performance metrics are NOT manuscript results.
"""

import numpy as np
import yaml
from pathlib import Path

from src.demo_data import make_demo
from src.spatial import partitions
from src.schema import FEATURES, MODEL_NAMES
from src.models.factory import create
from src.evaluation import metrics


def main():
    config = yaml.safe_load(
        Path("configs/demo.yaml").read_text(encoding="utf-8")
    )

    seed = config["seed"]

    # Synthetic demonstration dataset only
    df, grid, _ = make_demo(seed, True)

    # Identical spatial split for all four models
    _, train_idx, val_idx, _ = next(
        iter(partitions(
            df,
            block_m=config["reference_block_m"],
            buffer_m=config["reference_buffer_m"],
        ))
    )

    X_train = df.iloc[train_idx][FEATURES]
    y_train = df.iloc[train_idx]["label"]

    X_val = df.iloc[val_idx][FEATURES]
    y_val = df.iloc[val_idx]["label"]

    print("SYNTHETIC DATA — SMOKE TEST ONLY")
    print("Training samples:", len(train_idx))
    print("Validation samples:", len(val_idx))

    results = {}

    for name in MODEL_NAMES:
        print(f"\nTesting: {name}")

        model = create(name, config["models"], seed)
        model.fit(X_train, y_train)

        probabilities = model.predict_proba(X_val)[:, 1]

        if not np.all(np.isfinite(probabilities)):
            raise ValueError(
                f"Non-finite predictions from {name}"
            )

        if np.any((probabilities < 0) | (probabilities > 1)):
            raise ValueError(
                f"Invalid probability range from {name}"
            )

        scores = metrics(y_val, probabilities)
        auc = float(scores["AUROC"])

        if not np.isfinite(auc):
            raise ValueError(f"Invalid AUROC from {name}")

        results[name] = auc

        print(
            f"{name}: "
            f"n_train={len(train_idx)}, "
            f"n_validation={len(val_idx)}, "
            f"AUROC={auc:.4f}"
        )

    if len(results) != 4:
        raise RuntimeError("Not all four models completed")

    print("\nALL FOUR SYNTHETIC SMOKE FITS PASSED")
    print("These are NOT the published manuscript results.")


if __name__ == "__main__":
    main()
