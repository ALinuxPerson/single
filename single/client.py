"""This is the command line client."""
import typer as ty
import typing as t
from single.server import start
from single import enums

app = ty.Typer()


@app.command()
def install(
    packages: t.List[str] = ty.Argument(..., help="The packages to install."),
    providers: t.List[str] = ty.Option(
        [],
        metavar="PROVIDERS",
        help="The providers to use. By default every provider is used.",
    ),
) -> None:
    """Installs packages."""
    pass


@app.command()
def remove(
    packages: t.List[str] = ty.Argument(..., help="The packages to remove."),
    providers: t.List[str] = ty.Option(
        [],
        metavar="PROVIDERS",
        help="The providers to use. By default every provider is used.",
    ),
) -> None:
    """Removes packages."""
    pass


@app.command()
def update(
    packages: t.List[str] = ty.Argument(
        None,
        help="The packages to update. By default every package is updated. Please note that this command may have "
        "warnings or even error depending on your provider's implementation.",
    ),
    providers: t.List[str] = ty.Option(
        [],
        metavar="PROVIDERS",
        help="The providers to use. By default every provider is used.",
    ),
) -> None:
    """Updates packages."""
    pass


@app.command()
def server(
    port: int = ty.Option(25000, help="The port to start the server"),
    logging_level: enums.LoggingLevel = ty.Option("INFO", help="The logging level"),
) -> None:
    """This is the server for single."""
    start(port, logging_level)


def main() -> None:
    """This is the entry point for poetry to use as a command for `single`.

    Returns:
        Nothing, as far as I know.
    """
    return app()


if __name__ == "__main__":
    main()
