import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from scipy.stats import rankdata

def percentile_rank(prob):
    # Assumption documented: midranks 0-100. Confirm actual manuscript tie convention.
    return 100*rankdata(np.asarray(prob),method='average')/len(prob)

def classes(rank):
    return np.searchsorted([20,50,75,90],rank,side='right')

def redistribution(raw,msm):
    delta=percentile_rank(msm)-percentile_rank(raw)
    names=np.array(['strong suppression','moderate suppression','stable','moderate promotion','strong promotion'])
    return pd.DataFrame({'delta_p':np.asarray(msm)-np.asarray(raw),'delta_rank':delta,
        'category':names[np.digitize(delta,[-20,-5,5,20])]})

def targets(df, scores, top_fraction=.10, eps=1.5, min_samples=1,step=300):
    if not 0 < top_fraction < 1: raise ValueError("top_fraction must lie strictly between 0 and 1")
    if eps <= 0 or min_samples < 1: raise ValueError("invalid DBSCAN settings")
    if len(scores) != len(df): raise ValueError("score and grid lengths differ")
    ranks=percentile_rank(scores)
    picked=np.flatnonzero(ranks>=100*(1-top_fraction))
    grid=np.rint(df.iloc[picked][['x','y']].to_numpy()/step).astype(int)
    labels=DBSCAN(eps=eps,min_samples=min_samples,metric='euclidean').fit_predict(grid)
    members=[]
    for cluster in sorted(set(labels)-{-1}):
        ids=picked[labels==cluster]
        members.append({'cluster':int(cluster),'n_cells':int(len(ids)),
            'area_km2':len(ids)*step*step/1e6,'mean_score':float(np.mean(np.asarray(scores)[ids])),
            'max_score':float(np.max(np.asarray(scores)[ids])),'cell_ids':tuple(df.iloc[ids].cell_id.astype(int))})
    members.sort(key=lambda z:(-z['mean_score'],-z['n_cells'],-z['max_score'],z['cluster']))
    for i,z in enumerate(members): z['rank']=i+1
    return members

def jaccard(a,b):
    aa=set(a); bb=set(b)
    return len(aa&bb)/len(aa|bb) if aa|bb else 1.0
