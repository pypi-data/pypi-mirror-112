import typer
from .version import __version__

app = typer.Typer()

def version_callback(value: bool):
    if value:
        typer.echo(
            r"""
                LaTeX Template Generating System by Curvenote
            """
        )
        typer.echo(f"Version: {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    )
):
    return
