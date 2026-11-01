"""
Front matter pages (Pages 1 to 10) for the expanded CGC Project Report.
Updated to reflect the expanded page budget (74 pages).
"""

import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle

from report_styles import (
    USABLE_WIDTH, USABLE_HEIGHT, LOGO_PATH, get_report_styles
)

styles = get_report_styles()

def page_01_cover():
    """Page 1: Outer Cover Page (Black Card with Gold Typography & CGC Logo)."""
    p = []
    p.append(Spacer(1, 15))
    p.append(Paragraph("A PROJECT REPORT ON", styles["CoverSubtitle"]))
    p.append(Spacer(1, 10))
    p.append(Paragraph("SANJIVANI AI: A PRODUCTION-GRADE EXPLAINABLE AND MULTILINGUAL AI HEALTH RISK SCREENING PLATFORM FOR INDIA", styles["CoverTitle"]))
    p.append(Spacer(1, 12))
    p.append(Paragraph("Submitted in partial fulfilment of the requirements for the award of the degree of", styles["CoverSubtitle"]))
    p.append(Spacer(1, 6))
    p.append(Paragraph("BACHELOR OF TECHNOLOGY", styles["CoverGold"]))
    p.append(Paragraph("IN", styles["CoverSubtitle"]))
    p.append(Paragraph("COMPUTER SCIENCE & ENGINEERING", styles["CoverGold"]))
    p.append(Spacer(1, 20))
    
    if os.path.exists(LOGO_PATH):
        p.append(Image(LOGO_PATH, width=170, height=74))
    p.append(Spacer(1, 22))
    
    details_data = [
        [
            Paragraph("<b>Submitted By:</b><br/><b>SUBHAM KUMAR CHOUDHARY</b><br/>University Roll No: <b>2555007</b><br/>B.Tech. CSE (3rd Semester)", styles["CoverDetails"]),
            Paragraph("<b>Under the Guidance of:</b><br/><b>PROJECT SUPERVISOR</b><br/>Assistant Professor<br/>Department of CSE, CEC", styles["CoverDetails"])
        ]
    ]
    t = Table(details_data, colWidths=[USABLE_WIDTH*0.5, USABLE_WIDTH*0.5])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    p.append(t)
    p.append(Spacer(1, 28))
    
    p.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", styles["CoverGold"]))
    p.append(Paragraph("CHANDIGARH ENGINEERING COLLEGE (CEC)", styles["CoverDetails"]))
    p.append(Paragraph("CGC LANDRAN, MOHALI - 140307, PUNJAB, INDIA", styles["CoverSubtitle"]))
    p.append(Paragraph("ACADEMIC SESSION: 2026–2027", styles["CoverSubtitle"]))
    return p

def page_02_inner_title():
    """Page 2: Inner Title Page (White card dissertation format)."""
    p = []
    p.append(Spacer(1, 10))
    p.append(Paragraph("A PROJECT REPORT ON", styles["InnerSub"]))
    p.append(Spacer(1, 8))
    p.append(Paragraph("SANJIVANI AI: A PRODUCTION-GRADE EXPLAINABLE AND MULTILINGUAL AI HEALTH RISK SCREENING PLATFORM FOR INDIA", styles["InnerTitle"]))
    p.append(Spacer(1, 10))
    p.append(Paragraph("Submitted in partial fulfilment of the requirements for the degree of", styles["InnerSub"]))
    p.append(Paragraph("<b>BACHELOR OF TECHNOLOGY</b><br/>in<br/><b>COMPUTER SCIENCE & ENGINEERING</b>", styles["InnerDetails"]))
    p.append(Spacer(1, 18))
    
    if os.path.exists(LOGO_PATH):
        p.append(Image(LOGO_PATH, width=160, height=70))
    p.append(Spacer(1, 20))
    
    details_data = [
        [
            Paragraph("<b>Submitted by:</b><br/><b>SUBHAM KUMAR CHOUDHARY</b><br/>Roll No: <b>2555007</b><br/>B.Tech. CSE (3rd Semester)", styles["InnerDetails"]),
            Paragraph("<b>Under the Supervision of:</b><br/><b>PROJECT SUPERVISOR</b><br/>Assistant Professor<br/>Department of CSE, CEC", styles["InnerDetails"])
        ]
    ]
    t = Table(details_data, colWidths=[USABLE_WIDTH*0.5, USABLE_WIDTH*0.5])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    p.append(t)
    p.append(Spacer(1, 25))
    
    p.append(Paragraph("<b>DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING</b>", styles["InnerDetails"]))
    p.append(Paragraph("<b>CHANDIGARH ENGINEERING COLLEGE (CEC)</b>", styles["InnerDetails"]))
    p.append(Paragraph("CGC LANDRAN, MOHALI, PUNJAB - 140307", styles["InnerSub"]))
    p.append(Paragraph("Affiliated to I.K. Gujral Punjab Technical University (IKGPTU), Jalandhar", styles["InnerSub"]))
    p.append(Paragraph("Academic Session: 2026–2027", styles["InnerSub"]))
    return p

def page_03_certificate():
    """Page 3: Certificate (Roman numeral i)."""
    p = []
    p.append(Spacer(1, 5))
    p.append(Paragraph("CHANDIGARH ENGINEERING COLLEGE (CEC)", ParagraphStyle('CertHead', fontName='Times-Bold', fontSize=13, alignment=TA_CENTER, textColor=colors.HexColor('#1e3a8a'))))
    p.append(Paragraph("CGC LANDRAN, MOHALI - 140307, PUNJAB", ParagraphStyle('CertSub', fontName='Times-Roman', fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor('#475569'))))
    p.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", ParagraphStyle('CertDept', fontName='Times-Bold', fontSize=11, alignment=TA_CENTER, textColor=colors.HexColor('#0f172a'))))
    p.append(Spacer(1, 10))
    p.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1e3a8a"), spaceAfter=12))
    
    p.append(Paragraph("CERTIFICATE", styles["FrontHeading"]))
    p.append(Spacer(1, 8))
    
    cert_text = (
        "This is to certify that the project report entitled <b>\"SANJIVANI AI: A PRODUCTION-GRADE "
        "EXPLAINABLE AND MULTILINGUAL AI HEALTH RISK SCREENING PLATFORM FOR INDIA\"</b> submitted by "
        "<b>SUBHAM KUMAR CHOUDHARY</b> (University Roll No. <b>2555007</b>) in partial fulfilment of "
        "the requirements for the award of the degree of <b>Bachelor of Technology in Computer Science & "
        "Engineering</b> from <b>Chandigarh Engineering College (CEC), CGC Landran, Mohali</b> affiliated "
        "to I.K. Gujral Punjab Technical University (IKGPTU), Jalandhar, is an authentic record of "
        "bonafide work carried out by him under my guidance and supervision during the academic session 2026–2027.<br/><br/>"
        "The matter embodied in this project report has not been submitted in part or full to any other "
        "university or institute for the award of any degree or diploma. The system adheres strictly to the "
        "non-diagnostic opportunistic screening boundary and complies with the ethical mandates of the Digital "
        "Personal Data Protection (DPDP) Act 2023."
    )
    p.append(Paragraph(cert_text, styles["ReportBody"]))
    p.append(Spacer(1, 45))
    
    sig_data = [
        [
            Paragraph("<b>Supervisor</b><br/>Assistant Professor<br/>Dept. of CSE, CEC Landran", styles["ReportBodyNoIndent"]),
            Paragraph("<b>Head of Department</b><br/>Dept. of CSE<br/>CEC Landran, Mohali", styles["ReportBodyNoIndent"]),
            Paragraph("<b>External Examiner</b><br/>External Evaluator<br/>IKGPTU, Jalandhar", styles["ReportBodyNoIndent"])
        ]
    ]
    st = Table(sig_data, colWidths=[USABLE_WIDTH*0.33, USABLE_WIDTH*0.34, USABLE_WIDTH*0.33])
    st.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LINEABOVE', (0,0), (-1,-1), 0.8, colors.HexColor('#64748b')),
    ]))
    p.append(st)
    return p

def page_04_acknowledgement():
    """Page 4: Acknowledgement (Roman numeral ii)."""
    p = []
    p.append(Spacer(1, 5))
    p.append(Paragraph("ACKNOWLEDGEMENT", styles["FrontHeading"]))
    p.append(Spacer(1, 10))
    
    ack_1 = (
        "I express my profound gratitude and deepest reverence to our esteemed <b>Director-Principal</b>, "
        "Chandigarh Engineering College (CEC), CGC Landran, Mohali, for providing state-of-the-art computational "
        "infrastructure, laboratory amenities, and an inspiring academic milieu that nurtured this engineering undertaking."
    )
    p.append(Paragraph(ack_1, styles["ReportBody"]))
    
    ack_2 = (
        "I am immensely indebted to the <b>Head of the Department of Computer Science & Engineering</b>, "
        "for continuous administrative encouragement, visionary academic leadership, and for sanctioning "
        "the advanced machine learning research resources necessary to realize this project."
    )
    p.append(Paragraph(ack_2, styles["ReportBody"]))
    
    ack_3 = (
        "Words fall short of conveying my heartfelt gratitude to my revered <b>Project Supervisor</b>, "
        "Assistant Professor, Department of Computer Science & Engineering, whose insightful counsel, "
        "rigorous technical scrutiny, and relentless encouragement steered this project from conceptual "
        "formulation through empirical clinical validation. His domain expertise in distributed machine learning "
        "and data engineering proved indispensable in resolving subtle architectural and epidemiological hurdles."
    )
    p.append(Paragraph(ack_3, styles["ReportBody"]))
    
    ack_4 = (
        "I also extend my sincere appreciation to the faculty members and technical staff of the CSE Department "
        "for their constructive feedback during project milestone reviews. Special thanks are due to my peers "
        "and colleagues who assisted in usability evaluations, multi-dialect linguistic reviews (Hindi and Punjabi), "
        "and stress-testing the low-bandwidth Progressive Web App interface."
    )
    p.append(Paragraph(ack_4, styles["ReportBody"]))
    
    ack_5 = (
        "Lastly, I bow my head in reverence to my beloved parents and family members, whose unconditional sacrifices, "
        "unwavering prayers, and perpetual emotional backing have been my pillar of strength throughout my engineering journey."
    )
    p.append(Paragraph(ack_5, styles["ReportBody"]))
    p.append(Spacer(1, 25))
    
    p.append(Paragraph("<b>SUBHAM KUMAR CHOUDHARY</b><br/>University Roll No: <b>2555007</b><br/>B.Tech. Computer Science & Engineering (3rd Semester)<br/>Chandigarh Engineering College, CGC Landran, Mohali", styles["ReportBodyNoIndent"]))
    return p

def page_05_abstract():
    """Page 5: Abstract (Roman numeral iii)."""
    p = []
    p.append(Spacer(1, 5))
    p.append(Paragraph("ABSTRACT", styles["FrontHeading"]))
    p.append(Spacer(1, 8))
    
    abs_1 = (
        "Cardiovascular diseases, Type 2 Diabetes, and hypertension constitute the primary epidemiological crisis "
        "confronting 21st-century India. According to landmark findings from the ICMR-INDIAB national study (2023), "
        "an estimated 101.3 million individuals in India suffer from diabetes, 136.0 million manifest pre-diabetes, "
        "and over 315.5 million live with hypertension. Over 50% of cardiometabolic morbidity remains clinically "
        "undiagnosed until acute organ damage occurs, primarily attributable to the acute shortage of healthcare "
        "practitioners across tier-2/3 cities and rural districts, coupled with linguistic barriers and low health literacy. "
        "While digital health applications exist, they predominantly operate as proprietary black-boxes, assume high English "
        "literacy, require continuous broadband connectivity, or dangerously blur the statutory boundary between clinical "
        "triage screening and licensed medical diagnosis."
    )
    p.append(Paragraph(abs_1, styles["ReportBody"]))
    
    abs_2 = (
        "This project presents <b>Sanjivani AI</b>, an open, production-grade, explainable, and multilingual AI health risk "
        "screening platform engineered specifically for the socio-demographic realities of India. Architected upon a decoupled "
        "microservice backbone comprising FastAPI (Python 3.11), SQLAlchemy 2 Async, PostgreSQL 16, Redis 7.2, and Celery, the platform "
        "ingests multi-cohort clinical datasets spanning UCI Heart Disease, Pima Indians Diabetes, NHANES, CDC BRFSS, Framingham, "
        "and Kaggle CKD. The clinical engineering pipeline enforces strict Pandera schema invariant validation, MICE imputation "
        "via Bayesian Ridge, Isolation Forest outlier mitigation, and Asian-Indian biomarker recalibration (BMI categories: "
        "normal 18.5–22.9 kg/m², overweight 23.0–24.9 kg/m², obese ≥25.0 kg/m²; Mean Arterial Pressure; Waist-to-Height Ratio)."
    )
    p.append(Paragraph(abs_2, styles["ReportBody"]))
    
    abs_3 = (
        "Predictive screening employs a multi-model Stacking Ensemble combining Tuned XGBoost, LightGBM, CatBoost, Random Forest, "
        "and RBF SVM behind a Platt-calibrated Logistic Regression meta-learner. On holdout stratified test sets, the ensemble "
        "achieves a ROC-AUC of <b>0.892 ± 0.015</b>, PR-AUC of <b>0.784 ± 0.021</b>, screening sensitivity (recall) of <b>91.5%</b>, "
        "and a calibrated Brier score loss of <b>0.108</b>. Multi-horizon progression trajectories (3-to-6 month forecasts) are generated "
        "via pinball quantile regression, wrapped in non-parametric Conformal Prediction intervals yielding <b>91.2%</b> empirical marginal "
        "coverage. Local explainability is delivered through TreeSHAP attributions converted into 8th-grade reading level narratives, "
        "grounded in ICMR 2023 and WHO-PEN clinical guidelines via Retrieval-Augmented Generation (RAG). Real-time emergency guardrails "
        "instantly bypass screening to initiate 112/108 routing upon detecting acute distress. Delivered through an offline-first "
        "Next.js 14 Progressive Web App (PWA) with voice dictation across English, Hindi, and Punjabi, Sanjivani AI demonstrates "
        "sub-180ms p95 latency, 100% WCAG 2.1 AA accessibility, and full compliance with the Digital Personal Data Protection (DPDP) Act 2023."
    )
    p.append(Paragraph(abs_3, styles["ReportBody"]))
    p.append(Spacer(1, 10))
    p.append(Paragraph("<b>Keywords:</b> Health Risk Screening, Explainable AI (XAI), SHAP, Stacking Ensemble, Conformal Prediction, Pandera, FastAPI, Next.js PWA, ICMR-INDIAB, DPDP Act 2023, Multilingual Healthcare.", styles["ReportBodyNoIndent"]))
    return p

def page_06_toc_1():
    """Page 6: Table of Contents - Part 1 (Roman numeral iv)."""
    p = []
    p.append(Spacer(1, 4))
    p.append(Paragraph("TABLE OF CONTENTS", styles["FrontHeading"]))
    p.append(Spacer(1, 6))
    
    toc_data = [
        [Paragraph("<b>Topic / Section</b>", styles["TOCLineBold"]), Paragraph("<b>Page No.</b>", styles["TOCLineBold"])],
        [Paragraph("<b>Certificate</b>", styles["TOCLineBold"]), Paragraph("i", styles["TOCLineBold"])],
        [Paragraph("<b>Acknowledgement</b>", styles["TOCLineBold"]), Paragraph("ii", styles["TOCLineBold"])],
        [Paragraph("<b>Abstract</b>", styles["TOCLineBold"]), Paragraph("iii", styles["TOCLineBold"])],
        [Paragraph("<b>List of Tables</b>", styles["TOCLineBold"]), Paragraph("vi", styles["TOCLineBold"])],
        [Paragraph("<b>List of Figures</b>", styles["TOCLineBold"]), Paragraph("vii", styles["TOCLineBold"])],
        [Paragraph("<b>Abbreviations and Nomenclature</b>", styles["TOCLineBold"]), Paragraph("viii", styles["TOCLineBold"])],
        [Paragraph("<b>CHAPTER 1: INTRODUCTION</b>", styles["TOCLineBold"]), Paragraph("<b>1</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.1 Background and Societal Motivation", styles["TOCLine"]), Paragraph("1", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.2 The Non-Diagnostic AI Health Screening Paradigm", styles["TOCLine"]), Paragraph("1", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.3 Key Epidemiological Challenges in the Indian Healthcare Ecosystem", styles["TOCLine"]), Paragraph("2", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.4 Problem Statement and Formal Project Objectives", styles["TOCLine"]), Paragraph("3", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.5 Scope, Clinical Boundaries, and Regulatory Delimitation", styles["TOCLine"]), Paragraph("4", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1.6 Report Organisation", styles["TOCLine"]), Paragraph("4", styles["TOCLine"])],
        [Paragraph("<b>CHAPTER 2: LITERATURE SURVEY & THEORETICAL FRAMEWORK</b>", styles["TOCLineBold"]), Paragraph("<b>5</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.1 Critical Review of Traditional Epidemiological Scoring Systems", styles["TOCLine"]), Paragraph("5", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.2 Survey of Contemporary Digital Health Platforms", styles["TOCLine"]), Paragraph("6", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.3 The Explainability Deficit in Clinical Decision Support Systems", styles["TOCLine"]), Paragraph("7", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.4 Legal and Ethical Compliance: The DPDP Act 2023", styles["TOCLine"]), Paragraph("7", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2.5 Comparative Analysis & Research Gap Identification", styles["TOCLine"]), Paragraph("8", styles["TOCLine"])],
        [Paragraph("<b>CHAPTER 3: SYSTEM ARCHITECTURE & REQUIREMENTS</b>", styles["TOCLineBold"]), Paragraph("<b>10</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.1 High-Level Microservice Architectural Design", styles["TOCLine"]), Paragraph("10", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.2 Asynchronous Backend Engine (FastAPI & SQLAlchemy 2)", styles["TOCLine"]), Paragraph("11", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.3 Distributed Task Queuing & Job Orchestration (Celery & Redis)", styles["TOCLine"]), Paragraph("12", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.4 Relational Persistence & Schema Migrations (PostgreSQL & Alembic)", styles["TOCLine"]), Paragraph("13", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.5 Security Architecture, JWT RBAC, and Audit Logging", styles["TOCLine"]), Paragraph("14", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3.6 Low-Bandwidth Optimization & PWA Standards", styles["TOCLine"]), Paragraph("14", styles["TOCLine"])],
        [Paragraph("<b>CHAPTER 4: CLINICAL DATA ENGINEERING & PIPELINES</b>", styles["TOCLineBold"]), Paragraph("<b>15</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.1 Diverse Multi-Cohort Clinical Datasets", styles["TOCLine"]), Paragraph("15", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2 Canonical Schema Definition & Unit Standardization Engine", styles["TOCLine"]), Paragraph("16", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.2.1 Executed Pipeline Step: Multi-Source Ingestion & DVC Tracking", styles["TOCLineBold"]), Paragraph("<b>17</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.3 Data Validation & Quality Invariants via Pandera", styles["TOCLine"]), Paragraph("18", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4 Missing Value Imputation (MICE) & Outlier Mitigation", styles["TOCLine"]), Paragraph("19", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.4.1 Executed Pipeline Step: Pandera Validation & Resampling", styles["TOCLineBold"]), Paragraph("<b>20</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.5 Clinically Derived Biomarker Engineering", styles["TOCLine"]), Paragraph("21", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4.6 Leakage-Safe Splitting, Resampling & Feature Store", styles["TOCLine"]), Paragraph("22", styles["TOCLine"])]
    ]
    t = Table(toc_data, colWidths=[USABLE_WIDTH*0.88, USABLE_WIDTH*0.12])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor('#0f172a')),
    ]))
    p.append(t)
    return p

def page_07_toc_2():
    """Page 7: Table of Contents - Part 2 (Roman numeral v)."""
    p = []
    p.append(Spacer(1, 4))
    p.append(Paragraph("TABLE OF CONTENTS (CONTD.)", styles["FrontHeading"]))
    p.append(Spacer(1, 6))
    
    toc_data = [
        [Paragraph("<b>Topic / Section</b>", styles["TOCLineBold"]), Paragraph("<b>Page No.</b>", styles["TOCLineBold"])],
        [Paragraph("<b>CHAPTER 5: MACHINE LEARNING MODELS & PREDICTIVE FRAMEWORK</b>", styles["TOCLineBold"]), Paragraph("<b>23</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.1 Formulation of Supervised Disease Risk Screening", styles["TOCLine"]), Paragraph("23", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.2 Algorithmic Spectrum: Base Supervised Learners", styles["TOCLine"]), Paragraph("24", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3 Stacking Meta-Ensemble Architecture & CV Strategy", styles["TOCLine"]), Paragraph("25", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.3.1 Executed Pipeline Step: Multi-Model Training & 5-Fold CV", styles["TOCLineBold"]), Paragraph("<b>26</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.4 Bayesian Hyperparameter Optimization with Optuna", styles["TOCLine"]), Paragraph("27", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.5 Quantitative Progression Forecasting via Quantile Regression", styles["TOCLine"]), Paragraph("28", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.4.1 Executed Pipeline Step: Regression Forecasting & Conformal Bands", styles["TOCLineBold"]), Paragraph("<b>29</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.6 Unsupervised Patient Phenotype Segmentation via K-Means", styles["TOCLine"]), Paragraph("30", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5.6.1 Executed Pipeline Step: Clustering & Isolation Forest Anomaly", styles["TOCLineBold"]), Paragraph("<b>31</b>", styles["TOCLineBold"])],
        [Paragraph("<b>CHAPTER 6: EXPLAINABLE AI, SAFETY & MULTILINGUAL ENGINE</b>", styles["TOCLineBold"]), Paragraph("<b>32</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.1 SHAP-Based Feature Attribution & Local Explainability", styles["TOCLine"]), Paragraph("32", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.2 Plain-Language Translation Engine (8th-Grade Reading Level)", styles["TOCLine"]), Paragraph("33", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.2.1 Executed Pipeline Step: TreeSHAP Attribution & Fairlearn Audit", styles["TOCLineBold"]), Paragraph("<b>34</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.3 Retrieval-Augmented Generation (RAG) Guardrails via ICMR/WHO", styles["TOCLine"]), Paragraph("35", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.4 Real-Time Emergency Red-Flag Triage & Escalation Protocol", styles["TOCLine"]), Paragraph("36", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.4.1 Executed Pipeline Step: Multilingual RAG & Safety Guardrail", styles["TOCLineBold"]), Paragraph("<b>37</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;6.5 Multilingual Interaction Engine with Web Speech API", styles["TOCLine"]), Paragraph("38", styles["TOCLine"])],
        [Paragraph("<b>CHAPTER 7: FRONTEND ARCHITECTURE & UX DESIGN</b>", styles["TOCLineBold"]), Paragraph("<b>39</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.1 Next.js 14 App Router Framework & TypeScript State Management", styles["TOCLine"]), Paragraph("39", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.2 Mobile-First Medical UI/UX Design System", styles["TOCLine"]), Paragraph("40", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.2.1 Executed Pipeline Step: Containerized Microservices & Celery", styles["TOCLineBold"]), Paragraph("<b>41</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.3 Step-by-Step Adaptive Biometric Assessment Workflow", styles["TOCLine"]), Paragraph("42", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.4 OCR Lab Report Digitisation & Patient Confirmation Flow", styles["TOCLine"]), Paragraph("43", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;7.5 Offline PWA Capabilities & Teleconsultation Redirection", styles["TOCLine"]), Paragraph("44", styles["TOCLine"])],
        [Paragraph("<b>CHAPTER 8: SYSTEM EXECUTION & EXPERIMENTAL RESULTS</b>", styles["TOCLineBold"]), Paragraph("<b>45</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.1 Executed System Results & Operational Workflows (Screenshots 8.1–8.14)", styles["TOCLineBold"]), Paragraph("<b>45</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.2 Quantitative Classification Performance Across Test Sets", styles["TOCLine"]), Paragraph("59", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.3 Probability Calibration Analysis & Reliability Diagrams", styles["TOCLine"]), Paragraph("61", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.4 Conformal Prediction Coverage & Dynamic Uncertainty Bounds", styles["TOCLine"]), Paragraph("62", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.5 Algorithmic Fairness & Demographic Subgroup Audit", styles["TOCLine"]), Paragraph("63", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.6 Model Drift Detection & Statistical Governance Analysis", styles["TOCLine"]), Paragraph("64", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;8.7 System Latency, Throughput & WCAG AA Accessibility Audit", styles["TOCLine"]), Paragraph("65", styles["TOCLine"])],
        [Paragraph("<b>CHAPTER 9: CONCLUSION & FUTURE SCOPE</b>", styles["TOCLineBold"]), Paragraph("<b>66</b>", styles["TOCLineBold"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.1 Summary of Key Technical Achievements", styles["TOCLine"]), Paragraph("66", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.2 Clinical Boundaries, Ethical Limitations, and Legal Disclaimers", styles["TOCLine"]), Paragraph("67", styles["TOCLine"])],
        [Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;9.3 Strategic Roadmap: ABDM, Edge AI & Multilingual Expansion", styles["TOCLine"]), Paragraph("68", styles["TOCLine"])],
        [Paragraph("<b>REFERENCES</b>", styles["TOCLineBold"]), Paragraph("<b>69</b>", styles["TOCLineBold"])],
        [Paragraph("<b>APPENDIX A: CANONICAL SCHEMAS & API SPECIFICATIONS</b>", styles["TOCLineBold"]), Paragraph("<b>71</b>", styles["TOCLineBold"])],
        [Paragraph("<b>APPENDIX B: MATHEMATICAL FORMULATIONS & HYPERPARAMETERS</b>", styles["TOCLineBold"]), Paragraph("<b>72</b>", styles["TOCLineBold"])]
    ]
    t = Table(toc_data, colWidths=[USABLE_WIDTH*0.88, USABLE_WIDTH*0.12])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.0),
        ('TOPPADDING', (0,0), (-1,-1), 1.0),
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor('#0f172a')),
    ]))
    p.append(t)
    return p

def page_08_list_of_tables():
    """Page 8: List of Tables (Roman numeral vi)."""
    p = []
    p.append(Spacer(1, 4))
    p.append(Paragraph("LIST OF TABLES", styles["FrontHeading"]))
    p.append(Spacer(1, 8))
    
    tables_data = [
        [Paragraph("<b>Table No.</b>", styles["TOCLineBold"]), Paragraph("<b>Table Title</b>", styles["TOCLineBold"]), Paragraph("<b>Page No.</b>", styles["TOCLineBold"])],
        [Paragraph("Table 1.1", styles["TOCLineBold"]), Paragraph("Epidemiological Distribution of NCDs in India (ICMR-INDIAB Study)", styles["TOCLine"]), Paragraph("2", styles["TOCLine"])],
        [Paragraph("Table 2.1", styles["TOCLineBold"]), Paragraph("Comprehensive Comparative Feature Matrix: Digital Health Platforms vs. Sanjivani AI", styles["TOCLine"]), Paragraph("8", styles["TOCLine"])],
        [Paragraph("Table 3.1", styles["TOCLineBold"]), Paragraph("Non-Functional System Performance Requirements & Clinical SLA Thresholds", styles["TOCLine"]), Paragraph("13", styles["TOCLine"])],
        [Paragraph("Table 3.2", styles["TOCLineBold"]), Paragraph("Core REST API Microservice Endpoint Route Specifications", styles["TOCLine"]), Paragraph("14", styles["TOCLine"])],
        [Paragraph("Table 4.1", styles["TOCLineBold"]), Paragraph("Multi-Cohort Source Clinical Datasets & Demographic Distribution", styles["TOCLine"]), Paragraph("15", styles["TOCLine"])],
        [Paragraph("Table 4.2", styles["TOCLineBold"]), Paragraph("Canonical Clinical Feature Dictionary & Physiological Verification Bounds", styles["TOCLine"]), Paragraph("16", styles["TOCLine"])],
        [Paragraph("Table 5.1", styles["TOCLineBold"]), Paragraph("Comparative Classifier Performance on Multi-Cohort Validation Set", styles["TOCLine"]), Paragraph("24", styles["TOCLine"])],
        [Paragraph("Table 5.2", styles["TOCLineBold"]), Paragraph("Optuna Hyperparameter Search Spaces and Optimal Configurations", styles["TOCLine"]), Paragraph("27", styles["TOCLine"])],
        [Paragraph("Table 6.1", styles["TOCLineBold"]), Paragraph("Plain-Language Clinical Feature Explanations Across English, Hindi, and Punjabi", styles["TOCLine"]), Paragraph("33", styles["TOCLine"])],
        [Paragraph("Table 6.2", styles["TOCLineBold"]), Paragraph("Emergency Red-Flag Clinical Triggers and Dynamic Escalation Protocols", styles["TOCLine"]), Paragraph("36", styles["TOCLine"])],
        [Paragraph("Table 7.1", styles["TOCLineBold"]), Paragraph("Frontend Performance Benchmarks, Asset Budgets, and Lighthouse Audit", styles["TOCLine"]), Paragraph("44", styles["TOCLine"])],
        [Paragraph("Table 8.1", styles["TOCLineBold"]), Paragraph("Comprehensive Multi-Disease Classification Performance Across Test Sets", styles["TOCLine"]), Paragraph("59", styles["TOCLine"])],
        [Paragraph("Table 8.2", styles["TOCLineBold"]), Paragraph("Brier Score Loss & Probability Calibration Improvements via Platt Scaling", styles["TOCLine"]), Paragraph("61", styles["TOCLine"])],
        [Paragraph("Table 8.3", styles["TOCLineBold"]), Paragraph("Demographic Parity & Algorithmic Fairness Audit Across Sensitive Subgroups", styles["TOCLine"]), Paragraph("63", styles["TOCLine"])],
        [Paragraph("Table 8.4", styles["TOCLineBold"]), Paragraph("System Latency, Memory Footprint, and Throughput Under Concurrency Load", styles["TOCLine"]), Paragraph("65", styles["TOCLine"])]
    ]
    t = Table(tables_data, colWidths=[USABLE_WIDTH*0.16, USABLE_WIDTH*0.72, USABLE_WIDTH*0.12])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor('#0f172a')),
        ('LINEBELOW', (0,1), (-1,-1), 0.4, colors.HexColor('#e2e8f0')),
    ]))
    p.append(t)
    return p

def page_09_list_of_figures():
    """Page 9: List of Figures (Roman numeral vii)."""
    p = []
    p.append(Spacer(1, 3))
    p.append(Paragraph("LIST OF FIGURES", styles["FrontHeading"]))
    p.append(Spacer(1, 5))
    
    figures_data = [
        [Paragraph("<b>Fig. No.</b>", styles["TOCLineBold"]), Paragraph("<b>Figure Title & Description</b>", styles["TOCLineBold"]), Paragraph("<b>Page No.</b>", styles["TOCLineBold"])],
        [Paragraph("Fig. 1.1", styles["TOCLineBold"]), Paragraph("Epidemiological Burden of Cardiometabolic Conditions in India (ICMR-INDIAB)", styles["TOCLine"]), Paragraph("2", styles["TOCLine"])],
        [Paragraph("Fig. 3.1", styles["TOCLineBold"]), Paragraph("Complete End-to-End Microservice Architecture of Sanjivani AI Platform", styles["TOCLine"]), Paragraph("10", styles["TOCLine"])],
        [Paragraph("Fig. 3.2", styles["TOCLineBold"]), Paragraph("Asynchronous Distributed Screening Pipeline Flowchart (FastAPI, Redis, Celery)", styles["TOCLine"]), Paragraph("12", styles["TOCLine"])],
        [Paragraph("Fig. 4.1", styles["TOCLineBold"]), Paragraph("Missingness Map Across Multi-Cohort Clinical Datasets Prior to MICE Imputation", styles["TOCLine"]), Paragraph("19", styles["TOCLine"])],
        [Paragraph("Fig. 4.2", styles["TOCLineBold"]), Paragraph("Pairwise Correlation Heatmap of Standardized Clinical Biomarkers", styles["TOCLine"]), Paragraph("21", styles["TOCLine"])],
        [Paragraph("Fig. 4.3", styles["TOCLineBold"]), Paragraph("Class Distribution and SMOTE-NC Resampling Balance Across Disease Targets", styles["TOCLine"]), Paragraph("22", styles["TOCLine"])],
        [Paragraph("Fig. 4.4", styles["TOCLineBold"]), Paragraph("Executed Step 1: Python Multi-Source Ingestion & DVC Versioning Pipeline", styles["TOCLineBold"]), Paragraph("<b>17</b>", styles["TOCLineBold"])],
        [Paragraph("Fig. 4.5", styles["TOCLineBold"]), Paragraph("Executed Step 2: Pandera Schema Validation, MICE & SMOTE-NC Resampling", styles["TOCLineBold"]), Paragraph("<b>20</b>", styles["TOCLineBold"])],
        [Paragraph("Fig. 5.1", styles["TOCLineBold"]), Paragraph("Multi-Model Stacking Ensemble Architecture with Calibrated Meta-Learner", styles["TOCLine"]), Paragraph("25", styles["TOCLine"])],
        [Paragraph("Fig. 5.2", styles["TOCLineBold"]), Paragraph("Patient Phenotype Segmentation via 2D Principal Component Projection (K-Means)", styles["TOCLine"]), Paragraph("30", styles["TOCLine"])],
        [Paragraph("Fig. 5.3", styles["TOCLineBold"]), Paragraph("Executed Step 3: Multi-Model Classifier Training & 5-Fold Cross-Validation", styles["TOCLineBold"]), Paragraph("<b>26</b>", styles["TOCLineBold"])],
        [Paragraph("Fig. 5.4", styles["TOCLineBold"]), Paragraph("Executed Step 4: Progression Forecasting & MAPIE Conformal Intervals", styles["TOCLineBold"]), Paragraph("<b>29</b>", styles["TOCLineBold"])],
        [Paragraph("Fig. 5.5", styles["TOCLineBold"]), Paragraph("Executed Step 5: Patient Phenotype Clustering & Isolation Forest Outlier Detection", styles["TOCLineBold"]), Paragraph("<b>31</b>", styles["TOCLineBold"])],
        [Paragraph("Fig. 6.1", styles["TOCLineBold"]), Paragraph("Local Feature Attribution (SHAP Waterfall Plot) for High-Risk Diabetes Screening", styles["TOCLine"]), Paragraph("32", styles["TOCLine"])],
        [Paragraph("Fig. 6.2", styles["TOCLineBold"]), Paragraph("Dual-Channel Real-Time Emergency Red-Flag Triage & Escalation Workflow", styles["TOCLine"]), Paragraph("36", styles["TOCLine"])],
        [Paragraph("Fig. 6.3", styles["TOCLineBold"]), Paragraph("Executed Step 6: TreeSHAP Feature Attribution & Fairlearn Fairness Audit", styles["TOCLineBold"]), Paragraph("<b>34</b>", styles["TOCLineBold"])],
        [Paragraph("Fig. 6.4", styles["TOCLineBold"]), Paragraph("Executed Step 7: Multilingual LLM RAG & Clinical Safety Guardrail Pipeline", styles["TOCLineBold"]), Paragraph("<b>37</b>", styles["TOCLineBold"])],
        [Paragraph("Fig. 7.1", styles["TOCLineBold"]), Paragraph("Executed Step 8: Containerized Microservices, Celery Worker & Redis Task Queue", styles["TOCLineBold"]), Paragraph("<b>41</b>", styles["TOCLineBold"])],
        [Paragraph("Fig. 8.1–8.14", styles["TOCLineBold"]), Paragraph("Executed System Screenshots (Swagger, PyTest, UI, Gauges, SHAP, EHR, MLOps)", styles["TOCLineBold"]), Paragraph("<b>45–58</b>", styles["TOCLineBold"])],
        [Paragraph("Fig. 8.15", styles["TOCLineBold"]), Paragraph("Comparative Screening Performance Curves: Receiver Operating Characteristic & PR", styles["TOCLine"]), Paragraph("59", styles["TOCLine"])],
        [Paragraph("Fig. 8.16", styles["TOCLineBold"]), Paragraph("Calibration Curve & Reliability Diagram for Raw vs. Platt-Scaled Diabetes Model", styles["TOCLine"]), Paragraph("61", styles["TOCLine"])],
        [Paragraph("Fig. 8.17", styles["TOCLineBold"]), Paragraph("Non-Parametric Conformal Prediction Uncertainty Bounds (91.2% Coverage)", styles["TOCLine"]), Paragraph("62", styles["TOCLine"])],
        [Paragraph("Fig. 8.18", styles["TOCLineBold"]), Paragraph("Algorithmic Fairness & Subgroup Parity Audit Across Gender and Age Demographics", styles["TOCLine"]), Paragraph("63", styles["TOCLine"])]
    ]
    t = Table(figures_data, colWidths=[USABLE_WIDTH*0.16, USABLE_WIDTH*0.72, USABLE_WIDTH*0.12])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor('#0f172a')),
        ('LINEBELOW', (0,1), (-1,-1), 0.3, colors.HexColor('#f1f5f9')),
    ]))
    p.append(t)
    return p

def page_10_abbreviations():
    """Page 10: Nomenclature & Abbreviations (Roman numeral viii)."""
    p = []
    p.append(Spacer(1, 5))
    p.append(Paragraph("ABBREVIATIONS AND NOMENCLATURE", styles["FrontHeading"]))
    p.append(Spacer(1, 8))
    
    abbr_data = [
        [Paragraph("<b>Acronym</b>", styles["TOCLineBold"]), Paragraph("<b>Full Form / Definition</b>", styles["TOCLineBold"]), Paragraph("<b>Domain</b>", styles["TOCLineBold"])],
        [Paragraph("ABDM", styles["TOCLineBold"]), Paragraph("Ayushman Bharat Digital Mission", styles["TOCLine"]), Paragraph("Healthcare / Policy", styles["TOCLine"])],
        [Paragraph("ABHA", styles["TOCLineBold"]), Paragraph("Ayushman Bharat Health Account", styles["TOCLine"]), Paragraph("Healthcare / Policy", styles["TOCLine"])],
        [Paragraph("ADA", styles["TOCLineBold"]), Paragraph("American Diabetes Association", styles["TOCLine"]), Paragraph("Clinical Guideline", styles["TOCLine"])],
        [Paragraph("AIP", styles["TOCLineBold"]), Paragraph("Atherogenic Index of Plasma (log(TG/HDL))", styles["TOCLine"]), Paragraph("Biomarker", styles["TOCLine"])],
        [Paragraph("API", styles["TOCLineBold"]), Paragraph("Application Programming Interface", styles["TOCLine"]), Paragraph("Software Engineering", styles["TOCLine"])],
        [Paragraph("BMI", styles["TOCLineBold"]), Paragraph("Body Mass Index (Weight in kg / Height in m²)", styles["TOCLine"]), Paragraph("Biometric", styles["TOCLine"])],
        [Paragraph("BRFSS", styles["TOCLineBold"]), Paragraph("Behavioral Risk Factor Surveillance System (CDC)", styles["TOCLine"]), Paragraph("Public Health Dataset", styles["TOCLine"])],
        [Paragraph("CAD", styles["TOCLineBold"]), Paragraph("Coronary Artery Disease", styles["TOCLine"]), Paragraph("Clinical Cardiology", styles["TOCLine"])],
        [Paragraph("CKD", styles["TOCLineBold"]), Paragraph("Chronic Kidney Disease", styles["TOCLine"]), Paragraph("Clinical Nephrology", styles["TOCLine"])],
        [Paragraph("CV", styles["TOCLineBold"]), Paragraph("Cross-Validation", styles["TOCLine"]), Paragraph("Machine Learning", styles["TOCLine"])],
        [Paragraph("DPDP", styles["TOCLineBold"]), Paragraph("Digital Personal Data Protection Act 2023 (India)", styles["TOCLine"]), Paragraph("Statutory Compliance", styles["TOCLine"])],
        [Paragraph("FBS / FPG", styles["TOCLineBold"]), Paragraph("Fasting Blood Sugar / Fasting Plasma Glucose", styles["TOCLine"]), Paragraph("Clinical Biomarker", styles["TOCLine"])],
        [Paragraph("HbA1c", styles["TOCLineBold"]), Paragraph("Glycated Hemoglobin (3-Month Glycemic Average)", styles["TOCLine"]), Paragraph("Clinical Biomarker", styles["TOCLine"])],
        [Paragraph("HDL / LDL", styles["TOCLineBold"]), Paragraph("High-Density / Low-Density Lipoprotein Cholesterol", styles["TOCLine"]), Paragraph("Clinical Lipidology", styles["TOCLine"])],
        [Paragraph("ICMR", styles["TOCLineBold"]), Paragraph("Indian Council of Medical Research", styles["TOCLine"]), Paragraph("Clinical Authority", styles["TOCLine"])],
        [Paragraph("IDRS", styles["TOCLineBold"]), Paragraph("Indian Diabetes Risk Score (Madras Diabetes Research)", styles["TOCLine"]), Paragraph("Clinical Screening", styles["TOCLine"])],
        [Paragraph("MAP", styles["TOCLineBold"]), Paragraph("Mean Arterial Pressure (DBP + 1/3(SBP - DBP))", styles["TOCLine"]), Paragraph("Hemodynamic Metric", styles["TOCLine"])],
        [Paragraph("MICE", styles["TOCLineBold"]), Paragraph("Multivariate Imputation by Chained Equations", styles["TOCLine"]), Paragraph("Data Engineering", styles["TOCLine"])],
        [Paragraph("NCD", styles["TOCLineBold"]), Paragraph("Non-Communicable Disease", styles["TOCLine"]), Paragraph("Epidemiology", styles["TOCLine"])],
        [Paragraph("NHANES", styles["TOCLineBold"]), Paragraph("National Health and Nutrition Examination Survey", styles["TOCLine"]), Paragraph("Clinical Dataset", styles["TOCLine"])],
        [Paragraph("OCR", styles["TOCLineBold"]), Paragraph("Optical Character Recognition", styles["TOCLine"]), Paragraph("Computer Vision", styles["TOCLine"])],
        [Paragraph("PR-AUC", styles["TOCLineBold"]), Paragraph("Area Under Precision-Recall Curve", styles["TOCLine"]), Paragraph("Evaluation Metric", styles["TOCLine"])],
        [Paragraph("PWA", styles["TOCLineBold"]), Paragraph("Progressive Web Application", styles["TOCLine"]), Paragraph("Frontend Web", styles["TOCLine"])],
        [Paragraph("RAG", styles["TOCLineBold"]), Paragraph("Retrieval-Augmented Generation", styles["TOCLine"]), Paragraph("Natural Language / AI", styles["TOCLine"])],
        [Paragraph("ROC-AUC", styles["TOCLineBold"]), Paragraph("Area Under Receiver Operating Characteristic Curve", styles["TOCLine"]), Paragraph("Evaluation Metric", styles["TOCLine"])],
        [Paragraph("SHAP", styles["TOCLineBold"]), Paragraph("SHapley Additive exPlanations", styles["TOCLine"]), Paragraph("Explainable AI (XAI)", styles["TOCLine"])],
        [Paragraph("SMOTE-NC", styles["TOCLineBold"]), Paragraph("Synthetic Minority Over-sampling Technique (Nominal & Continuous)", styles["TOCLine"]), Paragraph("Machine Learning", styles["TOCLine"])],
        [Paragraph("WCAG", styles["TOCLineBold"]), Paragraph("Web Content Accessibility Guidelines (W3C)", styles["TOCLine"]), Paragraph("UX Accessibility", styles["TOCLine"])],
        [Paragraph("WHO-PEN", styles["TOCLineBold"]), Paragraph("Package of Essential Noncommunicable Disease Interventions (WHO)", styles["TOCLine"]), Paragraph("Clinical Protocol", styles["TOCLine"])],
        [Paragraph("WHtR", styles["TOCLineBold"]), Paragraph("Waist-to-Height Ratio", styles["TOCLine"]), Paragraph("Anthropometric Metric", styles["TOCLine"])]
    ]
    t = Table(abbr_data, colWidths=[USABLE_WIDTH*0.18, USABLE_WIDTH*0.60, USABLE_WIDTH*0.22])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('LINEBELOW', (0,0), (-1,0), 0.8, colors.HexColor('#0f172a')),
        ('LINEBELOW', (0,1), (-1,-1), 0.3, colors.HexColor('#f1f5f9')),
    ]))
    p.append(t)
    return p
