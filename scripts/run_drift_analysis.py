"""Script to generate Evidently data and model drift reports."""

import logging
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.audit import setup_structured_logging
from src.ml.datasets import generate_synthetic_clinical_cohort
from src.ml.drift import DriftMonitoringService

logger = setup_structured_logging()


def main():
    logger.info("Initializing Evidently Drift Monitoring...")
    # Reference baseline cohort (representing training distribution)
    ref_df = generate_synthetic_clinical_cohort(n_samples=1000, random_state=42)

    # Current production batch (with simulated mild demographic drift: slightly older cohort)
    curr_df = generate_synthetic_clinical_cohort(n_samples=500, random_state=99)
    curr_df["age"] = curr_df["age"] + 3.5

    service = DriftMonitoringService(reference_data=ref_df)
    report_path = "reports/generated/drift_report.html"

    logger.info("Running drift analysis tests...")
    summary = service.run_drift_analysis(
        current_data=curr_df,
        target_column="target_diabetes",
        save_html_path=report_path,
    )

    logger.info(f"Drift Analysis Status: {summary['status']}")
    logger.info(f"Drifted Features Ratio: {summary['drifted_features_ratio']:.2%}")
    logger.info(f"Report successfully saved to {report_path}")


if __name__ == "__main__":
    main()
