from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import httpx
import json

from app.core.config import settings


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str
    usage: Optional[dict] = None


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system: Optional[str] = None) -> LLMResponse:
        pass

    @abstractmethod
    def is_configured(self) -> bool:
        pass


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL.rstrip("/")
        self.model = settings.LLM_MODEL
        self.timeout = 30.0

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: Optional[str] = None) -> LLMResponse:
        if not self.is_configured():
            raise ValueError("LLM_API_KEY not configured")

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 2000,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        choice = data["choices"][0]
        content = choice["message"]["content"]
        usage = data.get("usage")

        return LLMResponse(
            content=content,
            provider="openai-compatible",
            model=self.model,
            usage=usage,
        )


class AnthropicProvider(LLMProvider):
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL.rstrip("/") if settings.LLM_BASE_URL else "https://api.anthropic.com"
        self.model = settings.LLM_MODEL
        self.timeout = 30.0

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: Optional[str] = None) -> LLMResponse:
        if not self.is_configured():
            raise ValueError("LLM_API_KEY not configured")

        messages = [{"role": "user", "content": prompt}]

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 2000,
            "temperature": 0.3,
        }
        if system:
            payload["system"] = system

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/v1/messages",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        content = data["content"][0]["text"]
        usage = data.get("usage")

        return LLMResponse(
            content=content,
            provider="anthropic",
            model=self.model,
            usage=usage,
        )


class GeminiProvider(LLMProvider):
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL.rstrip("/") if settings.LLM_BASE_URL else "https://generativelanguage.googleapis.com"
        self.model = settings.LLM_MODEL
        self.timeout = 30.0

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: Optional[str] = None) -> LLMResponse:
        if not self.is_configured():
            raise ValueError("LLM_API_KEY not configured")

        full_prompt = prompt
        if system:
            full_prompt = f"{system}\n\n{prompt}"

        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2000,
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/v1beta/models/{self.model}:generateContent",
                params={"key": self.api_key},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        content = data["candidates"][0]["content"]["parts"][0]["text"]
        usage = data.get("usageMetadata")

        return LLMResponse(
            content=content,
            provider="gemini",
            model=self.model,
            usage=usage,
        )


class OllamaProvider(LLMProvider):
    def __init__(self):
        self.base_url = settings.LLM_BASE_URL.rstrip("/") if settings.LLM_BASE_URL else "http://localhost:11434"
        self.model = settings.LLM_MODEL
        self.timeout = 60.0

    def is_configured(self) -> bool:
        return True  # Ollama doesn't require API key by default

    async def generate(self, prompt: str, system: Optional[str] = None) -> LLMResponse:
        full_prompt = prompt
        if system:
            full_prompt = f"{system}\n\n{prompt}"

        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 2000,
            },
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        content = data.get("response", "")
        usage = {"prompt_tokens": data.get("prompt_eval_count", 0), "completion_tokens": data.get("eval_count", 0)}

        return LLMResponse(
            content=content,
            provider="ollama",
            model=self.model,
            usage=usage,
        )


class LLMService:
    def __init__(self):
        self.providers = {
            "openai-compatible": OpenAICompatibleProvider(),
            "anthropic": AnthropicProvider(),
            "gemini": GeminiProvider(),
            "ollama": OllamaProvider(),
        }
        self.default_provider = settings.LLM_PROVIDER

    def get_provider(self, provider: Optional[str] = None) -> LLMProvider:
        provider_name = provider or self.default_provider
        if provider_name not in self.providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        return self.providers[provider_name]

    async def generate_explanation(
        self,
        lesson_content: str,
        question: str,
        provider: Optional[str] = None,
    ) -> LLMResponse:
        system = """You are an expert Claude Code tutor. Provide clear, accurate explanations grounded in the provided lesson content.
        Label your response as 'ADVISORY: This explanation is AI-generated and may contain inaccuracies. Verify against official documentation.'
        Do not fabricate information. If unsure, say so."""

        prompt = f"""Lesson content:
{lesson_content}

Question: {question}

Provide a helpful explanation based on the lesson content above."""

        llm_provider = self.get_provider(provider)
        if not llm_provider.is_configured():
            raise ValueError(f"Provider {llm_provider.__class__.__name__} not configured (missing LLM_API_KEY)")

        return await llm_provider.generate(prompt, system)

    def list_providers(self) -> list[str]:
        return list(self.providers.keys())