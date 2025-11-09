# Navi Architecture Blueprint

## 1. Purpose

Navi is a local-first neuro-adaptive copilot that senses the user’s attention rhythm and responds with coaching, structure, and emotional resonance. The architecture is designed so every component can evolve independently while staying lightweight enough for offline use.

## 2. High-Level Stack

- **Interface**: Gradio single-page app (SPA) with conversational stream, quick-action buttons, and ambience controls.
- **Orchestration Core (`navi_core`)**: Manages session state, routes events, and coordinates persistence.
- **Adaptive Mode Engine**: Infers current attention/emotional mode from text, timing, and optional biometric data.
- **Clarity AI Layer**: Detects cognitive distortions, sentiment, and key themes before LLM prompting.
- **Local LLM Runtime**: Ollama-served model that produces motivational replies, reframes, and micro-action prompts.
- **Task Translator**: Converts goals into “energy-aligned micro-actions” tailored to the active mode.
- **Memory Service**: SQLite + embedding index storing interactions, emotional metadata, and longitudinal insights.
- **Multimodal Anchors**: Sound/visual cue module triggered on mode transitions.
- **Scheduler Services**: Background jobs for reminders, mode re-evaluation, and restorative nudges.

The diagram below shows responsibility layers:

```
┌──────────────────────┐
│       Gradio UI      │
└─────────┬────────────┘
          │
┌─────────▼────────────┐
│     Orchestration     │
│   (navi_core hub)     │
└─┬───────┬───────┬─────┘
  │       │       │
  │       │    ┌──▼───────────┐
  │       │    │ Task Translator│
  │  ┌────▼───┐└──────┬────────┘
  │  │Adaptive│       │
  │  │ Mode   │   ┌───▼────────┐
  │  │ Engine │   │ Local LLM  │
  │  └────┬───┘   └────┬───────┘
  │       │            │
┌─▼────┐  │     ┌──────▼──────┐
│Clarity│  │     │ Memory/     │
│  AI   │  │     │ Persistence │
└─┬────┘  │     └──────┬──────┘
  │       │            │
  │  ┌────▼───────┐ ┌──▼───────────┐
  └──►Anchors/FX  │ │Schedulers/   │
     └────────────┘ │Integrations  │
                    └──────────────┘
```

## 3. Key Components

### 3.1 Gradio UI Shell
- Components: chat stream, “mode indicator” badge, quick actions (Reset, Spark, Ground), optional audio toggle.
- Responsibilities: capture user text, display responses, surface suggested micro-actions, emit explicit mode feedback (“this felt too intense”).
- Extensible to embed visual regulation cues or simple dashboards (e.g., “streaks,” “energy curve”).

### 3.2 Orchestration Core (`navi_core`)
- Maintains session context: current mode, pending tasks, emotion tags, conversation history pointers.
- Provides event bus for module communication.
- Exposes simple API to UI: `submit_entry`, `get_state_snapshot`, `acknowledge_action`.
- Invokes downstream services in order: Clarity AI → Adaptive Engine → Memory → LLM → Task Translator → Anchors.

### 3.3 Adaptive Mode Engine
- Combines rule-based heuristics with embedding classifier (SentenceTransformer + lightweight model).
- Produces `ModeResult`: `{mode, confidence, triggers, suggested_interventions}`.
- Uses smoothing to avoid rapid oscillation; publishes transition events when mode changes.

### 3.4 Clarity AI Layer
- Pipeline: text normalization → sentiment + tone → distortion detection (pattern library) → theme extraction.
- Outputs annotations that feed both Adaptive Mode Engine features and prompt conditioning.
- Offers inline reframes (e.g., highlight catastrophizing and suggest alternate framing).

### 3.5 Local LLM Runtime
- Ollama REST endpoint accessible via Python client.
- Prompt templates conditioned on `mode`, distortion annotations, and retrieved memories.
- Safety guardrails: token limit management, fallback responses when offline/unavailable.

### 3.6 Task Translator
- Library of templates per mode (e.g., “5-minute dopamine challenge,” “gentle checklist,” “celebration + debrief”).
- Consumes LLM suggestions + current context to produce structured micro-actions (`id`, `title`, `tone`, `duration_estimate`, `sensory_anchor`).
- Returns both natural language summary and machine-readable payload for UI rendering.

### 3.7 Memory & Persistence
- SQLite schema with tables for `interactions`, `modes`, `tasks`, `feedback`, `context_tags`.
- Embedding index (Faiss or in-memory vector store) for retrieval-augmented prompting.
- Memory retention policies: highlight “wins,” emotional peaks, recent breakdowns for personalized future prompts.

### 3.8 Multimodal Anchors
- Pluggable outputs: sound cues (Pygame), optional color palette hints, integration hooks for hardware (e.g., Philips Hue).
- Subscribes to event bus: triggers when `ModeResult` crosses thresholds or when Task Translator schedules transitions.

### 3.9 Scheduler & Integrations
- Uses `APScheduler` or Python `asyncio` tasks for periodic checks: hydration reminders, “wrap-up” prompts, rest intervals.
- Future integration layer for wearables (Fitbit/Oura) abstracted behind an adapter interface.

## 4. Deployment Philosophy

1. **Local-first**: run entirely offline except optional wearable integrations.
2. **Explainable**: surfaces why a mode was detected and why a specific intervention is suggested.
3. **Modular**: each subsystem replaceable (e.g., swap Gradio for Tauri, SQLite for Postgres).
4. **Privacy**: all data stored locally with explicit export/erase controls.

## 5. Roadmap Milestones

1. **Prototype Alpha**
   - Chat loop with mode detection heuristics.
   - Task Translator stub returning pre-built templates.
   - Memory logging basic metadata.
2. **Prototype Beta**
   - Train/evaluate lightweight classifier with sample transcripts.
   - Add cognitive distortion tagging + inline reframes.
   - Introduce sound cues and scheduler nudges.
3. **Therapeutic Coach Preview**
   - Personalized templates per user profile.
   - Wearable adapter support.
   - Insight dashboard (energy curve, successful interventions).

## 6. Risks & Mitigations

- **Mode misclassification** → Keep human override controls, log corrections for retraining.
- **LLM drift/offline failure** → Provide fallback script-based coaching responses.
- **User overwhelm** → Allow “quiet” mode that reduces prompts, summarizing instead of directing.
- **Data privacy** → Local encryption option and transparent storage map in UI.

## 7. Next Implementation Steps

1. Stand up Python package skeleton (`navi/`) with orchestrator, adaptive engine, and memory modules.
2. Implement Gradio UI stub linked to orchestrator (`/submit` route).
3. Create sample mode templates and heuristics.
4. Seed SQLite schema and simple persistence wrappers.

