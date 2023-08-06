from functools import partial
from typing import Any, Dict, Optional, Union

from google.oauth2.service_account import IDTokenCredentials

from myst.credentials import Credentials
from myst.endpoints import Endpoints
from myst.openapi_client import AuthenticatedClient as OpenapiAuthClient
from myst.openapi_client import Client as OpenapiClient
from myst.version import get_package_version


class Client:
    """HTTP client for interacting with the Myst API."""

    API_HOST = "https://api.dev.myst.ai"
    API_VERSION = "v1alpha2"

    USER_AGENT_PREFORMAT = "Myst/{api_version} PythonBindings/{package_version}"

    # Increase default timeout, since it's insufficient for some longer inserts/retrievals.
    API_TIMEOUT_SEC = 30

    def __init__(self, credentials: Optional[Credentials] = None):
        """A wrapper object providing convenient API access with credentials."""
        self.credentials = credentials

    @property
    def user_agent(self) -> str:
        """Gets the `User-Agent` header string to send to the Myst API with requests."""
        # Infer Myst API version and Myst Python client library version for current active versions.
        user_agent = self.USER_AGENT_PREFORMAT.format(
            api_version=self.API_VERSION, package_version=get_package_version()
        )
        return user_agent

    def add_user_agent(self, headers: Dict[str, str]) -> None:
        """Adds user agent header to provided headers dictionary."""
        headers.update({"User-Agent": self.user_agent})

    @property
    def openapi_client(self) -> Union[OpenapiClient, OpenapiAuthClient]:
        """An openapi client for making requests.

        This is constructed anew each time, because the credential token may have expired.
        """
        if self.credentials:
            klass: partial[OpenapiClient] = partial(OpenapiAuthClient, token=self.credentials.token)
        else:
            klass = partial(OpenapiClient)

        client = klass(f"{self.API_HOST}/{self.API_VERSION}", timeout=self.API_TIMEOUT_SEC)
        self.add_user_agent(client.headers)

        return client

    @property
    def endpoints(self) -> Endpoints:
        """The tree of endpoints of the API."""
        return Endpoints(self.openapi_client)
