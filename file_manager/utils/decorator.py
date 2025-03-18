import click


def save_logs(func):
    func = click.option("-s", "--save", is_flag=True, help="Save log message to file")(func)

    func = click.option(
        "-o",
        "--output",
        type=click.STRING,
        default=None,
        help="Path to output directory for the saved log file",
    )(func)

    func = click.option(
        "--log",
        type=click.STRING,
        default=lambda: f"{func.__name__}.log",
        help="Saved log file name",
    )(func)

    return func
