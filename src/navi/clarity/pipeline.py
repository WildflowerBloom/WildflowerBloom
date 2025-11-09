"""Baseline clarity pipeline combining sentiment, distortion tagging, and summaries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Protocol

try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover
    SentenceTransformer = None  # type: ignore


@dataclass
class ClarityResult:
    raw_text: str
    clarified_text: str
    sentiment: float
    arousal: float
    distortions: List[Dict[str, Any]]
    themes: List[str]
    embedding: List[float] | None = None


class DistortionDetector(Protocol):
    def detect(self, text: str) -> List[Dict[str, Any]]: ...


class SentimentModel(Protocol):
    def score(self, text: str) -> Dict[str, float]: ...


class DefaultDistortionDetector:
    """Rule-based detector to flag common cognitive distortions."""

    PATTERNS: Dict[str, List[str]] = {
        "catastrophizing": ["ruined", "disaster", "never", "always"],
        "all_or_nothing": ["always", "never", "completely"],
        "mind_reading": ["they think", "everyone probably"],
        "should_statements": ["should", "must", "supposed to"],
    }

    def detect(self, text: str) -> List[Dict[str, Any]]:
        matches: List[Dict[str, Any]] = []
        lower_text = text.lower()
        for label, keywords in self.PATTERNS.items():
            hits = [kw for kw in keywords if kw in lower_text]
            if hits:
                matches.append({"type": label, "keywords": hits, "confidence": min(0.9, 0.3 + 0.1 * len(hits))})
        return matches


class SimpleSentimentModel:
    """Placeholder sentiment model using a naive keyword approach."""

    POSITIVE = {"excited", "proud", "grateful", "win"}
    NEGATIVE = {"stuck", "tired", "hate", "awful", "overwhelmed"}

    def score(self, text: str) -> Dict[str, float]:
        lower_text = text.lower()
        pos_hits = sum(1 for word in self.POSITIVE if word in lower_text)
        neg_hits = sum(1 for word in self.NEGATIVE if word in lower_text)
        sentiment = (pos_hits - neg_hits) / max(1, pos_hits + neg_hits)
        arousal = min(1.0, (pos_hits + neg_hits) / 5.0)
        return {"sentiment": sentiment, "arousal": arousal}


class DefaultClarityPipeline:
    """Composes sentiment, distortion detection, and optional embeddings."""

    def __init__(
        self,
        *,
        distortion_detector: DistortionDetector | None = None,
        sentiment_model: SentimentModel | None = None,
        embedding_model_name: str | None = None,
    ) -> None:
        self.distortion_detector = distortion_detector or DefaultDistortionDetector()
        self.sentiment_model = sentiment_model or SimpleSentimentModel()
        self.embedding_model_name = embedding_model_name
        self._embedder = SentenceTransformer(embedding_model_name) if embedding_model_name else None

    def process(self, text: str) -> Dict[str, Any]:
        analysis = self.sentiment_model.score(text)
        distortions = self.distortion_detector.detect(text)
        clarified = self._clarify_text(text, distortions)
        embedding = self._encode(clarified)
        themes = self._extract_themes(text)

        return {
            "raw_text": text,
            "clarified_text": clarified,
            "sentiment": analysis["sentiment"],
            "arousal": analysis["arousal"],
            "distortions": distortions,
            "themes": themes,
            "embedding": embedding,
        }

    def _clarify_text(self, text: str, distortions: List[Dict[str, Any]]) -> str:
        if not distortions:
            return text.strip()
        notes = [f"{d['type'].replace('_', ' ')}?" for d in distortions]
        return f"{text.strip()} (notice: {', '.join(notes)})"

    def _encode(self, text: str) -> List[float] | None:
        if self._embedder is None:
            return None
        vector = self._embedder.encode(text, normalize_embeddings=True)
        return vector.tolist()  # type: ignore[return-value]

    def _extract_themes(self, text: str) -> List[str]:
        lower_text = text.lower()
        themes: List[str] = []
        if "work" in lower_text or "project" in lower_text:
            themes.append("workload")
        if "sleep" in lower_text or "rest" in lower_text:
            themes.append("restoration")
        if "friend" in lower_text or "family" in lower_text:
            themes.append("relationships")
        if not themes:
            themes.append("general")
        return themes

