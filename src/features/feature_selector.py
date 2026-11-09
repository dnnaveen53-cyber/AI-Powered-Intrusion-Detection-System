from __future__ import annotations

import numpy as np
from sklearn.feature_selection import SelectKBest, mutual_info_classif


class IntrusionFeatureSelector:
    def __init__(self, k: int | None = None) -> None:
        self.k = k
        self.selector = None

    def fit(self, features: np.ndarray, labels: np.ndarray) -> "IntrusionFeatureSelector":
        if self.k is None:
            self.k = min(30, features.shape[1])
        self.selector = SelectKBest(score_func=mutual_info_classif, k=self.k)
        self.selector.fit(features, labels)
        return self

    def transform(self, features: np.ndarray) -> np.ndarray:
        if self.selector is None:
            raise ValueError("Feature selector has not been fitted yet.")
        return self.selector.transform(features)

    def fit_transform(self, features: np.ndarray, labels: np.ndarray) -> np.ndarray:
        return self.fit(features, labels).transform(features)
