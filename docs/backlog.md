# Product Backlog & User Stories

## Priority Legend
- P0: Required for MVP launch.
- P1: Important for Beta.
- P2: Nice-to-have / Post-Beta.

## Core Stories

### P0 – Conversational Loop
- **Story**: As a user, I want Navi to respond in tone that matches my state so I feel understood.  
  - Acceptance: 5 scripted inputs covering each mode produce distinct tone + micro-action suggestions.
- **Story**: As a user, I want to mark a suggestion as “Too much” so Navi softens quickly.  
  - Acceptance: “Too much” reduces future suggestion intensity and logs feedback.
- **Story**: As a user, I want to see why Navi chose a mode.  
  - Acceptance: Mode panel reveals triggers/explanations in plain language.
- **Story**: As a user, I want to toggle quiet mode when overstimulated.  
  - Acceptance: Quiet toggle reduces response length, disables audio.

### P0 – Data Integrity
- **Story**: As a user, I want my sessions stored locally with option to wipe them.  
  - Acceptance: CLI command deletes data by date range, verified via DB query.
- **Story**: As a user, I want my daily wins surfaced so I can feel momentum.  
  - Acceptance: Summary view lists at least one positive tag per day if available.

### P1 – Adaptive Intelligence
- **Story**: As a user, I want Navi to learn from my feedback to improve mode detection.  
  - Acceptance: After manual label corrections, classifier adjusts probabilities on subsequent similar inputs.
- **Story**: As a user, I want to connect my wearable data to inform mode detection.  
  - Acceptance: Adapter ingests mock wearable data, adjusts features (beta flag).

### P1 – Therapist Collaboration
- **Story**: As a therapist, I want to add custom prompts aligned with my client’s plan.  
  - Acceptance: YAML templates recognized, appear for relevant modes.
- **Story**: As a therapist, I want anonymized summaries to review between sessions.  
  - Acceptance: Export file contains mode counts, wins, notes, no raw text unless opted in.

### P2 – Personalization
- **Story**: As a user, I want Navi to remember sensory anchors I like.  
  - Acceptance: Settings allow selecting anchor type; suggestions align with preference.
- **Story**: As a user, I want to name my motivational archetype (“Firestarter”) to shape tone.  
  - Acceptance: Archetype setting modifies prompt template descriptors.

## Technical Tasks

- P0: Implement config file loader/saver.
- P0: Add logging middleware for orchestrator events.
- P0: Create command `navi doctor` for diagnostics.
- P1: Build classifier training script using scikit-learn or PyTorch-lite.
- P1: Implement scheduler notifications in UI (toast, banner).
- P2: Integrate with smart light API (Philips Hue baseline).

## Research Tasks

- P0: Validate core tone prompts with 3 ADHD community members.
- P1: Interview therapists for export format preferences.
- P2: Explore federated learning frameworks for on-device aggregation.

## Bugs to Watch (Hypothetical)

- LLM fallback not triggered when server unreachable → add retry logic.
- Audio dispatch tries to load missing file → handle gracefully with notification.
- Long-running sessions cause UI slowdown → paginate conversation or lazy-load.

## Definition of Done

- Code reviewed.
- Tests (unit/integration) passing with coverage targets met.
- Documentation updated (README + relevant docs).
- UX review recorded for user-facing changes.
- Privacy implications considered; data purge commands updated if new data stored.

