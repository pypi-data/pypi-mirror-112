from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.string_detail_error import StringDetailError
from ...models.user_create import UserCreate
from ...models.user_get import UserGet
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: UserCreate,
) -> Dict[str, Any]:
    url = "{}/users/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, StringDetailError, UserGet]]:
    if response.status_code == 201:
        response_201 = UserGet.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = StringDetailError.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = StringDetailError.from_dict(response.json())

        return response_403
    if response.status_code == 409:
        response_409 = StringDetailError.from_dict(response.json())

        return response_409
    if response.status_code == 404:
        response_404 = StringDetailError.from_dict(response.json())

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, StringDetailError, UserGet]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: UserCreate,
) -> Response[Union[HTTPValidationError, StringDetailError, UserGet]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: UserCreate,
) -> Optional[Union[HTTPValidationError, StringDetailError, UserGet]]:
    """Creates a user."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: UserCreate,
) -> Response[Union[HTTPValidationError, StringDetailError, UserGet]]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: UserCreate,
) -> Optional[Union[HTTPValidationError, StringDetailError, UserGet]]:
    """Creates a user."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
