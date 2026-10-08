from __future__ import annotations

import time

from dime_cli.jobs.focus.focus import load_state
from dime_cli.jobs.todo.todo import load_todo_list


TODO_EMPTY_TEXT = "No tasks yet.\n\nCommands:\n  list\n  add <task>\n  complete <number>\n  reset todo"


def format_todo_panel() -> str:
    items = load_todo_list()
    if not items:
        return TODO_EMPTY_TEXT

    lines = []
    for index, item in enumerate(items, start=1):
        status = "[x]" if item["completed"] else "[ ]"
        lines.append(f"{index}. {status} {item['task']}")
    return "\n".join(lines)


def format_elapsed(state: dict[str, float | None]) -> str:
    elapsed = float(state.get("elapsed", 0) or 0)
    start_time = state.get("start_time")
    if start_time is not None:
        elapsed += time.time() - float(start_time)

    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def format_focus_panel() -> str:
    focus_state = load_state("focus")
    break_state = load_state("break")

    if focus_state["start_time"] is not None:
        active = "Focus"
    elif break_state["start_time"] is not None:
        active = "Break"
    else:
        active = "Idle"

    return "\n".join(
        [
            f"Status: {active}",
            f"Focus: {format_elapsed(focus_state)}",
            f"Break: {format_elapsed(break_state)}",
            "",
            "Commands:",
            "  start",
            "  stop",
            "  reset focus",
        ]
    )