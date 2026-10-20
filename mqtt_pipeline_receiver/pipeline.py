# --- pipeline.py ---
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from config import settings

class AnomalyPipeline:
    def __init__(self):
        self.pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("iforest", IsolationForest(contamination=0.25, random_state=42))
        ])
        self.trained = False

    def predict_batch(self, data: np.ndarray) -> np.ndarray:
        if not self.trained:
            preds = self.pipeline.fit_predict(data)
            self.trained = True
        else:
            preds = self.pipeline.predict(data)
        return preds