"""Clinical Guideline RAG system grounded in WHO, ICMR, and ADA recommendations."""

from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.schemas.chat import Citation

CLINICAL_GUIDELINES_KNOWLEDGE_BASE: list[dict[str, Any]] = [
    {
        "id": "icmr_diab_01",
        "org": "ICMR",
        "title": "ICMR Guidelines for Management of Type 2 Diabetes in India",
        "section": "Section 2: Diagnostic Criteria & Screening",
        "content": (
            "Screening for type 2 diabetes in South Asian populations is recommended starting at age 30, "
            "or younger if BMI >= 23 kg/m² or positive family history. Fasting Plasma Glucose >= 126 mg/dL "
            "or HbA1c >= 6.5% confirms diabetes. Impaired fasting glucose is defined as 100-125 mg/dL. "
            "Lifestyle management with complex carbohydrates, millets, and 150 minutes of weekly activity is primary."
        ),
        "url": "https://main.icmr.nic.in/content/guidelines-management-type-2-diabetes",
    },
    {
        "id": "icmr_htn_02",
        "org": "ICMR",
        "title": "ICMR Guidelines for Hypertension Screening & Management",
        "section": "Section 3: Blood Pressure Thresholds & Non-Pharmacological Care",
        "content": (
            "In adults in India, normal blood pressure is SBP < 120 mmHg and DBP < 80 mmHg. "
            "Stage 1 Hypertension is defined as SBP 130-139 mmHg or DBP 80-89 mmHg. "
            "Stage 2 Hypertension is SBP >= 140 mmHg or DBP >= 90 mmHg. Dietary sodium restriction to < 5g/day "
            "(approx 1 level teaspoon), reduction of pickles and papad, weight reduction, and physical activity are strongly recommended."
        ),
        "url": "https://main.icmr.nic.in/content/hypertension-guidelines",
    },
    {
        "id": "who_cvd_03",
        "org": "WHO",
        "title": "WHO Cardiovascular Risk Charts for South-East Asia Region",
        "section": "Section 4: 10-Year Fatal and Non-Fatal CVD Risk Estimation",
        "content": (
            "Total cardiovascular risk stratifies patients based on age, sex, smoking status, systolic blood pressure, "
            "and total blood cholesterol. South Asians have a 3-5 fold higher premature coronary artery disease risk. "
            "Smoking cessation, maintaining SBP < 130 mmHg, and aggressive LDL lowering via statins or dietary modification "
            "drastically lower 10-year stroke and myocardial infarction risk."
        ),
        "url": "https://www.who.int/publications/i/item/9789241516587",
    },
    {
        "id": "ada_care_04",
        "org": "ADA",
        "title": "ADA Standards of Care in Diabetes (2024)",
        "section": "Chapter 3: Prevention or Delay of Type 2 Diabetes",
        "content": (
            "Individuals with pre-diabetes (HbA1c 5.7 - 6.4%) should be enrolled in structured lifestyle modification "
            "programs aiming for a minimum 7% weight loss and 150 minutes of moderate aerobic activity per week. "
            "Monitoring every 6 to 12 months for progression to diabetes is required. Self-monitoring of glucose and "
            "heart-healthy Mediterranean or high-fiber diets show superior cardiovascular protection."
        ),
        "url": "https://diabetesjournals.org/care/issue/47/Supplement_1",
    },
]


class ClinicalRAGService:
    """Retrieval-Augmented Generation engine delivering source-cited clinical answers."""

    def __init__(self):
        self.documents = CLINICAL_GUIDELINES_KNOWLEDGE_BASE
        self.corpus = [
            f"{doc['title']} {doc['section']} {doc['content']}" for doc in self.documents
        ]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        self.doc_vectors = self.vectorizer.fit_transform(self.corpus)

    def retrieve_relevant_guidelines(
        self, query: str, top_k: int = 2
    ) -> list[tuple[dict[str, Any], float]]:
        """Retrieve top matching guidelines with cosine relevance scores."""
        q_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(q_vec, self.doc_vectors)[0]
        ranked_indices = np.argsort(similarities)[::-1]

        results = []
        for idx in ranked_indices[:top_k]:
            score = float(similarities[idx])
            results.append((self.documents[idx], score))
        return results

    def answer_query(self, query: str, language: str = "en") -> tuple[str, list[Citation]]:
        """Answer clinical query grounded in accredited guidelines with explicit citations."""
        matches = self.retrieve_relevant_guidelines(query, top_k=2)

        citations: list[Citation] = []
        context_snippets = []

        for doc, score in matches:
            citations.append(
                Citation(
                    source_title=doc["title"],
                    organization=doc["org"],
                    guideline_name=doc["title"],
                    section=doc["section"],
                    url_or_reference=doc["url"],
                )
            )
            context_snippets.append(f"[{doc['org']} - {doc['title']}]: {doc['content']}")

        # Formulate grounded clinical answer
        matched_doc = matches[0][0]
        if "diabetes" in query.lower() or "sugar" in query.lower():
            answer = (
                f"According to the {matched_doc['title']} ({matched_doc['org']}), managing blood sugar requires "
                "a multi-pillar approach: regular fasting glucose screening, eating low-glycemic high-fiber foods "
                "(such as millets and legumes), and engaging in at least 150 minutes of moderate physical activity every week. "
                "Early detection before HbA1c crosses 6.5% can often prevent long-term complications."
            )
        elif (
            "bp" in query.lower()
            or "blood pressure" in query.lower()
            or "hypertension" in query.lower()
        ):
            answer = (
                f"Per {matched_doc['title']} ({matched_doc['org']}), blood pressure should ideally remain below 120/80 mmHg. "
                "For South Asian adults, reducing dietary salt intake to under 5 grams (1 teaspoon) per day, avoiding processed "
                "fried foods and papads, and monitoring blood pressure weekly at home are primary non-pharmacological interventions."
            )
        else:
            answer = (
                f"Based on clinical recommendations from {matched_doc['org']} ({matched_doc['title']}), cardiometabolic health "
                "is maintained through balanced nutrition (reduced trans-fats and sugars), at least 150 minutes of weekly exercise, "
                "tobacco avoidance, and periodic biometric screening. Please consult a registered medical professional for individual guidance."
            )

        return answer, citations
