from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.layer_get import LayerGet
from ...models.layer_update import LayerUpdate
from ...models.string_detail_error import StringDetailError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    uuid: str,
    time_series_uuid: str,
    json_body: LayerUpdate,
) -> Dict[str, Any]:
    url = "{}/time_series/{time_series_uuid}/layers/{uuid}".format(
        client.base_url, uuid=uuid, time_series_uuid=time_series_uuid
    )

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
    if response.status_code == 200:
        response_200 = LayerGet.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = StringDetailError.from_dict(response.json())

        return response_404
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
    uuid: str,
    time_series_uuid: str,
    json_body: LayerUpdate,
) -> Response[Union[HTTPValidationError, LayerGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
        time_series_uuid=time_series_uuid,
        json_body=json_body,
    )

    response = httpx.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    uuid: str,
    time_series_uuid: str,
    json_body: LayerUpdate,
) -> Optional[Union[HTTPValidationError, LayerGet, StringDetailError]]:
    """Updates an existing layer for a time series."""

    return sync_detailed(
        client=client,
        uuid=uuid,
        time_series_uuid=time_series_uuid,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    uuid: str,
    time_series_uuid: str,
    json_body: LayerUpdate,
) -> Response[Union[HTTPValidationError, LayerGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
        time_series_uuid=time_series_uuid,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    uuid: str,
    time_series_uuid: str,
    json_body: LayerUpdate,
) -> Optional[Union[HTTPValidationError, LayerGet, StringDetailError]]:
    """Updates an existing layer for a time series."""

    return (
        await asyncio_detailed(
            client=client,
            uuid=uuid,
            time_series_uuid=time_series_uuid,
            json_body=json_body,
        )
    ).parsed
