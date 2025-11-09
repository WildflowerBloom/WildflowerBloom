"""Dispatch multimodal cues like sound effects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Protocol

try:
    import pygame
except ImportError:  # pragma: no cover
    pygame = None  # type: ignore


class AnchorBus(Protocol):
    def dispatch(self, event: Dict[str, Any]) -> None: ...


@dataclass
class SoundAnchorBus:
    """Play sound cues using pygame mixer."""

    enabled: bool = True
    _initialized: bool = False

    def dispatch(self, event: Dict[str, Any]) -> None:
        if not self.enabled or pygame is None:
            return
        cue = event.get("mode", {}).get("recommended_interventions", [])
        sound_id = cue[0] if cue else None
        if not sound_id:
            return
        sound_name = sound_id.replace("sound:", "")
        self._ensure_initialized()
        self._play_sound(sound_name)

    def _ensure_initialized(self) -> None:
        if self._initialized or pygame is None:
            return
        pygame.mixer.init()
        self._initialized = True

    def _play_sound(self, name: str) -> None:
        # Placeholder: in prototype, load from ./assets/sounds/{name}.wav
        # Real implementation should cache sounds and handle missing files gracefully.
        pass

