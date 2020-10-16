import typer as ty
from single import _enums as enums
from single.server import start as start_

app = ty.Typer()


@app.command()
def start(
    port: int = ty.Option(25000, help="The port to broadcast to."),
    logging_level: enums.LoggingLevel = ty.Option("INFO", help="The logging level."),
) -> None:
    """This is the command line frontend for the single server."""
    start_(port, logging_level)


if __name__ == "__main__":
    app()
