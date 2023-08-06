from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.user_get import UserGet
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Dict[str, Any]:
    url = "{}/users/{uuid}".format(client.base_url, uuid=uuid)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, UserGet]]:
    if response.status_code == 200:
        response_200 = UserGet.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, UserGet]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Response[Union[HTTPValidationError, UserGet]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Optional[Union[HTTPValidationError, UserGet]]:
    """Gets the requested user."""

    return sync_detailed(
        client=client,
        uuid=uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Response[Union[HTTPValidationError, UserGet]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Optional[Union[HTTPValidationError, UserGet]]:
    """Gets the requested user."""

    return (
        await asyncio_detailed(
            client=client,
            uuid=uuid,
        )
    ).parsed
