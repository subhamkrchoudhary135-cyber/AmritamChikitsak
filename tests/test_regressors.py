"""Tests for regression forecasters and Conformal Prediction intervals."""

import numpy as np
from src.ml.regressors import (
    ConformalBiomarkerForecaster,
    MultiTargetHealthForecaster,
    get_base_regressor,
)


def test_regressor_factory():
    for name in ["ridge", "lasso", "svr", "knn", "xgboost"]:
        reg = get_base_regressor(name)
        assert reg is not None


def test_conformal_biomarker_forecaster():
    np.random.seed(42)
    X = np.random.randn(100, 5)
    y = 100.0 + 2.5 * X[:, 0] - 1.2 * X[:, 1] + np.random.normal(0, 1.0, 100)

    forecaster = ConformalBiomarkerForecaster(
        "glucose_6m", base_model_name="ridge", coverage_alpha=0.10
    )
    forecaster.fit(X, y)

    preds, lower, upper = forecaster.predict(X[:5])
    assert len(preds) == 5
    assert (lower <= preds).all()
    assert (preds <= upper).all()
    assert forecaster.conformal_margin > 0.0


def test_multi_target_forecaster():
    np.random.seed(42)
    X = np.random.randn(80, 8)
    y_dict = {
        "target_glucose_6m": 100.0 + np.random.randn(80),
        "target_sbp_6m": 125.0 + np.random.randn(80),
        "target_continuous_risk": 35.0 + np.random.randn(80),
    }

    mf = MultiTargetHealthForecaster()
    mf.fit(X, y_dict)

    res = mf.forecast(X[:1])
    assert "forecasted_glucose_6m" in res
    assert "forecasted_sbp_6m" in res
    assert "continuous_risk_score" in res
    assert len(res["glucose_interval_6m"]) == 2
    assert res["glucose_interval_6m"][0] <= res["glucose_interval_6m"][1]
