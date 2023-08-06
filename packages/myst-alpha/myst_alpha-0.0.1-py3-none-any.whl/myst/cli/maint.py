import os
import textwrap
from dataclasses import dataclass, field
from importlib import import_module
from typing import ClassVar, Dict, List, Optional, Set, Tuple, Type

import toml
import typer
from openapi_python_client import Config, MetaType, create_new_client
from plumbum import FG, local
from plumbum.commands.processes import ProcessExecutionError

from myst.client import Client
from myst.settings import PROJECT_ROOT

app = typer.Typer()

import shutil


@app.callback()
def main():
    """Utilities for maintainers of this library."""


@app.command()
def generate_api_client():
    """Generates the openapi client library."""
    lib_path = PROJECT_ROOT / "myst"
    project_name = "generated_openapi_client"

    # Create a (clean) place for the project to go.
    gen_client_container_path = lib_path / project_name
    shutil.rmtree(gen_client_container_path.absolute(), ignore_errors=True)

    # Generate a project config under our custom name.
    config = Config()
    config.project_name_override = project_name

    # Schema is based on the API host and version.
    schema_url = f"{Client.API_HOST}/{Client.API_VERSION}/openapi.json"

    # Generate the openapi client in the correct directory
    os.chdir(lib_path.absolute())
    create_new_client(url=schema_url, path=None, meta=MetaType.POETRY, config=config)

    # Make sure all required dependencies are present in the parent project.
    child_toml_path = gen_client_container_path / "pyproject.toml"
    with child_toml_path.open("r") as ctf:
        child_toml = toml.load(ctf)

    parent_toml_path = PROJECT_ROOT / "pyproject.toml"
    with parent_toml_path.open("r") as ptf:
        parent_toml = toml.load(ptf)

    child_deps: Dict[str, str] = child_toml["tool"]["poetry"]["dependencies"]
    parent_deps: Dict[str, str] = parent_toml["tool"]["poetry"]["dependencies"]

    poetry = local["poetry"]
    for dep, ver in child_deps.items():
        if dep in parent_deps:
            parent_ver = parent_deps[dep]
            if ver != parent_ver:
                typer.echo(
                    typer.style(
                        f"OpenAPI client wants {dep} version {ver}, but {parent_ver} is specified.", fg="yellow"
                    )
                )
        else:
            typer.echo(typer.style(f"Adding OpenAPI client dependency {dep}={ver} to project", fg="green"))
            poetry["add", f"{dep}={ver}"] & FG

    # Move the generated client in the correct location.
    gen_client_code_path = gen_client_container_path / project_name
    client_code_dest = lib_path / "openapi_client"
    shutil.move(str(gen_client_code_path.absolute()), str(client_code_dest.absolute()))

    # We no longer need the client path dir.
    typer.echo(f"removing {gen_client_container_path.absolute()}")
    shutil.rmtree(str(gen_client_container_path.absolute()))

    # Add DO NOT EDIT marker
    marker_path = client_code_dest / "DO_NOT_EDIT.md"
    with marker_path.open("w") as marker_file:
        marker_file.write(
            textwrap.dedent(
                """
                # DO NOT EDIT #

                The files in this directory were auto-generated using [openapi-python-client](https://github.com/openapi-generators/openapi-python-client).
                To update them, please run `myst maint generate-api-client`.
                """
            )
        )

    typer.echo(typer.style("OpenAPI client code generated successfully!", fg="green"))


@dataclass
class MethodArgument:
    """Represents arguments to a method."""

    name: str
    type_: str
    optional: bool

    @property
    def as_str(self) -> str:
        """String representation for function declaration."""
        type_ = f"Optional[{self.type_}]" if self.optional else self.type_
        arg = f"{self.name}: {type_}"

        return arg

    @property
    def as_kwarg_str(self) -> str:
        """String representation for function invocation."""
        kwarg_str = f"{self.name} = {self.name}"

        return kwarg_str


@dataclass
class EndpointMethod:
    """Represents a particular API route."""

    name: str
    calls: str
    args: List[MethodArgument] = field(default_factory=list)
    returns: str = field(default="None")

    @property
    def as_str(self) -> str:
        """This method as Python code."""
        args_str = ", ".join(arg.as_str for arg in self.args)

        call_args = ",".join(arg.as_kwarg_str for arg in self.args)
        if call_args:
            call_args = f", {call_args}"

        text = textwrap.dedent(
            f'''
            def {self.name}(self, {args_str}) -> {self.returns}:
                """Calls the {self.name} endpoint"""
                return self.call_endpoint({self.calls}{call_args})
        '''
        )

        return text


@dataclass
class Endpoints:
    """Contains all of the data needed to generate a single Endpoints file."""

    DEFAULT_IMPORTS: ClassVar[Set[str]] = {
        "from myst.endpoints.base import EndpointsBase",
    }

    name: str
    imports: Set[str] = field(default_factory=set)
    methods: List[EndpointMethod] = field(default_factory=list)

    @property
    def module_name(self) -> str:
        return f"myst.openapi_client.api.{self.name}"

    @property
    def title(self) -> str:
        return self.name.title().replace("_", "")

    def add_method(self, name: str) -> None:
        """Add a method under this endpoints collection."""
        full_mod_name = f"{self.module_name}.{name}"
        self.imports.add(f"import {full_mod_name}")

        # Actually import the module.
        mod = import_module(full_mod_name)

        # Generate a method for this file name.
        method = EndpointMethod(name=name, calls=f"{full_mod_name}.sync_detailed")
        self.methods.append(method)

        actual_method = getattr(mod, "sync_detailed")
        annotations: Dict[str, Type] = actual_method.__annotations__

        # Annotate the return.
        r_mod, r_type, optional = self.unwrap_type(annotations["return"])
        method.returns = r_type
        if r_mod:
            self.imports.add(f"from {r_mod} import {r_type}")

        for arg, arg_type in annotations.items():
            if arg in ("client", "return"):
                continue

            arg_type_mod, arg_type_name, optional = self.unwrap_type(arg_type)
            method.args.append(MethodArgument(name=arg, type_=arg_type_name, optional=optional))

            # Make sure we import all of the types we need.
            if arg_type_mod:
                self.imports.add(f"from {arg_type_mod} import {arg_type_name}")

    @classmethod
    def unwrap_type(cls, type_: Type, is_optional: bool = False) -> Tuple[Optional[str], str, bool]:
        """Returns a nested model from response/union/optional/error-handling wrappers."""
        mod = type_.__module__
        if mod == "builtins":
            return (None, str(type_.__name__), is_optional)
        if not hasattr(type_, "__args__"):
            return (mod, type_.__name__, is_optional)
        if len(type_.__args__) == 1:
            return cls.unwrap_type(type_.__args__[0])
        else:
            without_error = [arg for arg in type_.__args__ if "error" not in str(arg)]
            without_unset = [arg for arg in without_error if "Unset" not in str(arg)]
            without_none = [arg for arg in without_unset if arg != None.__class__]
            if len(without_none) == 1:
                return cls.unwrap_type(without_none[0], is_optional=(without_none == without_error))
            else:
                raise RuntimeError(f"cannot unwrap args `{type_.__args__}` of type `{type_}")

    @property
    def as_str(self) -> str:
        """Write the Endpoints file."""
        text = textwrap.dedent(
            f'''
            class {self.title}(EndpointsBase):
                """API methods for the `{self.name}` routes."""

        '''
        )

        # Pre-pend imports.
        imports = "\n".join(self.imports | self.DEFAULT_IMPORTS)
        text = f"{imports}\n\n{text}"

        # Pre-pend warning.
        warning = textwrap.dedent(
            f'''
            """Endpoints for the `{self.name}` API routes.

            NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
            please run the `maint generate-endpoints` command (usually, after first running
            the `maint generate-api-client` command)
            """
        '''
        )
        text = f"{warning}\n{text}"

        # Append methods.
        for method in self.methods:
            text += textwrap.indent(method.as_str, prefix="    ")
            text += "\n"

        return text


@app.command()
def generate_endpoints():
    """Generate the client endpoints to the API based on the OpenApi auto-gen client."""
    api_dir = PROJECT_ROOT / "myst" / "openapi_client" / "api"
    endpoints_dir = PROJECT_ROOT / "myst" / "endpoints"

    for mod_dir in api_dir.glob("*"):
        # Pay attention only to non-dunder directories.
        if not mod_dir.is_dir():
            continue
        if mod_dir.name.startswith("__"):
            continue

        # The directory will correspond to an `Endpoints` object.
        endpoint = Endpoints(name=mod_dir.name)

        for method_file in mod_dir.glob("*.py"):
            # ignore dunder files (probably just __init__.py)
            if method_file.name.startswith("__"):
                continue

            try:
                endpoint.add_method(method_file.stem)
            except:
                raise RuntimeError(f"Error adding method `{method_file.name}` of endpoint `{endpoint.name}`")

        endpoint_path = endpoints_dir / f"{endpoint.name}.py"
        with open(endpoint_path, "w+") as endpoint_file:
            endpoint_file.write(endpoint.as_str)


@app.command()
def publish(to_prod: bool = typer.Option(False, help="Publish to prod PyPI servers.")) -> None:
    """Publish the library to PyPI using `poetry`."""
    poetry = local["poetry"]
    opts = ["publish"]

    if to_prod:
        typer.confirm("Are you sure you're ready to publish to PyPI?", abort=True)
        color = "yellow"
    else:
        # make sure the test repo is in the repos list
        repo_name = "testpypi"
        poetry["config", f"repositories.{repo_name}", "https://test.pypi.org/legacy/"]()

        color = "green"
        opts.extend(["--repository", repo_name])

    with local.cwd(PROJECT_ROOT):
        try:
            poetry["build"] & FG
            poetry[opts] & FG
            typer.echo(typer.style("Published to PyPI", fg=color))
        except ProcessExecutionError:
            typer.echo(typer.style("Publishing to PyPI failed!", fg="red"))
            raise typer.Exit(1)
