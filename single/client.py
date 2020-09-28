"""This is the command line client."""
import typer as ty
import typing as t

app = ty.Typer()


@app.command()
def install(
    packages: t.List[str] = ty.Argument(..., help="The packages to install."),
    sources: t.List[str] = ty.Option(
        [],
        metavar="SOURCES",
        help="The sources to use. By default every source is used.",
    ),
) -> None:
    """Installs packages."""
    pass


@app.command()
def remove(
    packages: t.List[str] = ty.Argument(..., help="The packages to remove."),
    sources: t.List[str] = ty.Option(
        [],
        metavar="SOURCES",
        help="The sources to use. By default every source is used.",
    ),
) -> None:
    """Removes packages."""
    pass


@app.command()
def update(
    packages: t.List[str] = ty.Argument(
        None,
        help="The packages to update. By default every package is updated. Please note that this command may have "
        "warnings or even error depending on your source's implementation.",
    ),
    sources: t.List[str] = ty.Option(
        [],
        metavar="SOURCES",
        help="The sources to use. By default every source is used.",
    ),
) -> None:
    """Updates packages."""
    pass


def main() -> None:
    """This is the entry point for poetry to use as a command for `single`.

    Returns:
        Nothing, as far as I know.
    """
    return app()


if __name__ == "__main__":
    main()
