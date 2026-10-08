from __future__ import annotations

import io
from contextlib import redirect_stdout

from dime_cli.jobs.focus.focus import run as run_focus
from dime_cli.jobs.news.main import run as run_news
from dime_cli.jobs.todo.todo import run as run_todo


GLOBAL_HELP = """Commands:
    list
    add <task>
    complete <number>
    reset todo
    start
    stop
    reset focus
    tech
    world
    refresh
    help
    exit
"""


def parse_command(raw: str) -> tuple[str, list[str]]:
    parts = raw.strip().split()
    if not parts:
        return "noop", []

    head = parts[0].lower()

    if head in {"quit", "exit"}:
        return "quit", []
    if head == "help":
        return "help", []
    if head == "refresh":
        return "refresh", []
    if head in {"list", "add", "complete"}:
        return "todo", parts
    if head in {"start", "stop"}:
        return "focus", parts
    if head == "reset":
        if len(parts) == 1 or parts[1] == "focus":
            return "focus", ["reset"]
        if parts[1] == "todo":
            return "todo", ["reset"]
    if head in {"tech", "world"}:
        return "news", parts
    if head in {"todo", "focus", "news"}:
        return head, parts[1:]
    return "unknown", parts


def capture_command_output(func, *args: str | None) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args)
    return buffer.getvalue().strip() or "Done."


def capture_news(category: str) -> str:
    return capture_command_output(run_news, category) or f"No {category} news returned."


def run_todo_command(payload: list[str]) -> str:
    action = payload[0] if payload else ""
    task = " ".join(payload[1:]) if len(payload) > 1 else None
    return capture_command_output(run_todo, action, task)


def run_focus_command(payload: list[str]) -> str:
    action = payload[0] if payload else ""
    return capture_command_output(run_focus, action)