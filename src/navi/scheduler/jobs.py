"""Scheduler wrapper for follow-up nudges."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from apscheduler.schedulers.background import BackgroundScheduler


@dataclass
class ReminderScheduler:
    """Wrap APScheduler to trigger gentle check-ins."""

    scheduler: BackgroundScheduler

    def __post_init__(self) -> None:
        if not self.scheduler.running:
            self.scheduler.start(paused=True)

    def schedule_follow_up(self, payload: Dict[str, Any]) -> None:
        from datetime import datetime, timedelta

        minutes = 5 if payload.get("mode", {}).get("mode") == "LowDopamine" else 10
        run_at = datetime.utcnow() + timedelta(minutes=minutes)
        self.scheduler.add_job(
            self._send_reminder,
            trigger="date",
            run_date=run_at,
            kwargs={"payload": payload},
            misfire_grace_time=60,
            id=f"follow_up_{payload.get('interaction_id')}",
            replace_existing=True,
        )

    def _send_reminder(self, payload: Dict[str, Any]) -> None:
        # Placeholder: integrate with UI notification or local toast.
        pass

