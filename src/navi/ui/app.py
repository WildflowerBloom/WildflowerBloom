"""Gradio interface shell for Navi."""

from __future__ import annotations

from typing import Any, Dict

import gradio as gr

from navi.core.orchestrator import Orchestrator


def build_interface(orchestrator: Orchestrator) -> gr.Blocks:
    """Return a Gradio Blocks interface bound to the orchestrator."""

    with gr.Blocks(title="Navi Copilot") as demo:
        chat = gr.Chatbot(label="Navi Conversation", height=400)
        mode_mark = gr.Markdown("**Mode:** ...")
        task_gallery = gr.JSON(label="Micro-Actions (debug view)", value=[])
        mode_state = gr.State({})

        def submit(user_text: str, history: list[tuple[str, str]], _state: Dict[str, Any]) -> tuple[list, Dict[str, Any]]:
            result = orchestrator.submit_entry(user_text)
            history = history + [(user_text, result["assistant_text"])]
            mode = result["mode"]["mode"]
            confidence = result["mode"]["confidence"]
            mode_markdown = f"**Mode:** {mode} _(confidence {confidence:.2f})_"
            tasks = result["micro_actions"]
            return history, {"mode": mode_markdown, "tasks": tasks}

        def update_render(data: Dict[str, Any]) -> tuple[str, list]:
            return data.get("mode", "**Mode:** ..."), data.get("tasks", [])

        user_input = gr.Textbox(label="Share your state", placeholder="Tell Navi what's happening...")
        submit_btn = gr.Button("Send")

        submit_btn.click(
            submit,
            inputs=[user_input, chat, mode_state],
            outputs=[chat, mode_state],
        ).then(
            update_render,
            inputs=[mode_state],
            outputs=[mode_mark, task_gallery],
        )

    return demo

