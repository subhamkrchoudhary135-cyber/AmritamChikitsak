"""Chatbot, RAG, and citation schemas."""

from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single chat turn."""

    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    """User query to the clinical guideline chatbot."""

    message: str = Field(..., min_length=2, max_length=2000)
    language: Literal["en", "hi", "pa"] = "en"
    patient_id: str | None = None
    conversation_history: list[ChatMessage] = Field(default_factory=list)


class Citation(BaseModel):
    """Source reference from accredited medical guidelines."""

    source_title: str
    organization: Literal["WHO", "ICMR", "ADA", "Ministry of Health India"]
    guideline_name: str
    section: str | None = None
    url_or_reference: str | None = None


class ChatResponse(BaseModel):
    """Response from RAG chatbot with safety guardrails and citations."""

    answer: str
    language: Literal["en", "hi", "pa"]
    citations: list[Citation]
    is_emergency: bool = False
    disclaimer: str = (
        "Sanjivani AI is an AI screening support tool and does not provide medical diagnoses "
        "or drug prescriptions. Always consult a licensed healthcare professional."
    )
