import os
import pickle
import numpy as np

def load_model(path: str):
    """
    Loads a pickled sklearn model.
    If file doesn't exist yet (first deploy), we build a dummy model
    that outputs a fixed score so CD doesn't fail.
    """
    if os.path.exists(path):
        with open(path, "rb") as f:
            model = pickle.load(f)
        print(f"[model] Loaded trained model from {path}")
        return model

    # fallback dummy "model"
    class DummyModel:
        def predict_proba(self, X):
            # X is list of [views, purchases]
            # Just return some heuristic as [p0, p1]
            probs = []
            for views, purchases in X:
                # heuristic: more purchases -> higher chance = 1
                score = 0.2 + 0.15 * purchases + 0.01 * views
                # clamp 0-0.99
                score = max(0.01, min(0.99, score))
                probs.append([1 - score, score])
            return np.array(probs)

    print("[model] Using DummyModel (no real model.pkl found)")
    return DummyModel()


def predict_proba_wrapper(model, X):
    """
    Returns the positive class probability for a single row.
    """
    proba = model.predict_proba(X)  # shape (n, 2)
    # return probability of class=1
    return float(proba[0][1])
