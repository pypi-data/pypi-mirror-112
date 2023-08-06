from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.layer_create import LayerCreate
from ...models.layer_get import LayerGet
from ...models.string_detail_error import StringDetailError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    time_series_uuid: str,
    json_body: LayerCreate,
) -> Dict[str, Any]:
    url = "{}/time_series/{time_series_uuid}/layers/".format(client.base_url, time_series_uuid=time_series_uuid)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, LayerGet, StringDetailError]]:
    if response.status_code == 201:
        response_201 = LayerGet.from_dict(response.json())

        return response_201
    if response.status_code == 404:
        response_404 = StringDetailError.from_dict(response.json())

        return response_404
    if response.status_code == 409:
        response_409 = StringDetailError.from_dict(response.json())

        return response_409
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, LayerGet, StringDetailError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    time_series_uuid: str,
    json_body: LayerCreate,
) -> Response[Union[HTTPValidationError, LayerGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        time_series_uuid=time_series_uuid,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    time_series_uuid: str,
    json_body: LayerCreate,
) -> Optional[Union[HTTPValidationError, LayerGet, StringDetailError]]:
    """Creates a layer for a time series."""

    return sync_detailed(
        client=client,
        time_series_uuid=time_series_uuid,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    time_series_uuid: str,
    json_body: LayerCreate,
) -> Response[Union[HTTPValidationError, LayerGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        time_series_uuid=time_series_uuid,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    time_series_uuid: str,
    json_body: LayerCreate,
) -> Optional[Union[HTTPValidationError, LayerGet, StringDetailError]]:
    """Creates a layer for a time series."""

    return (
        await asyncio_detailed(
            client=client,
            time_series_uuid=time_series_uuid,
            json_body=json_body,
        )
    ).parsed
