import typer

from doughstash_tui.app import run as run_tui

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """doughstash — personal finance and investment tracker."""
    if ctx.invoked_subcommand is None:
        run_tui()
