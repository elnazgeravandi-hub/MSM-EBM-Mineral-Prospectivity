def create(cfg, seed):
    from interpret.glassbox import ExplainableBoostingClassifier
    return ExplainableBoostingClassifier(**cfg, monotone_constraints=[1]*12, random_state=seed)
