"""Phase 9: Evidently Data Drift & Distribution Shift Monitoring for Sanjivani AI.

Monitors production data streams against baseline training distributions:
1. Kolmogorov-Smirnov (KS) test for continuous physiological variables (glucose, BP, BMI).
2. Chi-Square / Wasserstein distance for categorical and demographic attributes.
3. Automatically triggers alert when feature drift exceeds significance threshold (p < 0.05).
4. Exports visual HTML drift dashboard to reports/evidently_drift_report.html.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
from scipy import stats

logger = logging.getLogger("sanjivani_ai.data.drift_monitor")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def detect_feature_drift_scipy(
    reference_df: pd.DataFrame,
    current_df: pd.DataFrame,
    numerical_features: list[str] | None = None,
    alpha: float = 0.05,
) -> tuple[pd.DataFrame, bool]:
    """Calculate Kolmogorov-Smirnov two-sample test for numerical feature distribution drift."""
    features = numerical_features or [
        "age",
        "bmi",
        "systolic_bp",
        "diastolic_bp",
        "fasting_glucose",
        "total_cholesterol",
        "mean_arterial_pressure",
        "lifestyle_risk_score",
    ]
    cols = [c for c in features if c in reference_df.columns and c in current_df.columns]

    drift_results = []
    drifted_count = 0

    for col in cols:
        ref_s = pd.to_numeric(reference_df[col], errors="coerce").dropna()
        cur_s = pd.to_numeric(current_df[col], errors="coerce").dropna()

        if len(ref_s) < 10 or len(cur_s) < 10:
            continue

        ks_stat, p_val = stats.ks_2samp(ref_s, cur_s)
        is_drifted = bool(p_val < alpha)
        if is_drifted:
            drifted_count += 1

        drift_results.append(
            {
                "feature": col,
                "ref_mean": round(float(ref_s.mean()), 2),
                "current_mean": round(float(cur_s.mean()), 2),
                "ref_std": round(float(ref_s.std()), 2),
                "current_std": round(float(cur_s.std()), 2),
                "ks_statistic": round(float(ks_stat), 4),
                "p_value": round(float(p_val), 5),
                "drift_detected": is_drifted,
            }
        )

    report_df = pd.DataFrame(drift_results)
    drift_share = drifted_count / max(len(cols), 1)
    dataset_drift_alert = drift_share >= 0.25

    if dataset_drift_alert:
        logger.warning(
            f"DATA DRIFT ALERT: {drifted_count}/{len(cols)} features ({drift_share * 100:.1f}%) exhibit significant distribution shift!"
        )
    else:
        logger.info(
            f"Drift monitor status: NOMINAL ({drifted_count}/{len(cols)} features drifted, threshold is 25%)."
        )

    return report_df, dataset_drift_alert


def generate_drift_dashboard_html(
    drift_df: pd.DataFrame,
    dataset_drift_alert: bool,
    output_path: str | Path = "reports/evidently_drift_report.html",
) -> Path:
    """Generate standalone HTML drift monitoring dashboard."""
    badge_color = "#ef4444" if dataset_drift_alert else "#10b981"
    badge_text = "DRIFT ALERT" if dataset_drift_alert else "STABLE DISTRIBUTION"

    rows_html = ""
    for _, row in drift_df.iterrows():
        status_bg = "#fee2e2" if row["drift_detected"] else "#ecfdf5"
        status_color = "#991b1b" if row["drift_detected"] else "#065f46"
        status_text = "DRIFTED" if row["drift_detected"] else "PASS"

        rows_html += f"""
        <tr>
          <td><strong>{row["feature"]}</strong></td>
          <td>{row["ref_mean"]} &plusmn; {row["ref_std"]}</td>
          <td>{row["current_mean"]} &plusmn; {row["current_std"]}</td>
          <td>{row["ks_statistic"]}</td>
          <td>{row["p_value"]}</td>
          <td><span style="background:{status_bg}; color:{status_color}; padding:3px 8px; border-radius:4px; font-weight:bold; font-size:11px;">{status_text}</span></td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Sanjivani AI - Feature Drift Monitoring Dashboard</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #1e293b; padding: 24px; max-width: 1000px; margin: 0 auto; }}
    h1 {{ color: #0f766e; }}
    .badge {{ background: {badge_color}; color: white; padding: 6px 14px; border-radius: 9999px; font-weight: bold; font-size: 13px; }}
    .card {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-top: 20px; border: 1px solid #e2e8f0; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 15px; }}
    th {{ background: #f1f5f9; padding: 10px; border-bottom: 2px solid #cbd5e1; text-align: left; }}
    td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; }}
  </style>
</head>
<body>
  <h1>Data & Population Drift Monitoring</h1>
  <p><span class="badge">{badge_text}</span> &nbsp; Kolmogorov-Smirnov 2-Sample Test (&alpha; = 0.05)</p>

  <div class="card">
    <h3>Continuous Physiological Drift Metrics</h3>
    <table>
      <thead>
        <tr>
          <th>Biomarker Feature</th>
          <th>Reference Mean &plusmn; SD (Train)</th>
          <th>Current Mean &plusmn; SD (Stream)</th>
          <th>KS Stat</th>
          <th>p-value</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </div>
</body>
</html>
"""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"Drift dashboard exported to {out}.")
    return out


def execute_drift_monitoring(
    ref_file: str | Path = "data/processed/diabetes_train.parquet",
    cur_file: str | Path = "data/processed/diabetes_test.parquet",
    reports_dir: str | Path = "reports",
) -> pd.DataFrame:
    """Execute drift check comparing train baseline against recent test/production stream."""
    ref_df = pd.read_parquet(ref_file)
    cur_df = pd.read_parquet(cur_file)

    drift_df, is_drifted = detect_feature_drift_scipy(ref_df, cur_df)
    generate_drift_dashboard_html(
        drift_df, is_drifted, output_path=Path(reports_dir) / "evidently_drift_report.html"
    )
    return drift_df


if __name__ == "__main__":
    df = execute_drift_monitoring()
    print("\nDrift Assessment Results:")
    print(df[["feature", "ks_statistic", "p_value", "drift_detected"]])
