import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score,average_precision_score,matthews_corrcoef,balanced_accuracy_score,recall_score,brier_score_loss

def metrics(y,p,threshold=.5):
    y=np.asarray(y);p=np.asarray(p)
    if len(np.unique(y))<2: raise ValueError('Both classes required for AUROC')
    h=p>=threshold
    return dict(AUROC=roc_auc_score(y,p),AP=average_precision_score(y,p),
      MCC=matthews_corrcoef(y,h),balanced_accuracy=balanced_accuracy_score(y,h),
      recall=recall_score(y,h),Brier=brier_score_loss(y,p))

def calibration(y,p,bins=10):
    df=pd.DataFrame({'label':y,'prob':p})
    df['bin']=pd.qcut(df['prob'].rank(method='first'),q=bins,labels=False,duplicates='drop')
    return df.groupby('bin').agg(predicted=('prob','mean'),observed=('label','mean'),count=('label','size')).reset_index()

def capture_curve(y,score):
    order=np.argsort(-np.asarray(score),kind='stable'); arr=np.asarray(y)[order]
    return pd.DataFrame({'area_fraction':np.arange(1,len(y)+1)/len(y),
        'positive_capture':np.cumsum(arr)/arr.sum()})
