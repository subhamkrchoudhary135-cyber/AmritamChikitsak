"""Conversational clinical guideline RAG chatbot endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_current_user, get_db
from src.core.audit import audit_logger
from src.db.models import User
from src.llm.guardrails import STATUTORY_DISCLAIMER, ClinicalGuardrails
from src.llm.rag import ClinicalRAGService
from src.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Clinical Chatbot"])
rag_service = ClinicalRAGService()


@router.post("", response_model=ChatResponse)
async def chat_with_clinical_guidelines(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Grounded RAG conversational assistant adhering to WHO, ICMR, and ADA guidelines.

    Enforces:
    - Rejection of prescription requests and medical diagnosis
    - Emergency red-flag symptom triage
    - Accredited clinical citation tracking
    - Statutory non-diagnostic clinical disclaimer.
    """
    # 1. Guardrail evaluation
    is_blocked, rejection_msg = ClinicalGuardrails.sanitize_and_check_query(
        payload.message, user_id=current_user.id
    )

    if is_blocked and rejection_msg:
        is_emergency = "EMERGENCY" in rejection_msg
        return ChatResponse(
            answer=rejection_msg,
            language=payload.language,
            citations=[],
            is_emergency=is_emergency,
            disclaimer=STATUTORY_DISCLAIMER,
        )

    # 2. RAG Knowledge Retrieval & Grounding
    answer, citations = rag_service.answer_query(payload.message, language=payload.language)

    # 3. Audit trail (Zero PII logged)
    audit_logger.log_event(
        action="CHAT_COMPLETED",
        user_id=current_user.id,
        role=current_user.role,
        resource_type="CHAT",
        resource_id=current_user.id,
        details={"citation_count": len(citations), "language": payload.language},
    )

    return ChatResponse(
        answer=answer,
        language=payload.language,
        citations=citations,
        is_emergency=False,
        disclaimer=STATUTORY_DISCLAIMER,
    )
