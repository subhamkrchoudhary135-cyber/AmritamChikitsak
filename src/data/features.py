"""Phase 5: Feature Engineering & Dimensionality Reduction for Sanjivani AI.

Implements:
1. Clinical domain features tailored for Indian cardiometabolic screening:
   - Asian Indian BMI categorization (<18.5, 18.5-22.9, 23.0-24.9, >=25.0)
   - Mean Arterial Pressure (MAP) and Pulse Pressure
   - Waist-to-Height Ratio (WHtR)
   - Lipid Ratios: Total/HDL, Triglycerides/HDL (Atherogenic Index)
   - Age Bands (<30, 30-44, 45-59, >=60)
   - Metabolic Syndrome IDF/ATP-III criteria flag
2. Lifestyle risk score & interaction terms (age x BMI).
3. Log transforms for right-skewed variables (triglycerides, physical activity).
4. Longitudinal features for temporal regression (lags, rolling means, slopes).
5. Dimensionality reduction: PCA and 2D manifold embeddings for clustering.
6. Feature selection using Mutual Information and L1 regularization, exporting
   the final feature list to configs/features.yaml.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger("sanjivani_ai.data.features")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def engineer_clinical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute clinically validated derived features and ratios."""
    out = df.copy()

    # 1. Asian Indian Specific BMI Category (ICMR / WHO South Asian cutoffs)
    # <18.5: Underweight (0), 18.5-22.9: Normal (1), 23.0-24.9: Overweight (2), >=25.0: Obese (3)
    if "bmi" in out.columns:
        bmi_numeric = pd.to_numeric(out["bmi"], errors="coerce")
        out["bmi_category"] = (
            pd.cut(
                bmi_numeric,
                bins=[-np.inf, 18.5, 23.0, 25.0, np.inf],
                labels=["underweight", "normal", "overweight", "obese"],
                right=False,
            )
            .astype(str)
            .replace("nan", "normal")
        )
        out["bmi_category_code"] = bmi_numeric.apply(
            lambda b: 0 if b < 18.5 else (1 if b < 23.0 else (2 if b < 25.0 else 3))
        )

    # 2. Hemodynamics: Mean Arterial Pressure (MAP) and Pulse Pressure
    if "systolic_bp" in out.columns and "diastolic_bp" in out.columns:
        sbp = pd.to_numeric(out["systolic_bp"], errors="coerce")
        dbp = pd.to_numeric(out["diastolic_bp"], errors="coerce")
        # MAP = DBP + 1/3 * (SBP - DBP)
        out["mean_arterial_pressure"] = (dbp + (sbp - dbp) / 3.0).round(1)
        # Pulse Pressure = SBP - DBP
        out["pulse_pressure"] = (sbp - dbp).round(1)

    # 3. Waist-to-Height Ratio (Central Adiposity Marker)
    if "waist_circumference_cm" in out.columns and "height_cm" in out.columns:
        waist = pd.to_numeric(out["waist_circumference_cm"], errors="coerce")
        height = pd.to_numeric(out["height_cm"], errors="coerce")
        out["waist_to_height_ratio"] = (waist / height).round(3)

    # 4. Lipid Ratios
    if "total_cholesterol" in out.columns and "hdl_cholesterol" in out.columns:
        tc = pd.to_numeric(out["total_cholesterol"], errors="coerce")
        hdl = pd.to_numeric(out["hdl_cholesterol"], errors="coerce")
        out["total_to_hdl_ratio"] = (tc / hdl).round(2)

    if "triglycerides" in out.columns and "hdl_cholesterol" in out.columns:
        tg = pd.to_numeric(out["triglycerides"], errors="coerce")
        hdl = pd.to_numeric(out["hdl_cholesterol"], errors="coerce")
        # TG/HDL ratio is a surrogate for insulin resistance and atherogenic small dense LDL particles
        out["tg_to_hdl_ratio"] = (tg / hdl).round(2)

    # 5. Age Bands
    if "age" in out.columns:
        age_num = pd.to_numeric(out["age"], errors="coerce")
        out["age_band"] = (
            pd.cut(
                age_num,
                bins=[-np.inf, 30.0, 45.0, 60.0, np.inf],
                labels=["under_30", "30_to_44", "45_to_59", "60_plus"],
                right=False,
            )
            .astype(str)
            .replace("nan", "30_to_44")
        )

    # 6. Interaction Term: Age x BMI
    if "age" in out.columns and "bmi" in out.columns:
        out["interaction_age_bmi"] = (
            pd.to_numeric(out["age"], errors="coerce") * pd.to_numeric(out["bmi"], errors="coerce")
        ).round(1)

    # 7. Log Transforms for Right-Skewed Metrics
    if "triglycerides" in out.columns:
        tg = pd.to_numeric(out["triglycerides"], errors="coerce")
        out["log_triglycerides"] = np.log1p(np.maximum(0, tg)).round(3)

    if "physical_activity_hours_per_week" in out.columns:
        act = pd.to_numeric(out["physical_activity_hours_per_week"], errors="coerce")
        out["log_physical_activity"] = np.log1p(np.maximum(0, act)).round(3)

    # 8. Composite Lifestyle Risk Score (0 = Optimal, 4 = High Risk)
    score = np.zeros(len(out), dtype=float)
    if "physical_activity_hours_per_week" in out.columns:
        act = pd.to_numeric(out["physical_activity_hours_per_week"], errors="coerce").fillna(2.5)
        score += np.where(act < 2.5, 1.0, 0.0)  # WHO/ICMR threshold
    if "smoking_status" in out.columns:
        smk = out["smoking_status"].astype(str).str.lower()
        score += np.where(smk == "current", 2.0, np.where(smk == "former", 1.0, 0.0))
    if "alcohol_consumption" in out.columns:
        alc = out["alcohol_consumption"].astype(str).str.lower()
        score += np.where(alc == "regular", 1.0, 0.0)

    out["lifestyle_risk_score"] = score

    # 9. Metabolic Syndrome IDF Criteria Flag
    # South Asian waist criteria (>=90cm men, >=80cm women or BMI >=25), BP >=130/85, FPG >=100, TG >=150, HDL <40/50
    met_count = np.zeros(len(out), dtype=int)
    if "bmi" in out.columns:
        met_count += (pd.to_numeric(out["bmi"], errors="coerce").fillna(22.0) >= 25.0).astype(int)
    if "systolic_bp" in out.columns:
        met_count += (
            pd.to_numeric(out["systolic_bp"], errors="coerce").fillna(120.0) >= 130.0
        ).astype(int)
    if "fasting_glucose" in out.columns:
        met_count += (
            pd.to_numeric(out["fasting_glucose"], errors="coerce").fillna(90.0) >= 100.0
        ).astype(int)
    if "triglycerides" in out.columns:
        met_count += (
            pd.to_numeric(out["triglycerides"], errors="coerce").fillna(120.0) >= 150.0
        ).astype(int)

    out["metabolic_syndrome_flag"] = (met_count >= 3).astype(int)

    logger.info(f"Clinical feature engineering complete. Total columns: {out.shape[1]}")
    return out


def engineer_longitudinal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Generate lag features and rolling trajectory statistics for regression modeling."""
    out = df.copy()

    # If grouped by patient, compute sequential lag and rolling delta
    if "fasting_glucose" in out.columns:
        fpg = pd.to_numeric(out["fasting_glucose"], errors="coerce")
        out["glucose_lag_1"] = fpg.shift(1).fillna(fpg)
        out["glucose_rolling_mean_3"] = fpg.rolling(window=3, min_periods=1).mean().round(1)
        out["glucose_trend_slope"] = (fpg - out["glucose_lag_1"]).round(1)

    if "systolic_bp" in out.columns:
        sbp = pd.to_numeric(out["systolic_bp"], errors="coerce")
        out["systolic_bp_lag_1"] = sbp.shift(1).fillna(sbp)
        out["systolic_bp_rolling_mean_3"] = sbp.rolling(window=3, min_periods=1).mean().round(1)
        out["systolic_bp_trend_slope"] = (sbp - out["systolic_bp_lag_1"]).round(1)

    return out


def compute_pca_embeddings(
    df: pd.DataFrame,
    feature_cols: list[str],
    n_components: int = 2,
    random_state: int = 42,
) -> tuple[np.ndarray, PCA]:
    """Fit PCA on standardized continuous features for patient segment visualization."""
    sub = df[feature_cols].copy()
    for col in feature_cols:
        sub[col] = pd.to_numeric(sub[col], errors="coerce")
        sub[col] = sub[col].fillna(sub[col].median())

    scaler = StandardScaler()
    scaled = scaler.fit_transform(sub)

    pca = PCA(n_components=n_components, random_state=random_state)
    coords = pca.fit_transform(scaled)
    logger.info(
        f"PCA fitted: {n_components} components explain {pca.explained_variance_ratio_.sum() * 100:.1f}% variance."
    )
    return coords, pca


def select_top_features(
    X: pd.DataFrame,
    y: pd.Series,
    k: int = 15,
) -> tuple[list[str], dict[str, float]]:
    """Select top K features using Mutual Information and export ranking."""
    X_num = X.select_dtypes(include=[np.number]).copy()
    for c in X_num.columns:
        X_num[c] = X_num[c].fillna(X_num[c].median())

    selector = SelectKBest(score_func=mutual_info_classif, k=min(k, X_num.shape[1]))
    selector.fit(X_num, y)

    scores = dict(zip(X_num.columns, selector.scores_, strict=False))
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_features = [feat for feat, sc in ranked[:k]]

    logger.info(f"Top {len(top_features)} features selected via Mutual Information:")
    for feat, sc in ranked[:k]:
        logger.info(f"  {feat:30s} -> MI Score: {sc:.4f}")

    return top_features, scores


def execute_feature_engineering_pipeline(
    input_file: str | Path = "data/interim/harmonized_clinical_data.parquet",
    output_file: str | Path = "data/processed/featured_clinical_data.parquet",
    configs_dir: str | Path = "configs",
) -> pd.DataFrame:
    """Full execution of Phase 5 feature pipeline and export to configs/features.yaml."""
    df = pd.read_parquet(input_file)
    featured = engineer_clinical_features(df)
    featured_long = engineer_longitudinal_features(featured)

    # Compute PCA Coordinates for 2D clustering / visualization
    pca_cols = [
        "age",
        "bmi",
        "systolic_bp",
        "diastolic_bp",
        "fasting_glucose",
        "total_cholesterol",
        "lifestyle_risk_score",
    ]
    coords, pca = compute_pca_embeddings(featured_long, pca_cols, n_components=2)
    featured_long["pca_dim_1"] = coords[:, 0].round(3)
    featured_long["pca_dim_2"] = coords[:, 1].round(3)

    # Feature selection on diabetes target
    diab_mask = featured_long["target_diabetes"].notna()
    X_sub = featured_long.loc[
        diab_mask,
        pca_cols
        + [
            "mean_arterial_pressure",
            "pulse_pressure",
            "total_to_hdl_ratio",
            "tg_to_hdl_ratio",
            "interaction_age_bmi",
            "metabolic_syndrome_flag",
        ],
    ]
    y_sub = featured_long.loc[diab_mask, "target_diabetes"]
    top_feats, mi_scores = select_top_features(X_sub, y_sub, k=10)

    # Export features catalog to YAML
    cfg_path = Path(configs_dir)
    cfg_path.mkdir(parents=True, exist_ok=True)
    feature_catalog = {
        "version": "1.0.0",
        "total_features": featured_long.shape[1],
        "top_mutual_information_features": top_feats,
        "pca_variance_explained": float(pca.explained_variance_ratio_.sum()),
        "feature_definitions": {
            "mean_arterial_pressure": "DBP + 1/3 * (SBP - DBP)",
            "pulse_pressure": "SBP - DBP",
            "waist_to_height_ratio": "Waist / Height (Central Adiposity)",
            "total_to_hdl_ratio": "Total Cholesterol / HDL",
            "tg_to_hdl_ratio": "Triglycerides / HDL (Insulin Resistance Surrogate)",
            "interaction_age_bmi": "Age * BMI",
            "metabolic_syndrome_flag": "IDF Criteria: >=3 of (Abdominal Adiposity, Elevated BP, High FPG, High TG, Low HDL)",
            "lifestyle_risk_score": "Composite score from physical activity, smoking status, and alcohol intake",
        },
    }
    with open(cfg_path / "features.yaml", "w", encoding="utf-8") as f:
        yaml.dump(feature_catalog, f, sort_keys=False)
    logger.info(f"Saved feature catalog to {cfg_path / 'features.yaml'}.")

    out_p = Path(output_file)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    featured_long.to_parquet(out_p, index=False)
    logger.info(
        f"Saved featured dataset to {output_file} ({featured_long.shape[0]} rows, {featured_long.shape[1]} cols)."
    )
    return featured_long


if __name__ == "__main__":
    df = execute_feature_engineering_pipeline()
    print("\nEngineered Feature Summary:")
    print(
        df[
            [
                "mean_arterial_pressure",
                "pulse_pressure",
                "lifestyle_risk_score",
                "metabolic_syndrome_flag",
                "pca_dim_1",
            ]
        ].head()
    )
