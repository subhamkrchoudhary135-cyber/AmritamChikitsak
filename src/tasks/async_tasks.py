"""Asynchronous background tasks for batch screenings, drift analysis, and PDF compilation."""

import logging
from typing import Any

import pandas as pd

from src.tasks.celery_app import celery_app

logger = logging.getLogger("sanjivani_ai.tasks")


@celery_app.task(name="tasks.async_batch_screening")
def async_batch_screening(batch_biometrics_list: list[dict[str, Any]]) -> dict[str, Any]:
    """Execute batch screening asynchronously across large epidemiological or corporate cohorts."""
    from src.ml.registry import model_registry
    from src.schemas.screening import ScreeningInput

    if not model_registry.is_loaded:
        model_registry.load_or_train()

    results = []
    for bio in batch_biometrics_list:
        try:
            inp = ScreeningInput(**bio)
            conds, fore, pheno, shap_factors = model_registry.run_screening_inference(inp)
            results.append(
                {
                    "status": "SUCCESS",
                    "continuous_risk": fore.continuous_risk_score_100,
                    "cluster_label": pheno.cluster_label,
                    "diabetes_risk": conds["diabetes"].risk_level.value,
                    "heart_disease_risk": conds["heart_disease"].risk_level.value,
                    "hypertension_risk": conds["hypertension"].risk_level.value,
                }
            )
        except Exception as e:
            results.append({"status": "FAILED", "error": str(e)})

    return {
        "processed_count": len(results),
        "results": results,
    }


@celery_app.task(name="tasks.async_generate_evidently_drift_report")
def async_generate_evidently_drift_report(
    current_records: list[dict[str, Any]],
    output_html_path: str = "reports/generated/drift_report.html",
) -> dict[str, Any]:
    """Background task to run Evidently drift detection suite."""
    from src.ml.datasets import generate_synthetic_clinical_cohort
    from src.ml.drift import DriftMonitoringService

    reference_df = generate_synthetic_clinical_cohort(n_samples=500, random_state=42)
    current_df = pd.DataFrame(current_records)

    service = DriftMonitoringService(reference_data=reference_df)
    report_summary = service.run_drift_analysis(
        current_data=current_df,
        save_html_path=output_html_path,
    )
    return report_summary
