import typer

from myst.client import Client
from myst.credentials import GoogleConsoleCredentials

app = typer.Typer()


@app.callback()
def main():
    """User management commands."""
    pass


@app.command()
def get_me(use_cache: bool = True, use_console: bool = True):
    """Returns the server's concept of the user using local credentials."""
    creds = GoogleConsoleCredentials(use_console=use_console, use_cache=use_cache)
    client = Client(credentials=creds)
    typer.echo(client.endpoints.users.get_me())
