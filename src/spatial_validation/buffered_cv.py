import numpy as np
from scipy.spatial import cKDTree

def fold_ids(x, y, block_m=6000, n_folds=5):
    # Paper Eq. 5-6: origin offset 3000 m (not the minimum dataset coordinate)
    bc=np.floor((np.asarray(x,dtype=float)-3000)/block_m).astype(np.int64)
    br=np.floor((np.asarray(y,dtype=float)-3000)/block_m).astype(np.int64)
    return (bc+2*br)%n_folds

def partitions(df, block_m=6000, buffer_m=900, n_folds=5, occurrence_exclusion=False):
    xy=df[['x','y']].to_numpy(dtype=float)
    y=df.label.to_numpy()
    folds=fold_ids(xy[:,0],xy[:,1],block_m,n_folds)
    for k in range(n_folds):
        v=np.flatnonzero(folds==k)
        c=np.flatnonzero(folds!=k)
        if not len(v) or not len(c): raise ValueError('empty fold; increase synthetic grid extent')
        distances=cKDTree(xy[v]).query(xy[c], k=1)[0]
        tr=c[distances>buffer_m] # <= buffer excluded
        if occurrence_exclusion:
            if 'occurrence_id' not in df: raise ValueError('need occurrence_id')
            ids=set(df.iloc[v].loc[df.iloc[v].label==1,'occurrence_id'].tolist())
            ids.discard(-1)
            tr=np.asarray([i for i in tr if not (y[i]==1 and df.iloc[i].occurrence_id in ids)], dtype=int)
        if len(np.unique(y[v]))!=2 or len(np.unique(y[tr]))!=2:
            raise ValueError('Both classes required in train and validation folds')
        mindist=float(cKDTree(xy[v]).query(xy[tr],k=1)[0].min())
        assert mindist>buffer_m-1e-9
        yield k,tr,v,dict(fold=k+1,block_m=block_m,buffer_m=buffer_m,
            positive_validation=int(y[v].sum()),background_validation=int(len(v)-y[v].sum()),
            positive_train=int(y[tr].sum()),background_train=int(len(tr)-y[tr].sum()),
            excluded_train=int(len(c)-len(tr)),min_distance_m=mindist)
