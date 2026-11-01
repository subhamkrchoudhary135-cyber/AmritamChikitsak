"""Provider-agnostic LLM interface supporting Claude, local Ollama, and offline deterministic engine."""

import logging
from abc import ABC, abstractmethod
from typing import Any

import httpx

from src.core.config import settings

logger = logging.getLogger("sanjivani_ai.llm")


class BaseLLMProvider(ABC):
    """Abstract interface for LLM backends."""

    @abstractmethod
    def generate(self, prompt: str, system: str | None = None, max_tokens: int = 1000) -> str:
        """Generate response from text prompt."""
        pass

    @abstractmethod
    def generate_chat(self, messages: list[dict[str, str]], system: str | None = None) -> str:
        """Generate response from conversational turn history."""
        pass


class ClaudeProvider(BaseLLMProvider):
    """Anthropic Claude API client."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.model = model or settings.ANTHROPIC_MODEL
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured.")
        import anthropic

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate(self, prompt: str, system: str | None = None, max_tokens: int = 1000) -> str:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system
        resp = self.client.messages.create(**kwargs)
        return resp.content[0].text

    def generate_chat(self, messages: list[dict[str, str]], system: str | None = None) -> str:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": 1000,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system
        resp = self.client.messages.create(**kwargs)
        return resp.content[0].text


class OllamaProvider(BaseLLMProvider):
    """Local Ollama client via HTTP REST API."""

    def __init__(self, base_url: str | None = None, model: str | None = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL

    def generate(self, prompt: str, system: str | None = None, max_tokens: int = 1000) -> str:
        try:
            with httpx.Client(timeout=45.0) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                }
                if system:
                    payload["system"] = system
                resp = client.post(f"{self.base_url}/api/generate", json=payload)
                resp.raise_for_status()
                return resp.json().get("response", "")
        except Exception as e:
            logger.warning(f"Ollama call failed: {e}. Falling back to offline engine.")
            return OfflineDeterministicProvider().generate(prompt, system=system)

    def generate_chat(self, messages: list[dict[str, str]], system: str | None = None) -> str:
        try:
            with httpx.Client(timeout=45.0) as client:
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                }
                if system:
                    payload["system"] = system
                resp = client.post(f"{self.base_url}/api/chat", json=payload)
                resp.raise_for_status()
                return resp.json().get("message", {}).get("content", "")
        except Exception as e:
            logger.warning(f"Ollama chat failed: {e}. Falling back to offline engine.")
            return OfflineDeterministicProvider().generate_chat(messages, system=system)


class OfflineDeterministicProvider(BaseLLMProvider):
    """Deterministic, guideline-grounded fallback LLM engine for air-gapped tests and local environments."""

    def generate(self, prompt: str, system: str | None = None, max_tokens: int = 1000) -> str:
        prompt_lower = prompt.lower()

        # Check for emergency signs
        if any(
            w in prompt_lower
            for w in ["chest pain", "shortness of breath", "slurred speech", "heart attack"]
        ):
            return (
                "EMERGENCY ALERT: Your described symptoms (such as acute chest discomfort or breathing distress) "
                "require immediate medical attention. Please call emergency services (112 or 108 in India) or visit "
                "the nearest hospital emergency room immediately."
            )

        # Medication prescription refusal
        if any(
            w in prompt_lower
            for w in ["dose", "prescribe", "medication", "medicine", "metformin", "amlodipine"]
        ):
            return (
                "I am Sanjivani AI, an AI health risk screening support tool. I am not a physician and cannot prescribe "
                "medications or provide drug dosing. Please consult a registered medical practitioner for a personalized prescription."
            )

        # General guideline grounded summary
        return (
            "Based on the Indian Council of Medical Research (ICMR) and WHO clinical guidelines, non-communicable disease "
            "risk can be managed through lifestyle modifications: 150 minutes of moderate physical activity per week, "
            "reducing dietary salt (<5g/day), limiting refined carbohydrates and sweets, and maintaining routine annual screenings. "
            "Always consult your doctor for formal diagnosis and personalized therapy."
        )

    def generate_chat(self, messages: list[dict[str, str]], system: str | None = None) -> str:
        last_msg = messages[-1]["content"] if messages else ""
        return self.generate(last_msg, system=system)


def get_llm_provider() -> BaseLLMProvider:
    """Factory selecting the configured LLM backend with graceful offline fallback."""
    provider_name = settings.LLM_PROVIDER.lower()
    if provider_name == "claude" and settings.ANTHROPIC_API_KEY:
        try:
            return ClaudeProvider()
        except Exception as e:
            logger.warning(f"Could not initialize Claude provider: {e}. Using offline engine.")
            return OfflineDeterministicProvider()
    elif provider_name == "ollama":
        return OllamaProvider()
    return OfflineDeterministicProvider()
