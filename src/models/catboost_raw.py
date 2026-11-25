from catboost import CatBoostClassifier

def create(cfg, seed):
    return CatBoostClassifier(**cfg, random_seed=seed,allow_writing_files=False)
