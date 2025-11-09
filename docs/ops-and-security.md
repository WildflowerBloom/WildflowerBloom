# Operations, Privacy, and Safety Playbook

## Deployment Model

- Local desktop application launched via CLI (`python -m navi.main`) or packaged executable.
- Optional headless mode exposing REST API for custom clients.
- All data stored on user’s filesystem; no cloud persistence by default.

## Configuration

- `.navi/config.yaml` (auto-created) with:
  - `model_name`: Ollama model alias.
  - `audio.enabled`: bool.
  - `scheduler.enabled`: bool.
  - `privacy.encryption`: `none` (MVP) or `passphrase` (future).
  - `therapist_templates`: path to custom YAML.
- Provide CLI commands:
  - `navi config view`
  - `navi config set key=value`
  - `navi export --summary` or `--full`

## Logging

- `~/.navi/logs/navi.log` rotating file (max 5MB × 5 files).
- Log levels: INFO for mode transitions, WARNING for fallback usage, ERROR for crashes.
- Ensure logs omit raw user text unless verbose debug mode enabled.

## Backup & Recovery

- Daily reminder to export zipped backup (`memory.db + memory.json`).
- Auto-backup before app upgrade or schema migration.
- Recovery script to restore from backup with integrity check.

## Privacy Controls

- **Data Purge**: `navi purge --since YYYY-MM-DD` deletes interactions + associated embeddings.
- **Selective Share**: generate sanitized summary (counts, sentiments, wins) without raw messages.
- **Opt-out Metrics**: disable local analytics (keeps only minimal logs).

## Security Considerations

- Run Ollama locally; ensure port accessible only to localhost.
- If exposing API, require token-based auth (bearer token stored in config).
- Sandbox third-party templates by validating YAML schema and limiting actions.
- Future: implement SQLCipher encryption with passphrase prompt on launch.

## Safety Protocol

- **Crisis Language Detection**:
  - Keywords set triggers emergency response template with hotline resources (customizable per region).
  - Disable micro-actions and encourage seeking human support.
- **User Override**: immediate “Quiet Mode” toggle to reduce stimulation.
- **Therapist Escalation**: user can mark message “share with therapist” to tag entry for export.

## Monitoring & Updates

- Use semantic versioning; maintain `CHANGELOG.md`.
- Publish checksum for release packages.
- Update routine: prompt user when new templates or scripts available, allow manual review before applying.

## Operational Runbook

1. **Startup Checklist**
   - Ensure Ollama server running.
   - Verify `memory.db` accessible.
   - Confirm audio devices optional: fail gracefully if not available.
2. **Incident Response**
   - On unhandled exception: show gentle error UI, auto-save logs, prompt user to send anonymized report (if they choose).
   - Provide `navi doctor` command to run diagnostics (DB integrity, config validation).
3. **Performance Tuning**
   - Allow switching to smaller LLM model.
   - Provide config for embedding model selection.

## Compliance (Future Planning)

- Prepare for HIPAA-aligned workflows if used by therapists (encryption, audit trail).
- Document data retention policies for pilot testers (default 90-day retention with user control).
- Setup consent flow for collecting anonymized telemetry (opt-in only).

