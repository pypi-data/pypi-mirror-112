from typer import Typer
from octadocs.cli import sparql

app = Typer()

app.add_typer(sparql.app)
