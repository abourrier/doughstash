from importlib.metadata import version

from textual.app import App, ComposeResult
from textual.widgets import Static


class DoughstashApp(App):
    """Textual app for doughstash."""

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Static(f"doughstash {version('doughstash-tui')}")


def run() -> None:
    DoughstashApp().run()
