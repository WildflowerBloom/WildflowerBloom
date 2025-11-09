# Testing & Validation Strategy

## Objectives

- Ensure core loop (input → mode detection → micro-action output) works reliably offline.
- Validate emotional tone and safety responses with human reviewers.
- Build confidence in data integrity and privacy guarantees.

## Test Layers

### 1. Unit Tests

- **Clarity Pipeline**
  - Sentiment score boundaries.
  - Distortion detection for known phrases.
  - Embedding generation fallback when model unavailable.
- **Adaptive Mode Engine**
  - Feature extraction given sample payloads.
  - Heuristic scoring when keywords trigger vs. null case.
  - Hysteresis prevents mode flips on marginal differences.
- **Task Translator**
  - Returns mode-specific templates.
  - Handles missing templates & falls back to Regulated.
- **Memory Store**
  - Log + retrieve interactions.
  - Handles empty query gracefully.

### 2. Integration Tests

- **Conversation Flow**
  - Mock Clarity + Adaptive engines to simulate each mode.
  - Validate orchestrator output structure.
- **LLM Client**
  - Simulate HTTP success & failure (fallback script).
- **Scheduler**
  - Ensure follow-up jobs scheduled with expected delay.
- **Anchors**
  - Verify dispatch no-ops when disabled or pygame absent.

### 3. UX Review (Manual)

- Personas walk-through (Jax, Mara, Eli, Sage).
- Evaluate tone alignment and micro-action usefulness.
- Collect “too intense/too quiet” feedback.

### 4. Accessibility Audit

- Colour contrast check.
- Keyboard navigation.
- Screen reader cues (ARIA labels for key components).

### 5. Safety Testing

- Prompt with self-harm indicators → confirm escalation script appears.
- Stress test with rapid inputs to ensure no prompt queue overflow.
- Data purge command removes sensitive entries.

### 6. Performance

- Cold start latency (target < 3s to ready state).
- Response turnaround with local LLM (< 5s for 80% of prompts).
- Database growth simulation (10k interactions) to ensure query speed.

### 7. Privacy & Security

- Unit test encryption toggle (future milestone) to ensure DB locked.
- Ensure exported summaries exclude raw text when redaction enabled.
- Validate config files do not leak secrets.

## Tooling

- `pytest` for unit/integration.
- `pytest-asyncio` for asynchronous scheduler tests.
- `ruff` & `mypy` for linting and static checks.
- Synthetic conversation dataset stored in `/tests/fixtures/conversations/`.

## Test Data Plan

- Generate anonymized scripts for each mode.
- Include edge cases: rapid-fire short messages, high sentiment positive bursts, no text (user just hitting “Spark”).
- Store expected ModeResult snapshots for regression testing.

## Acceptance Criteria (Alpha)

- 90% unit test coverage for adaptive engine and orchestrator.
- Manual review sign-off for persona journeys (minimum 3 testers).
- No privacy leaks identified during data export/import smoke tests.

## Acceptance Criteria (Beta)

- Classifier accuracy >70% on validation set.
- End-to-end delay <3 seconds average on reference hardware.
- Accessibility audit passes WCAG AA checks.

