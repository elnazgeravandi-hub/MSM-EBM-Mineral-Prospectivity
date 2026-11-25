"""L2 logistic baseline; scaler fitted within each training fold."""
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def create(cfg, seed):
    return make_pipeline(StandardScaler(), LogisticRegression(**cfg, random_state=seed))
