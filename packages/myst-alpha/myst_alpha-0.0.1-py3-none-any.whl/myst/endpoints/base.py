from functools import partial
from typing import Any, Callable, Optional, Union

from myst.exceptions import MystAPIError, MystClientError, UnAuthenticatedError
from myst.openapi_client.client import AuthenticatedClient, Client
from myst.openapi_client.types import Response


class EndpointsBase:
    """Wrapper around auto-generated endpoints."""

    def __init__(self, client: Union[Client, AuthenticatedClient]):
        self.client = client

    def call_endpoint(self, func: Callable[..., Any], **kwargs) -> Any:
        """Calls the provided endpoint with an instance of the client.

        This function handles any errors returned from the API, including retries.
        """
        expected_client: Optional[Union[Client, AuthenticatedClient]] = func.__annotations__.get("client", None)

        if not expected_client:
            raise ValueError(f"No client parameter on `{func}` -- is it an API endpoint?")
        if expected_client is AuthenticatedClient and not isinstance(self.client, AuthenticatedClient):
            raise UnAuthenticatedError(
                f"API endpoint `{func}` expected authentication; did you pass `credentials` to `Client()`?"
            )

        try:
            resp: Response = func(client=self.client, **kwargs)
        except:
            raise MystClientError("Unexpected error making API request.")

        # Handle non-successful status codes from the API.
        if resp.status_code < 200 or resp.status_code >= 300:
            error = partial(MystAPIError, status_code=resp.status_code)
            if resp.parsed:
                raise error(message=resp.parsed)
            else:
                raise error(message="Unknown error from API")

        # TODO: assert that the response is of the correct type?
        return resp.parsed
