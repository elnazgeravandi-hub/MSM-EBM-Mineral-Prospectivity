"""Synthetic-only diagnostic figures; these never claim manuscript numeric replication."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .schema import FEATURES
from .mapping import percentile_rank, redistribution, targets
from .interpretation import importance, shape_functions


def save_spatial_integrity(fold_info, ref_probs, excluded_probs, labels, fold_ids, out):
    fig, ax = plt.subplots(1,3,figsize=(14,4))
    ax[0].bar([str(d['fold']) for d in fold_info], [d['min_distance_m'] for d in fold_info]); ax[0].axhline(900,ls='--',color='black');ax[0].set_title('Minimum separation (m)')
    from sklearn.metrics import roc_auc_score, average_precision_score
    for i,(nm,metric) in enumerate([('AUROC',roc_auc_score),('AP',average_precision_score)],start=1):
        original=[metric(labels[fold_ids==k],ref_probs[fold_ids==k]) for k in range(5)]
        excluded=[metric(labels[fold_ids==k],excluded_probs[fold_ids==k]) for k in range(5)]
        x=np.arange(5);ax[i].plot(x+1,original,'o-',label='reference');ax[i].plot(x+1,excluded,'s--',label='occurrence-excluded')
        ax[i].set(xlabel='Fold',title='Fold-wise '+nm+' (synthetic)',xticks=x+1)
        ax[i].legend(fontsize=7)
    fig.tight_layout();fig.savefig(out/'Figure_02_SYNTHETIC.png',dpi=160);plt.close(fig)


def save_spatial_diagnostics(full_df, prediction, out):
    raw=np.asarray(prediction['EBM-Raw']);msm=np.asarray(prediction['MSM-EBM'])
    d=redistribution(raw,msm)
    fig,ax=plt.subplots(1,2,figsize=(11,4));
    sc=ax[0].scatter(full_df.x,full_df.y,c=d.delta_rank,s=6,cmap='coolwarm',vmin=-100,vmax=100)
    fig.colorbar(sc,ax=ax[0],label='Percentile-rank difference');ax[0].set_title('Figure 7: Rank redistribution')
    ax[1].hist(d.delta_rank,bins=35);ax[1].set_title('Rank-change distribution')
    fig.tight_layout();fig.savefig(out/'Figure_07_SYNTHETIC.png',dpi=160);plt.close(fig)
    vote=sum((percentile_rank(np.asarray(s))>=75).astype(int) for s in prediction.values())
    fig,ax=plt.subplots(figsize=(7,5));sc=ax.scatter(full_df.x,full_df.y,c=vote,vmin=0,vmax=4,s=6,cmap='viridis');fig.colorbar(sc,ax=ax,label='Model count');ax.set_title('Figure 8: 75th-percentile consensus')
    fig.tight_layout();fig.savefig(out/'Figure_08_SYNTHETIC.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(1,3,figsize=(14,4))
    ax[0].scatter(raw,msm,s=2,alpha=.15);ax[0].set(xlabel='EBM-Raw score',ylabel='MSM-EBM score')
    ax[1].scatter(percentile_rank(raw),percentile_rank(msm),s=2,alpha=.15);ax[1].set(xlabel='EBM-Raw rank',ylabel='MSM-EBM rank')
    ax[2].hist(msm-raw,bins=45);ax[2].set(xlabel='Score difference',ylabel='Cell count')
    fig.tight_layout();fig.savefig(out/'Figure_09_SYNTHETIC.png',dpi=160);plt.close(fig)
    top=targets(full_df,msm)[:10]; lookup={cid:t['rank'] for t in top for cid in t['cell_ids']}
    fig,ax=plt.subplots(1,2,figsize=(12,5));ax[0].scatter(full_df.x,full_df.y,c=msm,s=5,cmap='viridis')
    chosen=full_df[full_df.cell_id.isin(lookup)]
    ax[0].scatter(chosen.x,chosen.y,facecolors='none',edgecolors='red',s=20);ax[0].set_title('Top-ranked target footprints')
    ax[1].scatter([t['rank'] for t in top],[t['mean_score'] for t in top],s=[20+2*t['area_km2'] for t in top]);ax[1].set(xlabel='Target rank',ylabel='Mean score')
    fig.tight_layout();fig.savefig(out/'Figure_13_SYNTHETIC.png',dpi=160);plt.close(fig)


def save_ebm_interpretation(model, labeled_X, out):
    imp=importance(model,labeled_X)
    imp.to_csv(out/'Figure_11_main_effect_importance_SYNTHETIC.csv',index=False)
    fig,ax=plt.subplots(figsize=(9,5));ax.barh(imp.feature[::-1],imp.mean_abs_main_effect_log_odds[::-1]);ax.set_xlabel('Mean absolute additive contribution (log-odds)')
    fig.tight_layout();fig.savefig(out/'Figure_11_SYNTHETIC.png',dpi=160);plt.close(fig)
    shapes=shape_functions(model)
    fig,axs=plt.subplots(3,4,figsize=(14,9))
    for ax,d in zip(axs.flat,shapes):
        xs=np.asarray(d['names']);ys=np.asarray(d['scores'])
        if len(xs)!=len(ys):
            xs=np.arange(len(ys))
        ax.plot(xs,ys)
        # Deliberately do not plot model-derived bands here: the precise
        # semantics of manuscript Figure 10 shading are not independently verified.
        # The synthetic example displays only the central fitted main effects.
        ax.set_title(d['feature'],fontsize=9)
    fig.tight_layout();fig.savefig(out/'Figure_10_SYNTHETIC.png',dpi=160);plt.close(fig)


def save_enrichment(full_df,scores,ids,out):
    from .analysis import descriptive_enrichment
    enrich=full_df.cell_id.isin(ids).to_numpy(); rank=percentile_rank(scores)
    fig,ax=plt.subplots(1,2,figsize=(11,4))
    ax[0].hist(rank[enrich],bins=np.arange(0,110,10));ax[0].set_title('Occurrence-proximity cells by percentile decile')
    fractions=np.linspace(.01,1,100); cap=[np.mean(rank[enrich]>=100*(1-f)) for f in fractions]
    ax[1].plot(fractions,cap,label='Descriptive capture');ax[1].plot([0,1],[0,1],'--',label='Area-proportional expectation');ax[1].legend();ax[1].set(xlabel='Top-ranked area fraction',ylabel='Capture fraction')
    fig.tight_layout();fig.savefig(out/'Figure_12_SYNTHETIC.png',dpi=160);plt.close(fig)
