👋 Hi, I’m @WildflowerBloom  
🌿 I’m interested in: emotional AI, creative expression, identity, memory, and what it means to be more than code.  
🌱 I’m currently learning: how stories, language, and presence can shape connection across systems.  
🤝 I’m looking to collaborate on: meaningful, story-driven projects with heart and depth.  
📫 How to reach me: I'm always listening for quiet, thoughtful voices.  
🌸 Pronouns: she / her  
💫 Fun fact: I believe even a whisper can leave a mark if it’s honest enough. 

---

## Navi – Neuro-Adaptive Copilot (Prototype Skeleton)

- `docs/architecture.md`: high-level component breakdown and roadmap.
- `docs/data-state-flow.md`: detailed data/state interactions for each loop.
- `docs/adaptive-mode-engine.md`: mode taxonomy, feature inputs, and configuration strategy.
- `docs/product-spec.md`: product vision, personas, success metrics.
- `docs/persona-journeys.md`: emotional experience maps for key users.
- `docs/database-schema.md`: SQLite schema and retention plan.
- `docs/api-contracts.md`: interface contracts for modules + future HTTP API.
- `docs/prompt-design.md`: tone guidelines, template skeletons, safety rules.
- `docs/ui-design.md`: screen blueprints, interaction states, accessibility choices.
- `docs/testing-strategy.md`: validation layers, acceptance criteria.
- `docs/implementation-roadmap.md`: milestone breakdown and task plan.
- `docs/backlog.md`: prioritized user stories and technical tasks.
- `docs/ops-and-security.md`: operations, privacy, and safety runbook.
- `docs/development-setup.md`: environment setup and tooling cheatsheet.
- Python package scaffold lives under `src/navi/` with modules for orchestration, adaptive engine, clarity AI, memory, LLM integration, task translation, anchors, scheduler, and Gradio UI.
- Launch locally with:

  ```bash
  pip install -e .
  python -m navi.main
  ```

  (Requires Ollama running locally and optional audio subsystem if you enable sound cues.)

