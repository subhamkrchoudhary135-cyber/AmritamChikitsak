"""Biomarker trajectory and continuous risk regressors with Conformal Prediction intervals."""

from typing import Any

import numpy as np
from sklearn.linear_model import Lasso, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor


def get_base_regressor(model_name: str, random_state: int = 42) -> Any:
    """Instantiate a regression algorithm by name."""
    name = model_name.lower()
    if name == "ridge":
        return Ridge(alpha=1.0, random_state=random_state)
    elif name == "lasso":
        return Lasso(alpha=0.1, random_state=random_state)
    elif name == "svr":
        return SVR(kernel="rbf", C=1.0, epsilon=0.1)
    elif name == "knn":
        return KNeighborsRegressor(n_neighbors=7, weights="distance")
    elif name == "xgboost":
        return XGBRegressor(
            n_estimators=120,
            max_depth=5,
            learning_rate=0.08,
            random_state=random_state,
        )
    else:
        raise ValueError(f"Unknown regressor model name: {model_name}")


class ConformalBiomarkerForecaster:
    """Biomarker regression forecaster with distribution-free Conformal Prediction intervals.

    Produces point estimates and rigorous $(1 - \\alpha)$ coverage prediction intervals:
    $[\\hat{y} - q_{1-\\alpha}, \\hat{y} + q_{1-\\alpha}]$.
    """

    def __init__(
        self,
        target_name: str,
        base_model_name: str = "xgboost",
        coverage_alpha: float = 0.10,  # 90% coverage
        random_state: int = 42,
    ):
        self.target_name = target_name
        self.base_model_name = base_model_name
        self.coverage_alpha = coverage_alpha
        self.random_state = random_state
        self.model: Any | None = None
        self.conformal_margin: float = 5.0
        self.metrics: dict[str, float] = {}

    def fit(self, X: np.ndarray, y: np.ndarray) -> "ConformalBiomarkerForecaster":
        """Fit model and calibrate conformal prediction residual threshold."""
        # Split into training (80%) and conformal calibration (20%)
        n = len(X)
        split_idx = int(n * 0.8)
        indices = np.random.RandomState(self.random_state).permutation(n)
        train_idx, calib_idx = indices[:split_idx], indices[split_idx:]

        X_train, y_train = X[train_idx], y[train_idx]
        X_calib, y_calib = X[calib_idx], y[calib_idx]

        self.model = get_base_regressor(self.base_model_name, random_state=self.random_state)
        self.model.fit(X_train, y_train)

        # Calibrate conformal prediction residuals on hold-out calibration set
        calib_preds = self.model.predict(X_calib)
        residuals = np.abs(y_calib - calib_preds)

        # Compute empirical quantile with finite-sample correction: ceil((n+1)(1-alpha))/n
        n_calib = len(calib_idx)
        level = np.ceil((n_calib + 1) * (1.0 - self.coverage_alpha)) / n_calib
        level = float(np.clip(level, 0.0, 1.0))
        self.conformal_margin = float(np.quantile(residuals, level))

        # Metrics on calibration split
        mae = mean_absolute_error(y_calib, calib_preds)
        rmse = np.sqrt(mean_squared_error(y_calib, calib_preds))
        r2 = r2_score(y_calib, calib_preds)

        self.metrics = {
            "mae": float(mae),
            "rmse": float(rmse),
            "r2": float(r2),
            "conformal_margin": self.conformal_margin,
            "coverage_confidence": 1.0 - self.coverage_alpha,
        }
        return self

    def predict(self, X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return point prediction, lower conformal bound, and upper conformal bound."""
        if self.model is None:
            raise RuntimeError("Model is not fitted.")

        preds = self.model.predict(X)
        lower_bounds = preds - self.conformal_margin
        upper_bounds = preds + self.conformal_margin
        return preds, lower_bounds, upper_bounds


class MultiTargetHealthForecaster:
    """Composite forecaster for Glucose trajectory, Systolic BP trajectory, and Continuous Risk."""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.glucose_forecaster = ConformalBiomarkerForecaster(
            "target_glucose_6m", "xgboost", random_state=random_state
        )
        self.sbp_forecaster = ConformalBiomarkerForecaster(
            "target_sbp_6m", "ridge", random_state=random_state
        )
        self.risk_forecaster = ConformalBiomarkerForecaster(
            "target_continuous_risk", "xgboost", random_state=random_state
        )

    def fit(self, X: np.ndarray, y_dict: dict[str, np.ndarray]) -> "MultiTargetHealthForecaster":
        """Fit all 3 forecasters."""
        self.glucose_forecaster.fit(X, y_dict["target_glucose_6m"])
        self.sbp_forecaster.fit(X, y_dict["target_sbp_6m"])
        self.risk_forecaster.fit(X, y_dict["target_continuous_risk"])
        return self

    def forecast(self, X: np.ndarray) -> dict[str, Any]:
        """Compute forecasts with conformal prediction intervals."""
        gluc_pred, gluc_low, gluc_high = self.glucose_forecaster.predict(X)
        sbp_pred, sbp_low, sbp_high = self.sbp_forecaster.predict(X)
        risk_pred, risk_low, risk_high = self.risk_forecaster.predict(X)

        return {
            "forecasted_glucose_6m": float(gluc_pred[0]),
            "forecasted_glucose_3m": float(
                gluc_pred[0] * 0.5 + X[0, 7] * 0.5 if X.shape[1] > 7 else gluc_pred[0]
            ),
            "glucose_interval_6m": (float(gluc_low[0]), float(gluc_high[0])),
            "forecasted_sbp_6m": float(sbp_pred[0]),
            "forecasted_sbp_3m": float(
                sbp_pred[0] * 0.5 + X[0, 4] * 0.5 if X.shape[1] > 4 else sbp_pred[0]
            ),
            "sbp_interval_6m": (float(sbp_low[0]), float(sbp_high[0])),
            "continuous_risk_score": float(np.clip(risk_pred[0], 0.0, 100.0)),
            "risk_interval": (
                float(np.clip(risk_low[0], 0.0, 100.0)),
                float(np.clip(risk_high[0], 0.0, 100.0)),
            ),
        }
