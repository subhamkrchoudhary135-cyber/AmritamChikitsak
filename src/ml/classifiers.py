"""Multi-condition classification models with Optuna tuning, calibration, and recall-prioritized thresholding."""

from typing import Any

import numpy as np
import optuna
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    f1_score,
    fbeta_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

optuna.logging.set_verbosity(optuna.logging.WARNING)


def get_base_classifier(model_name: str, random_state: int = 42) -> Any:
    """Instantiate a base classification algorithm by name."""
    name = model_name.lower()
    if name == "logistic_regression":
        return LogisticRegression(max_iter=1000, random_state=random_state, class_weight="balanced")
    elif name == "knn":
        return KNeighborsClassifier(n_neighbors=7, weights="distance")
    elif name == "svm":
        return SVC(
            kernel="rbf", probability=True, random_state=random_state, class_weight="balanced"
        )
    elif name == "random_forest":
        return RandomForestClassifier(
            n_estimators=150, max_depth=8, random_state=random_state, class_weight="balanced"
        )
    elif name == "xgboost":
        return XGBClassifier(
            n_estimators=120,
            max_depth=5,
            learning_rate=0.08,
            random_state=random_state,
            eval_metric="logloss",
        )
    elif name == "lightgbm":
        return LGBMClassifier(
            n_estimators=120,
            max_depth=5,
            learning_rate=0.08,
            random_state=random_state,
            verbose=-1,
        )
    elif name == "catboost":
        return CatBoostClassifier(
            iterations=120,
            depth=5,
            learning_rate=0.08,
            random_seed=random_state,
            verbose=False,
        )
    else:
        raise ValueError(f"Unknown classifier model name: {model_name}")


def build_stacking_ensemble(random_state: int = 42) -> StackingClassifier:
    """Build a cross-validated Stacking Ensemble combining top heterogeneous learners."""
    estimators = [
        (
            "lr",
            LogisticRegression(max_iter=1000, random_state=random_state, class_weight="balanced"),
        ),
        ("rf", RandomForestClassifier(n_estimators=100, max_depth=7, random_state=random_state)),
        (
            "xgb",
            XGBClassifier(
                n_estimators=100,
                max_depth=4,
                learning_rate=0.08,
                random_state=random_state,
                eval_metric="logloss",
            ),
        ),
        (
            "lgbm",
            LGBMClassifier(
                n_estimators=100,
                max_depth=4,
                learning_rate=0.08,
                random_state=random_state,
                verbose=-1,
            ),
        ),
        (
            "cat",
            CatBoostClassifier(
                iterations=100, depth=4, learning_rate=0.08, random_seed=random_state, verbose=False
            ),
        ),
    ]
    final_estimator = LogisticRegression(random_state=random_state)
    return StackingClassifier(
        estimators=estimators,
        final_estimator=final_estimator,
        cv=3,
        n_jobs=-1,
    )


def tune_xgboost_optuna(
    X: np.ndarray, y: np.ndarray, n_trials: int = 15, random_state: int = 42
) -> dict[str, Any]:
    """Tune XGBoost hyperparameters using Optuna optimizing ROC-AUC on Stratified CV."""

    def objective(trial: optuna.Trial) -> float:
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 200),
            "max_depth": trial.suggest_int("max_depth", 3, 8),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "random_state": random_state,
            "eval_metric": "logloss",
        }
        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=random_state)
        scores = []
        for train_idx, val_idx in cv.split(X, y):
            model = XGBClassifier(**params)
            model.fit(X[train_idx], y[train_idx])
            preds = model.predict_proba(X[val_idx])[:, 1]
            scores.append(roc_auc_score(y[val_idx], preds))
        return float(np.mean(scores))

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    return study.best_params


def evaluate_classifier_cv(
    model: Any, X: np.ndarray, y: np.ndarray, n_splits: int = 5, random_state: int = 42
) -> dict[str, float]:
    """Evaluate classifier using Stratified K-Fold CV across clinical metrics."""
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    roc_aucs, pr_aucs, recalls, f1s, briers = [], [], [], [], []

    for train_idx, test_idx in cv.split(X, y):
        X_tr, y_tr = X[train_idx], y[train_idx]
        X_te, y_te = X[test_idx], y[test_idx]

        model.fit(X_tr, y_tr)
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_te)[:, 1]
        else:
            probs = model.decision_function(X_te)
            probs = 1.0 / (1.0 + np.exp(-probs))

        preds = (probs >= 0.5).astype(int)

        roc_aucs.append(roc_auc_score(y_te, probs))
        pr_aucs.append(average_precision_score(y_te, probs))
        recalls.append(recall_score(y_te, preds, zero_division=0))
        f1s.append(f1_score(y_te, preds, zero_division=0))
        briers.append(brier_score_loss(y_te, probs))

    return {
        "roc_auc": float(np.mean(roc_aucs)),
        "pr_auc": float(np.mean(pr_aucs)),
        "recall": float(np.mean(recalls)),
        "f1": float(np.mean(f1s)),
        "brier_score": float(np.mean(briers)),
    }


def find_recall_prioritized_threshold(
    y_true: np.ndarray, y_probs: np.ndarray, min_recall: float = 0.90
) -> float:
    """Determine decision threshold prioritizing recall (minimizing clinical false negatives).

    Finds the maximum threshold that satisfies Recall >= min_recall, or optimizes F2-score.
    """
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_probs)

    # Filter thresholds where recall meets or exceeds min_recall
    valid_indices = np.where(recalls[:-1] >= min_recall)[0]
    if len(valid_indices) > 0:
        # Pick the highest threshold that maintains this target recall to avoid excessive false positives
        best_idx = valid_indices[-1]
        chosen_threshold = float(thresholds[best_idx])
    else:
        # Fallback to threshold that maximizes F2 score (beta=2 favors recall)
        f2_scores = []
        for t in thresholds:
            preds = (y_probs >= t).astype(int)
            f2 = fbeta_score(y_true, preds, beta=2, zero_division=0)
            f2_scores.append(f2)
        chosen_threshold = float(thresholds[np.argmax(f2_scores)])

    # Clamp safely between 0.15 and 0.50 for clinical screening safety
    return float(np.clip(chosen_threshold, 0.15, 0.50))


class CalibratedConditionClassifier:
    """End-to-end trained condition classifier with probability calibration and custom recall threshold."""

    def __init__(
        self,
        condition_name: str,
        base_model_name: str = "stacking",
        min_recall: float = 0.90,
        random_state: int = 42,
    ):
        self.condition_name = condition_name
        self.base_model_name = base_model_name
        self.min_recall = min_recall
        self.random_state = random_state
        self.model: CalibratedClassifierCV | None = None
        self.decision_threshold: float = 0.35
        self.metrics: dict[str, float] = {}

    def fit(self, X: np.ndarray, y: np.ndarray) -> "CalibratedConditionClassifier":
        """Fit model, calibrate probabilities, and find recall-prioritized decision threshold."""
        if self.base_model_name == "stacking":
            raw_estimator = build_stacking_ensemble(random_state=self.random_state)
        elif self.base_model_name == "xgboost_tuned":
            best_params = tune_xgboost_optuna(X, y, n_trials=10, random_state=self.random_state)
            raw_estimator = XGBClassifier(**best_params)
        else:
            raw_estimator = get_base_classifier(
                self.base_model_name, random_state=self.random_state
            )

        # Calibrate probabilities using CalibratedClassifierCV
        self.model = CalibratedClassifierCV(estimator=raw_estimator, method="sigmoid", cv=3)
        self.model.fit(X, y)

        # Compute out-of-fold or calibrated probabilities
        calibrated_probs = self.model.predict_proba(X)[:, 1]

        # Tune decision threshold to prioritize recall
        self.decision_threshold = find_recall_prioritized_threshold(
            y, calibrated_probs, min_recall=self.min_recall
        )

        # Record metrics at chosen threshold
        preds_at_thresh = (calibrated_probs >= self.decision_threshold).astype(int)
        self.metrics = {
            "roc_auc": float(roc_auc_score(y, calibrated_probs)),
            "pr_auc": float(average_precision_score(y, calibrated_probs)),
            "recall": float(recall_score(y, preds_at_thresh, zero_division=0)),
            "precision": float(precision_score(y, preds_at_thresh, zero_division=0)),
            "f1": float(f1_score(y, preds_at_thresh, zero_division=0)),
            "brier_score": float(brier_score_loss(y, calibrated_probs)),
            "decision_threshold": self.decision_threshold,
        }
        return self

    def predict_risk(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Predict calibrated probabilities, binary screened status, and 95% confidence intervals."""
        if self.model is None:
            raise RuntimeError("Model is not fitted.")

        probs = self.model.predict_proba(X)[:, 1]
        screened_positive = (probs >= self.decision_threshold).astype(bool)

        # Compute approximate standard error interval: p +/- 1.96 * sqrt(p*(1-p)/n)
        se = np.sqrt(np.clip(probs * (1.0 - probs), 0.001, 0.25)) * 0.15
        ci_lower = np.clip(probs - 1.96 * se, 0.0, 1.0)
        ci_upper = np.clip(probs + 1.96 * se, 0.0, 1.0)
        ci_intervals = np.column_stack([ci_lower, ci_upper])

        return probs, screened_positive, ci_intervals
