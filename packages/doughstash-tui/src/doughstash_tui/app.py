from importlib.metadata import version
from typing import TYPE_CHECKING

from textual.app import App, ComposeResult
from textual.widgets import Static

if TYPE_CHECKING:
    from sqlalchemy import Engine


class DoughstashApp(App):
    """Textual app for doughstash."""

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, engine: Engine) -> None:
        super().__init__()
        self.engine = engine

    def compose(self) -> ComposeResult:
        yield Static(f"doughstash {version('doughstash-tui')}")


def run(engine: Engine) -> None:
    DoughstashApp(engine).run()
