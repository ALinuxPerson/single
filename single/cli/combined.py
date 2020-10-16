from single.cli.client import app as client
from single.cli.server import app as server
import typer as ty

app = ty.Typer()
app.add_typer(client, name="client")
app.add_typer(server, name="server")


if __name__ == "__main__":
    app()
