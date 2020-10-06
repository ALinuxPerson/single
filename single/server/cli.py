import typer
from single.server import start
from single.server import enums as e


def main(
    port: int = typer.Option(25000, help="The port to start the server"),
    logging_level: e.LoggingLevel = typer.Option("INFO", help="The logging level."),
) -> None:
    """This is a server for single."""
    start(port, logging_level)


if __name__ == "__main__":
    typer.run(main)
