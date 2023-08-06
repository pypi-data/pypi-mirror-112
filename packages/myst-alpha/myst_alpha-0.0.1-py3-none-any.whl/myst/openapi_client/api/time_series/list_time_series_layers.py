from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.resource_list_layer_get import ResourceListLayerGet
from ...models.string_detail_error import StringDetailError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    time_series_uuid: str,
) -> Dict[str, Any]:
    url = "{}/time_series/{time_series_uuid}/layers/".format(client.base_url, time_series_uuid=time_series_uuid)

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
) -> Optional[Union[HTTPValidationError, ResourceListLayerGet, StringDetailError]]:
    if response.status_code == 200:
        response_200 = ResourceListLayerGet.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = StringDetailError.from_dict(response.json())

        return response_404
    if response.status_code == 403:
        response_403 = StringDetailError.from_dict(response.json())

        return response_403
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[HTTPValidationError, ResourceListLayerGet, StringDetailError]]:
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
) -> Response[Union[HTTPValidationError, ResourceListLayerGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        time_series_uuid=time_series_uuid,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    time_series_uuid: str,
) -> Optional[Union[HTTPValidationError, ResourceListLayerGet, StringDetailError]]:
    """Lists layers for a time series."""

    return sync_detailed(
        client=client,
        time_series_uuid=time_series_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    time_series_uuid: str,
) -> Response[Union[HTTPValidationError, ResourceListLayerGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        time_series_uuid=time_series_uuid,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    time_series_uuid: str,
) -> Optional[Union[HTTPValidationError, ResourceListLayerGet, StringDetailError]]:
    """Lists layers for a time series."""

    return (
        await asyncio_detailed(
            client=client,
            time_series_uuid=time_series_uuid,
        )
    ).parsed
