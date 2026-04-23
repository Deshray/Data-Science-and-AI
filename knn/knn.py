"""
knn.py — k-Nearest Neighbours Classifier: NumPy implementation from scratch

No sklearn used for the core algorithm. Supports:
  - Euclidean, Manhattan, Minkowski distance metrics
  - Plurality voting (handles ties by choosing lower label index)
  - k-fold cross-validation for optimal k selection
  - Accuracy, precision, recall, F1 (macro-averaged)
  - Decision boundary computation for 2D feature sets
"""

from __future__ import annotations
import numpy as np


class KNNClassifier:
    """
    k-Nearest Neighbours classifier implemented from scratch with NumPy.

    Distance computation is vectorised — no Python loops over training points.
    Prediction for a single query: O(n·d) distance matrix row + O(n log n) sort.
    """

    METRICS = ("euclidean", "manhattan", "minkowski")

    def __init__(self, k: int = 3, metric: str = "euclidean", p: float = 3.0):
        """
        Parameters
        ----------
        k      : number of neighbours
        metric : "euclidean", "manhattan", or "minkowski"
        p      : exponent for Minkowski distance (ignored for other metrics)
        """
        if k <= 0:
            raise ValueError(f"k must be positive, got {k}")
        if metric not in self.METRICS:
            raise ValueError(f"metric must be one of {self.METRICS}")

        self.k      = k
        self.metric = metric
        self.p      = p
        self._X: np.ndarray | None = None
        self._y: np.ndarray | None = None

    # ── Training ──────────────────────────────────────────────────────────────

    def fit(self, X: np.ndarray, y: np.ndarray) -> "KNNClassifier":
        """
        Store training data (lazy — no computation at fit time).

        Parameters
        ----------
        X : (n_train, n_features) float array
        y : (n_train,) integer label array
        """
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        if X.ndim != 2:
            raise ValueError("X must be 2D")
        if len(X) != len(y):
            raise ValueError("X and y must have the same length")
        self._X = X
        self._y = y
        return self

    # ── Distance ─────────────────────────────────────────────────────────────

    def _distances(self, query: np.ndarray) -> np.ndarray:
        """
        Vectorised distance from `query` to all training points.
        query : (n_features,) — always 1D when called from predict loop
        Returns : (n_train,)
        """
        diff = self._X - query   # broadcast (n_train, d) - (d,) = (n_train, d)

        if self.metric == "euclidean":
            return np.sqrt((diff ** 2).sum(axis=1))
        elif self.metric == "manhattan":
            return np.abs(diff).sum(axis=1)
        else:   # minkowski
            return (np.abs(diff) ** self.p).sum(axis=1) ** (1 / self.p)

    # ── Prediction ────────────────────────────────────────────────────────────

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels for each row of X.

        For each query:
          1. Compute distances to all training points  O(n·d)
          2. Partial-sort to find k nearest            O(n + k log k)
          3. Majority vote                              O(k)

        Returns (n_test,) integer label array.
        """
        self._check_fitted()
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X[None, :]

        eff_k = min(self.k, len(self._X))
        preds = np.empty(len(X), dtype=self._y.dtype)

        for i, query in enumerate(X):
            dists = self._distances(query)           # (n_train,)
            nn_idx = np.argpartition(dists, eff_k - 1)[:eff_k]
            nn_labels = self._y[nn_idx]
            preds[i] = self._majority_vote(nn_labels)

        return preds

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Return class vote fractions for each query.
        Shape: (n_test, n_classes) where classes are sorted unique labels.
        """
        self._check_fitted()
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X[None, :]

        classes   = np.unique(self._y)
        eff_k     = min(self.k, len(self._X))
        proba     = np.zeros((len(X), len(classes)))

        for i, query in enumerate(X):
            dists   = self._distances(query)
            nn_idx  = np.argpartition(dists, eff_k - 1)[:eff_k]
            nn_lbl  = self._y[nn_idx]
            for j, cls in enumerate(classes):
                proba[i, j] = np.sum(nn_lbl == cls) / eff_k

        return proba

    # ── Evaluation ────────────────────────────────────────────────────────────

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Accuracy on (X, y)."""
        return float(np.mean(self.predict(X) == np.asarray(y)))

    def classification_report(self, X: np.ndarray,
                                y: np.ndarray) -> dict:
        """
        Macro-averaged precision, recall, F1, and per-class breakdown.
        """
        y_true = np.asarray(y)
        y_pred = self.predict(X)
        classes = np.unique(y_true)

        acc = float(np.mean(y_pred == y_true))
        per_class = {}
        precisions, recalls, f1s = [], [], []

        for cls in classes:
            tp = int(np.sum((y_pred == cls) & (y_true == cls)))
            fp = int(np.sum((y_pred == cls) & (y_true != cls)))
            fn = int(np.sum((y_pred != cls) & (y_true == cls)))

            prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            rec  = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1   = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0

            per_class[int(cls)] = {"precision": round(prec, 4),
                                    "recall":    round(rec,  4),
                                    "f1":        round(f1,   4),
                                    "support":   int(np.sum(y_true == cls))}
            precisions.append(prec); recalls.append(rec); f1s.append(f1)

        return {
            "accuracy":          round(acc, 4),
            "macro_precision":   round(float(np.mean(precisions)), 4),
            "macro_recall":      round(float(np.mean(recalls)), 4),
            "macro_f1":          round(float(np.mean(f1s)), 4),
            "per_class":         per_class,
        }

    # ── Cross-validation ──────────────────────────────────────────────────────

    @staticmethod
    def cross_val_accuracy(X: np.ndarray, y: np.ndarray,
                            k_neighbours: int,
                            n_folds: int = 5,
                            metric: str = "euclidean",
                            seed: int = 42) -> float:
        """
        Stratified k-fold cross-validation accuracy for a given k_neighbours.
        """
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        rng = np.random.default_rng(seed)

        # Stratified fold indices
        classes = np.unique(y)
        fold_ids = np.zeros(len(y), dtype=int)
        for cls in classes:
            idx = np.where(y == cls)[0]
            rng.shuffle(idx)
            for i, j in enumerate(idx):
                fold_ids[j] = i % n_folds

        accs = []
        for fold in range(n_folds):
            val_mask   = fold_ids == fold
            train_mask = ~val_mask
            model = KNNClassifier(k=k_neighbours, metric=metric)
            model.fit(X[train_mask], y[train_mask])
            accs.append(model.score(X[val_mask], y[val_mask]))

        return float(np.mean(accs))

    @staticmethod
    def select_k(X: np.ndarray, y: np.ndarray,
                  k_range: range = range(1, 21),
                  n_folds: int = 5,
                  metric: str = "euclidean") -> dict:
        """
        Cross-validate over a range of k values and return the best.
        Returns dict mapping k → cv_accuracy, plus best_k and best_acc.
        """
        results = {}
        for k in k_range:
            if k > len(X) * (1 - 1 / n_folds):
                break
            acc = KNNClassifier.cross_val_accuracy(X, y, k,
                                                    n_folds=n_folds,
                                                    metric=metric)
            results[k] = round(acc, 4)

        best_k = max(results, key=results.get)
        return {"k_scores": results,
                "best_k": best_k,
                "best_acc": results[best_k]}

    # ── Decision boundary (2D only) ───────────────────────────────────────────

    def decision_boundary_grid(self, X: np.ndarray,
                                 resolution: int = 150) -> tuple:
        """
        Compute predicted class for a grid over the 2D feature space.
        Returns (xx, yy, Z) suitable for contour plotting.
        Only valid when X has exactly 2 features.
        """
        if X.shape[1] != 2:
            raise ValueError("Decision boundary requires exactly 2 features")

        margin = 0.5
        x_min, x_max = X[:, 0].min() - margin, X[:, 0].max() + margin
        y_min, y_max = X[:, 1].min() - margin, X[:, 1].max() + margin

        xx, yy = np.meshgrid(
            np.linspace(x_min, x_max, resolution),
            np.linspace(y_min, y_max, resolution),
        )
        grid   = np.c_[xx.ravel(), yy.ravel()]
        Z      = self.predict(grid).reshape(xx.shape)
        return xx, yy, Z

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _check_fitted(self):
        if self._X is None:
            raise RuntimeError("Call fit() before predict()")

    @staticmethod
    def _majority_vote(labels: np.ndarray) -> int:
        """Return the most common label. Ties broken by smallest label."""
        values, counts = np.unique(labels, return_counts=True)
        return int(values[np.argmax(counts)])

    def __repr__(self) -> str:
        return f"KNNClassifier(k={self.k}, metric='{self.metric}')"
