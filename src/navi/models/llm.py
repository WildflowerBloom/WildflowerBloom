"""Wrapper around Ollama local LLM runtime."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import httpx


@dataclass
class LocalLLMResponse:
    text: str
    metadata: Dict[str, Any]


@dataclass
class OllamaClient:
    """Minimal client for Ollama's HTTP API."""

    base_url: str = "http://localhost:11434"
    model: str = "llama3"
    timeout_seconds: float = 30.0

    def generate(self, prompt: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "prompt": self._compose_prompt(prompt, metadata),
            "stream": False,
        }
        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(f"{self.base_url}/api/generate", json=payload)
                response.raise_for_status()
                data = response.json()
        except (httpx.RequestError, httpx.HTTPStatusError):
            return {
                "text": self._fallback_response(prompt, metadata),
                "metadata": {"source": "fallback"},
            }
        return {"text": data.get("response", ""), "metadata": {"source": "ollama"}}

    def _compose_prompt(self, user_text: str, metadata: Dict[str, Any]) -> str:
        mode = metadata.get("mode", {}).get("mode", "Regulated")
        tone = metadata.get("mode", {}).get("intensity", "medium")
        distortions = metadata.get("clarity", {}).get("distortions", [])
        memory_lines = []
        for memory in metadata.get("memories", [])[:3]:
            memory_lines.append(f"- {memory.get('raw_text', '')}")

        prompt_sections = [
            "You are Navi, a neuro-adaptive copilot who supports ADHD and nonlinear thinkers.",
            f"Current mode: {mode} (intensity: {tone}).",
            f"User said: {user_text}",
        ]
        if distortions:
            prompt_sections.append(f"Cognitive distortions detected: {distortions}")
        if memory_lines:
            prompt_sections.append("Recent relevant memories:\n" + "\n".join(memory_lines))
        prompt_sections.append("Respond with warmth, clarity, and a single next step suggestion.")
        return "\n\n".join(prompt_sections)

    def _fallback_response(self, user_text: str, metadata: Dict[str, Any]) -> str:
        mode = metadata.get("mode", {}).get("mode", "Regulated")
        return (
            f"[Fallback Coach - {mode}] I hear you: {user_text}. "
            "Let's take one gentle step forward: try a 5-minute focus burst or a stretch break."
        )

