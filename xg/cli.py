import typer

from xg.commands.init import init

app = typer.Typer()

app.command()(init)


@app.command()
def hello():
    typer.echo("Hello! This is xgit...")


def main(args: str = None):
    app()
