"""Central coordination layer for Navi subsystems."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol, TypedDict


class ModeResult(TypedDict):
    mode: str
    confidence: float
    intensity: str
    triggers: List[str]
    recommended_interventions: List[str]
    explanations: List[str]


class AdaptiveEngine(Protocol):
    """Protocol for adaptive mode inference engines."""

    def evaluate(self, payload: Dict[str, Any]) -> ModeResult: ...

    def override(self, mode: str, reason: str) -> ModeResult: ...


class ClarityPipeline(Protocol):
    """Protocol for text clarification and annotation."""

    def process(self, text: str) -> Dict[str, Any]: ...


class MemoryStore(Protocol):
    """Protocol for persistence layer interactions."""

    def log_interaction(self, record: Dict[str, Any]) -> int: ...

    def retrieve_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]: ...


class TaskTranslator(Protocol):
    """Protocol for translating goals into micro-actions."""

    def translate(self, context: Dict[str, Any]) -> List[Dict[str, Any]]: ...


class LLMClient(Protocol):
    """Protocol for local LLM interaction."""

    def generate(self, prompt: str, metadata: Dict[str, Any]) -> Dict[str, Any]: ...


class AnchorBus(Protocol):
    """Protocol for multimodal cues."""

    def dispatch(self, event: Dict[str, Any]) -> None: ...


class Scheduler(Protocol):
    """Protocol for job scheduling."""

    def schedule_follow_up(self, payload: Dict[str, Any]) -> None: ...


@dataclass
class SessionState:
    """Snapshot of the active dialogue loop."""

    session_id: str
    current_mode: Optional[str] = None
    mode_confidence: float = 0.0
    momentum_score: int = 0
    overwhelm_counter: int = 0
    pending_tasks: List[Dict[str, Any]] = field(default_factory=list)
    recent_interaction_ids: List[int] = field(default_factory=list)
    flags: Dict[str, Any] = field(default_factory=dict)


class Orchestrator:
    """Coordinates Navi subsystems to produce responses."""

    def __init__(
        self,
        *,
        session: SessionState,
        clarity: ClarityPipeline,
        adaptive_engine: AdaptiveEngine,
        memory_store: MemoryStore,
        llm: LLMClient,
        task_translator: TaskTranslator,
        anchors: AnchorBus,
        scheduler: Scheduler,
    ) -> None:
        self.session = session
        self.clarity = clarity
        self.adaptive_engine = adaptive_engine
        self.memory_store = memory_store
        self.llm = llm
        self.task_translator = task_translator
        self.anchors = anchors
        self.scheduler = scheduler

    def submit_entry(self, text: str, *, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Main entry point for UI submissions."""
        metadata = metadata or {}
        timestamp = datetime.utcnow().isoformat()

        clarity_payload = self.clarity.process(text)
        adaptive_payload = {
            "text": text,
            "clarity": clarity_payload,
            "session": self.session,
            "metadata": metadata,
        }
        mode_result = self.adaptive_engine.evaluate(adaptive_payload)
        self._update_mode(mode_result)

        memories = self.memory_store.retrieve_similar(clarity_payload.get("clarified_text", text))
        prompt_context = {
            "text": text,
            "clarity": clarity_payload,
            "mode": mode_result,
            "memories": memories,
            "session_flags": self.session.flags,
        }

        llm_response = self.llm.generate(text, prompt_context)
        micro_actions = self.task_translator.translate(
            {
                "mode": mode_result,
                "clarity": clarity_payload,
                "llm_response": llm_response,
                "session": self.session,
            }
        )
        self.session.pending_tasks.extend(micro_actions)

        record = {
            "timestamp": timestamp,
            "raw_text": text,
            "clarity": clarity_payload,
            "mode": mode_result,
            "llm_response": llm_response,
            "micro_actions": micro_actions,
            "metadata": metadata,
        }
        interaction_id = self.memory_store.log_interaction(record)
        self.session.recent_interaction_ids.append(interaction_id)

        anchor_event = {"type": "mode_transition", "mode": mode_result}
        self.anchors.dispatch(anchor_event)
        self.scheduler.schedule_follow_up(
            {"interaction_id": interaction_id, "mode": mode_result, "timestamp": timestamp}
        )

        return {
            "assistant_text": llm_response.get("text", ""),
            "mode": mode_result,
            "micro_actions": micro_actions,
            "memories_used": memories,
            "timestamp": timestamp,
        }

    def acknowledge_action(self, task_id: str, status: str, note: Optional[str] = None) -> ModeResult:
        """Mark a suggested micro-action as completed, skipped, or overwhelming."""
        retain: List[Dict[str, Any]] = []
        selected: Optional[Dict[str, Any]] = None
        for task in self.session.pending_tasks:
            if task.get("id") == task_id:
                selected = task
            else:
                retain.append(task)
        self.session.pending_tasks = retain

        if selected is None:
            raise ValueError(f"Unknown task: {task_id}")

        feedback_record = {
            "task": selected,
            "status": status,
            "note": note,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.memory_store.log_interaction(
            {"type": "task_feedback", "payload": feedback_record, "mode": self.session.current_mode}
        )

        if status == "completed":
            self.session.momentum_score += 1
        elif status == "overwhelmed":
            self.session.overwhelm_counter += 1

        mode_result = self.adaptive_engine.evaluate(
            {
                "text": selected.get("title", ""),
                "clarity": {"annotations": []},
                "session": self.session,
                "metadata": {"feedback_status": status},
            }
        )
        self._update_mode(mode_result)
        return mode_result

    def override_mode(self, mode: str, reason: str) -> ModeResult:
        """Force switch to user-selected mode and log reasoning."""
        mode_result = self.adaptive_engine.override(mode, reason)
        self._update_mode(mode_result)
        self.memory_store.log_interaction(
            {
                "type": "mode_override",
                "mode": mode_result,
                "reason": reason,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        return mode_result

    def _update_mode(self, mode_result: ModeResult) -> None:
        self.session.current_mode = mode_result["mode"]
        self.session.mode_confidence = mode_result["confidence"]

