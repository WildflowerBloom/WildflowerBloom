# Navi Product Specification

## Vision

Navi is a neuro-adaptive copilot designed to harmonize with attention rhythms seen in ADHD and other nonlinear thinkers. Instead of punishing oscillating focus, Navi amplifies momentum by pairing emotional resonance with contextual coaching so users feel guided, not managed.

## Target Personas

1. **Momentum-Seeking Creator**  
   - Needs: reclaim creative flow after dopamine crashes, flexible structure for artistic bursts.  
   - Pain: traditional productivity apps feel rigid; shame spiral after missed self-imposed deadlines.

2. **Executive Function Juggler**  
   - Needs: translate overwhelm into doable actions, emotional validation in frantic contexts.  
   - Pain: task lists balloon, sensory overload triggers avoidance, wants gentler accountability.

3. **Therapist/Coach Companion**  
   - Needs: support sessions with data on client rhythms, offer between-session nudges aligned with therapeutic goals.  
   - Pain: limited insight once clients leave sessions; current tools lack emotional nuance.

## Problem Statement

Current productivity/coaching tools assume consistent focus loops, leaning on compliance and rewards for completion. Users dealing with ADHD-style attention dynamics cycle between hyperfocus, exhaustion, and emotional turbulence, causing mistrust in tools that feel punitive. Navi reframes these signals into supportive guidance, celebrating wins and softening crashes.

## Value Proposition

- Adaptive modulation that mirrors emotional intensity and energy.
- Local-first privacy, giving users control over their own patterns and data.
- Action translation that converts overwhelm into dopamine-aligned micro-moves.
- Persistent memory that builds a compassionate narrative of progress.

## Success Metrics (MVP)

- **Engagement**: >60% daily active users return on day 7 of testing cohort.
- **Task Conversion**: Users accept or complete ≥1 suggested micro-action in 40%+ of sessions.
- **Emotional Feedback**: Average satisfaction rating ≥4/5; <15% interactions flagged as “too much”.
- **Mode Accuracy**: 70% of user overrides agree with predicted mode or lead to learning adjustment.

## Feature Checklist (Prototype Alpha)

- Conversational UI with adaptive tone responses.
- Mode detection heuristics with transparent explanations.
- Cognitive distortion tagging and inline reframes.
- Task Translator library for core modes (LowDopamine, Overwhelm, Hyperfocus, Crash, Regulated).
- SQLite-backed memory with emotion/context tagging.
- Sound cue hooks and simple scheduling for follow-ups.

## Feature Checklist (Prototype Beta)

- Lightweight classifier trained on curated transcripts (synthetic + pilot data).
- User feedback loop for correcting modes and calibrating tone.
- Basic insights dashboard: momentum trend, emotional mix, successful interventions.
- Optional wearable integration abstraction.
- Export/erase data tools with encryption toggle.

## Long-Term Differentiators

- Multimodal anchors (scent, lighting, haptic) via plugin adapters.
- Personalized motivational archetypes that evolve with user stories.
- Narrative analytics for therapists/coaches showing qualitative growth, not just metrics.
- Community template sharing with privacy-preserving mechanisms (federated learning roadmap).

## Non-Goals (for now)

- Cloud-based team collaboration (single-user focus first).
- Heavy analytics on productivity (avoid reinforcing guilt-based metrics).
- Integration with third-party AI services requiring cloud data sharing.

## Constraints & Assumptions

- Runs on consumer hardware (laptop/desktop) with local Ollama models.
- Works offline except optional integrations.
- Audio cues optional; default to silent if no audio device.
- System will gather synthetic data for initial mode classifier training; production data remains local.

## Stakeholders

- **Founder/Creator**: shapes emotional framing & storytelling.
- **Technical Builder**: delivers local app, maintains modular services.
- **Therapist/Coach Advisors**: ensure interventions align with trauma-informed care.
- **Pilot Users**: provide qualitative feedback loops for iteration.

## Open Questions

- Best way to surface “why we suggested this” without overwhelming user?
- How to gracefully pause interventions when user indicates sensory overload?
- What minimum dataset size is needed for on-device classifier to add value over heuristics?

