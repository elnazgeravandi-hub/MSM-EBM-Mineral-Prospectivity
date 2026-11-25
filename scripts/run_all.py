"""Run from repo root: python -m scripts.run_all --data synthetic"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from src.demo_data import make_demo
from src.schema import FEATURES,MODEL_NAMES
from src.spatial import partitions,fold_ids
from src.models.factory import create as build_model
from src.evaluation import metrics
from src.mapping import percentile_rank,redistribution,targets
from src.analysis import target_sensitivity
from src.checks import validate_grid
from src.figures import save_evaluation,save_maps
from src.figures_extra import save_spatial_integrity,save_spatial_diagnostics,save_ebm_interpretation,save_enrichment
from src.analysis import descriptive_enrichment,require_no_enrichment_overlap

def execute(data='synthetic',quick=False,config_path='configs/demo.yaml'):
    config=yaml.safe_load(Path(config_path).read_text())
    if data != 'synthetic':
        raise ValueError('Public runner intentionally accepts synthetic data only. Private-data loader is not distributed.')
    out=Path('outputs/synthetic_demo');out.mkdir(parents=True,exist_ok=True)
    df,grid,enrichment_ids=make_demo(seed=config['seed'],quick=quick)
    validate_grid(df)
    Path('data/synthetic').mkdir(parents=True,exist_ok=True)
    df.to_csv('data/synthetic/demo.csv',index=False)
    X=df[FEATURES];y=df.label.to_numpy(); all_rows=[]; count_rows=[];scores_by_config={}; fold_rows=[]
    configs=[(6000,900)] if quick else [tuple(v) for v in config['spatial_configs']]
    for block,buffer in configs:
        folds=list(partitions(df,block,buffer))
        for k,tr,v,info in folds: count_rows.append(info)
        for name in MODEL_NAMES:
            oof=np.full(len(df),np.nan)
            for k,tr,v,info in folds:
                m=build_model(name,config['models'],config['seed'])
                m.fit(X.iloc[tr],y[tr]);prob=m.predict_proba(X.iloc[v])[:,1]
                oof[v]=prob
                fold_rows.append(dict(model=name,**info,**metrics(y[v],prob)))
            assert np.isfinite(oof).all(), 'Every row must have exactly one OOF prediction'
            pooled=metrics(y,oof)
            all_rows.append(dict(model=name,block_m=block,buffer_m=buffer,**pooled))
            scores_by_config[(block,buffer,name)]=oof
    pd.DataFrame(count_rows).to_csv(out/'Table_04_fold_counts_SYNTHETIC.csv',index=False)
    fold=pd.DataFrame(fold_rows);fold.to_csv(out/'fold_metrics_SYNTHETIC.csv',index=False)
    summary=fold.groupby(['model','block_m','buffer_m'])[['AUROC','AP','MCC','balanced_accuracy','recall','Brier']].agg(['mean','std'])
    summary.to_csv(out/'Table_05_spatial_sensitivity_SYNTHETIC.csv')
    pd.DataFrame(all_rows).to_csv(out/'Table_07_pooled_OOF_SYNTHETIC.csv',index=False)
    ref=(6000,900)
    oof_rows=[]
    for name in MODEL_NAMES:
        probs=scores_by_config[(*ref,name)]
        oof_rows.append(pd.DataFrame({'cell_id':df.cell_id,'label':y,'model':name,'prob':probs}))
    oof=pd.concat(oof_rows,ignore_index=True)
    oof.to_csv(out/'OOF_reference_SYNTHETIC.csv',index=False)
    save_evaluation(oof,out)
    models={}; predictions={}
    for name in MODEL_NAMES:
        mod=build_model(name,config['models'],config['seed']);mod.fit(X,y)
        predictions[name]=mod.predict_proba(grid[FEATURES])[:,1];models[name]=mod
    full=grid[['cell_id','x','y']].copy()
    for name,p in predictions.items():
        col=name.lower().replace(' ','_').replace('-','_')
        full[f'{col}_score']=p;full[f'{col}_rank']=percentile_rank(p)
    full.to_csv(out/'full_area_predictions_SYNTHETIC.csv',index=False)
    save_maps(predictions,grid,out)
    save_spatial_diagnostics(grid,predictions,out)
    save_ebm_interpretation(models['MSM-EBM'],X,out)
    redis=redistribution(predictions['EBM-Raw'],predictions['MSM-EBM'])
    redis.to_csv(out/'Figure_07_09_redistribution_SYNTHETIC.csv',index=False)
    votes=sum((percentile_rank(p)>=75).astype(int) for p in predictions.values())
    pd.DataFrame({'cell_id':grid.cell_id,'consensus':votes}).to_csv(out/'Figure_08_consensus_SYNTHETIC.csv',index=False)
    base=targets(grid,predictions['MSM-EBM'])
    target_sensitivity(grid,predictions['MSM-EBM']).to_csv(out/'Table_09_target_sensitivity_SYNTHETIC.csv',index=False)
    pd.DataFrame([{k:v for k,v in t.items() if k!='cell_ids'} for t in base[:10]]).to_csv(out/'Figure_13_top_targets_SYNTHETIC.csv',index=False)
    require_no_enrichment_overlap(df,enrichment_ids)
    descriptive_enrichment(grid,predictions,enrichment_ids).to_csv(out/'Table_08_enrichment_SYNTHETIC.csv',index=False)
    save_enrichment(grid,predictions['MSM-EBM'],enrichment_ids,out)
    # The two MSM-EBM OOF comparisons use the same partitions and validation rows.
    ref_folds=list(partitions(df,6000,900))
    exclude_probs=np.full(len(df),np.nan)
    for k,tr,v,info in partitions(df,6000,900,occurrence_exclusion=True):
        mod=build_model('MSM-EBM',config['models'],config['seed'])
        mod.fit(X.iloc[tr],y[tr]);exclude_probs[v]=mod.predict_proba(X.iloc[v])[:,1]
    assert np.isfinite(exclude_probs).all()
    save_spatial_integrity([info for _,_,_,info in ref_folds],scores_by_config[(6000,900,'MSM-EBM')],exclude_probs,y,fold_ids(df.x,df.y),out)
    # Reference and one-at-a-time hyperparameter sensitivity: never used for tuning.
    if not quick:
        from copy import deepcopy
        sensitivity=[]
        variants=[('EBM-Raw','reference',None,None),('MSM-EBM','reference',None,None),
                  ('EBM-Raw','lr_0.0125','ebm',('learning_rate',0.0125)),('MSM-EBM','lr_0.0125','ebm',('learning_rate',0.0125)),
                  ('EBM-Raw','bins_128','ebm',('max_bins',128)),('MSM-EBM','bins_128','ebm',('max_bins',128)),
                  ('CatBoost-Raw','depth_4','catboost',('depth',4)),('CatBoost-Raw','depth_5','catboost',('depth',5)),('CatBoost-Raw','depth_6','catboost',('depth',6))]
        for name,tag,section,setting in variants:
            cfg=deepcopy(config['models'])
            if section:cfg[section][setting[0]]=setting[1]
            for k,tr,v,info in ref_folds:
                m=build_model(name,cfg,config['seed']);m.fit(X.iloc[tr],y[tr])
                sensitivity.append(dict(model=name,variation=tag,fold=k+1,**metrics(y[v],m.predict_proba(X.iloc[v])[:,1])))
        ss=pd.DataFrame(sensitivity)
        ss.to_csv(out/'Table_06_folds_SYNTHETIC.csv',index=False)
        ss.groupby(['model','variation'])[['AUROC','AP','MCC','balanced_accuracy','recall','Brier']].agg(['mean','std']).to_csv(out/'Table_06_hyperparameters_SYNTHETIC.csv')
    print(f'Demo complete: {out.resolve()} ; NOT manuscript numerical reproduction.')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--data',default='synthetic');ap.add_argument('--quick',action='store_true');ap.add_argument('--config',default='configs/demo.yaml')
    a=ap.parse_args();execute(a.data,a.quick,a.config)
