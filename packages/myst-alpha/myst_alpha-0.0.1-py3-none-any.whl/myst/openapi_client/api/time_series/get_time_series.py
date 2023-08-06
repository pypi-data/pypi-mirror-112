from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.string_detail_error import StringDetailError
from ...models.time_series_get import TimeSeriesGet
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Dict[str, Any]:
    url = "{}/time_series/{uuid}".format(client.base_url, uuid=uuid)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
    if response.status_code == 200:
        response_200 = TimeSeriesGet.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = StringDetailError.from_dict(response.json())

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
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
) -> Response[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
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
) -> Optional[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
    """Gets a time series by its unique identifier."""

    return sync_detailed(
        client=client,
        uuid=uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Response[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
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
) -> Optional[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
    """Gets a time series by its unique identifier."""

    return (
        await asyncio_detailed(
            client=client,
            uuid=uuid,
        )
    ).parsed
