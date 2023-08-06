from typer import Typer
from octadocs.cli import query

app = Typer()

app.add_typer(query.app)


@app.command()
def alter() -> None:
    ...
