from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.time_series_insert import TimeSeriesInsert
from ...models.time_series_insert_result_get import TimeSeriesInsertResultGet
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    uuid: str,
    json_body: TimeSeriesInsert,
) -> Dict[str, Any]:
    url = "{}/time_series/{uuid}:insert".format(client.base_url, uuid=uuid)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, TimeSeriesInsertResultGet]]:
    if response.status_code == 200:
        response_200 = TimeSeriesInsertResultGet.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, TimeSeriesInsertResultGet]]:
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
    json_body: TimeSeriesInsert,
) -> Response[Union[HTTPValidationError, TimeSeriesInsertResultGet]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    uuid: str,
    json_body: TimeSeriesInsert,
) -> Optional[Union[HTTPValidationError, TimeSeriesInsertResultGet]]:
    """Inserts time series data."""

    return sync_detailed(
        client=client,
        uuid=uuid,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    uuid: str,
    json_body: TimeSeriesInsert,
) -> Response[Union[HTTPValidationError, TimeSeriesInsertResultGet]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    uuid: str,
    json_body: TimeSeriesInsert,
) -> Optional[Union[HTTPValidationError, TimeSeriesInsertResultGet]]:
    """Inserts time series data."""

    return (
        await asyncio_detailed(
            client=client,
            uuid=uuid,
            json_body=json_body,
        )
    ).parsed
