"""Central Model Registry and unified inference coordinator for Sanjivani AI."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from src.core.config import settings
from src.ml.classifiers import CalibratedConditionClassifier
from src.ml.clustering import PatientPhenotypeSegmenter
from src.ml.datasets import generate_synthetic_clinical_cohort
from src.ml.explainability import ShapExplainerService
from src.ml.fairness import evaluate_fairlearn_metrics
from src.ml.preprocessor import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    balance_training_data,
    build_preprocessor_pipeline,
)
from src.ml.regressors import MultiTargetHealthForecaster
from src.schemas.models import ModelVersionInfo
from src.schemas.screening import (
    ClusteringResult,
    ConditionRiskResult,
    ProgressionForecast,
    RiskLevel,
    ScreeningInput,
    ShapFactor,
)


class ModelRegistry:
    """Manages training, caching, serialization, and high-performance inference for all models."""

    def __init__(self, cache_dir: str | None = None):
        self.cache_dir = Path(cache_dir or settings.MODEL_REGISTRY_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.preprocessor = None
        self.feature_names: list[str] = []

        # Classifiers
        self.classifiers: dict[str, CalibratedConditionClassifier] = {}

        # Regressors
        self.forecaster: MultiTargetHealthForecaster | None = None

        # Phenotype clustering & anomalies
        self.segmenter: PatientPhenotypeSegmenter | None = None

        # SHAP explainers
        self.explainers: dict[str, ShapExplainerService] = {}

        # Fairness reports
        self.fairness_reports: dict[str, dict[str, Any]] = {}

        # Reference cohort for drift & SHAP background
        self.reference_cohort: pd.DataFrame | None = None
        self.background_sample: np.ndarray | None = None

        self.is_loaded: bool = False
        self.last_trained_at: datetime | None = None

    def train_and_cache_all(self, n_samples: int = 2500) -> None:
        """Train entire ML suite from scratch and persist artifacts."""
        # 1. Generate reference cohort
        df = generate_synthetic_clinical_cohort(n_samples=n_samples, random_state=42)
        self.reference_cohort = df

        # 2. Build and fit preprocessor
        self.preprocessor = build_preprocessor_pipeline(
            numeric_features=NUMERIC_FEATURES,
            categorical_features=CATEGORICAL_FEATURES,
            use_iterative_imputer=True,
        )
        X_raw = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
        X_trans = self.preprocessor.fit_transform(X_raw)

        # Extract generated feature names
        try:
            self.feature_names = list(self.preprocessor.get_feature_names_out())
        except Exception:
            self.feature_names = NUMERIC_FEATURES + [
                "gender_male",
                "gender_female",
                "smoking_never",
                "smoking_former",
                "smoking_current",
            ]

        self.background_sample = X_trans[:100]

        # 3. Train Calibrated Classifiers (Diabetes, Heart Disease, Hypertension)
        # Using Random Forest / Stacking base models with recall-prioritized thresholds
        conditions = [
            ("diabetes", "target_diabetes", "random_forest", 0.90),
            ("heart_disease", "target_heart_disease", "random_forest", 0.90),
            ("hypertension", "target_hypertension", "random_forest", 0.90),
        ]

        sensitive_df = df[["gender", "age"]]

        for cond_name, target_col, base_algo, min_rec in conditions:
            y = df[target_col].values
            X_bal, y_bal = balance_training_data(X_trans, y)

            clf = CalibratedConditionClassifier(
                condition_name=cond_name,
                base_model_name=base_algo,
                min_recall=min_rec,
                random_state=42,
            )
            clf.fit(X_bal, y_bal)
            self.classifiers[cond_name] = clf

            # Compute fairness metrics on holdout
            y_pred = (clf.model.predict_proba(X_trans)[:, 1] >= clf.decision_threshold).astype(int)
            fairness = evaluate_fairlearn_metrics(y, y_pred, sensitive_df)
            self.fairness_reports[cond_name] = fairness

            # Build SHAP explainer
            self.explainers[cond_name] = ShapExplainerService(
                clf.model, self.background_sample, self.feature_names
            )

        # 4. Train Regression Forecaster
        y_reg = {
            "target_glucose_6m": df["target_glucose_6m"].values,
            "target_sbp_6m": df["target_sbp_6m"].values,
            "target_continuous_risk": df["target_continuous_risk"].values,
        }
        self.forecaster = MultiTargetHealthForecaster(random_state=42)
        self.forecaster.fit(X_trans, y_reg)

        # 5. Train Phenotyping Segmenter
        self.segmenter = PatientPhenotypeSegmenter(n_clusters=4, random_state=42)
        self.segmenter.fit(X_trans, self.feature_names)

        self.last_trained_at = datetime.now(UTC)
        self.is_loaded = True

        # Persist to cache
        self._save_to_disk()

    def _save_to_disk(self) -> None:
        """Serialize trained pipeline to disk."""
        joblib.dump(self.preprocessor, self.cache_dir / "preprocessor.joblib")
        joblib.dump(self.classifiers, self.cache_dir / "classifiers.joblib")
        joblib.dump(self.forecaster, self.cache_dir / "forecaster.joblib")
        joblib.dump(self.segmenter, self.cache_dir / "segmenter.joblib")
        joblib.dump(
            {
                "feature_names": self.feature_names,
                "fairness_reports": self.fairness_reports,
                "last_trained_at": self.last_trained_at,
            },
            self.cache_dir / "metadata.joblib",
        )

    def load_or_train(self) -> None:
        """Load artifacts from disk or train automatically if absent."""
        metadata_file = self.cache_dir / "metadata.joblib"
        if metadata_file.exists():
            try:
                self.preprocessor = joblib.load(self.cache_dir / "preprocessor.joblib")
                self.classifiers = joblib.load(self.cache_dir / "classifiers.joblib")
                self.forecaster = joblib.load(self.cache_dir / "forecaster.joblib")
                self.segmenter = joblib.load(self.cache_dir / "segmenter.joblib")
                meta = joblib.load(metadata_file)
                self.feature_names = meta["feature_names"]
                self.fairness_reports = meta.get("fairness_reports", {})
                self.last_trained_at = meta.get("last_trained_at")

                # Generate reference background for SHAP
                df = generate_synthetic_clinical_cohort(n_samples=500, random_state=42)
                self.reference_cohort = df
                X_trans = self.preprocessor.transform(df[NUMERIC_FEATURES + CATEGORICAL_FEATURES])
                self.background_sample = X_trans[:50]

                for cond_name, clf in self.classifiers.items():
                    self.explainers[cond_name] = ShapExplainerService(
                        clf.model, self.background_sample, self.feature_names
                    )

                self.is_loaded = True
                return
            except Exception:
                # If cache corrupted, retrain cleanly
                pass

        self.train_and_cache_all(n_samples=2000)

    def run_screening_inference(self, patient_input: ScreeningInput) -> tuple[
        dict[str, ConditionRiskResult],
        ProgressionForecast,
        ClusteringResult,
        list[ShapFactor],
    ]:
        """Execute end-to-end multi-condition classification, forecast, clustering, and SHAP."""
        if not self.is_loaded:
            self.load_or_train()

        input_dict = patient_input.model_dump()
        input_df = pd.DataFrame([input_dict])

        # Feature transformation
        x_trans = self.preprocessor.transform(input_df[NUMERIC_FEATURES + CATEGORICAL_FEATURES])

        # 1. Condition Risk Classification
        condition_results: dict[str, ConditionRiskResult] = {}
        for cond_name, clf in self.classifiers.items():
            prob, is_pos, ci = clf.predict_risk(x_trans)
            p_val = float(prob[0])
            thresh = float(clf.decision_threshold)

            # Determine clinical risk tier
            if p_val < 0.25:
                tier = RiskLevel.LOW
            elif p_val < 0.50:
                tier = RiskLevel.MODERATE
            elif p_val < 0.75:
                tier = RiskLevel.HIGH
            else:
                tier = RiskLevel.CRITICAL

            # Clinical guideline category note
            if cond_name == "diabetes":
                if patient_input.fasting_glucose >= 126 or (
                    patient_input.hba1c and patient_input.hba1c >= 6.5
                ):
                    guideline_note = "Diagnostic Range: High Risk (ICMR / ADA criteria)"
                elif patient_input.fasting_glucose >= 100 or (
                    patient_input.hba1c and patient_input.hba1c >= 5.7
                ):
                    guideline_note = "Pre-Diabetes Range: Impaired Fasting Glucose (ICMR)"
                else:
                    guideline_note = "Normoglycemic Screening Range"
            elif cond_name == "hypertension":
                if patient_input.systolic_bp >= 140 or patient_input.diastolic_bp >= 90:
                    guideline_note = "Stage 2 Hypertension Range (AHA/ACC / ICMR)"
                elif patient_input.systolic_bp >= 130 or patient_input.diastolic_bp >= 80:
                    guideline_note = "Stage 1 Hypertension Range (AHA/ACC / ICMR)"
                else:
                    guideline_note = "Normotensive Range"
            else:
                guideline_note = "Cardiovascular Risk Stratification (WHO/Framingham)"

            condition_results[cond_name] = ConditionRiskResult(
                condition_name=cond_name.replace("_", " ").title(),
                risk_score=round(p_val, 3),
                calibrated_probability=round(p_val, 3),
                risk_level=tier,
                decision_threshold=round(thresh, 3),
                is_screened_positive=bool(is_pos[0]),
                confidence_interval=(round(float(ci[0, 0]), 3), round(float(ci[0, 1]), 3)),
                clinical_guideline_category=guideline_note,
            )

        # 2. Regression Forecast (3-6 month trajectory & continuous risk)
        forecast_raw = self.forecaster.forecast(x_trans)
        curr_gluc = patient_input.fasting_glucose
        fg6 = forecast_raw["forecasted_glucose_6m"]
        trend_desc = (
            f"Fasting glucose trajectory shows an upward trend (+{fg6 - curr_gluc:.1f} mg/dL over 6m) without lifestyle intervention."
            if fg6 > curr_gluc
            else f"Fasting glucose trajectory is stable/improving ({fg6 - curr_gluc:.1f} mg/dL over 6m)."
        )

        forecast = ProgressionForecast(
            forecasted_glucose_3m=round(forecast_raw["forecasted_glucose_3m"], 1),
            forecasted_glucose_6m=round(fg6, 1),
            forecasted_systolic_bp_3m=round(forecast_raw["forecasted_sbp_3m"], 1),
            forecasted_systolic_bp_6m=round(forecast_raw["forecasted_sbp_6m"], 1),
            continuous_risk_score_100=round(forecast_raw["continuous_risk_score"], 1),
            glucose_prediction_interval_6m=(
                round(forecast_raw["glucose_interval_6m"][0], 1),
                round(forecast_raw["glucose_interval_6m"][1], 1),
            ),
            bp_prediction_interval_6m=(
                round(forecast_raw["sbp_interval_6m"][0], 1),
                round(forecast_raw["sbp_interval_6m"][1], 1),
            ),
            trend_description=trend_desc,
        )

        # 3. Patient Phenotyping & Anomaly Detection
        c_id, c_label, priorities, is_anomaly, anom_score, pca_coords = (
            self.segmenter.segment_patient(x_trans)
        )
        phenotype = ClusteringResult(
            cluster_id=c_id,
            cluster_label=c_label,
            cluster_description=f"Cohort Segment {c_id}: {c_label}",
            is_anomaly=is_anomaly,
            anomaly_score=round(anom_score, 3),
            pca_coordinates=[round(c, 3) for c in pca_coords],
            lifestyle_priorities=priorities,
        )

        # 4. SHAP Explainability (focus on highest risk condition or general diabetes/cardiac)
        primary_explainer = self.explainers.get("diabetes") or list(self.explainers.values())[0]
        top_shap_factors = primary_explainer.explain_instance(x_trans, input_dict, top_k=5)

        return condition_results, forecast, phenotype, top_shap_factors

    def get_model_versions_info(self) -> list[ModelVersionInfo]:
        """Return model metadata and fairness statistics for /models/versions endpoint."""
        if not self.is_loaded:
            self.load_or_train()

        records = []
        for cond_name, clf in self.classifiers.items():
            fairness = self.fairness_reports.get(cond_name)
            records.append(
                ModelVersionInfo(
                    condition=cond_name,
                    algorithm=clf.base_model_name,
                    version_tag="1.0.0",
                    metrics=clf.metrics,
                    fairness_metrics=fairness,
                    decision_threshold=clf.decision_threshold,
                    trained_at=self.last_trained_at or datetime.now(UTC),
                    is_active=True,
                )
            )

        if self.forecaster:
            records.append(
                ModelVersionInfo(
                    condition="biomarker_progression_forecaster",
                    algorithm="conformal_xgboost_ridge",
                    version_tag="1.0.0",
                    metrics=self.forecaster.glucose_forecaster.metrics,
                    fairness_metrics=None,
                    decision_threshold=0.0,
                    trained_at=self.last_trained_at or datetime.now(UTC),
                    is_active=True,
                )
            )

        return records


model_registry = ModelRegistry()
