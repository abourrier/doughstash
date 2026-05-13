from pathlib import Path
from typing import Annotated

import typer
from doughstash_db.engine import create_engine
from doughstash_tui.app import run as run_tui

from doughstash_cli.config import ENV_DB_PATH, Config

app = typer.Typer()


@app.callback()
def main(
    ctx: typer.Context,
    db_path: Annotated[
        Path,
        typer.Option(
            "--db-path",
            "-d",
            envvar=ENV_DB_PATH,
            help="Path to the SQLite database file.",
        ),
    ],
) -> None:
    """Manage personal finances and investments."""
    ctx.obj = Config(db_path=db_path)


@app.command()
def tui(ctx: typer.Context) -> None:
    """Launch the doughstash TUI."""
    config: Config = ctx.obj
    engine = create_engine(f"sqlite:///{config.db_path}")
    try:
        run_tui(engine)
    finally:
        engine.dispose()
