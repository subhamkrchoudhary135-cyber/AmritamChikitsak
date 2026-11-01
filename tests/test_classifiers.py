"""Tests for classifiers, stacking ensembles, calibration, and threshold selection."""

import numpy as np
from src.ml.classifiers import (
    CalibratedConditionClassifier,
    find_recall_prioritized_threshold,
    get_base_classifier,
)


def test_classifier_factory():
    for name in [
        "logistic_regression",
        "knn",
        "svm",
        "random_forest",
        "xgboost",
        "lightgbm",
        "catboost",
    ]:
        clf = get_base_classifier(name)
        assert clf is not None


def test_recall_prioritized_threshold_selection():
    y_true = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    # Calibrated probabilities
    y_probs = np.array([0.1, 0.2, 0.25, 0.3, 0.45, 0.6, 0.75, 0.9])

    thresh = find_recall_prioritized_threshold(y_true, y_probs, min_recall=0.90)
    assert 0.15 <= thresh <= 0.50

    # Predictions at threshold should achieve high recall
    preds = (y_probs >= thresh).astype(int)
    recall = np.sum((preds == 1) & (y_true == 1)) / np.sum(y_true == 1)
    assert recall >= 0.75


def test_calibrated_condition_classifier():
    np.random.seed(42)
    X = np.random.randn(80, 6)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)

    clf = CalibratedConditionClassifier(
        "diabetes", base_model_name="random_forest", min_recall=0.85
    )
    clf.fit(X, y)

    probs, screened, ci = clf.predict_risk(X[:5])
    assert len(probs) == 5
    assert (probs >= 0.0).all() and (probs <= 1.0).all()
    assert len(screened) == 5
    assert ci.shape == (5, 2)
