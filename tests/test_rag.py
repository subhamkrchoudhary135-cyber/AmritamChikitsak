"""Tests for Guideline RAG system and Lab Report OCR extractor."""

from src.llm.ocr_parser import LabReportTextExtractor
from src.llm.rag import ClinicalRAGService


def test_clinical_rag_retrieval_and_citations():
    rag = ClinicalRAGService()

    answer, citations = rag.answer_query("What is the ICMR cutoff for diabetes screening in India?")
    assert len(answer) > 20
    assert len(citations) > 0
    assert any(c.organization in ["ICMR", "WHO", "ADA"] for c in citations)


def test_lab_report_ocr_regex_extraction():
    sample_lab_text = """
    PATIENT HEALTH CHECK REPORT
    Age: 46 Yrs | Sex: Female
    Blood Pressure: 135/88 mmHg
    FBS (Fasting Blood Sugar): 122.5 mg/dL
    HbA1c: 6.4 %
    Total Cholesterol: 215 mg/dL
    Triglycerides: 180 mg/dL
    Height: 158 cm | Weight: 68 kg
    """

    extracted = LabReportTextExtractor.extract_biometrics_from_text(sample_lab_text)

    assert extracted["age"] == 46
    assert extracted["gender"] == "female"
    assert extracted["systolic_bp"] == 135.0
    assert extracted["diastolic_bp"] == 88.0
    assert extracted["fasting_glucose"] == 122.5
    assert extracted["hba1c"] == 6.4
    assert extracted["total_cholesterol"] == 215.0
    assert extracted["height_cm"] == 158.0
    assert extracted["weight_kg"] == 68.0
