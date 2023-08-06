from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.project_get import ProjectGet
from ...models.project_update import ProjectUpdate
from ...models.string_detail_error import StringDetailError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    uuid: str,
    json_body: ProjectUpdate,
) -> Dict[str, Any]:
    url = "{}/projects/{uuid}".format(client.base_url, uuid=uuid)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, ProjectGet, StringDetailError]]:
    if response.status_code == 200:
        response_200 = ProjectGet.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = StringDetailError.from_dict(response.json())

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, ProjectGet, StringDetailError]]:
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
    json_body: ProjectUpdate,
) -> Response[Union[HTTPValidationError, ProjectGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
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
    json_body: ProjectUpdate,
) -> Optional[Union[HTTPValidationError, ProjectGet, StringDetailError]]:
    """Updates a project."""

    return sync_detailed(
        client=client,
        uuid=uuid,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    uuid: str,
    json_body: ProjectUpdate,
) -> Response[Union[HTTPValidationError, ProjectGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    uuid: str,
    json_body: ProjectUpdate,
) -> Optional[Union[HTTPValidationError, ProjectGet, StringDetailError]]:
    """Updates a project."""

    return (
        await asyncio_detailed(
            client=client,
            uuid=uuid,
            json_body=json_body,
        )
    ).parsed
