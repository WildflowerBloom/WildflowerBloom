# Data Model & Storage Plan

Navi stores all data locally using SQLite for structured records and optional vector index for semantic retrieval. Users can opt into encryption (future milestone) but schema is designed to work in plain SQLite for prototype.

## Overview

- `interactions`: each conversational turn with metadata.
- `modes`: history of detected modes per interaction.
- `tasks`: micro-actions generated and their lifecycle.
- `feedback`: explicit qualitative feedback entries.
- `context_tags`: key/value pairs to annotate an interaction.
- `embedding_cache`: optional vector storage for retrieval (if FAISS not used).

## Entity Relationship Diagram (Textual)

```
interactions (1) ──< modes (many)
interactions (1) ──< tasks (many)
interactions (1) ──< context_tags (many)
tasks (1) ──< feedback (many)
```

## Table Definitions

### `interactions`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Unique interaction ID |
| `timestamp` | TEXT (ISO8601) | When the input was received |
| `raw_text` | TEXT | Original user input |
| `clarified_text` | TEXT | Clarity-processed text |
| `sentiment` | REAL | Sentiment score (-1..1) |
| `arousal` | REAL | Arousal/intensity (0..1) |
| `llm_response` | TEXT | Assistant response (JSON blob) |
| `session_id` | TEXT | Identifier for session/thread |
| `metadata` | TEXT | JSON string for extra fields |

### `modes`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | |
| `interaction_id` | INTEGER | FK to `interactions.id` |
| `mode` | TEXT | Mode label (`LowDopamine`, etc.) |
| `confidence` | REAL | 0..1 confidence |
| `intensity` | TEXT | `low`, `medium`, `high` |
| `triggers` | TEXT | JSON list describing signals |
| `explanations` | TEXT | Human-readable reasons |

### `tasks`

| Column | Type | Description |
|--------|------|-------------|
| `id` | TEXT PRIMARY KEY | `template-id + uuid` |
| `interaction_id` | INTEGER | FK to `interactions.id` |
| `title` | TEXT | Display title |
| `tone` | TEXT | `playful`, `gentle`, etc. |
| `description` | TEXT | Detailed instruction |
| `duration_estimate` | INTEGER | Minutes |
| `sensory_anchor` | TEXT | e.g., `sound:ignite_chime` |
| `status` | TEXT | `suggested`, `completed`, `skipped`, `overwhelmed` |
| `status_timestamp` | TEXT | Last update ISO8601 |

### `feedback`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | |
| `task_id` | TEXT | FK to `tasks.id` |
| `timestamp` | TEXT | When feedback recorded |
| `type` | TEXT | `user_note`, `therapist_note`, etc. |
| `note` | TEXT | Freeform |

### `context_tags`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | |
| `interaction_id` | INTEGER | FK to `interactions.id` |
| `key` | TEXT | e.g., `emotion` |
| `value` | TEXT | e.g., `hopeful` |

### `embedding_cache` (optional)

| Column | Type | Description |
|--------|------|-------------|
| `interaction_id` | INTEGER PRIMARY KEY | FK to `interactions.id` |
| `vector` | BLOB | Serialized embedding (if not using FAISS) |

## Indices

- `CREATE INDEX idx_modes_interaction ON modes(interaction_id);`
- `CREATE INDEX idx_tasks_interaction ON tasks(interaction_id);`
- `CREATE INDEX idx_tags_interaction ON context_tags(interaction_id);`
- `CREATE INDEX idx_tasks_status ON tasks(status);`

## Migration Approach

- Use lightweight migration scripts in Python (`alembic` optional later).
- Keep a `schema_version` table for upgrade path.
- Provide export script to dump JSON + SQLite backup for user control.

## Data Retention & Privacy

- Users can purge interactions by range (date or tag).
- Optional encryption: wrap SQLite with SQLCipher or store DB in encrypted filesystem.
- Provide sanitized summary export for sharing with therapists (no raw text if user opts).

