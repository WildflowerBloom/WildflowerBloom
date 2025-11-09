# API Contracts & Module Interfaces

This document defines the key interfaces between Navi’s modules so builders can implement components independently. All interfaces are Python-first but can be adapted to other languages if needed.

## 1. Orchestrator API

### `submit_entry`
```python
def submit_entry(self, text: str, *, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
```
- **Inputs**:
  - `text`: raw user input.
  - `metadata`: optional dict containing client hints (`{"mode_feedback": "too_intense"}` etc.).
- **Outputs**:
  ```json
  {
    "assistant_text": "...",
    "mode": {
      "mode": "LowDopamine",
      "confidence": 0.72,
      "intensity": "medium",
      "triggers": ["heuristic:+0.20", "classifier:0.52"],
      "recommended_interventions": ["sound:ignite_chime", "template:spark_challenge"],
      "explanations": ["Mode LowDopamine: Energy dip; needs momentum spark.", "Signals: heuristic:+0.20, classifier:0.52"]
    },
    "micro_actions": [
      {
        "id": "spark_challenge-uuid",
        "title": "5-minute dopamine challenge",
        "tone": "playful",
        "description": "...",
        "duration_estimate": 5,
        "sensory_anchor": "sound:ignite_chime"
      }
    ],
    "memories_used": [...],
    "timestamp": "2025-11-09T14:22:31Z"
  }
  ```

### `acknowledge_action`
```python
def acknowledge_action(self, task_id: str, status: str, note: Optional[str] = None) -> ModeResult
```
- `status` allowed values: `completed`, `skipped`, `overwhelmed`.
- Returns updated `ModeResult`.

### `override_mode`
```python
def override_mode(self, mode: str, reason: str) -> ModeResult
```
- Forces new mode, logs override.

## 2. Clarity Pipeline

```python
class ClarityPipeline(Protocol):
    def process(self, text: str) -> Dict[str, Any]: ...
```
- Output structure:
```json
{
  "raw_text": "...",
  "clarified_text": "...",
  "sentiment": -0.35,
  "arousal": 0.6,
  "distortions": [{"type": "catastrophizing", "keywords": ["never"], "confidence": 0.7}],
  "themes": ["workload", "relationships"],
  "embedding": [...]
}
```

## 3. Adaptive Mode Engine

```python
class AdaptiveEngine(Protocol):
    def evaluate(self, payload: Dict[str, Any]) -> ModeResult: ...
    def override(self, mode: str, reason: str) -> ModeResult: ...
```

- `payload` includes:
  - `text`
  - `clarity` (from Clarity pipeline)
  - `session` (SessionState dataclass)
  - `metadata` (from UI)
- `ModeResult` typed dict described in orchestrator.

## 4. Memory Store

```python
class MemoryStore(Protocol):
    def log_interaction(self, record: Dict[str, Any]) -> int: ...
    def retrieve_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]: ...
```

- `record` must include `timestamp`, `raw_text`, `clarity`, `mode`, `llm_response`, `micro_actions`.
- `retrieve_similar` returns ordered list of previous interactions or empty array.

## 5. LLM Client

```python
class LLMClient(Protocol):
    def generate(self, prompt: str, metadata: Dict[str, Any]) -> Dict[str, Any]: ...
```

- Must handle offline fallback by returning structure:
```json
{
  "text": "...",
  "metadata": {"source": "ollama" | "fallback"}
}
```

## 6. Task Translator

```python
class TaskTranslator(Protocol):
    def translate(self, context: Dict[str, Any]) -> List[Dict[str, Any]]: ...
```

- Input context:
  - `mode`: ModeResult
  - `clarity`: Clarity output
  - `llm_response`: LLM response dict
  - `session`: SessionState
- Output micro-action structure (aligns with orchestrator example).

## 7. Anchor Bus

```python
class AnchorBus(Protocol):
    def dispatch(self, event: Dict[str, Any]) -> None: ...
```

- Example event:
```json
{
  "type": "mode_transition",
  "mode": ModeResult,
  "timestamp": "..."
}
```

## 8. Scheduler

```python
class Scheduler(Protocol):
    def schedule_follow_up(self, payload: Dict[str, Any]) -> None: ...
```

- Payload includes `interaction_id`, `mode`, and `timestamp`.
- Should register jobs that eventually notify UI or other channels.

## 9. UI Contract

Front-end should interact with orchestrator via simple HTTP or direct function call. Suggested endpoints if wrapping in FastAPI:

- `POST /api/entry` → body `{ "text": "...", "metadata": {...} }`.
- `POST /api/task/{task_id}/ack` → `{ "status": "completed", "note": "" }`.
- `POST /api/mode/override` → `{ "mode": "Regulated", "reason": "user-selected" }`.
- `GET /api/state` → returns session snapshot (current mode, pending tasks).

Response payloads mirror structures described above.

## 10. Event Types

- `mode_transition`: emitted after evaluate, consumed by anchors/scheduler.
- `task_feedback`: logged when user responds to micro-action.
- `memory_update`: fired whenever new interaction stored (future instrumentation).

## 11. Error Handling & Status Codes (if HTTP)

- `400` for validation errors (e.g., unknown task ID).
- `503` if LLM backend unavailable and fallback fails.
- `500` for unexpected exceptions (log to local file).

## 12. Logging & Telemetry Events

- `navi.event.mode` – payload includes old/new mode, triggers.
- `navi.event.task` – payload includes task_id, status.
- `navi.event.scheduler` – payload includes job_id, fire_time.

Logs stored locally; optional integration with UI log viewer.

