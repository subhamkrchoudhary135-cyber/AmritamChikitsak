"""PDF Report generation endpoint using ReportLab."""

import io

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_current_user, get_db
from src.core.audit import audit_logger
from src.core.security import UserRole
from src.db.models import Patient, Screening, User

router = APIRouter(prefix="/reports", tags=["Reports"])


def build_screening_pdf(
    patient: Patient,
    screening: Screening,
    language: str = "en",
) -> bytes:
    """Generate professional clinical screening summary PDF with ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0D47A1"),
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#546E7A"),
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1A237E"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#263238"),
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Italic"],
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#C62828"),
    )

    story = []

    # 1. Header
    story.append(Paragraph("<b>Sanjivani AI Health Risk Screening Summary</b>", title_style))
    story.append(
        Paragraph(
            "AI-Powered Screening Support Platform | Grounded in ICMR, WHO & ADA Protocols",
            subtitle_style,
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D47A1"), spaceAfter=10)
    )

    # 2. Patient Demographics & Screening Metadata Table
    bio = screening.input_biometrics
    patient_data = [
        [
            Paragraph("<b>Patient Name:</b>", body_style),
            Paragraph(patient.full_name, body_style),
            Paragraph("<b>Screening ID:</b>", body_style),
            Paragraph(screening.id[:13] + "...", body_style),
        ],
        [
            Paragraph("<b>Age / Sex:</b>", body_style),
            Paragraph(f"{patient.age} yrs / {patient.gender.capitalize()}", body_style),
            Paragraph("<b>Screening Date:</b>", body_style),
            Paragraph(screening.created_at.strftime("%d-%b-%Y %H:%M UTC"), body_style),
        ],
        [
            Paragraph("<b>ABHA ID:</b>", body_style),
            Paragraph(patient.abha_id or "Not Registered", body_style),
            Paragraph("<b>Primary Language:</b>", body_style),
            Paragraph(language.upper(), body_style),
        ],
    ]
    t_patient = Table(patient_data, colWidths=[100, 165, 100, 165])
    t_patient.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F7FA")),
                ("PADDING", (0, 0), (-1, -1), 4),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CFD8DC")),
            ]
        )
    )
    story.append(t_patient)
    story.append(Spacer(1, 10))

    # 3. Biomarkers Table
    story.append(Paragraph("<b>Recorded Biometrics & Clinical Vitals</b>", section_heading))
    bio_data = [
        [
            "Systolic BP",
            f"{bio.get('systolic_bp')} mmHg",
            "Fasting Glucose",
            f"{bio.get('fasting_glucose')} mg/dL",
        ],
        [
            "Diastolic BP",
            f"{bio.get('diastolic_bp')} mmHg",
            "HbA1c",
            f"{bio.get('hba1c', 'N/A')} %",
        ],
        [
            "BMI",
            f"{bio.get('bmi')} kg/m²",
            "Total Cholesterol",
            f"{bio.get('total_cholesterol', 'N/A')} mg/dL",
        ],
        [
            "Activity",
            f"{bio.get('physical_activity_hours_per_week', 0)} hrs/wk",
            "Smoking Status",
            str(bio.get("smoking_status")).capitalize(),
        ],
    ]
    t_bio = Table(bio_data, colWidths=[120, 145, 120, 145])
    t_bio.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#ECEFF1")),
                ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#ECEFF1")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B0BEC5")),
                ("PADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t_bio)
    story.append(Spacer(1, 10))

    # 4. Multi-Condition Risk Assessment Table
    story.append(Paragraph("<b>Calibrated Risk Stratification</b>", section_heading))
    conds = screening.classification_results
    cond_rows = [
        [
            "Condition",
            "Calibrated Prob",
            "Risk Level",
            "Screened Status",
            "Clinical Guideline Category",
        ]
    ]

    for cond_key, res in conds.items():
        cond_rows.append(
            [
                res.get("condition_name", cond_key.title()),
                f"{float(res.get('calibrated_probability', 0)):.1%}",
                res.get("risk_level", "LOW"),
                "POSITIVE" if res.get("is_screened_positive") else "NEGATIVE",
                res.get("clinical_guideline_category", "N/A"),
            ]
        )

    t_cond = Table(cond_rows, colWidths=[90, 80, 80, 90, 190])
    t_cond.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1A237E")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B0BEC5")),
                ("ALIGN", (1, 0), (3, -1), "CENTER"),
                ("PADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t_cond)
    story.append(Spacer(1, 10))

    # 5. Regression Forecast & Trajectory
    fore = screening.regression_forecast
    story.append(Paragraph("<b>Biomarker Trajectory & 6-Month Prognosis</b>", section_heading))
    fore_text = (
        f"<b>Continuous Cardiometabolic Risk Index:</b> {fore.get('continuous_risk_score_100')}/100<br/>"
        f"<b>Forecasted Fasting Glucose (6 Months):</b> {fore.get('forecasted_glucose_6m')} mg/dL "
        f"(90% Conformal Prediction Interval: {fore.get('glucose_prediction_interval_6m', [0, 0])[0]} - {fore.get('glucose_prediction_interval_6m', [0, 0])[1]} mg/dL)<br/>"
        f"<b>Forecasted Systolic BP (6 Months):</b> {fore.get('forecasted_systolic_bp_6m')} mmHg<br/>"
        f"<b>Trajectory Assessment:</b> {fore.get('trend_description')}"
    )
    story.append(Paragraph(fore_text, body_style))
    story.append(Spacer(1, 10))

    # 6. Top 5 SHAP Explanations
    story.append(
        Paragraph("<b>Top Influential Risk Factors (Explainable AI - SHAP)</b>", section_heading)
    )
    shap_factors = screening.explainability_shap
    shap_rows = [["Factor", "Current Value", "Impact", "Clinical Guidance"]]
    for f in shap_factors[:5]:
        shap_rows.append(
            [
                f.get("feature_name_friendly", f.get("feature")),
                str(f.get("patient_value")),
                f.get("direction", "").replace("_", " ").title(),
                f.get("actionable_advice", ""),
            ]
        )

    t_shap = Table(shap_rows, colWidths=[120, 80, 80, 250])
    t_shap.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#37474F")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CFD8DC")),
                ("PADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(t_shap)
    story.append(Spacer(1, 14))

    # 7. Statutory Non-Diagnostic Clinical Disclaimer
    story.append(
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E57373"), spaceAfter=6)
    )
    story.append(Paragraph(screening.clinical_disclaimer, disclaimer_style))

    doc.build(story)
    return buffer.getvalue()


@router.get("/pdf")
async def generate_screening_report_pdf(
    screening_id: str = Query(..., description="Screening identifier"),
    language: str = Query("en", pattern="^(en|hi|pa)$"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate downloadable clinical screening summary PDF with ReportLab."""
    stmt = select(Screening).where(Screening.id == screening_id)
    screening = (await db.execute(stmt)).scalar_one_or_none()

    if not screening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Screening record not found"
        )

    stmt_pat = select(Patient).where(Patient.id == screening.patient_id)
    patient = (await db.execute(stmt_pat)).scalar_one_or_none()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Associated patient not found"
        )

    # Authorization
    if current_user.role == UserRole.PATIENT.value and patient.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    pdf_bytes = build_screening_pdf(patient, screening, language=language)

    audit_logger.log_event(
        action="PDF_REPORT_GENERATED",
        user_id=current_user.id,
        role=current_user.role,
        resource_type="REPORT_PDF",
        resource_id=screening_id,
        details={"language": language, "bytes": len(pdf_bytes)},
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename=Sanjivani AI_Screening_{screening_id[:8]}.pdf",
        },
    )
