import numpy as np
from src.synthetic import create
from src.spatial import partitions,fold_ids
from src.fuzzy import small,mslarge
from src.mapping import percentile_rank,targets

def test_membership():
    assert small(0)==1
    assert small(1500)==.5
    assert np.isclose(mslarge(np.array([0.,1.,2.]),mean=1,std=1)[2],.5)

def test_spatial_buffer_and_same_folds():
    df=create(nx=36,ny=30)
    parts=list(partitions(df,6000,900))
    assert len(parts)==5
    assert set(np.concatenate([v for _,_,v,_ in parts]))==set(range(len(df)))
    assert all(meta['min_distance_m']>900 for _,_,_,meta in parts)

def test_targets():
    df=create(nx=36,ny=30)
    t=targets(df,df.granitoid.to_numpy())
    assert t and t[0]['rank']==1
    assert all(v['n_cells']>=1 for v in t)
