import os
from typing import Callable, Any

import click


def save_logs(func: Callable[[Any, ...], None]) -> Callable[[Any, ...], None]:
    save = click.option("-s", "--save", is_flag=True, help="Save log message to file")
    output = click.option(
        "-o",
        "--output",
        type=click.STRING,
        default=lambda: os.getcwd(),
        help="Path to output directory for the saved log file",
    )
    log = click.option(
        "--log",
        type=click.STRING,
        default=lambda: f"{func.__name__}.log",
        help="Saved log file name",
    )
    return save(output(log(func)))


def sort_order_results(func: Callable[[Any, ...], None]) -> Callable[[Any, ...], None]:
    sort = click.option(
        "--sort",
        type=click.Choice(["name", "size", "date", "modified", "type"], case_sensitive=False),
        help="Sorting criteria",
    )
    desc = click.option(
        "--desc",
        is_flag=True,
        help="Display result in descending order",
    )
    return sort(desc(func))
