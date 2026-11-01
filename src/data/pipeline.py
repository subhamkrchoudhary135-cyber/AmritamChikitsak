"""Phase 9: Master DAG Pipeline Orchestrator for Sanjivani AI.

Orchestrates the complete data engineering lifecycle:
  [Ingest] -> [Harmonize & Clean] -> [Pandera Validate] -> [Feature Engineering]
  -> [Leakage-Safe Split] -> [Imbalance & Fairness Audit] -> [EDA & HTML Reports]
  -> [Evidently Drift Monitor]

Can be invoked end-to-end via:
  python -m src.data.pipeline --stage all
  or via Makefile target: make pipeline
"""

from __future__ import annotations

import argparse
import logging
import time

logger = logging.getLogger("sanjivani_ai.pipeline")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def run_pipeline(
    stage: str = "all", raw_dir: str = "data/raw", force_download: bool = False
) -> None:
    """Execute stages of the Sanjivani AI clinical data pipeline."""
    t_start = time.time()
    logger.info(f"=== Starting Sanjivani AI Clinical Data Pipeline (Stage: {stage.upper()}) ===")

    # STAGE 1: INGESTION
    if stage in ("all", "ingest"):
        from src.data.ingest import ingest_all_sources

        logger.info("[1/8] Ingesting all 8 clinical data sources...")
        ingest_all_sources(raw_dir=raw_dir, force=force_download)

    # STAGE 2: HARMONIZE & CLEAN
    if stage in ("all", "clean"):
        from src.data.clean import execute_harmonization_and_cleaning

        logger.info(
            "[2/8] Harmonizing schemas, normalizing units, and applying physiological bounds..."
        )
        execute_harmonization_and_cleaning(raw_dir=raw_dir)

    # STAGE 3: PANDERA VALIDATE
    if stage in ("all", "validate"):
        import pandas as pd
        from src.data.validate import generate_missingness_report, validate_clinical_dataframe

        logger.info("[3/8] Running Pandera physiological constraints & missingness audit...")
        df_clean = pd.read_parquet("data/interim/harmonized_clinical_data.parquet")
        validate_clinical_dataframe(df_clean, fail_loudly=True)
        generate_missingness_report(df_clean)

    # STAGE 4: FEATURE ENGINEERING
    if stage in ("all", "features"):
        from src.data.features import execute_feature_engineering_pipeline

        logger.info(
            "[4/8] Engineering domain clinical features, PCA manifolds, and MI feature selection..."
        )
        execute_feature_engineering_pipeline()

    # STAGE 5: LEAKAGE-SAFE SPLITTING
    if stage in ("all", "split"):
        from src.data.split import execute_splitting

        logger.info(
            "[5/8] Performing patient group-aware, stratified, and temporal train/val/test splits..."
        )
        execute_splitting()

    # STAGE 6: IMBALANCE & DEMOGRAPHIC FAIRNESS
    if stage in ("all", "fairness"):
        from src.data.imbalance_fairness import execute_imbalance_and_fairness_phase

        logger.info(
            "[6/8] Auditing class imbalance, cross-validation resampling, and demographic fairness..."
        )
        execute_imbalance_and_fairness_phase()

    # STAGE 7: EDA & REPORTS
    if stage in ("all", "reports"):
        from src.data.reports import execute_all_reports

        logger.info("[7/8] Generating visual EDA plots and interactive HTML data quality report...")
        execute_all_reports()

    # STAGE 8: DATA DRIFT MONITORING
    if stage in ("all", "drift"):
        from src.data.drift_monitor import execute_drift_monitoring

        logger.info("[8/8] Assessing feature distribution drift against reference baseline...")
        execute_drift_monitoring()

    elapsed = time.time() - t_start
    logger.info(f"=== Sanjivani AI Data Pipeline Completed Successfully in {elapsed:.2f}s ===")


def main():
    parser = argparse.ArgumentParser(description="Sanjivani AI Clinical Data Pipeline Orchestrator")
    parser.add_argument(
        "--stage",
        type=str,
        default="all",
        choices=[
            "all",
            "ingest",
            "clean",
            "validate",
            "features",
            "split",
            "fairness",
            "reports",
            "drift",
        ],
        help="Pipeline stage to execute",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force redownload of cached raw datasets",
    )
    args = parser.parse_args()
    run_pipeline(stage=args.stage, force_download=args.force)


if __name__ == "__main__":
    main()
