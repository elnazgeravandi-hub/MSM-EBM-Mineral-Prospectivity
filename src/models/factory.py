from . import logistic, ebm_raw, catboost_raw, msm_ebm
from ..schema import MODEL_NAMES

def create(name, cfg, seed):
    if name==MODEL_NAMES[0]: return logistic.create(cfg['logistic'],seed)
    if name==MODEL_NAMES[1]: return ebm_raw.create(cfg['ebm'],seed)
    if name==MODEL_NAMES[2]: return catboost_raw.create(cfg['catboost'],seed)
    if name==MODEL_NAMES[3]: return msm_ebm.create(cfg['ebm'],seed)
    raise ValueError(name)
