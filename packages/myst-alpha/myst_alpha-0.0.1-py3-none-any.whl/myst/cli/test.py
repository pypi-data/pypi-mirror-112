import sys
from dataclasses import dataclass, field
from functools import partial
from typing import Any, Callable, Dict

import typer
from plumbum import FG, local
from plumbum.commands.processes import ProcessExecutionError

from myst.settings import PROJECT_ROOT


@dataclass(frozen=True)
class Task:
    """Represents a test task."""

    name: str
    should_run: bool
    func: Callable[[], None] = field(repr=False)

    def run(self) -> bool:
        """Runs the task

        Returns:
            bool: whether the task succeeded
        """
        try:
            self.func()  # type: ignore[misc]
            return True
        except typer.Exit:
            return False


app = typer.Typer()


@app.callback()
def main():
    """Tests for the client library"""
    pass


@app.command()
def all(
    run_pytest: bool = typer.Option(True, help="Include pytest in suite run"),
    run_mypy: bool = typer.Option(True, help="Include mypy in suite run"),
    run_black: bool = typer.Option(True, help="Include black in suite run"),
    run_isort: bool = typer.Option(True, help="Include isort in suite run"),
    run_twine: bool = typer.Option(True, help="Include twine in suite run"),
    fix: bool = typer.Option(False, help="automagically fix where possible"),
):
    """Runs all tasks in the test suite."""
    tasks = [
        Task("pytest", run_pytest, pytest),
        Task("mypy", run_mypy, mypy),
        Task("black", run_black, partial(black, fix=fix)),
        Task("isort", run_isort, partial(isort, fix=fix)),
        Task("twine", run_twine, partial(twine)),
    ]

    results: Dict[Task, bool] = {task: task.run() for task in tasks if task.should_run}
    failed = {task for task, result in results.items() if result is False}
    if any(failed):
        typer.echo(typer.style(f"Failed test tasks: {[f.name for f in failed]}", fg="red"))
        raise typer.Exit(1)
    else:
        typer.echo(typer.style(f"All {len(results)} test tasks succeeded!", fg="green"))


@app.command()
def pytest():
    """Runs pytest unit tests for the codebase."""
    with local.cwd(PROJECT_ROOT):
        try:
            local["pytest"] & FG
            typer.echo(typer.style("pytest succeeded!", fg="green"))
        except ProcessExecutionError:
            typer.echo(typer.style("pytest failed!", fg="red"))
            raise typer.Exit(1)


@app.command()
def mypy():
    """Runs mypy."""
    typer.echo(typer.style("Running mypy...", fg="yellow"))

    with local.cwd(PROJECT_ROOT):
        try:
            local["mypy"]["--show-error-codes", "."] & FG
            typer.echo(typer.style("mypy succeeded!", fg="green"))
        except ProcessExecutionError:
            typer.echo(typer.style("mypy failed!", fg="red"))
            raise typer.Exit(1)


@app.command()
def black(fix: bool = typer.Option(False, help="fix errors")):
    """Runs black."""
    typer.echo(typer.style("Running black...", fg="yellow"))

    # Make options for black.
    black_opts = ["--target-version=py36"]
    if not fix:
        black_opts.append("--check")
    black_opts.append(".")

    # Actually run it.
    with local.cwd(PROJECT_ROOT):
        try:
            local["black"][black_opts] & FG
            typer.echo(typer.style("black succeeded!", fg="green"))
        except ProcessExecutionError:
            typer.echo(typer.style("black failed!", fg="red"))
            raise typer.Exit(1)


@app.command()
def isort(fix: bool = typer.Option(False, help="fix errors")):
    """Runs isort."""
    typer.echo(typer.style("Running isort...", fg="yellow"))

    # Make options for isort.
    isort_opts = []
    if not fix:
        isort_opts.append("--check")
    isort_opts.append(".")

    # Actually run it.
    with local.cwd(PROJECT_ROOT):
        try:
            local["isort"][isort_opts] & FG
            typer.echo(typer.style("isort succeeded!", fg="green"))
        except ProcessExecutionError:
            typer.echo(typer.style("isort failed!", fg="red"))
            raise typer.Exit(1)


@app.command()
def twine():
    """Runs twine package test."""
    dist_dir = PROJECT_ROOT / "dist"

    with local.cwd(PROJECT_ROOT):
        try:
            local["poetry"]["build", "--no-interaction"] & FG
            local["twine"]["check", "--strict", str(dist_dir / "*")] & FG
            typer.echo(typer.style("package build succeeded!", fg="green"))
        except ProcessExecutionError:
            typer.echo(typer.style("package build failed!", fg="red"))
            raise typer.Exit(1)
