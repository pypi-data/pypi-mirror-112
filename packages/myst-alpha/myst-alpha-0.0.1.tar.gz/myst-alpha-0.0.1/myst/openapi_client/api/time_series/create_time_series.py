from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.string_detail_error import StringDetailError
from ...models.time_series_create import TimeSeriesCreate
from ...models.time_series_get import TimeSeriesGet
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: TimeSeriesCreate,
) -> Dict[str, Any]:
    url = "{}/time_series/".format(client.base_url)

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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
    if response.status_code == 201:
        response_201 = TimeSeriesGet.from_dict(response.json())

        return response_201
    if response.status_code == 409:
        response_409 = StringDetailError.from_dict(response.json())

        return response_409
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
    json_body: TimeSeriesCreate,
) -> Response[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
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
    json_body: TimeSeriesCreate,
) -> Optional[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
    """Creates a time series."""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: TimeSeriesCreate,
) -> Response[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
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
    json_body: TimeSeriesCreate,
) -> Optional[Union[HTTPValidationError, StringDetailError, TimeSeriesGet]]:
    """Creates a time series."""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
