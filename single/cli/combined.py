from single.cli.client import app as client
from single.cli.server import app as server
import typer as ty

app = ty.Typer(
    help="This is the combined command line for the single client and the single server. If you want to "
    "use them individually, use 'singlec' for the client and 'singles' for the server."
)
app.add_typer(client, name="client")
app.add_typer(server, name="server")


if __name__ == "__main__":
    app()
