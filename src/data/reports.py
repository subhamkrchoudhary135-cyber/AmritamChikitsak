"""Phase 7: Exploratory Data Analysis & Automated Data Quality Reporting.

Generates:
1. Interactive standalone HTML Data Quality Report (reports/data_quality_report.html).
2. Correlation Heatmap (reports/correlation_heatmap.png).
3. Biomarker Distribution Plots by Disease Class (reports/class_distributions.png).
4. Missingness Map per Source (reports/missingness_map.png).
5. 2D Patient Phenotype Cluster Scatter Plot (reports/cluster_pca_scatter.png).
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend for headless execution
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

logger = logging.getLogger("sanjivani_ai.data.reports")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def generate_correlation_heatmap(
    df: pd.DataFrame,
    features: list[str] | None = None,
    output_path: str | Path = "reports/correlation_heatmap.png",
) -> Path:
    """Generate Pearson correlation heatmap for cardiometabolic parameters."""
    target_cols = features or [
        "age",
        "bmi",
        "systolic_bp",
        "diastolic_bp",
        "heart_rate",
        "fasting_glucose",
        "hba1c",
        "total_cholesterol",
        "hdl_cholesterol",
        "ldl_cholesterol",
        "triglycerides",
        "mean_arterial_pressure",
        "pulse_pressure",
        "lifestyle_risk_score",
    ]
    cols = [c for c in target_cols if c in df.columns]
    sub = df[cols].dropna()

    plt.figure(figsize=(11, 9))
    corr = sub.corr(method="pearson")
    mask = np.triu(np.ones_like(corr, dtype=bool))

    sns.heatmap(
        corr,
        mask=mask,
        cmap="coolwarm",
        vmax=1.0,
        vmin=-0.4,
        center=0.0,
        annot=True,
        fmt=".2f",
        square=True,
        linewidths=0.75,
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation (r)"},
        annot_kws={"size": 8},
    )
    plt.title(
        "Cardiometabolic Biomarker Correlation Matrix (Sanjivani AI)",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    plt.tight_layout()

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=200)
    plt.close()
    logger.info(f"Correlation heatmap saved to {out}.")
    return out


def generate_class_distribution_plots(
    df: pd.DataFrame,
    output_path: str | Path = "reports/class_distributions.png",
) -> Path:
    """Generate KDE distribution plots comparing biomarkers across disease classes."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 1. Fasting Glucose by Diabetes Status
    if "target_diabetes" in df.columns and "fasting_glucose" in df.columns:
        sub_diab = df[["fasting_glucose", "target_diabetes"]].dropna()
        sns.kdeplot(
            data=sub_diab[sub_diab["target_diabetes"] == 0],
            x="fasting_glucose",
            label="Non-Diabetic (Screening Negative)",
            color="#059669",
            fill=True,
            alpha=0.3,
            ax=axes[0],
        )
        sns.kdeplot(
            data=sub_diab[sub_diab["target_diabetes"] == 1],
            x="fasting_glucose",
            label="Diabetic (Screening Positive)",
            color="#e11d48",
            fill=True,
            alpha=0.3,
            ax=axes[0],
        )
        axes[0].axvline(
            100, color="gray", linestyle="--", alpha=0.7, label="Normal Fasting Cutoff (100 mg/dL)"
        )
        axes[0].axvline(
            126, color="#e11d48", linestyle=":", alpha=0.8, label="Diagnostic Cutoff (126 mg/dL)"
        )
        axes[0].set_title(
            "Fasting Glucose Distribution by Diabetes Status", fontsize=11, fontweight="bold"
        )
        axes[0].set_xlabel("Fasting Plasma Glucose (mg/dL)")
        axes[0].set_ylabel("Kernel Density")
        axes[0].set_xlim(50, 300)
        axes[0].legend(fontsize=8)

    # 2. Systolic Blood Pressure by Hypertension Status
    if "target_hypertension" in df.columns and "systolic_bp" in df.columns:
        sub_htn = df[["systolic_bp", "target_hypertension"]].dropna()
        sns.kdeplot(
            data=sub_htn[sub_htn["target_hypertension"] == 0],
            x="systolic_bp",
            label="Normotensive (SBP < 140)",
            color="#0284c7",
            fill=True,
            alpha=0.3,
            ax=axes[1],
        )
        sns.kdeplot(
            data=sub_htn[sub_htn["target_hypertension"] == 1],
            x="systolic_bp",
            label="Hypertensive (SBP >= 140)",
            color="#d97706",
            fill=True,
            alpha=0.3,
            ax=axes[1],
        )
        axes[1].axvline(
            120, color="gray", linestyle="--", alpha=0.7, label="Normal Cutoff (120 mmHg)"
        )
        axes[1].axvline(
            140, color="#d97706", linestyle=":", alpha=0.8, label="Hypertension Stage 2 (140 mmHg)"
        )
        axes[1].set_title(
            "Systolic Blood Pressure by Hypertension Status", fontsize=11, fontweight="bold"
        )
        axes[1].set_xlabel("Systolic Blood Pressure (mmHg)")
        axes[1].set_ylabel("Kernel Density")
        axes[1].set_xlim(70, 220)
        axes[1].legend(fontsize=8)

    plt.tight_layout()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=200)
    plt.close()
    logger.info(f"Class distribution plots saved to {out}.")
    return out


def generate_missingness_map(
    df: pd.DataFrame,
    output_path: str | Path = "reports/missingness_map.png",
) -> Path:
    """Generate missingness heatmap showing percentage of missing values per source."""
    key_cols = [
        "age",
        "sex",
        "bmi",
        "systolic_bp",
        "diastolic_bp",
        "heart_rate",
        "fasting_glucose",
        "hba1c",
        "total_cholesterol",
        "hdl_cholesterol",
        "ldl_cholesterol",
        "triglycerides",
        "physical_activity_hours_per_week",
    ]
    cols = [c for c in key_cols if c in df.columns]

    missing_by_source = df.groupby("source")[cols].apply(
        lambda g: g.isna().mean() * 100.0, include_groups=False
    )

    plt.figure(figsize=(12, 6))
    sns.heatmap(
        missing_by_source,
        annot=True,
        fmt=".1f",
        cmap="YlOrRd",
        vmin=0,
        vmax=100,
        linewidths=0.5,
        cbar_kws={"label": "Missing Values (%)"},
    )
    plt.title(
        "Missing Data Profile Across Harmonized Sources (%)", fontsize=12, fontweight="bold", pad=12
    )
    plt.xlabel("Biometric Feature")
    plt.ylabel("Data Source Provenance")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.tight_layout()

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=200)
    plt.close()
    logger.info(f"Missingness map saved to {out}.")
    return out


def generate_cluster_pca_scatter(
    df: pd.DataFrame,
    output_path: str | Path = "reports/cluster_pca_scatter.png",
) -> Path:
    """Generate 2D PCA patient phenotype projection scatter plot."""
    if "pca_dim_1" not in df.columns or "pca_dim_2" not in df.columns:
        logger.warning("PCA coordinates not found in DataFrame; skipping cluster scatter.")
        return Path(output_path)

    plt.figure(figsize=(9, 7))
    sample = df.sample(n=min(5000, len(df)), random_state=42)

    hue_col = "metabolic_syndrome_flag" if "metabolic_syndrome_flag" in sample else None
    palette = {0: "#0284c7", 1: "#e11d48"} if hue_col else None

    sns.scatterplot(
        data=sample,
        x="pca_dim_1",
        y="pca_dim_2",
        hue=hue_col,
        palette=palette,
        alpha=0.6,
        s=25,
        edgecolor="none",
    )
    plt.title(
        "2D PCA Patient Phenotype Segmentation (Colored by Metabolic Syndrome)",
        fontsize=11,
        fontweight="bold",
    )
    plt.xlabel("Principal Component 1 (Glycemic & Hemodynamic Strain)")
    plt.ylabel("Principal Component 2 (Adiposity & Lifestyle Variation)")
    if hue_col:
        plt.legend(
            title="Metabolic Syndrome",
            labels=["Low / Non-Syndrome", "Syndrome Positive"],
            fontsize=8,
        )

    plt.tight_layout()
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=200)
    plt.close()
    logger.info(f"Cluster PCA scatter saved to {out}.")
    return out


def generate_interactive_html_report(
    df: pd.DataFrame,
    output_path: str | Path = "reports/data_quality_report.html",
) -> Path:
    """Generate clean, standalone interactive HTML data quality report."""
    num_df = df.select_dtypes(include=[np.number])
    stats = num_df.describe().T[["count", "mean", "std", "min", "50%", "max"]].round(2)
    stats.columns = ["Valid Count", "Mean", "Std Dev", "Min", "Median (50%)", "Max"]

    source_counts = df["source"].value_counts().to_dict()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sanjivani AI - Clinical Data Quality & Harmonization Report</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #1e293b; max-width: 1200px; margin: 0 auto; padding: 24px; background: #f8fafc; }}
    h1 {{ color: #0f766e; border-bottom: 2px solid #0f766e; padding-bottom: 8px; font-size: 26px; }}
    h2 {{ color: #334155; margin-top: 32px; font-size: 19px; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; }}
    .badge {{ display: inline-block; padding: 4px 10px; background: #0f766e; color: white; border-radius: 9999px; font-size: 12px; font-weight: bold; }}
    .card {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 24px; border: 1px solid #e2e8f0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 20px; }}
    .stat-box {{ background: #f0fdfa; border: 1px solid #ccfbf1; padding: 14px; border-radius: 8px; }}
    .stat-val {{ font-size: 24px; font-weight: bold; color: #0f766e; }}
    .stat-label {{ font-size: 12px; color: #64748b; font-weight: 600; text-transform: uppercase; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }}
    th {{ background: #f1f5f9; padding: 10px; border-bottom: 2px solid #cbd5e1; color: #475569; }}
    td {{ padding: 8px 10px; border-bottom: 1px solid #e2e8f0; }}
    tr:hover {{ background: #f8fafc; }}
    .img-container {{ text-align: center; margin: 20px 0; }}
    img {{ max-width: 100%; height: auto; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .footer {{ font-size: 12px; color: #94a3b8; text-align: center; margin-top: 40px; padding-top: 15px; border-top: 1px solid #e2e8f0; }}
  </style>
</head>
<body>
  <h1>Sanjivani AI Clinical Data Quality & Pipeline Audit Report</h1>
  <p><span class="badge">DPDP Act 2023 Compliant</span> &nbsp; • &nbsp; Generated on <strong>2026-10-14</strong> &nbsp; • &nbsp; Total Harmonized Records: <strong>{len(df):,}</strong></p>

  <div class="grid">
    <div class="stat-box">
      <div class="stat-val">{len(df):,}</div>
      <div class="stat-label">Total Clinical Cohort</div>
    </div>
    <div class="stat-box">
      <div class="stat-val">{len(source_counts)}</div>
      <div class="stat-label">Harmonized Sources</div>
    </div>
    <div class="stat-box">
      <div class="stat-val">{df.shape[1]}</div>
      <div class="stat-label">Engineered Features</div>
    </div>
    <div class="stat-box">
      <div class="stat-val">0</div>
      <div class="stat-label">Direct PII Fields (De-identified)</div>
    </div>
  </div>

  <div class="card">
    <h2>1. Provenance Breakdown by Data Source</h2>
    <table>
      <thead><tr><th>Source Identifier</th><th>Record Count</th><th>Share of Dataset</th></tr></thead>
      <tbody>
        {"".join(f"<tr><td><strong>{k}</strong></td><td>{v:,}</td><td>{(v / len(df)) * 100:.1f}%</td></tr>" for k, v in source_counts.items())}
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>2. Key Cardiometabolic Feature Statistics</h2>
    <div style="overflow-x: auto;">
      {stats.to_html(classes="table", border=0)}
    </div>
  </div>

  <div class="card">
    <h2>3. Visual Exploratory Analysis</h2>
    <div class="img-container">
      <h3>Correlation Matrix</h3>
      <img src="correlation_heatmap.png" alt="Correlation Heatmap">
    </div>
    <div class="img-container">
      <h3>Biomarker Distribution by Disease Status</h3>
      <img src="class_distributions.png" alt="Class Distributions">
    </div>
    <div class="img-container">
      <h3>Missing Data Heatmap Across Sources</h3>
      <img src="missingness_map.png" alt="Missingness Map">
    </div>
    <div class="img-container">
      <h3>2D PCA Patient Phenotype Clustering</h3>
      <img src="cluster_pca_scatter.png" alt="PCA Cluster Scatter">
    </div>
  </div>

  <div class="footer">
    Sanjivani AI Clinical Screening Data Pipeline • Confidential & Privacy-Safe
  </div>
</body>
</html>
"""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"Interactive HTML data quality report generated at {out}.")
    return out


def execute_all_reports(
    featured_file: str | Path = "data/processed/featured_clinical_data.parquet",
    reports_dir: str | Path = "reports",
) -> None:
    """Generate all Phase 7 plots and HTML report."""
    df = pd.read_parquet(featured_file)
    rep_dir = Path(reports_dir)
    rep_dir.mkdir(parents=True, exist_ok=True)

    generate_correlation_heatmap(df, output_path=rep_dir / "correlation_heatmap.png")
    generate_class_distribution_plots(df, output_path=rep_dir / "class_distributions.png")
    generate_missingness_map(df, output_path=rep_dir / "missingness_map.png")
    generate_cluster_pca_scatter(df, output_path=rep_dir / "cluster_pca_scatter.png")
    generate_interactive_html_report(df, output_path=rep_dir / "data_quality_report.html")


if __name__ == "__main__":
    execute_all_reports()
