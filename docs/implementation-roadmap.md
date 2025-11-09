# Implementation Roadmap & Build Plan

## Milestone Overview

| Milestone | Timeline (ideal) | Goals |
|-----------|------------------|-------|
| M0 – Foundation | Week 1 | Setup repo, environment, core scaffolding |
| M1 – Conversation Loop | Weeks 2-3 | Working chat flow with heuristics + micro-actions |
| M2 – Memory & Insights | Weeks 4-5 | Persistent storage, basic insights screen |
| M3 – Adaptive Intelligence | Weeks 6-7 | Classifier training, feedback loop |
| M4 – Pilot Beta | Weeks 8-10 | UX polish, accessibility, therapist export |

## Detailed Tasks

### M0 – Foundation
- Install dependencies; confirm Ollama model availability.
- Implement CLI entry (`python -m navi.main`) & ensure Gradio UI launches.
- Set up continuous integration script (formatting, linting, tests).
- Create `tests/` scaffolding with sample fixtures.

### M1 – Conversation Loop
- Flesh out Clarity pipeline with sentiment/detection tests.
- Implement real heuristics with configurable YAML files.
- Wire Task Translator templates to UI cards.
- Add HTTP API layer (FastAPI or Flask) to separate backend from Gradio if desired.
- Manual QA for each core mode using scripted inputs.

### M2 – Memory & Insights
- Finalize SQLite schema; add ORM models via SQLAlchemy.
- Implement retrieval-based memory context injection for LLM prompts.
- Create “Today’s Rhythm” view (narrative insights).
- Build export/import commands (JSON + SQLite backup).
- Add basic encryption toggle (optional).

### M3 – Adaptive Intelligence
- Collect synthetic transcripts, label with modes.
- Train lightweight classifier (logistic regression) offline; integrate into Adaptive Engine.
- Implement user feedback UI for correcting mode predictions.
- Add scheduler follow-up notifications (Gradio toast or separate channel).
- Introduce wearable adapter interface with mock data (for future integration).

### M4 – Pilot Beta
- Conduct accessibility audit; implement keyboard navigation, ARIA roles.
- Add personalization settings (mode intensity slider, anchor preference).
- Build therapist export summary (Markdown/CSV).
- Run closed pilot with 5-10 users; collect qualitative feedback and adjust tone templates.
- Document deployment & update operations playbook.

## Backlog (Post-Beta Ideas)
- Cross-device sync via encrypted peer-to-peer database.
- Multimodal anchors (smart lights, haptic wearables).
- Federated learning strategy for classifier updates.
- Companion mobile app with offline sync.

## Team Roles

- **Product/Experience Lead**: maintain tone guidelines, review micro-action library.
- **ML Engineer**: own classifier pipeline, feature tuning, evaluation.
- **Backend Engineer**: implement orchestrator, storage, API.
- **Frontend Engineer**: craft Gradio UI, later migrate to custom interface (React/Tauri).
- **Therapist Advisor**: review interventions for psychological safety.

## Delivery Checklist per Milestone

- Feature implemented & documented.
- Tests written/passed (unit + integration).
- Manual QA with persona scripts.
- Update README + changelog.
- Gather and log feedback for next iteration.

## Risk Mitigation

- **LLM Latency**: support streaming UI or fallback scripts for instant responses.
- **Data Loss**: automated daily backup reminders; ensure write-ahead logging on SQLite.
- **Scope Creep**: separate backlog vs. milestone features; lock MVP before adding integrations.

## Communication Cadence

- Weekly build sync (async doc + optional call).
- Daily Slack/Discord check-ins for blockers.
- Monthly therapist advisory review.

