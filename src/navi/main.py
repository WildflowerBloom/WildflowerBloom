"""CLI entry point to launch Navi UI."""

from __future__ import annotations

from pathlib import Path

from navi.app import create_orchestrator
from navi.ui import build_interface


def main(storage_path: str | None = None) -> None:
    orchestrator = create_orchestrator(Path(storage_path) if storage_path else None)
    interface = build_interface(orchestrator)
    interface.launch(server_name="0.0.0.0", server_port=7860, inbrowser=False)


if __name__ == "__main__":
    main()

