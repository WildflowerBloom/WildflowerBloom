# Development Environment Setup

## 1. Prerequisites

- Python 3.10+
- Pipx or virtualenv
- `ollama` installed locally (https://ollama.ai/download)
- Optional: `ffmpeg` for advanced audio cues, `sqlite3` CLI for debugging.

## 2. Clone & Install

```bash
git clone <repo>
cd navi
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
```

## 3. Verify Ollama

```bash
ollama serve  # ensure server running
ollama pull llama3
```

Set preferred model in `~/.navi/config.yaml` once app runs.

## 4. Run Application

```bash
python -m navi.main
```

Launches Gradio UI at http://localhost:7860. For headless API mode:

```bash
uvicorn navi.api:app --reload
```
(API module to be implemented in M1.)

## 5. Tests & Linting

```bash
pytest
ruff check src tests
mypy src/navi
```

## 6. Database Location

- Default path: `~/.navi/memory.db`
- To reset: `rm ~/.navi/memory.db`
- For manual inspection: `sqlite3 ~/.navi/memory.db`

## 7. Environment Variables

- `NAVI_CONFIG_DIR`: override default config path.
- `NAVI_MODEL`: fallback model name.
- `NAVI_DISABLE_AUDIO=1`: disable sound dispatch.

## 8. Sample Data

- `tests/fixtures/` (to create): store JSON/YAML transcripts for automated tests.
- `docs/sample-conversations/` can host curated scripts for manual QA.

## 9. Packaging (Future)

- Use `pyinstaller` or `briefcase` for desktop packaging.
- Ensure `.navi` directory created on first run with default config.

## 10. Troubleshooting

- **LLM timeout**: check Ollama logs; fallback script should activate.
- **Audio errors**: install `pygame` dependencies (SDL). On Linux: `sudo apt-get install libsdl2-dev`.
- **Scheduler not firing**: ensure system clock correct; check logs for APScheduler warnings.

