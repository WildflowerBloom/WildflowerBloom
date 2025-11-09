"""Implementation of the adaptive mode inference pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Protocol, Tuple, TypedDict

from .features import FeatureExtractor, FeatureVector


class ModeResult(TypedDict):
    mode: str
    confidence: float
    intensity: str
    triggers: List[str]
    recommended_interventions: List[str]
    explanations: List[str]


@dataclass
class ModeConfig:
    name: str
    description: str
    hysteresis: float = 0.15
    interventions: List[str] = field(default_factory=list)
    anchors: List[str] = field(default_factory=list)
    hard_triggers: List[Dict[str, Any]] = field(default_factory=list)


class Classifier(Protocol):
    """Protocol expected from probabilistic classifiers."""

    def predict_proba(self, features: FeatureVector) -> Dict[str, float]: ...

    def update(self, features: FeatureVector, label: str) -> None: ...


class HeuristicEngine(Protocol):
    """Protocol for rule-based heuristics used in tandem with classifier."""

    def score(self, payload: Dict[str, Any]) -> Dict[str, float]: ...


class AdaptiveModeEngine:
    """Combines heuristics, classifier, and smoothing to produce mode updates."""

    def __init__(
        self,
        *,
        modes: Dict[str, ModeConfig],
        feature_extractor: FeatureExtractor,
        classifier: Classifier,
        heuristics: HeuristicEngine,
        default_mode: str = "Regulated",
    ) -> None:
        self.modes = modes
        self.feature_extractor = feature_extractor
        self.classifier = classifier
        self.heuristics = heuristics
        self.current_mode = default_mode
        self.current_confidence = 0.0

    def evaluate(self, payload: Dict[str, Any]) -> ModeResult:
        features = self.feature_extractor.extract(payload)
        heuristic_scores = self.heuristics.score(payload)
        classifier_scores = self.classifier.predict_proba(features)

        combined = self._combine_scores(heuristic_scores, classifier_scores)
        best_mode, confidence = max(combined.items(), key=lambda item: item[1])
        selected_mode = self._apply_hysteresis(best_mode, confidence)

        mode_config = self.modes[selected_mode]
        triggers = self._identify_triggers(heuristic_scores, classifier_scores, selected_mode)

        result: ModeResult = {
            "mode": selected_mode,
            "confidence": confidence,
            "intensity": self._intensity_for(confidence),
            "triggers": triggers,
            "recommended_interventions": mode_config.interventions,
            "explanations": self._explanations_for(selected_mode, triggers),
        }
        self.current_mode = selected_mode
        self.current_confidence = confidence
        return result

    def override(self, mode: str, reason: str) -> ModeResult:
        mode_config = self.modes.get(mode)
        if mode_config is None:
            raise ValueError(f"Unknown mode override: {mode}")
        self.current_mode = mode
        self.current_confidence = 1.0
        return {
            "mode": mode,
            "confidence": 1.0,
            "intensity": "medium",
            "triggers": ["user_override"],
            "recommended_interventions": mode_config.interventions,
            "explanations": [reason],
        }

    def _combine_scores(
        self, heuristics: Dict[str, float], classifier: Dict[str, float]
    ) -> Dict[str, float]:
        combined: Dict[str, float] = {}
        for mode_name in self.modes:
            base = classifier.get(mode_name, 0.0)
            combined[mode_name] = min(1.0, base + heuristics.get(mode_name, 0.0))
        return combined

    def _apply_hysteresis(self, candidate_mode: str, confidence: float) -> str:
        if candidate_mode == self.current_mode:
            return candidate_mode
        current_threshold = self.modes[self.current_mode].hysteresis
        if confidence - self.current_confidence >= current_threshold:
            return candidate_mode
        return self.current_mode

    def _identify_triggers(
        self,
        heuristic_scores: Dict[str, float],
        classifier_scores: Dict[str, float],
        selected_mode: str,
    ) -> List[str]:
        triggers: List[str] = []
        heur_score = heuristic_scores.get(selected_mode, 0.0)
        if heur_score > 0:
            triggers.append(f"heuristic:+{heur_score:.2f}")
        model_score = classifier_scores.get(selected_mode, 0.0)
        triggers.append(f"classifier:{model_score:.2f}")
        return triggers

    def _explanations_for(self, mode: str, triggers: List[str]) -> List[str]:
        config = self.modes[mode]
        summary = f"Mode {mode}: {config.description}"
        trigger_text = ", ".join(triggers)
        return [summary, f"Signals: {trigger_text}"]

    def record_feedback(self, payload: Dict[str, Any]) -> None:
        """Update classifier with user feedback data."""
        label = payload.get("label")
        features = payload.get("features")
        if not isinstance(label, str) or not isinstance(features, dict):
            return
        self.classifier.update(features, label)

