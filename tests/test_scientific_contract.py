import numpy as np
import pandas as pd
import pytest
import yaml
from pathlib import Path
from src.synthetic import create
from src.spatial import fold_ids, partitions
from src.schema import FEATURES
from src.checks import validate_grid
from src.analysis import descriptive_enrichment,target_sensitivity,require_no_enrichment_overlap
from src.mapping import percentile_rank,redistribution
from src.models import ebm_raw,msm_ebm

def test_published_configuration_locked():
    d=yaml.safe_load(Path('configs/manuscript.yaml').read_text())
    assert d['seed']==42 and d['threshold']==0.5
    assert d['models']['ebm']['max_rounds']==1200 and d['models']['ebm']['outer_bags']==4
    assert d['models']['ebm']['interactions']==0 and d['models']['catboost']['iterations']==300

def test_coordinate_rule_exact():
    x=np.array([3000.,8999.,9000.,-3000.]);y=np.array([3000.]*4)
    expected=(np.floor((x-3000)/6000).astype(int))%5
    np.testing.assert_array_equal(fold_ids(x,y),expected)

def test_no_training_validation_overlap():
    df=create(nx=36,ny=30)
    for k,tr,v,info in partitions(df,6000,900):
        assert not set(tr)&set(v)
        assert info['min_distance_m']>900
        assert sum(df.iloc[v].label==1)>0 and sum(df.iloc[tr].label==0)>0

def test_synthetic_input_contract():
    df=create(nx=36,ny=30)
    assert validate_grid(df)
    bad=df.copy();bad.loc[0,FEATURES[0]]=2
    with pytest.raises(ValueError,match='outside'):validate_grid(bad)

def test_enrichment_not_external_validation():
    df=create(nx=36,ny=30)
    with pytest.raises(ValueError,match='overlaps'):require_no_enrichment_overlap(df, [0])
    result=descriptive_enrichment(df, {'test':np.arange(len(df))},list(df.cell_id.tail(10)))
    assert result.loc[0,'enrichment_count']==10
    assert result.loc[0,'top_10_pct_capture']==100

def test_target_sensitivity_exact_configurations():
    df=create(nx=36,ny=30)
    tab=target_sensitivity(df,df[FEATURES[0]].to_numpy())
    assert len(tab)==10
    ref=tab[(tab.top_fraction==.10)&(tab.eps==1.5)&(tab.min_samples==1)].iloc[0]
    assert ref.footprint_jaccard==1.0
    assert ref.reference_targets_matched==ref.reference_target_count

def test_ebm_constraints_matched(monkeypatch):
    import sys,types
    class Fake:
        def __init__(self,**kw):self.kw=kw
    inte=types.ModuleType('interpret');glass=types.ModuleType('interpret.glassbox')
    glass.ExplainableBoostingClassifier=Fake
    monkeypatch.setitem(sys.modules,'interpret',inte);monkeypatch.setitem(sys.modules,'interpret.glassbox',glass)
    cfg=dict(interactions=0,max_bins=64,max_rounds=1200)
    a=ebm_raw.create(cfg,42).kw;b=msm_ebm.create(cfg,42).kw
    assert {k:v for k,v in a.items() if k!='monotone_constraints'}=={k:v for k,v in b.items() if k!='monotone_constraints'}
    assert a['monotone_constraints']==[0]*12 and b['monotone_constraints']==[1]*12
