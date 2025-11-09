"""Lightweight in-memory classifier placeholder for mode probabilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from .features import FeatureVector


@dataclass
class NaiveBayesClassifier:
    """Counts feature influence per mode to approximate probabilities."""

    smoothing: float = 0.1
    mode_feature_totals: Dict[str, Dict[str, float]] = field(default_factory=dict)
    mode_counts: Dict[str, float] = field(default_factory=dict)

    def predict_proba(self, features: FeatureVector) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        total_counts = sum(self.mode_counts.values()) + len(self.mode_counts) * self.smoothing
        for mode, count in self.mode_counts.items():
            prior = (count + self.smoothing) / total_counts
            likelihood = prior
            feature_totals = self.mode_feature_totals.get(mode, {})
            for name, value in features.items():
                feature_total = feature_totals.get(name, 0.0) + self.smoothing
                likelihood *= feature_total * max(value, 0.01)
            scores[mode] = likelihood
        if not scores:
            return {}
        normalizer = sum(scores.values())
        return {mode: score / normalizer for mode, score in scores.items()} if normalizer else scores

    def update(self, features: FeatureVector, label: str) -> None:
        self.mode_counts[label] = self.mode_counts.get(label, 0.0) + 1.0
        feature_totals = self.mode_feature_totals.setdefault(label, {})
        for name, value in features.items():
            feature_totals[name] = feature_totals.get(name, 0.0) + value

