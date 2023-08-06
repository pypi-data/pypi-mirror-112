from typing import Optional

import typer

from myst.cli.maint import app as maint_app
from myst.cli.test import app as test_app
from myst.cli.user import app as user_app
from myst.version import get_package_version

app = typer.Typer()
app.add_typer(maint_app, name="maint")
app.add_typer(test_app, name="tests")
app.add_typer(user_app, name="user")


def show_version(should: bool):
    """Shows the version and exits."""
    if should:
        typer.echo(get_package_version())
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=show_version,
        is_eager=True,
        help="Show version and exit",
    )
) -> None:
    """Myst AI client library package"""
    pass
