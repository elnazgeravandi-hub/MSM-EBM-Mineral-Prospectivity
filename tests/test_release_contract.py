import numpy as np
from src.demo_data import make_demo
from src.analysis import require_no_enrichment_overlap
from src.mapping import percentile_rank,redistribution,targets
from src.figures_extra import save_spatial_diagnostics,save_enrichment
from src.fuzzy import small


def test_synthetic_grid_is_separate_and_unlabeled():
    labeled,grid,ids=make_demo(42,True)
    assert len(labeled)<len(grid)
    assert 'label' not in grid and 'occurrence_id' not in grid
    assert require_no_enrichment_overlap(labeled,ids) is None


def test_grid_predicted_positions_and_target_ranking():
    _,grid,_=make_demo(42,True)
    p=grid.granitoid.to_numpy()
    assert len(percentile_rank(p))==len(grid)
    assert all(t['rank']==i+1 for i,t in enumerate(targets(grid,p)))


def test_extra_plots_smoke(tmp_path):
    _,grid,ids=make_demo(42,True)
    p=grid.granitoid.to_numpy()
    pred={'Logistic Regression':p,'EBM-Raw':p*.8,'CatBoost-Raw':p*.9,'MSM-EBM':p}
    save_spatial_diagnostics(grid,pred,tmp_path)
    save_enrichment(grid,p,ids,tmp_path)
    for k in (7,8,9,12,13):
        assert (tmp_path/f'Figure_{k:02d}_SYNTHETIC.png').stat().st_size>1000


def test_percentile_delta_zero_identical_scores():
    a=np.linspace(.1,.9,100)
    assert np.all(redistribution(a,a).delta_rank==0)
