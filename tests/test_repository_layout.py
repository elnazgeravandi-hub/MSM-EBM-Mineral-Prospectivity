"""Check clean, canonical module paths and spatial imports."""
from src.models import logistic, ebm_raw, catboost_raw, msm_ebm
from src.models.factory import create
from src.spatial import partitions as public_partitions
from src.spatial_validation.buffered_cv import partitions as actual_partitions


def test_canonical_model_modules():
    assert callable(logistic.create)
    assert callable(ebm_raw.create)
    assert callable(catboost_raw.create)
    assert callable(msm_ebm.create)
    assert callable(create)


def test_spatial_validation_reexport():
    assert public_partitions is actual_partitions
