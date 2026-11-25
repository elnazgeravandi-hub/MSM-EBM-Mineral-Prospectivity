"""Native EBM main-effect attribution; no SHAP or surrogate explanations."""
import numpy as np
import pandas as pd
from .schema import FEATURES


def contributions(model, X):
    """Return additive contribution per feature on log-odds scale.

    interpret-core EBM.eval_terms is used; caller checks main-effect-only model.
    """
    if not hasattr(model, "eval_terms"):
        raise TypeError("EBM with eval_terms is required")
    if len(getattr(model, "term_features_", [])) != len(FEATURES) or any(len(t) != 1 for t in model.term_features_):
        raise ValueError("Expected exactly 12 main effects and zero interactions")
    terms = np.asarray(model.eval_terms(X), dtype=float)
    if terms.shape != (len(X), len(FEATURES)):
        raise ValueError("Unexpected main-effect contribution shape")
    return pd.DataFrame(terms, columns=FEATURES)


def importance(model, X):
    vals = contributions(model, X)
    return pd.DataFrame({"feature": FEATURES, "mean_abs_main_effect_log_odds": vals.abs().mean().to_numpy()}).sort_values("mean_abs_main_effect_log_odds", ascending=False)


def shape_functions(model):
    """Extract global plot coordinates and variation bands from interpret model.

    Bands (if supplied) are model-derived uncertainty/variability displays,
    not confidence intervals unless explicitly established by library semantics.
    """
    explanation = model.explain_global()
    rows=[]
    for i, name in enumerate(FEATURES):
        d = explanation.data(i)
        if not isinstance(d, dict):
            raise ValueError(f"No global explanation data for {name}")
        rows.append({"feature": name, "names": d.get("names"), "scores": d.get("scores"), "lower_bounds": d.get("lower_bounds"), "upper_bounds": d.get("upper_bounds")})
    return rows
