"""Feature extraction utilities for Adaptive Mode Engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Protocol

FeatureVector = Dict[str, float]


class FeatureExtractor(Protocol):
    def extract(self, payload: Dict[str, Any]) -> FeatureVector: ...


@dataclass
class DefaultFeatureExtractor:
    """Transforms clarity + session metadata into features."""

    def extract(self, payload: Dict[str, Any]) -> FeatureVector:
        text: str = payload.get("text", "")
        clarity: Dict[str, Any] = payload.get("clarity", {})
        session = payload.get("session")

        sentiment = float(clarity.get("sentiment", 0.0))
        arousal = float(clarity.get("arousal", 0.0))
        distortion_count = float(len(clarity.get("distortions", [])))

        features: FeatureVector = {
            "sentiment": sentiment,
            "arousal": arousal,
            "distortion_count": distortion_count,
            "text_length": min(len(text) / 500.0, 1.0),
        }

        if session is not None:
            features["momentum_score"] = min(session.momentum_score / 5.0, 1.0)
            features["overwhelm_counter"] = min(session.overwhelm_counter / 5.0, 1.0)

        metadata = payload.get("metadata") or {}
        if metadata.get("feedback_status") == "overwhelmed":
            features["recent_overwhelm_feedback"] = 1.0
        elif metadata.get("feedback_status") == "completed":
            features["recent_overwhelm_feedback"] = 0.0

        return features

