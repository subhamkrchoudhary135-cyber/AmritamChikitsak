"""Comprehensive Test Suite for Sanjivani AI Clinical Data Pipeline.

Tests:
1. Unit conversions (bi-directional glucose, cholesterol, height, weight).
2. Base DataLoader checksum verification and immutability.
3. Pandera physiological constraints & failure modes on invalid inputs.
4. Outlier flagging and missingness indicator generation.
5. Strict anti-leakage guarantee (imputer/scaler stats match train only).
6. Group-aware splitting with zero patient ID overlap.
7. Feature engineering calculations (MAP, pulse pressure, WHtR, Asian BMI cutoffs).
8. DPDP Act 2023 pseudonymization and Right to Erasure.
9. Data drift detection (KS-test).
10. Full end-to-end integration test with Faker synthetic clinical cohort.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from faker import Faker
from pandera.errors import SchemaErrors
from src.data.clean import (
    add_missingness_indicators,
    cholesterol_mgdl_to_mmol,
    cholesterol_mmol_to_mgdl,
    clean_physiological_ranges,
    flag_outliers,
    glucose_mgdl_to_mmol,
    glucose_mmol_to_mgdl,
    height_cm_to_inches,
    height_inches_to_cm,
    weight_kg_to_lbs,
    weight_lbs_to_kg,
)
from src.data.drift_monitor import detect_feature_drift_scipy, generate_drift_dashboard_html
from src.data.features import engineer_clinical_features
from src.data.ingest import PimaDiabetesDataLoader, UCIHeartDataLoader
from src.data.privacy import execute_right_to_erasure, hash_identifier, sanitize_pii_columns
from src.data.split import (
    build_leakage_safe_preprocessor,
    sanitize_feature_matrix,
    split_stratified_group,
    verify_no_data_leakage,
)
from src.data.validate import validate_clinical_dataframe


# ==============================================================================
# 1. UNIT CONVERSIONS TESTS
# ==============================================================================
def test_glucose_unit_conversions():
    # 5.55 mmol/L is ~ 100.0 mg/dL
    mmol = 5.55
    mgdl = glucose_mmol_to_mgdl(mmol)
    assert abs(mgdl - 100.0) < 0.2
    assert abs(glucose_mgdl_to_mmol(mgdl) - mmol) < 1e-4


def test_cholesterol_unit_conversions():
    # 5.17 mmol/L is ~ 200.0 mg/dL
    mmol = 5.17
    mgdl = cholesterol_mmol_to_mgdl(mmol)
    assert abs(mgdl - 199.9) < 0.5
    assert abs(cholesterol_mgdl_to_mmol(mgdl) - mmol) < 1e-4


def test_anthropometric_unit_conversions():
    # Height: 68 inches ~ 172.72 cm
    inches = 68.0
    cm = height_inches_to_cm(inches)
    assert abs(cm - 172.72) < 1e-2
    assert abs(height_cm_to_inches(cm) - inches) < 1e-4

    # Weight: 154 lbs ~ 69.85 kg
    lbs = 154.0
    kg = weight_lbs_to_kg(lbs)
    assert abs(kg - 69.85) < 0.1
    assert abs(weight_kg_to_lbs(kg) - lbs) < 1e-4


# ==============================================================================
# 2. DATA INGESTION & CHECKSUM VERIFICATION
# ==============================================================================
def test_pima_loader_and_caching(tmp_path):
    loader = PimaDiabetesDataLoader(raw_dir=tmp_path)
    df = loader.load_raw()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert (tmp_path / "pima_diabetes.csv").exists()

    # Checksum computation
    chk = loader.compute_checksum(loader.raw_file_path)
    assert isinstance(chk, str) and len(chk) == 64


# ==============================================================================
# 3. PANDERA VALIDATION & PHYSIOLOGICAL BOUNDS
# ==============================================================================
def test_pandera_valid_dataframe():
    valid_data = pd.DataFrame(
        {
            "age": [35.0, 52.0],
            "sex": ["male", "female"],
            "bmi": [23.4, 28.1],
            "systolic_bp": [120.0, 138.0],
            "diastolic_bp": [78.0, 88.0],
            "fasting_glucose": [92.0, 115.0],
            "hba1c": [5.4, 6.2],
            "total_cholesterol": [180.0, 220.0],
            "smoking_status": ["never", "former"],
            "source": ["nhanes_subset", "framingham_heart"],
            "patient_id": ["pat_001", "pat_002"],
        }
    )
    passed, err = validate_clinical_dataframe(valid_data, fail_loudly=True)
    assert passed is True
    assert err is None


def test_pandera_rejects_impossible_vitals():
    # Negative age, zero BP, and astronomical glucose must fail Pandera check
    invalid_data = pd.DataFrame(
        {
            "age": [-5.0],  # Invalid: age < 1
            "sex": ["male"],
            "bmi": [24.0],
            "systolic_bp": [0.0],  # Invalid: SBP < 60
            "diastolic_bp": [80.0],
            "fasting_glucose": [2500.0],  # Invalid: glucose > 600
            "hba1c": [5.0],
            "total_cholesterol": [180.0],
            "smoking_status": ["never"],
            "source": ["nhanes_subset"],
            "patient_id": ["pat_999"],
        }
    )
    with pytest.raises(SchemaErrors):
        validate_clinical_dataframe(invalid_data, fail_loudly=True)


def test_clean_physiological_bounds_sets_nan():
    raw_df = pd.DataFrame(
        {
            "age": [45.0, -10.0],  # -10 out of bounds -> should become NaN
            "systolic_bp": [120.0, 0.0],  # 0 out of bounds -> should become NaN
            "fasting_glucose": [90.0, 850.0],  # 850 out of bounds -> should become NaN
            "sex": ["male", "female"],
            "smoking_status": ["never", "current"],
            "alcohol_consumption": ["none", "occasional"],
        }
    )
    cleaned, violations = clean_physiological_ranges(raw_df)
    assert pd.isna(cleaned.loc[1, "age"])
    assert pd.isna(cleaned.loc[1, "systolic_bp"])
    assert pd.isna(cleaned.loc[1, "fasting_glucose"])
    assert cleaned.loc[0, "age"] == 45.0


def test_missingness_indicators():
    df = pd.DataFrame(
        {
            "fasting_glucose": [95.0, np.nan, 120.0],
            "systolic_bp": [np.nan, 130.0, 140.0],
        }
    )
    flagged = add_missingness_indicators(df, ["fasting_glucose", "systolic_bp"])
    assert "fasting_glucose_was_missing" in flagged.columns
    assert "systolic_bp_was_missing" in flagged.columns
    assert flagged.loc[1, "fasting_glucose_was_missing"] == 1
    assert flagged.loc[0, "fasting_glucose_was_missing"] == 0


def test_outlier_flagging():
    df = pd.DataFrame(
        {
            "systolic_bp": [120, 122, 118, 125, 121, 119, 124, 250],  # 250 is outlier
            "fasting_glucose": [90, 92, 88, 95, 91, 89, 93, 400],
            "total_cholesterol": [180, 185, 175, 190, 182, 178, 184, 550],
            "bmi": [23, 24, 22, 25, 23.5, 22.8, 24.2, 58],
        }
    )
    flagged = flag_outliers(df)
    assert "is_iqr_outlier" in flagged.columns
    assert "is_isolation_outlier" in flagged.columns
    assert flagged["is_iqr_outlier"].iloc[-1] == 1


# ==============================================================================
# 4. ANTI-LEAKAGE AUDIT & SPLITTING TESTS
# ==============================================================================
def test_group_aware_split_no_patient_leakage():
    # 100 rows with repeated patient IDs (10 patients with 10 rows each)
    patients = [f"patient_{i // 10}" for i in range(100)]
    df = pd.DataFrame(
        {
            "patient_id": patients,
            "target_diabetes": [0, 1] * 50,
            "fasting_glucose": np.random.normal(100, 15, size=100),
        }
    )
    train_df, val_df, test_df = split_stratified_group(
        df, target_col="target_diabetes", group_col="patient_id"
    )

    train_p = set(train_df["patient_id"])
    val_p = set(val_df["patient_id"])
    test_p = set(test_df["patient_id"])

    assert len(train_p.intersection(val_p)) == 0, "Patient overlap between train and val!"
    assert len(train_p.intersection(test_p)) == 0, "Patient overlap between train and test!"
    assert len(val_p.intersection(test_p)) == 0, "Patient overlap between val and test!"


def test_anti_leakage_preprocessor_verification():
    X_train = pd.DataFrame(
        {
            "age": [20.0, 30.0, 40.0],  # Median = 30.0
            "bmi": [22.0, 24.0, 26.0],  # Median = 24.0
            "sex": ["male", "female", "male"],
        }
    )
    X_test = pd.DataFrame(
        {
            "age": [80.0, 90.0, 100.0],  # Very high values
            "bmi": [35.0, 40.0, 45.0],
            "sex": ["female", "female", "female"],
        }
    )
    preprocessor = build_leakage_safe_preprocessor(["age", "bmi"], ["sex"])
    assert verify_no_data_leakage(preprocessor, X_train, X_test, ["age", "bmi"]) is True


def test_sanitize_feature_matrix_strips_targets():
    df = pd.DataFrame(
        {
            "target_diabetes": [0, 1],
            "target_heart_disease": [1, 0],
            "target_hypertension": [0, 1],
            "bmi": [24.0, 28.0],
            "measurement_date": ["2026-01-01", "2026-01-02"],
        }
    )
    clean_mat = sanitize_feature_matrix(df, current_target="target_diabetes")
    assert "target_diabetes" in clean_mat.columns
    assert "target_heart_disease" not in clean_mat.columns
    assert "target_hypertension" not in clean_mat.columns
    assert "measurement_date" not in clean_mat.columns


# ==============================================================================
# 5. FEATURE ENGINEERING CALCULATIONS
# ==============================================================================
def test_clinical_feature_ratios():
    df = pd.DataFrame(
        {
            "bmi": [17.5, 21.0, 24.0, 27.5],  # underweight, normal, overweight, obese
            "systolic_bp": [130.0, 120.0, 140.0, 150.0],
            "diastolic_bp": [85.0, 80.0, 90.0, 95.0],
            "waist_circumference_cm": [75.0, 80.0, 92.0, 105.0],
            "height_cm": [165.0, 170.0, 168.0, 162.0],
            "total_cholesterol": [180.0, 200.0, 240.0, 260.0],
            "hdl_cholesterol": [50.0, 50.0, 40.0, 35.0],
            "triglycerides": [120.0, 150.0, 200.0, 300.0],
            "physical_activity_hours_per_week": [4.0, 3.0, 1.0, 0.5],
            "smoking_status": ["never", "never", "former", "current"],
            "alcohol_consumption": ["none", "none", "occasional", "regular"],
            "age": [25.0, 40.0, 55.0, 65.0],
            "fasting_glucose": [85.0, 95.0, 110.0, 145.0],
        }
    )
    featured = engineer_clinical_features(df)

    # 1. Asian BMI Codes
    assert list(featured["bmi_category_code"]) == [0, 1, 2, 3]

    # 2. Mean Arterial Pressure (MAP) = DBP + 1/3 * (SBP - DBP)
    # Row 0: 85 + (130 - 85)/3 = 85 + 15 = 100.0
    assert abs(featured.loc[0, "mean_arterial_pressure"] - 100.0) < 0.2

    # 3. Pulse Pressure = SBP - DBP
    # Row 0: 130 - 85 = 45.0
    assert abs(featured.loc[0, "pulse_pressure"] - 45.0) < 0.1

    # 4. Metabolic Syndrome Flag: Row 3 meets all 5 criteria -> flag = 1
    assert featured.loc[3, "metabolic_syndrome_flag"] == 1


# ==============================================================================
# 6. PRIVACY, DE-IDENTIFICATION & RIGHT TO ERASURE
# ==============================================================================
def test_privacy_pii_sanitization():
    df = pd.DataFrame(
        {
            "full_name": ["Rajesh Sharma"],
            "phone_number": ["+919876543210"],
            "abha_id": ["91-1234-5678-9012"],
            "patient_id": ["pat_12345"],
            "systolic_bp": [124.0],
        }
    )
    sanitized = sanitize_pii_columns(df)
    assert "full_name" not in sanitized.columns
    assert "phone_number" not in sanitized.columns
    assert "abha_id" not in sanitized.columns
    assert sanitized.loc[0, "patient_id"].startswith("hash_")


def test_right_to_erasure_purges_records(tmp_path):
    target_pid = "purge_target_001"
    hashed_pid = f"hash_{hash_identifier(target_pid)}"

    csv_file = tmp_path / "app_screenings.csv"
    pd.DataFrame(
        {
            "patient_id": [target_pid, "keep_patient_002"],
            "systolic_bp": [130, 120],
        }
    ).to_csv(csv_file, index=False)

    parquet_file = tmp_path / "harmonized.parquet"
    pd.DataFrame(
        {
            "patient_id": [hashed_pid, "hash_other_patient"],
            "fasting_glucose": [110, 95],
        }
    ).to_parquet(parquet_file, index=False)

    audit_log = tmp_path / "erasure.log"
    res = execute_right_to_erasure(
        patient_id=target_pid,
        data_paths=[csv_file, parquet_file],
        audit_log_path=audit_log,
    )
    assert res["status"] == "SUCCESS"
    assert res["total_purged_rows"] == 2

    # Verify rows no longer exist
    df_csv = pd.read_csv(csv_file)
    assert target_pid not in df_csv["patient_id"].values
    df_parquet = pd.read_parquet(parquet_file)
    assert hashed_pid not in df_parquet["patient_id"].values


# ==============================================================================
# 7. DATA DRIFT MONITORING
# ==============================================================================
def test_drift_detection_flags_distribution_shift(tmp_path):
    rng = np.random.default_rng(42)
    ref = pd.DataFrame(
        {
            "fasting_glucose": rng.normal(95, 10, size=200),
            "systolic_bp": rng.normal(120, 10, size=200),
        }
    )
    # Shift glucose by +35 mg/dL in current stream
    curr = pd.DataFrame(
        {
            "fasting_glucose": rng.normal(130, 12, size=200),
            "systolic_bp": rng.normal(121, 10, size=200),
        }
    )
    drift_df, is_drifted = detect_feature_drift_scipy(
        ref, curr, numerical_features=["fasting_glucose", "systolic_bp"]
    )
    glucose_drift = drift_df[drift_df["feature"] == "fasting_glucose"]["drift_detected"].iloc[0]
    assert bool(glucose_drift) is True
    assert is_drifted is True  # 1/2 drifted is 50%, >= 25% threshold
    html_out = generate_drift_dashboard_html(
        drift_df, is_drifted, output_path=tmp_path / "drift.html"
    )
    assert html_out.exists()


# ==============================================================================
# 8. INTEGRATION TEST WITH FAKER
# ==============================================================================
def test_end_to_end_pipeline_integration(tmp_path):
    """Run end-to-end mini pipeline on Faker synthetic cohort."""
    fake = Faker()
    Faker.seed(42)
    n = 100

    # Generate synthetic patient cohort
    records = []
    for i in range(n):
        age = fake.random_int(min=20, max=75)
        sex = fake.random_element(elements=["male", "female"])
        bmi = round(fake.pyfloat(min_value=18.0, max_value=35.0), 1)
        sbp = round(fake.pyfloat(min_value=95.0, max_value=175.0), 1)
        dbp = round(sbp * 0.65, 1)
        fpg = round(fake.pyfloat(min_value=70.0, max_value=220.0), 1)
        records.append(
            {
                "age": age,
                "sex": sex,
                "bmi": bmi,
                "systolic_bp": sbp,
                "diastolic_bp": dbp,
                "fasting_glucose": fpg,
                "hba1c": round((fpg + 46.7) / 28.7, 1),
                "total_cholesterol": round(fake.pyfloat(min_value=140.0, max_value=280.0), 1),
                "smoking_status": fake.random_element(elements=["never", "former", "current"]),
                "target_diabetes": 1 if fpg > 120 else 0,
                "source": "synthetic_test",
                "patient_id": f"syn_{i:04d}",
            }
        )

    raw_df = pd.DataFrame(records)

    # 1. Validate
    passed, _ = validate_clinical_dataframe(raw_df, fail_loudly=True)
    assert passed is True

    # 2. Engineer features
    feat_df = engineer_clinical_features(raw_df)
    assert "mean_arterial_pressure" in feat_df.columns
    assert "lifestyle_risk_score" in feat_df.columns

    # 3. Split
    tr, va, te = split_stratified_group(feat_df, target_col="target_diabetes")
    assert len(tr) == 60
    assert len(va) == 20
    assert len(te) == 20

    # 4. Save and assert artifacts exist
    tr.to_parquet(tmp_path / "train.parquet")
    assert (tmp_path / "train.parquet").exists()


# ==============================================================================
# 9. COMPREHENSIVE PIPELINE STAGE & LOADER COVERAGE
# ==============================================================================
def test_all_individual_data_loaders(tmp_path):
    from src.data.ingest import (
        AppConsentedDataLoader,
        BRFSSDataLoader,
        FraminghamHeartDataLoader,
        KaggleCKDDataLoader,
        NHANESDataLoader,
        SklearnDiabetesDataLoader,
    )

    l_uci = UCIHeartDataLoader(raw_dir=tmp_path)
    df_uci = l_uci.load_raw()
    assert len(df_uci) > 0

    l_skl = SklearnDiabetesDataLoader(raw_dir=tmp_path)
    df_skl = l_skl.load_raw()
    assert len(df_skl) > 0

    l_fra = FraminghamHeartDataLoader(raw_dir=tmp_path)
    df_fra = l_fra.load_raw()
    assert len(df_fra) > 0

    l_nh = NHANESDataLoader(raw_dir=tmp_path)
    df_nh = l_nh.load_raw()
    assert len(df_nh) > 0

    l_br = BRFSSDataLoader(raw_dir=tmp_path)
    df_br = l_br.load_raw()
    assert len(df_br) > 0

    l_ck = KaggleCKDDataLoader(raw_dir=tmp_path)
    df_ck = l_ck.load_raw()
    assert len(df_ck) > 0

    l_app = AppConsentedDataLoader(raw_dir=tmp_path)
    df_app = l_app.load_raw()
    assert len(df_app) > 0


def test_clean_and_harmonize_execution(tmp_path):
    from src.data.clean import execute_harmonization_and_cleaning
    from src.data.validate import generate_missingness_report

    df_clean = execute_harmonization_and_cleaning(raw_dir="data/raw", interim_dir=tmp_path)
    assert len(df_clean) > 0
    assert (tmp_path / "harmonized_clinical_data.parquet").exists()

    report = generate_missingness_report(df_clean, reports_dir=tmp_path)
    assert len(report) > 0
    assert (tmp_path / "missingness_report.csv").exists()


def test_features_and_pca_pipeline(tmp_path):
    from src.data.features import execute_feature_engineering_pipeline

    feat_out = tmp_path / "featured.parquet"
    df_feat = execute_feature_engineering_pipeline(
        input_file="data/interim/harmonized_clinical_data.parquet",
        output_file=feat_out,
        configs_dir=tmp_path,
    )
    assert feat_out.exists()
    assert (tmp_path / "features.yaml").exists()
    assert "pca_dim_1" in df_feat.columns


def test_split_and_temporal_execution(tmp_path):
    from src.data.split import execute_splitting

    splits = execute_splitting(
        interim_file="data/interim/harmonized_clinical_data.parquet",
        processed_dir=tmp_path,
    )
    assert "diabetes" in splits
    assert "heart_disease" in splits
    assert "hypertension" in splits
    assert "regression" in splits
    assert (tmp_path / "diabetes_train.parquet").exists()


def test_reports_and_visualizations(tmp_path):
    from src.data.reports import execute_all_reports

    execute_all_reports(
        featured_file="data/processed/featured_clinical_data.parquet",
        reports_dir=tmp_path,
    )
    assert (tmp_path / "correlation_heatmap.png").exists()
    assert (tmp_path / "class_distributions.png").exists()
    assert (tmp_path / "missingness_map.png").exists()
    assert (tmp_path / "cluster_pca_scatter.png").exists()
    assert (tmp_path / "data_quality_report.html").exists()


def test_drift_monitoring_execution(tmp_path):
    from src.data.drift_monitor import execute_drift_monitoring

    drift_df = execute_drift_monitoring(
        ref_file="data/processed/diabetes_train.parquet",
        cur_file="data/processed/diabetes_test.parquet",
        reports_dir=tmp_path,
    )
    assert len(drift_df) > 0
    assert (tmp_path / "evidently_drift_report.html").exists()


def test_pipeline_runner_stages():
    from src.data.pipeline import run_pipeline

    # Test individual runner stages
    run_pipeline(stage="validate")
    run_pipeline(stage="drift")
