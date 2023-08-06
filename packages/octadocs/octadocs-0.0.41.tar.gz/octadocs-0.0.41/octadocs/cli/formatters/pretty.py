import itertools
from typing import Union

from classes import typeclass
from more_itertools import consume
from octadocs.types import SelectResult
from rdflib import URIRef, Literal, BNode
from rich.console import Console
from rich.table import Table


@typeclass
def pretty_print_value(rdflib_value: Union[URIRef, Literal, BNode]) -> str:
    raise NotImplementedError()


@pretty_print_value.instance(URIRef)
def _pretty_print_value_uri_ref(uriref: URIRef) -> str:
    """Format URI Ref."""
    return f'🔗 {uriref}'


@pretty_print_value.instance(Literal)
def _pretty_print_literal(literal: Literal) -> str:
    if isinstance(literal.value, bool):
        icon = '✅' if literal.value else '❌'
        return f'{icon} {literal.value}'

    if isinstance(literal.value, int):
        return f'🔢️ {literal.value}'

    elif isinstance(literal.value, str):
        return f'🔡 {literal.value}'

    raise Exception(f'Type {type(literal.value)} of {literal.value} unknown.')


@pretty_print_value.instance(BNode)
def _pretty_print_bnode(bnode: BNode) -> str:
    """Print a blank node."""
    return f'😶 {bnode}'


def pretty_print_select_result(select_result: SelectResult):
    """Print a SPARQL query result in style."""
    if not select_result:
        return

    table = Table(
        show_header=True,
        header_style="bold magenta",
    )

    first_row = select_result[0]

    consume(map(table.add_column, first_row.keys()))
    consume(itertools.starmap(
        table.add_row,
        [
            map(
                pretty_print_value,
                row.values(),
            )
            for row in select_result
        ],
    ))

    Console().print(table)
