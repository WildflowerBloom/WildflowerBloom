# Adaptive Mode Engine Specification

The Adaptive Mode Engine (AME) senses the user’s attention rhythm and emotional needs, emitting actionable mode labels that shape Navi’s behavior. This document defines the state machine, feature set, heuristics, and extensibility points.

## 1. Goals

- Detect shifts between energetic, overwhelmed, and depleted states using minimal signals.
- Provide interpretable mode reports that can be surfaced to the user.
- Support lightweight training/refinement on local data without cloud dependencies.
- Allow human override and rapid experimentation with new modes or heuristics.

## 2. Mode Taxonomy (v1)

| Mode          | Description | Primary Tone | Core Interventions |
|---------------|-------------|--------------|--------------------|
| `LowDopamine` | Initiation feels impossible, low energy, negative self-talk. | Energetic + playful | Micro-dares, novelty triggers, 5-minute challenge. |
| `Overwhelm`   | Too many threads, anxious language, sensory overload. | Grounding + directive | Simplify, pick single next step, sensory reset prompt. |
| `Hyperfocus`  | Deep tunnel on one task, risk of burnout or ignoring needs. | Protective | Timeboxing, hydration/movement reminders, checkpoint. |
| `Crash`       | Emotional dip after effort, shame loops, exhaustion. | Gentle + validating | Restorative actions, compassion, journaling. |
| `Regulated`   | Stable attention, receptive to planning/celebration. | Balanced coach | Planning, reflective questions, momentum building. |

Modes can be extended by adding configuration files under `adaptive_modes/<mode_name>.yaml`.

## 3. Inputs & Feature Engineering

- **Textual**:
  - Keyword clusters (e.g., “stuck”, “can’t start”, “frazzled”).
  - Part-of-speech ratios (long run-on sentences → overwhelm).
  - Sentiment polarity and intensity scores.
  - Cognitive distortion counts (catastrophizing, all-or-nothing).
- **Temporal/Behavioral**:
  - Time since last response.
  - Message length variance.
  - Task completion streaks/drops.
  - UI-provided feedback buttons (“too much”, “more hype”).
- **Physiological (optional)**:
  - Heart rate variability trend (low HRV + fatigue wording → crash).
  - Activity level baselines (inactivity + negative tone → low dopamine).

All features normalized to `[0,1]`, appended into a feature vector per interaction.

## 4. Processing Pipeline

1. **Feature Extraction Stage**
   - Functions housed in `navi/adaptive/features.py`.
   - Returns dictionary keyed by feature name with real-valued scores.
2. **Heuristic Layer**
   - Rule-based scores from YAML config:
     ```
     - name: low_dopa_keywords
       when: any(keyword in text for keyword in ["stuck", "no energy", "can't start"])
       score: {"LowDopamine": +0.3}
     ```
   - Aggregated into provisional mode score map.
3. **Classifier Layer**
   - Logistic regression or shallow neural net trained on local transcripts.
   - Input: feature vector; Output: probability distribution across modes.
4. **Smoothing & Hysteresis**
   - Maintain rolling window (last 3 mode outputs).
   - Only switch modes if new mode probability exceeds current mode by `delta >= θ` (default 0.15) or if a rule marks “hard trigger”.
5. **Intervention Selection**
   - Each mode config includes default interventions (`sound_cue`, `micro_action_templates`, `tone_profile`).
   - AME emits suggestions based on intensity level derived from confidence.

## 5. Output Contract

```python
ModeResult = TypedDict(
    "ModeResult",
    {
        "mode": str,
        "confidence": float,
        "intensity": str,   # "low", "medium", "high"
        "triggers": List[str],
        "recommended_interventions": List[str],
        "explanations": List[str],
    },
)
```

- `triggers`: list of feature names or heuristics that contributed.
- `recommended_interventions`: keys looked up by Task Translator / Anchors.
- `explanations`: human-readable couple of sentences for transparency.

## 6. Human Feedback Loop

- UI provides `mode_correct`, `mode_incorrect`, or alternative selection.
- Feedback stored in `mode_feedback` table:
  - `session_id`, `timestamp`, `predicted_mode`, `user_mode`, `notes`.
- Periodically retrain classifier using aggregated samples (offline job).
- Override path: if user picks different mode, system immediately shifts and logs reason.

## 7. Configuration Structure

Example YAML (`adaptive_modes/low_dopamine.yaml`):

```
name: LowDopamine
description: "Energy dip; needs momentum spark."
tone_profile:
  temperature: 0.8
  style: "playful hype"
hard_triggers:
  - keywords: ["can't start", "stuck", "zero energy"]
    min_sentiment: -0.2
signals:
  heuristics:
    - feature: "task_initiation_failures"
      threshold: 0.6
      weight: 0.2
interventions:
  anchors: ["sound:ignite_chime"]
  templates: ["spark_challenge", "dopamine_timer"]
```

## 8. Extensibility

- Add new modes by dropping new YAML and updating classifier label set.
- Swap classifier model by implementing `ModeClassifierProtocol` with methods `predict_proba`, `update`.
- Optional plugin system (`adaptive/plugins`) to ingest new sensors or heuristics.

## 9. Testing Strategy

- Unit tests:
  - Feature extraction accuracy given sample phrases.
  - Hysteresis logic prevents oscillation.
  - YAML parsing produces expected default interventions.
- Scenario tests:
  - Replay transcript sequences, ensure mode sequences match expectations.
  - Inject feedback corrections and confirm probability distribution shifts.

## 10. Roadmap for AME

1. **MVP**: rule-based heuristics + smoothing.
2. **Enhanced**: logistic regression trained on curated dataset (synthetic + anonymized logs).
3. **Adaptive**: on-device continual learning with user feedback weighting.
4. **Multimodal**: incorporate wearable energy curves and audio cues.

