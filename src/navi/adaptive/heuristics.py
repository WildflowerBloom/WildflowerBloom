"""Rule-based heuristics supporting mode inference."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class HeuristicRule:
    mode: str
    weight: float
    keywords: List[str] = field(default_factory=list)
    min_sentiment: float | None = None
    max_sentiment: float | None = None


@dataclass
class KeywordHeuristicEngine:
    rules: List[HeuristicRule]

    def score(self, payload: Dict[str, Any]) -> Dict[str, float]:
        text: str = payload.get("text", "").lower()
        clarity: Dict[str, Any] = payload.get("clarity", {})
        sentiment = float(clarity.get("sentiment", 0.0))

        scores: Dict[str, float] = {}
        for rule in self.rules:
            sentiment_ok = True
            if rule.min_sentiment is not None and sentiment < rule.min_sentiment:
                sentiment_ok = False
            if rule.max_sentiment is not None and sentiment > rule.max_sentiment:
                sentiment_ok = False

            if not rule.keywords or not sentiment_ok:
                continue

            if any(keyword in text for keyword in rule.keywords):
                scores[rule.mode] = scores.get(rule.mode, 0.0) + rule.weight
        return scores

