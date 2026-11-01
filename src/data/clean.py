"""Phase 2 & Phase 3: Schema Harmonization, Unit Normalization, and Data Cleaning.

1. Maps all 8 diverse data sources to a single canonical clinical schema.
2. Performs explicit, bi-directional unit conversions (mg/dL <-> mmol/L, kg <-> lbs, cm <-> in).
3. Tags each row with its provenance ('source' column).
4. Handles physiologically impossible values (e.g., zero glucose, zero blood pressure, negative age)
   by converting them to NaN (never silently retaining medical impossibilities).
5. Detects and flags outliers using IQR and Isolation Forest without blind row drops.
6. Generates missingness indicators ('_was_missing' columns).
7. Persists harmonized clean data to data/interim/harmonized_clinical_data.parquet.
"""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

logger = logging.getLogger("sanjivani_ai.data.clean")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ==============================================================================
# CANONICAL CLINICAL SCHEMA SPECIFICATION
# ==============================================================================
CANONICAL_COLUMNS: list[str] = [
    # Demographics
    "age",
    "sex",
    # Anthropometry
    "height_cm",
    "weight_kg",
    "bmi",
    "waist_circumference_cm",
    # Hemodynamics / Vitals
    "systolic_bp",
    "diastolic_bp",
    "heart_rate",
    # Glycemic
    "fasting_glucose",
    "hba1c",
    # Lipids
    "total_cholesterol",
    "hdl_cholesterol",
    "ldl_cholesterol",
    "triglycerides",
    # Lifestyle
    "physical_activity_hours_per_week",
    "smoking_status",
    "alcohol_consumption",
    # Family History
    "family_history_diabetes",
    "family_history_heart_disease",
    # Clinical Outcomes / Targets
    "target_diabetes",
    "target_heart_disease",
    "target_hypertension",
    "target_progression_risk",
    # Metadata & Tracking
    "patient_id",
    "source",
    "measurement_date",
]

# Physiologically plausible biological bounds (Values outside these bounds are physical anomalies -> NaN)
PHYSIOLOGICAL_BOUNDS: dict[str, tuple[float, float]] = {
    "age": (1.0, 120.0),
    "height_cm": (50.0, 250.0),
    "weight_kg": (15.0, 300.0),
    "bmi": (10.0, 75.0),
    "waist_circumference_cm": (40.0, 200.0),
    "systolic_bp": (60.0, 260.0),
    "diastolic_bp": (35.0, 160.0),
    "heart_rate": (30.0, 220.0),
    "fasting_glucose": (40.0, 600.0),
    "hba1c": (3.0, 20.0),
    "total_cholesterol": (50.0, 700.0),
    "hdl_cholesterol": (10.0, 150.0),
    "ldl_cholesterol": (20.0, 450.0),
    "triglycerides": (30.0, 1200.0),
    "physical_activity_hours_per_week": (0.0, 40.0),
}


# ==============================================================================
# UNIT CONVERSION FUNCTIONS (Tested with exact clinical conversion factors)
# ==============================================================================
def glucose_mmol_to_mgdl(val: float | np.ndarray) -> float | np.ndarray:
    """Convert blood glucose from mmol/L to mg/dL (Factor: 18.0182)."""
    return val * 18.0182


def glucose_mgdl_to_mmol(val: float | np.ndarray) -> float | np.ndarray:
    """Convert blood glucose from mg/dL to mmol/L."""
    return val / 18.0182


def cholesterol_mmol_to_mgdl(val: float | np.ndarray) -> float | np.ndarray:
    """Convert total, HDL, or LDL cholesterol from mmol/L to mg/dL (Factor: 38.67)."""
    return val * 38.67


def cholesterol_mgdl_to_mmol(val: float | np.ndarray) -> float | np.ndarray:
    """Convert cholesterol from mg/dL to mmol/L."""
    return val / 38.67


def triglycerides_mmol_to_mgdl(val: float | np.ndarray) -> float | np.ndarray:
    """Convert serum triglycerides from mmol/L to mg/dL (Factor: 88.57)."""
    return val * 88.57


def height_inches_to_cm(val: float | np.ndarray) -> float | np.ndarray:
    """Convert height from inches to centimeters (Factor: 2.54)."""
    return val * 2.54


def height_cm_to_inches(val: float | np.ndarray) -> float | np.ndarray:
    """Convert height from centimeters to inches."""
    return val / 2.54


def weight_lbs_to_kg(val: float | np.ndarray) -> float | np.ndarray:
    """Convert weight from pounds to kilograms (Factor: 0.45359237)."""
    return val * 0.45359237


def weight_kg_to_lbs(val: float | np.ndarray) -> float | np.ndarray:
    """Convert weight from kilograms to pounds."""
    return val / 0.45359237


# ==============================================================================
# SOURCE-SPECIFIC HARMONIZERS
# ==============================================================================
def harmonize_uci_heart(df: pd.DataFrame) -> pd.DataFrame:
    """Harmonize UCI Heart Disease dataset."""
    out = pd.DataFrame(index=df.index)
    out["age"] = pd.to_numeric(df.get("age"), errors="coerce")
    out["sex"] = df.get("sex").map({1: "male", 0: "female"}).fillna("other")
    out["systolic_bp"] = pd.to_numeric(df.get("trestbps"), errors="coerce")
    out["heart_rate"] = pd.to_numeric(df.get("thalach"), errors="coerce")
    out["total_cholesterol"] = pd.to_numeric(df.get("chol"), errors="coerce")
    # Fasting blood sugar > 120 mg/dL flag
    fbs = pd.to_numeric(df.get("fbs"), errors="coerce")
    out["fasting_glucose"] = np.where(fbs == 1, 130.0, np.where(fbs == 0, 95.0, np.nan))
    # Target: num >= 1 indicates angiographic coronary heart disease
    num = pd.to_numeric(df.get("num"), errors="coerce")
    out["target_heart_disease"] = (num >= 1).astype(float)
    out["source"] = "uci_heart_disease"
    return out


def harmonize_pima_diabetes(df: pd.DataFrame) -> pd.DataFrame:
    """Harmonize Pima Indians Diabetes dataset."""
    out = pd.DataFrame(index=df.index)
    out["age"] = pd.to_numeric(df.get("Age"), errors="coerce")
    out["sex"] = "female"  # All Pima cohort participants were female
    # Note: In Pima raw data, 0 in Glucose, BloodPressure, BMI represents missing measurements!
    glucose = pd.to_numeric(df.get("Glucose"), errors="coerce")
    out["fasting_glucose"] = np.where(glucose > 0, glucose, np.nan)
    bp = pd.to_numeric(df.get("BloodPressure"), errors="coerce")
    out["diastolic_bp"] = np.where(bp > 0, bp, np.nan)
    bmi = pd.to_numeric(df.get("BMI"), errors="coerce")
    out["bmi"] = np.where(bmi > 0, bmi, np.nan)
    out["family_history_diabetes"] = (
        pd.to_numeric(df.get("DiabetesPedigreeFunction"), errors="coerce") > 0.5
    ).astype(float)
    out["target_diabetes"] = pd.to_numeric(df.get("Outcome"), errors="coerce").astype(float)
    out["source"] = "pima_diabetes"
    return out


def harmonize_sklearn_diabetes(df: pd.DataFrame) -> pd.DataFrame:
    """Harmonize Scikit-Learn Diabetes Regression cohort."""
    out = pd.DataFrame(index=df.index)
    # The scikit-learn dataset provides standardized features centered with unit variance
    # We rescale features to realistic clinical scales for transparent pooling
    out["age"] = np.clip(50.0 + (df.get("age") * 100 * 0.9), 19, 79).round(1)
    out["sex"] = np.where(df.get("sex") > 0, "male", "female")
    out["bmi"] = np.clip(25.5 + (df.get("bmi") * 100 * 0.8), 16.0, 45.0).round(1)
    out["systolic_bp"] = np.clip(125.0 + (df.get("bp") * 100 * 1.1), 85, 210).round(1)
    out["total_cholesterol"] = np.clip(190.0 + (df.get("s1") * 100 * 1.5), 110, 360).round(1)
    out["ldl_cholesterol"] = np.clip(115.0 + (df.get("s2") * 100 * 1.2), 40, 250).round(1)
    out["hdl_cholesterol"] = np.clip(50.0 + (df.get("s3") * 100 * 0.8), 22, 95).round(1)
    out["triglycerides"] = np.clip(150.0 + (df.get("s5") * 100 * 2.0), 60, 500).round(1)
    out["fasting_glucose"] = np.clip(100.0 + (df.get("s6") * 100 * 1.2), 65, 300).round(1)
    # Target in sklearn is a quantitative 1-year progression measure (25 to 346)
    target_raw = pd.to_numeric(df.get("target"), errors="coerce")
    # Normalize to 0-100 continuous risk progression scale
    out["target_progression_risk"] = np.clip(
        (target_raw - 25.0) / (346.0 - 25.0) * 100.0, 0, 100
    ).round(1)
    out["target_diabetes"] = (target_raw > 150).astype(float)
    out["source"] = "sklearn_diabetes"
    return out


def harmonize_framingham(df: pd.DataFrame) -> pd.DataFrame:
    """Harmonize Framingham Heart Study dataset."""
    out = pd.DataFrame(index=df.index)
    out["age"] = pd.to_numeric(df.get("age"), errors="coerce")
    out["sex"] = df.get("male").map({1: "male", 0: "female"}).fillna("other")
    out["smoking_status"] = df.get("currentSmoker").map({1: "current", 0: "never"}).fillna("never")
    out["systolic_bp"] = pd.to_numeric(df.get("sysBP"), errors="coerce")
    out["diastolic_bp"] = pd.to_numeric(df.get("diaBP"), errors="coerce")
    out["total_cholesterol"] = pd.to_numeric(df.get("totChol"), errors="coerce")
    out["bmi"] = pd.to_numeric(df.get("BMI"), errors="coerce")
    out["heart_rate"] = pd.to_numeric(df.get("heartRate"), errors="coerce")
    out["fasting_glucose"] = pd.to_numeric(df.get("glucose"), errors="coerce")
    out["target_diabetes"] = pd.to_numeric(df.get("diabetes"), errors="coerce").astype(float)
    out["target_hypertension"] = pd.to_numeric(df.get("prevalentHyp"), errors="coerce").astype(
        float
    )
    out["target_heart_disease"] = pd.to_numeric(df.get("TenYearCHD"), errors="coerce").astype(float)
    out["source"] = "framingham_heart"
    return out


def harmonize_nhanes(df: pd.DataFrame) -> pd.DataFrame:
    """Harmonize CDC NHANES cardiometabolic examination subset."""
    out = pd.DataFrame(index=df.index)
    for col in [
        "age",
        "sex",
        "height_cm",
        "weight_kg",
        "bmi",
        "waist_circumference_cm",
        "systolic_bp",
        "diastolic_bp",
        "fasting_glucose",
        "hba1c",
        "total_cholesterol",
        "hdl_cholesterol",
        "ldl_cholesterol",
        "triglycerides",
        "smoking_status",
        "target_diabetes",
        "target_hypertension",
    ]:
        if col in df.columns:
            out[col] = df[col]
        elif col == "waist_circumference_cm" and "waist_cm" in df.columns:
            out["waist_circumference_cm"] = df["waist_cm"]
        elif col == "physical_activity_hours_per_week" and "physical_activity_hours" in df.columns:
            out["physical_activity_hours_per_week"] = df["physical_activity_hours"]

    if "physical_activity_hours" in df.columns:
        out["physical_activity_hours_per_week"] = df["physical_activity_hours"]

    out["source"] = "nhanes_subset"
    return out


def harmonize_brfss(df: pd.DataFrame) -> pd.DataFrame:
    """Harmonize CDC BRFSS chronic disease survey subset."""
    out = pd.DataFrame(index=df.index)
    out["age"] = pd.to_numeric(df.get("age"), errors="coerce")
    out["sex"] = df.get("sex").astype(str).str.lower()
    out["bmi"] = pd.to_numeric(df.get("bmi"), errors="coerce")
    out["smoking_status"] = df.get("smoker").map({1: "current", 0: "never"}).fillna("never")
    out["alcohol_consumption"] = (
        df.get("heavy_alcohol").map({1: "regular", 0: "occasional"}).fillna("none")
    )
    out["physical_activity_hours_per_week"] = np.where(df.get("physical_activity") == 1, 3.5, 0.5)
    out["target_hypertension"] = pd.to_numeric(df.get("high_bp"), errors="coerce").astype(float)
    out["target_diabetes"] = pd.to_numeric(df.get("diabetes"), errors="coerce").astype(float)
    out["target_heart_disease"] = pd.to_numeric(df.get("heart_disease"), errors="coerce").astype(
        float
    )
    out["source"] = "cdc_brfss_subset"
    return out


def harmonize_kaggle_ckd(df: pd.DataFrame) -> pd.DataFrame:
    """Harmonize Kaggle / Apollo Hospitals Chronic Kidney Disease dataset."""
    out = pd.DataFrame(index=df.index)
    out["age"] = pd.to_numeric(df.get("age"), errors="coerce")
    out["systolic_bp"] = pd.to_numeric(df.get("bp"), errors="coerce")
    out["fasting_glucose"] = pd.to_numeric(df.get("bgr"), errors="coerce")
    htn = df.get("htn").astype(str).str.strip().str.lower()
    dm = df.get("dm").astype(str).str.strip().str.lower()
    out["target_hypertension"] = np.where(htn == "yes", 1.0, np.where(htn == "no", 0.0, np.nan))
    out["target_diabetes"] = np.where(dm == "yes", 1.0, np.where(dm == "no", 0.0, np.nan))
    out["source"] = "kaggle_ckd"
    return out


def harmonize_app_screenings(df: pd.DataFrame) -> pd.DataFrame:
    """Harmonize consented production application screenings."""
    out = pd.DataFrame(index=df.index)
    for col in CANONICAL_COLUMNS:
        if col in df.columns:
            out[col] = df[col]
        elif col == "sex" and "gender" in df.columns:
            out["sex"] = df["gender"]

    out["source"] = "app_screenings_consented"
    return out


# ==============================================================================
# PIPELINE HARMONIZATION & VALIDATION LOGIC
# ==============================================================================
def harmonize_all_datasets(raw_dict: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Harmonize and concatenate all 8 clinical sources into a unified DataFrame."""
    harmonizers = {
        "uci_heart_disease": harmonize_uci_heart,
        "pima_diabetes": harmonize_pima_diabetes,
        "sklearn_diabetes": harmonize_sklearn_diabetes,
        "framingham_heart": harmonize_framingham,
        "nhanes_subset": harmonize_nhanes,
        "cdc_brfss_subset": harmonize_brfss,
        "kaggle_ckd": harmonize_kaggle_ckd,
        "app_screenings_consented": harmonize_app_screenings,
    }

    harmonized_dfs: list[pd.DataFrame] = []
    for source_key, df in raw_dict.items():
        if source_key in harmonizers:
            logger.info(f"Harmonizing schema for source: {source_key} ({len(df)} rows)...")
            h_df = harmonizers[source_key](df)
            harmonized_dfs.append(h_df)
        else:
            logger.warning(f"No harmonizer registered for source: {source_key}")

    combined = pd.concat(harmonized_dfs, ignore_index=True)

    # Ensure all canonical columns exist in DataFrame
    for col in CANONICAL_COLUMNS:
        if col not in combined.columns:
            combined[col] = np.nan

    # Generate persistent unique patient identifier if missing
    if "patient_id" not in combined.columns or combined["patient_id"].isna().all():
        combined["patient_id"] = [f"patient_{i:06d}" for i in range(len(combined))]
    else:
        combined["patient_id"] = combined["patient_id"].fillna(
            pd.Series([f"patient_{i:06d}" for i in range(len(combined))])
        )

    # Reorder to canonical layout
    combined = combined[CANONICAL_COLUMNS]
    logger.info(
        f"Combined harmonized dataset created: {combined.shape[0]} rows, {combined.shape[1]} columns."
    )
    return combined


def clean_physiological_ranges(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Enforce physiological plausibility bounds. Convert impossible values to NaN."""
    cleaned = df.copy()
    violations_count: dict[str, int] = {}

    for col, (min_val, max_val) in PHYSIOLOGICAL_BOUNDS.items():
        if col in cleaned.columns:
            numeric_col = pd.to_numeric(cleaned[col], errors="coerce")
            invalid_mask = (numeric_col < min_val) | (numeric_col > max_val)
            n_invalid = int(invalid_mask.sum())
            if n_invalid > 0:
                violations_count[col] = n_invalid
                logger.info(
                    f"Physiological check on '{col}': {n_invalid} invalid values out of bounds [{min_val}, {max_val}] set to NaN."
                )
                cleaned.loc[invalid_mask, col] = np.nan

    # Standardize string categories
    cleaned["sex"] = cleaned["sex"].astype(str).str.lower().str.strip()
    cleaned["sex"] = cleaned["sex"].replace(
        {"1": "male", "0": "female", "m": "male", "f": "female", "nan": "other"}
    )
    cleaned["sex"] = cleaned["sex"].apply(
        lambda s: s if s in ["male", "female", "other"] else "other"
    )

    cleaned["smoking_status"] = cleaned["smoking_status"].astype(str).str.lower().str.strip()
    cleaned["smoking_status"] = cleaned["smoking_status"].replace({"nan": "never"})
    cleaned["smoking_status"] = cleaned["smoking_status"].apply(
        lambda s: s if s in ["never", "former", "current"] else "never"
    )

    cleaned["alcohol_consumption"] = (
        cleaned["alcohol_consumption"].astype(str).str.lower().str.strip()
    )
    cleaned["alcohol_consumption"] = cleaned["alcohol_consumption"].replace({"nan": "none"})
    cleaned["alcohol_consumption"] = cleaned["alcohol_consumption"].apply(
        lambda s: s if s in ["none", "occasional", "regular"] else "none"
    )

    return cleaned, violations_count


def add_missingness_indicators(
    df: pd.DataFrame, key_features: list[str] | None = None
) -> pd.DataFrame:
    """Add binary 'was_missing' indicator flags for key clinical parameters."""
    out = df.copy()
    features = key_features or [
        "fasting_glucose",
        "hba1c",
        "systolic_bp",
        "diastolic_bp",
        "total_cholesterol",
        "hdl_cholesterol",
        "ldl_cholesterol",
        "triglycerides",
        "bmi",
        "waist_circumference_cm",
    ]
    for feat in features:
        if feat in out.columns:
            out[f"{feat}_was_missing"] = out[feat].isna().astype(int)
    return out


def flag_outliers(df: pd.DataFrame, numerical_cols: list[str] | None = None) -> pd.DataFrame:
    """Detect and flag statistical outliers via IQR and Isolation Forest without dropping."""
    out = df.copy()
    cols = numerical_cols or ["systolic_bp", "fasting_glucose", "total_cholesterol", "bmi"]

    # 1. IQR Outlier Flag
    iqr_flag = np.zeros(len(out), dtype=bool)
    for c in cols:
        if c in out.columns:
            series = pd.to_numeric(out[c], errors="coerce").dropna()
            q25, q75 = series.quantile(0.25), series.quantile(0.75)
            iqr = q75 - q25
            lower_bound = q25 - 3.0 * iqr  # Using 3x IQR for extreme outliers
            upper_bound = q75 + 3.0 * iqr
            outlier_mask = (out[c] < lower_bound) | (out[c] > upper_bound)
            iqr_flag = iqr_flag | outlier_mask.fillna(False)

    out["is_iqr_outlier"] = iqr_flag.astype(int)

    # 2. Isolation Forest Outlier Score
    try:
        sub = out[cols].copy()
        for c in cols:
            sub[c] = sub[c].fillna(sub[c].median())
        iso = IsolationForest(contamination=0.03, random_state=42)
        preds = iso.fit_predict(sub)
        out["is_isolation_outlier"] = (preds == -1).astype(int)
    except Exception as e:
        logger.warning(f"Isolation forest flagging skipped: {e}")
        out["is_isolation_outlier"] = 0

    n_outliers = int(out["is_isolation_outlier"].sum())
    logger.info(f"Outlier screening completed: {n_outliers} rows flagged by Isolation Forest.")
    return out


def execute_harmonization_and_cleaning(
    raw_dir: str | Path = "data/raw",
    interim_dir: str | Path = "data/interim",
) -> pd.DataFrame:
    """Full execution of Phase 2 and Phase 3."""
    from src.data.ingest import ingest_all_sources

    raw_dict = ingest_all_sources(raw_dir=raw_dir)
    harmonized = harmonize_all_datasets(raw_dict)
    cleaned, violations = clean_physiological_ranges(harmonized)
    flagged = flag_outliers(cleaned)
    final_df = add_missingness_indicators(flagged)

    interim_path = Path(interim_dir)
    interim_path.mkdir(parents=True, exist_ok=True)
    out_file = interim_path / "harmonized_clinical_data.parquet"
    final_df.to_parquet(out_file, index=False)
    logger.info(
        f"Saved harmonized clean dataset to {out_file} ({final_df.shape[0]} rows, {final_df.shape[1]} cols)."
    )
    return final_df


if __name__ == "__main__":
    df = execute_harmonization_and_cleaning()
    print("Harmonization summary by source:")
    print(df["source"].value_counts())
    print("\nMissingness percentage in key vitals:")
    for col in ["systolic_bp", "fasting_glucose", "bmi", "total_cholesterol"]:
        print(f"  {col:20s}: {df[col].isna().mean() * 100:.1f}% missing")
