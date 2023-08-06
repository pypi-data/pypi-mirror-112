from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.time_series_query_result_get import TimeSeriesQueryResultGet
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    uuid: str,
    start_time: str,
    end_time: str,
    as_of_time: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/time_series/{uuid}:query".format(client.base_url, uuid=uuid)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "start_time": start_time,
        "end_time": end_time,
        "as_of_time": as_of_time,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, TimeSeriesQueryResultGet]]:
    if response.status_code == 200:
        response_200 = TimeSeriesQueryResultGet.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, TimeSeriesQueryResultGet]]:
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
    start_time: str,
    end_time: str,
    as_of_time: Union[Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, TimeSeriesQueryResultGet]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
        start_time=start_time,
        end_time=end_time,
        as_of_time=as_of_time,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    uuid: str,
    start_time: str,
    end_time: str,
    as_of_time: Union[Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, TimeSeriesQueryResultGet]]:
    """Queries time series data."""

    return sync_detailed(
        client=client,
        uuid=uuid,
        start_time=start_time,
        end_time=end_time,
        as_of_time=as_of_time,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    uuid: str,
    start_time: str,
    end_time: str,
    as_of_time: Union[Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, TimeSeriesQueryResultGet]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
        start_time=start_time,
        end_time=end_time,
        as_of_time=as_of_time,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    uuid: str,
    start_time: str,
    end_time: str,
    as_of_time: Union[Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, TimeSeriesQueryResultGet]]:
    """Queries time series data."""

    return (
        await asyncio_detailed(
            client=client,
            uuid=uuid,
            start_time=start_time,
            end_time=end_time,
            as_of_time=as_of_time,
        )
    ).parsed
