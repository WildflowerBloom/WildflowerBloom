# Navi Data & State Flow Guide

This document traces the life of a user interaction through Navi’s subsystems, highlighting data contracts, storage touchpoints, and feedback loops. All flows assume a single local user session.

## 1. Entities & State Snapshots

- **Session State** (in-memory, orchestrator):
  - `session_id`
  - `current_mode` + confidence
  - `pending_tasks` (micro-actions awaiting acknowledgment)
  - `recent_interactions` (IDs referencing SQLite)
  - `flags` (e.g., wearable_connected, quiet_mode_enabled)
- **Persistent Records** (SQLite):
  - `interactions`: timestamp, raw_input, clarified_input, reply_id, mode_id, distortion_tags.
  - `modes`: mode label, confidence, triggers, interventions delivered.
  - `tasks`: micro-action payloads, completion status, user feedback.
  - `feedback`: explicit thumbs up/down, intensity notes, override requests.
  - `context_tags`: key-value pairs (e.g., `emotion=hopeful`, `environment=home`, `routine=dog_walk`).
- **Embeddings Store** (in-memory or Faiss index):
  - SentenceTransformer vectors keyed by interaction IDs to support similarity search.

## 2. Primary Interaction Loop

1. **User Input Arrives**
   - UI sends `{text, timestamp, optional_mode_feedback}` to `navi_core`.
   - Orchestrator logs a provisional interaction with status `pending_processing`.

2. **Clarity AI Pass**
   - Text normalization (lowercasing, emoji handling).
   - Sentiment score, arousal estimate.
   - Cognitive distortion detection (pattern rules + logistic regression).
   - Outputs `clarified_input`, `annotations` (list of `{type, span, strength}`).
   - Stored temporarily in session state; appended to provisional interaction.

3. **Feature Extraction & Mode Inference**
   - Features:
     - Linguistic cues (keywords, sentence length).
     - Temporal markers (time since last message, response latency).
     - Annotation summary (distortion counts, sentiment).
     - Optional biometric metrics (heart rate trend, sleep debt).
   - Adaptive Mode Engine returns `ModeResult`.
   - Orchestrator updates `current_mode` if confidence surpasses hysteresis threshold; emits `mode_transition` event if changed.

4. **Memory Retrieval**
   - Query embeddings store using clarified input.
   - Retrieve top-k past interactions with similar context, wins, or interventions.
   - Compose `memory_context` snippet for LLM prompt.

5. **Prompt Assembly & LLM Call**
   - Template slots:
     - `mode_profile`: description of active mode’s tone + rules.
     - `clarified_input`: user request reframed.
     - `annotations`: cognitive flags to address in response.
     - `recent_actions`: pending or completed micro-actions.
     - `memory_context`: relevant memories.
   - Ollama returns `llm_reply` (assistant narrative) plus optional structured suggestions if model supports tools.
   - Timeout or offline fallback triggers script-based response generator.

6. **Task Translation**
   - Takes `ModeResult`, `llm_reply`, `annotations`.
   - Selects template bank keyed to `current_mode`.
   - Generates `micro_actions` list:
     ```
     {
       "id": uuid,
       "title": "5-minute dopamine challenge",
       "tone": "playful",
       "description": "...",
       "duration_estimate": 5,
       "sensory_anchor": "chime_burst",
       "verification": {"type": "self_report"}
     }
     ```
   - Attaches to orchestrator session state and persists to `tasks`.

7. **Response Packaging**
   - Orchestrator builds payload to UI:
     - `assistant_text` (LLM reply + optional inline reframes).
     - `mode_indicator` (name, color, confidence).
     - `micro_actions` (cards with buttons).
     - `anchors_trigger` (e.g., `sound:fire_chime`).
   - Marks provisional interaction as `complete`, writes row to SQLite, logs embeddings.

8. **Anchors & Scheduler Notifications**
   - Event bus propagates `anchors_trigger` to sound module.
   - Scheduler receives context for follow-up (e.g., “check-in after 7 minutes”).

## 3. Task Completion Feedback Loop

1. User clicks “Done” or “Too much” in UI.
2. UI sends event to orchestrator with `{task_id, status, feedback_note}`.
3. Orchestrator updates session state:
   - Completed tasks increment `momentum_score`.
   - Abandoned tasks increase `overwhelm_counter`.
4. Adaptive Mode Engine re-evaluates with new features; may shift mode (e.g., success → `Regulated`).
5. Memory store logs completion with emotion tags for future reinforcement.

## 4. Periodic Check-Ins

- Scheduler triggers after inactivity (e.g., 15 minutes):
  - Pulls latest `current_mode`, `last_interaction`.
  - Sends gentle prompt or suggests restorative action.
- End-of-day summary job:
  - Aggregates tasks completed, emotional shifts.
  - Stores digest entry and optionally renders UI recap the next session.

## 5. Error & Offline Handling

- **LLM Timeout**:
  - Orchestrator falls back to rule-based script (`adaptive_scripts/{mode}.yaml`).
  - Flags interaction `llm_fallback=true` for later review.
- **Database Lock/Failure**:
  - Write to local JSON buffer; retry later.
  - Alert UI with banner if persistence loses sync.
- **Mode Confidence Low**:
  - Present UI question: “Does this feel more like overwhelm or dopamine crash?”
  - User selection feeds back into Adaptive Engine training set.

## 6. Data Privacy Controls

- Local encryption option wrapping SQLite via SQLCipher or simple AES layer.
- Daily backup routine (compressed JSON + DB file) stored in user-specified path.
- Erasure flow: user requests purge → orchestrator wipes tables and embeddings, clears session cache.

## 7. Integration Hooks

- **Wearables**:
  - Adapter pulls data periodically, normalizes to `energy_signal`.
  - Router merges into feature vector before mode inference.
- **Calendar / Todo Apps**:
  - Imported tasks tagged with `source` and run through Task Translator for alignment.
- These integrations stay optional; architecture isolates them behind the event bus to avoid core coupling.

