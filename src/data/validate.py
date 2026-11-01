"""Phase 3: Pandera Schema Validation & Quality Audit for Sanjivani AI.

Implements:
1. Declarative Pandera DataFrameSchema with physiological constraints.
2. Loud failure modes for schema / dtype violations and out-of-range values.
3. Detailed missingness reporting per column and per clinical data source.
4. Export of validation audit metrics to reports/missingness_report.csv.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

try:
    from pandera.pandas import Check, Column, DataFrameSchema
    from pandera.pandas.errors import SchemaErrors
except ImportError:
    from pandera import Check, Column, DataFrameSchema
    from pandera.errors import SchemaErrors

logger = logging.getLogger("sanjivani_ai.data.validate")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ==============================================================================
# PANDERA CLINICAL SCHEMA DEFINITION
# ==============================================================================
ClinicalDataFrameSchema = DataFrameSchema(
    columns={
        "age": Column(
            float,
            checks=[Check.in_range(1.0, 120.0, error="Age must be between 1 and 120")],
            nullable=True,
            coerce=True,
        ),
        "sex": Column(
            str,
            checks=[
                Check.isin(["male", "female", "other"], error="Sex must be male, female, or other")
            ],
            nullable=False,
        ),
        "bmi": Column(
            float,
            checks=[Check.in_range(10.0, 75.0, error="BMI must be between 10.0 and 75.0 kg/m²")],
            nullable=True,
            coerce=True,
        ),
        "systolic_bp": Column(
            float,
            checks=[
                Check.in_range(60.0, 260.0, error="Systolic BP must be between 60 and 260 mmHg")
            ],
            nullable=True,
            coerce=True,
        ),
        "diastolic_bp": Column(
            float,
            checks=[
                Check.in_range(35.0, 160.0, error="Diastolic BP must be between 35 and 160 mmHg")
            ],
            nullable=True,
            coerce=True,
        ),
        "fasting_glucose": Column(
            float,
            checks=[
                Check.in_range(
                    40.0, 600.0, error="Fasting glucose must be between 40 and 600 mg/dL"
                )
            ],
            nullable=True,
            coerce=True,
        ),
        "hba1c": Column(
            float,
            checks=[Check.in_range(3.0, 20.0, error="HbA1c must be between 3.0% and 20.0%")],
            nullable=True,
            coerce=True,
        ),
        "total_cholesterol": Column(
            float,
            checks=[
                Check.in_range(
                    50.0, 700.0, error="Total cholesterol must be between 50 and 700 mg/dL"
                )
            ],
            nullable=True,
            coerce=True,
        ),
        "smoking_status": Column(
            str,
            checks=[Check.isin(["never", "former", "current"], error="Smoking status invalid")],
            nullable=False,
        ),
        "source": Column(
            str,
            checks=[
                Check.isin(
                    [
                        "uci_heart_disease",
                        "pima_diabetes",
                        "sklearn_diabetes",
                        "framingham_heart",
                        "nhanes_subset",
                        "cdc_brfss_subset",
                        "kaggle_ckd",
                        "app_screenings_consented",
                        "synthetic_test",
                    ]
                )
            ],
            nullable=False,
        ),
        "patient_id": Column(str, nullable=False),
    },
    strict=False,  # Allow extra feature and target columns
    coerce=True,
)


def validate_clinical_dataframe(
    df: pd.DataFrame, fail_loudly: bool = True
) -> tuple[bool, SchemaErrors | None]:
    """Validate DataFrame against ClinicalDataFrameSchema using Pandera.

    If fail_loudly is True, raises SchemaErrors on violation.
    """
    logger.info("Running Pandera physiological and schema validation...")
    try:
        ClinicalDataFrameSchema.validate(df, lazy=True)
        logger.info("Pandera schema validation PASSED. All constraints and dtypes verified.")
        return True, None
    except SchemaErrors as err:
        logger.error(f"Pandera validation FAILED with {len(err.failure_cases)} violation cases.")
        logger.error(f"Sample failure cases:\n{err.failure_cases.head(10)}")
        if fail_loudly:
            raise err
        return False, err


def generate_missingness_report(
    df: pd.DataFrame, reports_dir: str | Path = "reports"
) -> pd.DataFrame:
    """Generate detailed missingness audit overall and stratified by data source."""
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)

    # 1. Overall Missingness
    overall_missing = df.isna().mean().rename("overall_missing_pct") * 100.0
    overall_count = df.isna().sum().rename("missing_count")

    # 2. Missingness by Source
    source_grouped = df.groupby("source")
    by_source_missing = source_grouped.apply(
        lambda g: g.drop(columns=["source"], errors="ignore").isna().mean() * 100.0,
        include_groups=False,
    ).T

    report = pd.concat([overall_count, overall_missing, by_source_missing], axis=1)
    report = report.round(2)

    csv_path = reports_path / "missingness_report.csv"
    report.to_csv(csv_path)
    logger.info(f"Missingness audit report saved to {csv_path}.")
    return report


if __name__ == "__main__":
    from src.data.clean import execute_harmonization_and_cleaning

    data = execute_harmonization_and_cleaning()
    passed, _ = validate_clinical_dataframe(data, fail_loudly=True)
    report = generate_missingness_report(data)
    print("\nMissingness Summary Top 10:")
    print(report[["missing_count", "overall_missing_pct"]].head(10))
