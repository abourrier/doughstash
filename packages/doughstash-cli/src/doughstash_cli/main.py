import typer
from doughstash_tui.app import run as run_tui

app = typer.Typer()


@app.command()
def tui() -> None:
    """Launch the doughstash TUI."""
    run_tui()
