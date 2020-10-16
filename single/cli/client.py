import typer as ty
import typing as t

app = ty.Typer(help="This is the command line frontend for the single client.")


@app.command()
def install(
    packages: t.List[str] = ty.Argument(..., help="The packages to install."),
    providers: t.List[str] = ty.Option(
        [],
        metavar="PROVIDERS",
        help="The providers to use. By default every provider is used.",
    ),
) -> None:
    """This is a client frontend for package installation."""
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
    """This is a client frontend for package removal."""
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
    """This is a client frontend for package updating."""
    pass


if __name__ == "__main__":
    app()
