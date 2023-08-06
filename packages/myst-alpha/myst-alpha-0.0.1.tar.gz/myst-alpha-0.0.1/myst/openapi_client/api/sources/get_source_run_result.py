from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.source_run_result_get import SourceRunResultGet
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    source_uuid: str,
    uuid: str,
) -> Dict[str, Any]:
    url = "{}/sources/{source_uuid}/source_run_results/{uuid}".format(
        client.base_url, source_uuid=source_uuid, uuid=uuid
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, None, SourceRunResultGet]]:
    if response.status_code == 200:
        response_200 = SourceRunResultGet.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, None, SourceRunResultGet]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    source_uuid: str,
    uuid: str,
) -> Response[Union[HTTPValidationError, None, SourceRunResultGet]]:
    kwargs = _get_kwargs(
        client=client,
        source_uuid=source_uuid,
        uuid=uuid,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    source_uuid: str,
    uuid: str,
) -> Optional[Union[HTTPValidationError, None, SourceRunResultGet]]:
    """Gets a source run result by its unique identifier."""

    return sync_detailed(
        client=client,
        source_uuid=source_uuid,
        uuid=uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    source_uuid: str,
    uuid: str,
) -> Response[Union[HTTPValidationError, None, SourceRunResultGet]]:
    kwargs = _get_kwargs(
        client=client,
        source_uuid=source_uuid,
        uuid=uuid,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    source_uuid: str,
    uuid: str,
) -> Optional[Union[HTTPValidationError, None, SourceRunResultGet]]:
    """Gets a source run result by its unique identifier."""

    return (
        await asyncio_detailed(
            client=client,
            source_uuid=source_uuid,
            uuid=uuid,
        )
    ).parsed
