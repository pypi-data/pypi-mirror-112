import csv
import sys
from pathlib import Path

from octadocs.cli.formatters.pretty import pretty_print_select_result
from octadocs.octiron import Octiron
from octadocs.storage import DiskCacheStorage
from octadocs.types import QueryResultsFormat, SelectResult
from typer import Option, Argument, Typer

app = Typer(name='query')


def create_octiron() -> Octiron:
    octiron = Octiron(root_directory=Path.cwd() / 'docs')

    disk_cache_storage = DiskCacheStorage(octiron=octiron)
    disk_cache_storage.load()

    return octiron


@app.command(name='file')
def query_file(
    path: Path = Argument(..., dir_okay=False, exists=True, allow_dash=True),
):
    """Run a SPARQL query stored in a file."""
    octiron = create_octiron()

    query_result = octiron.query(path.read_text())
    pretty_print_select_result(query_result)


@app.command(name='text')
def query_text(
    fmt: QueryResultsFormat = Option(
        default=QueryResultsFormat.CSV,
        metavar='format',
    ),
    query_text: str = Argument(..., metavar='query'),
) -> None:
    """Run a SPARQL query against the graph."""
    octiron = create_octiron()

    query_result = octiron.query(query_text)

    pretty_print_select_result(query_result)
    return

    if isinstance(query_result, SelectResult):
        if not query_result:
            return

        first_row = query_result[0]
        fieldnames = first_row.keys()

        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(query_result)

    else:
        raise ValueError(f'SPARQL result format {query_result} not recognized.')
