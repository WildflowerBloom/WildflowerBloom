"""Application factory to assemble Navi subsystems."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from apscheduler.schedulers.background import BackgroundScheduler

from navi.adaptive import AdaptiveModeEngine, ModeConfig
from navi.adaptive.classifier import NaiveBayesClassifier
from navi.adaptive.features import DefaultFeatureExtractor
from navi.adaptive.heuristics import HeuristicRule, KeywordHeuristicEngine
from navi.clarity import DefaultClarityPipeline
from navi.core.orchestrator import Orchestrator, SessionState
from navi.memory import SQLiteMemoryStore
from navi.models import OllamaClient
from navi.tasks import DefaultTaskTranslator
from navi.anchors import SoundAnchorBus
from navi.scheduler import ReminderScheduler


def create_orchestrator(storage_path: Path | None = None) -> Orchestrator:
    memory_path = storage_path or Path.home() / ".navi" / "memory.db"
    session = SessionState(session_id="default")

    clarity = DefaultClarityPipeline()
    feature_extractor = DefaultFeatureExtractor()
    classifier = NaiveBayesClassifier()
    heuristics = KeywordHeuristicEngine(
        rules=[
            HeuristicRule(mode="LowDopamine", weight=0.2, keywords=["stuck", "tired", "can't start"]),
            HeuristicRule(mode="Overwhelm", weight=0.2, keywords=["too much", "everything", "overwhelmed"]),
            HeuristicRule(mode="Crash", weight=0.2, keywords=["exhausted", "burned out", "done"]),
            HeuristicRule(mode="Hyperfocus", weight=0.1, keywords=["still going", "keep pushing"]),
        ]
    )
    modes: Dict[str, ModeConfig] = {
        "LowDopamine": ModeConfig(
            name="LowDopamine",
            description="Energy dip; needs momentum spark.",
            interventions=["sound:ignite_chime", "template:spark_challenge"],
        ),
        "Overwhelm": ModeConfig(
            name="Overwhelm",
            description="Too many threads; simplify and ground.",
            interventions=["sound:ground_bell", "template:grounding_reset"],
        ),
        "Hyperfocus": ModeConfig(
            name="Hyperfocus",
            description="Protect energy with checkpoints.",
            interventions=["sound:soft_chime", "template:checkpoint"],
        ),
        "Crash": ModeConfig(
            name="Crash",
            description="Gentle recovery after effort.",
            interventions=["sound:wave_wash", "template:restoration"],
        ),
        "Regulated": ModeConfig(
            name="Regulated",
            description="Balanced focus; ready for planning.",
            interventions=["sound:sparkle", "template:celebrate_plan"],
        ),
    }
    adaptive_engine = AdaptiveModeEngine(
        modes=modes,
        feature_extractor=feature_extractor,
        classifier=classifier,
        heuristics=heuristics,
        default_mode="Regulated",
    )

    memory_store = SQLiteMemoryStore(path=memory_path)
    llm_client = OllamaClient()
    task_translator = DefaultTaskTranslator()
    anchors = SoundAnchorBus()
    scheduler = ReminderScheduler(scheduler=BackgroundScheduler())

    orchestrator = Orchestrator(
        session=session,
        clarity=clarity,
        adaptive_engine=adaptive_engine,
        memory_store=memory_store,
        llm=llm_client,
        task_translator=task_translator,
        anchors=anchors,
        scheduler=scheduler,
    )

    return orchestrator

