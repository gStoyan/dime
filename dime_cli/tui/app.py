from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, Static

from dime_cli.tui.commands import GLOBAL_HELP, capture_news, parse_command, run_focus_command, run_todo_command
from dime_cli.tui.panels import format_focus_panel, format_todo_panel


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
        self.query_one("#todo-panel", Static).update(self._wrap_panel("Todo", format_todo_panel()))
        self.refresh_focus_panel()
        if fetch_news:
            try:
                self.news_cache = capture_news(self.current_news)
            except Exception as error:
                self.news_cache = f"Unable to load {self.current_news} news.\n{error}"
        self.query_one("#news-panel", Static).update(
            self._wrap_panel(f"News: {self.current_news}", self.news_cache)
        )

    def refresh_focus_panel(self) -> None:
        self.query_one("#focus-panel", Static).update(self._wrap_panel("Focus", format_focus_panel()))

    def _wrap_panel(self, title: str, body: str) -> str:
        return f"[b]{title}[/b]\n\n{body}"

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw = event.value.strip()
        event.input.value = ""
        kind, payload = parse_command(raw)

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
                message = run_todo_command(payload)
                self.refresh_panels(fetch_news=False)
            elif kind == "focus":
                message = run_focus_command(payload)
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