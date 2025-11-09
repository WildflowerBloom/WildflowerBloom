"""Translate abstract goals into energy-aligned micro-actions."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class TaskTemplate:
    id: str
    mode: str
    title: str
    tone: str
    description: str
    duration: int
    sensory_anchor: str | None = None


DEFAULT_TEMPLATES: List[TaskTemplate] = [
    TaskTemplate(
        id="spark_challenge",
        mode="LowDopamine",
        title="5-minute dopamine challenge",
        tone="playful",
        description="Set a timer for 5 minutes. Race yourself to reset one small zone.",
        duration=5,
        sensory_anchor="sound:ignite_chime",
    ),
    TaskTemplate(
        id="grounding_reset",
        mode="Overwhelm",
        title="Grounding triage",
        tone="calm",
        description="Take 90 seconds. Name 3 things in sight, 2 you can touch, 1 you can breathe into.",
        duration=2,
        sensory_anchor="sound:ground_bell",
    ),
    TaskTemplate(
        id="checkpoint",
        mode="Hyperfocus",
        title="Checkpoint break",
        tone="protective",
        description="Pause for water and scan your body. Decide if the next 10 minutes still matter.",
        duration=3,
        sensory_anchor="sound:soft_chime",
    ),
    TaskTemplate(
        id="restoration",
        mode="Crash",
        title="Compassion reset",
        tone="gentle",
        description="Wrap yourself in a blanket or favorite hoodie. Breathe with hand on heart for 10 breaths.",
        duration=4,
        sensory_anchor="sound:wave_wash",
    ),
    TaskTemplate(
        id="celebrate_plan",
        mode="Regulated",
        title="Celebrate + plan",
        tone="affirming",
        description="Note 1 win, 1 emotion, 1 next seed you want to plant.",
        duration=4,
        sensory_anchor="sound:sparkle",
    ),
]


@dataclass
class DefaultTaskTranslator:
    """Maps responses into actionable suggestions."""

    templates: List[TaskTemplate] = field(default_factory=lambda: DEFAULT_TEMPLATES)

    def translate(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        mode = context.get("mode", {}).get("mode", "Regulated")
        matching = [template for template in self.templates if template.mode == mode]
        if not matching:
            matching = [template for template in self.templates if template.mode == "Regulated"]

        tasks: List[Dict[str, Any]] = []
        for template in matching[:2]:
            tasks.append(
                {
                    "id": f"{template.id}-{uuid.uuid4()}",
                    "title": template.title,
                    "tone": template.tone,
                    "description": template.description,
                    "duration_estimate": template.duration,
                    "sensory_anchor": template.sensory_anchor,
                }
            )
        return tasks

