from __future__ import annotations

import io
import time
from contextlib import redirect_stdout

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Footer, Header, Input, Static

from dime_cli.jobs.focus.focus import run as run_focus
from dime_cli.jobs.focus.focus import load_state
from dime_cli.jobs.news.main import run as run_news
from dime_cli.jobs.todo.todo import load_todo_list, run as run_todo


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


def _format_todo_panel() -> str:
    items = load_todo_list()
    if not items:
        return "No tasks yet.\n\nCommands:\n  list\n  add <task>\n  complete <number>\n  reset todo"

    lines = []
    for index, item in enumerate(items, start=1):
        status = "[x]" if item["completed"] else "[ ]"
        lines.append(f"{index}. {status} {item['task']}")
    return "\n".join(lines)


def _format_elapsed(state: dict[str, float | None]) -> str:
    elapsed = float(state.get("elapsed", 0) or 0)
    start_time = state.get("start_time")
    if start_time is not None:
        elapsed += time.time() - float(start_time)

    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def _format_focus_panel() -> str:
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
            f"Focus: {_format_elapsed(focus_state)}",
            f"Break: {_format_elapsed(break_state)}",
            "",
            "Commands:",
            "  start",
            "  stop",
            "  reset focus",
        ]
    )


def _capture_news(category: str) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        run_news(category)
    return buffer.getvalue().strip() or f"No {category} news returned."


def _parse_command(raw: str) -> tuple[str, list[str]]:
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
    if head == "start" or head == "stop":
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


def _run_and_capture(func, *args: str | None) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func(*args)
    return buffer.getvalue().strip() or "Done."


class DimeTextualApp(App[None]):
    CSS = """
    Screen {
        layout: vertical;
    }

    #body {
        height: 1fr;
        padding: 1 2;
    }

    .panel {
        border: round $accent;
        padding: 1;
        width: 1fr;
        height: 1fr;
    }

    #left-column,
    #right-column {
        width: 1fr;
        height: 1fr;
    }

    #command-bar {
        dock: bottom;
        height: 3;
        margin: 0 2 1 2;
    }

    #status {
        dock: bottom;
        height: 4;
        margin: 0 2 1 2;
        border: round $secondary;
        padding: 0 1;
    }
    """

    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="body"):
            with Vertical(id="left-column"):
                yield Static(id="todo-panel", classes="panel")
            with Vertical(id="right-column"):
                yield Static(id="focus-panel", classes="panel")
                yield Static(id="news-panel", classes="panel")
        yield Static("Type 'help' for commands.", id="status")
        yield Input(placeholder="Try: add finish report, start, tech, refresh", id="command-bar")
        yield Footer()

    def on_mount(self) -> None:
        self.current_news = "tech"
        self.news_cache = "Loading news..."
        self.refresh_panels(fetch_news=True)
        self.set_interval(1, self.refresh_focus_panel)

    def refresh_panels(self, fetch_news: bool = False) -> None:
        self.query_one("#todo-panel", Static).update(self._wrap_panel("Todo", _format_todo_panel()))
        self.refresh_focus_panel()
        if fetch_news:
            try:
                self.news_cache = _capture_news(self.current_news)
            except Exception as error:
                self.news_cache = f"Unable to load {self.current_news} news.\n{error}"
        self.query_one("#news-panel", Static).update(
            self._wrap_panel(f"News: {self.current_news}", self.news_cache)
        )

    def refresh_focus_panel(self) -> None:
        self.query_one("#focus-panel", Static).update(self._wrap_panel("Focus", _format_focus_panel()))

    def _wrap_panel(self, title: str, body: str) -> str:
        return f"[b]{title}[/b]\n\n{body}"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        event.input.value = ""
        kind, payload = _parse_command(raw)

        if kind == "noop":
            return
        if kind == "quit":
            self.exit()
            return
        if kind == "help":
            self.query_one("#status", Static).update(GLOBAL_HELP.strip())
            return
        if kind == "refresh":
            self.refresh_panels(fetch_news=True)
            self.query_one("#status", Static).update("Panels refreshed.")
            return
        if kind == "unknown":
            self.query_one("#status", Static).update(f"Unknown command: {raw}")
            return

        try:
            if kind == "todo":
                action = payload[0] if payload else ""
                task = " ".join(payload[1:]) if len(payload) > 1 else None
                message = _run_and_capture(run_todo, action, task)
                self.refresh_panels(fetch_news=False)
            elif kind == "focus":
                action = payload[0] if payload else ""
                message = _run_and_capture(run_focus, action)
                self.refresh_panels(fetch_news=False)
            else:
                category = payload[0] if payload else self.current_news
                self.current_news = category
                self.refresh_panels(fetch_news=True)
                message = f"Loaded {category} news."
        except Exception as error:
            message = str(error)

        self.query_one("#status", Static).update(message)


def run_textual_app() -> None:
    DimeTextualApp().run()