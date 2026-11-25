import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve,precision_recall_curve
from .evaluation import calibration,capture_curve

def save_evaluation(df,out):
    for figure in (5,6):
        fig,axes=plt.subplots(1,3 if figure==5 else 2,figsize=(15 if figure==5 else 10,4))
        for name,g in df.groupby('model',sort=False):
            y=g.label.to_numpy();p=g.prob.to_numpy()
            if figure==5:
                f,t,_=roc_curve(y,p);axes[0].plot(f,t,label=name)
                pr,re,_=precision_recall_curve(y,p);axes[1].plot(re,pr,label=name)
                c=capture_curve(y,p);axes[2].plot(c.area_fraction,c.positive_capture,label=name)
            else:
                c=calibration(y,p);axes[0].plot(c.predicted,c.observed,marker='o',label=name)
                axes[1].bar(name,np.mean((y-p)**2))
        if figure==5:
            for ax,title in zip(axes,['ROC','Precision–Recall','Success-rate capture']):ax.set_title(title)
        else:
            axes[0].plot([0,1],[0,1],'--',c='gray');axes[0].set_title('Quantile reliability');axes[1].set_title('Brier score');axes[1].tick_params(axis='x',rotation=70)
        axes[0].legend(fontsize=7)
        fig.tight_layout();fig.savefig(out/f'Figure_{figure:02d}_SYNTHETIC.png',dpi=180);plt.close(fig)

def save_maps(predictions,df,out):
    models=list(predictions)
    fig,axs=plt.subplots(2,2,figsize=(11,8))
    for ax,name in zip(axs.flat,models):
        sc=ax.scatter(df.x,df.y,c=predictions[name],s=5,cmap='viridis',vmin=0,vmax=1);ax.set_title(name)
    fig.colorbar(sc,ax=list(axs.flat),shrink=.7)
    fig.savefig(out/'Figure_04_SYNTHETIC.png',dpi=150);plt.close(fig)
