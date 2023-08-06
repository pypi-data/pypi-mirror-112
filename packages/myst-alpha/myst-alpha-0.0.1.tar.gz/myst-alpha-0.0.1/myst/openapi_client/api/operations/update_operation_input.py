from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.input_get import InputGet
from ...models.input_update import InputUpdate
from ...models.string_detail_error import StringDetailError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    uuid: str,
    operation_uuid: str,
    json_body: InputUpdate,
) -> Dict[str, Any]:
    url = "{}/operations/{operation_uuid}/inputs/{uuid}".format(
        client.base_url, uuid=uuid, operation_uuid=operation_uuid
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, InputGet, StringDetailError]]:
    if response.status_code == 200:
        response_200 = InputGet.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = StringDetailError.from_dict(response.json())

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, InputGet, StringDetailError]]:
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
    operation_uuid: str,
    json_body: InputUpdate,
) -> Response[Union[HTTPValidationError, InputGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
        operation_uuid=operation_uuid,
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
    operation_uuid: str,
    json_body: InputUpdate,
) -> Optional[Union[HTTPValidationError, InputGet, StringDetailError]]:
    """Updates an existing input for an operation."""

    return sync_detailed(
        client=client,
        uuid=uuid,
        operation_uuid=operation_uuid,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    uuid: str,
    operation_uuid: str,
    json_body: InputUpdate,
) -> Response[Union[HTTPValidationError, InputGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
        operation_uuid=operation_uuid,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    uuid: str,
    operation_uuid: str,
    json_body: InputUpdate,
) -> Optional[Union[HTTPValidationError, InputGet, StringDetailError]]:
    """Updates an existing input for an operation."""

    return (
        await asyncio_detailed(
            client=client,
            uuid=uuid,
            operation_uuid=operation_uuid,
            json_body=json_body,
        )
    ).parsed
