import pytest
from typer import Exit
from typer.testing import CliRunner

from myst.cli import app


@pytest.fixture
def runner():
    return CliRunner()


def test_version(runner):
    """Run should invoke the myst app."""
    # All three tasks should run and will succeed.
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert len(result.stdout.strip().split(".")) == 3
