"""Fail-closed end-to-end demo verification on a fully provisioned Python 3.11 env."""
from pathlib import Path
import numpy as np
import pandas as pd
from src.schema import FEATURES
from src.models.factory import create
from src.demo_data import make_demo
from src.interpretation import contributions
from scripts.run_all import execute
import yaml


def main():
    cfg=yaml.safe_load(Path('configs/demo.yaml').read_text())
    labeled,_,_=make_demo(cfg['seed'],quick=True)
    X=labeled[FEATURES]
    a=create('EBM-Raw',cfg['models'],cfg['seed'])
    b=create('MSM-EBM',cfg['models'],cfg['seed'])
    assert np.array_equal(np.asarray(a.monotone_constraints),np.zeros(12))
    assert np.array_equal(np.asarray(b.monotone_constraints),np.ones(12))
    b.fit(X,labeled.label)
    c=contributions(b,X)
    assert c.shape == (len(X),12)
    # Verify model-native monotonic response, at fixed values of other features.
    anchor=X.iloc[[0]].copy()
    for feature in FEATURES:
        probe=pd.concat([anchor]*32,ignore_index=True)
        probe[feature]=np.linspace(0,1,32)
        native=contributions(b,probe)[feature].to_numpy()
        if np.any(np.diff(native)<-1e-7):
            raise AssertionError(f'Not monotone non-decreasing: {feature}')
    execute(data='synthetic',quick=True,config_path='configs/demo.yaml')
    out=Path('outputs/synthetic_demo')
    mandatory=['Table_04_fold_counts_SYNTHETIC.csv','Table_05_spatial_sensitivity_SYNTHETIC.csv',
     'Table_07_pooled_OOF_SYNTHETIC.csv','Table_08_enrichment_SYNTHETIC.csv',
     'Table_09_target_sensitivity_SYNTHETIC.csv','Figure_02_SYNTHETIC.png',
     'Figure_04_SYNTHETIC.png','Figure_05_SYNTHETIC.png','Figure_06_SYNTHETIC.png',
     'Figure_07_SYNTHETIC.png','Figure_08_SYNTHETIC.png','Figure_09_SYNTHETIC.png',
     'Figure_10_SYNTHETIC.png','Figure_11_SYNTHETIC.png',
     'Figure_12_SYNTHETIC.png','Figure_13_SYNTHETIC.png']
    missing=[f for f in mandatory if not (out/f).is_file() or (out/f).stat().st_size==0]
    if missing:raise RuntimeError(f'Missing or empty synthetic artifacts: {missing}')
    assert len(pd.read_csv(out/'Table_07_pooled_OOF_SYNTHETIC.csv'))==4
    print('FULL SYNTHETIC INTEGRATION CHECK PASSED; NOT A REPRODUCTION OF CONFIDENTIAL RESULTS.')

if __name__=='__main__':main()
