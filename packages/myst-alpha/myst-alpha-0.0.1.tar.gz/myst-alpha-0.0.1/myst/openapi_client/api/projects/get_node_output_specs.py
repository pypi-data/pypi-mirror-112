from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.output_specs_get import OutputSpecsGet
from ...models.string_detail_error import StringDetailError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_uuid: str,
    node_uuid: str,
) -> Dict[str, Any]:
    url = "{}/projects/{project_uuid}/nodes/{node_uuid}:get_output_specs".format(
        client.base_url, project_uuid=project_uuid, node_uuid=node_uuid
    )

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[OutputSpecsGet, StringDetailError]]:
    if response.status_code == 200:
        response_200 = OutputSpecsGet.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = StringDetailError.from_dict(response.json())

        return response_404
    if response.status_code == 422:
        response_422 = StringDetailError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[OutputSpecsGet, StringDetailError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_uuid: str,
    node_uuid: str,
) -> Response[Union[OutputSpecsGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        project_uuid=project_uuid,
        node_uuid=node_uuid,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_uuid: str,
    node_uuid: str,
) -> Optional[Union[OutputSpecsGet, StringDetailError]]:
    """Returns the output specs for the specified node."""

    return sync_detailed(
        client=client,
        project_uuid=project_uuid,
        node_uuid=node_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_uuid: str,
    node_uuid: str,
) -> Response[Union[OutputSpecsGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        project_uuid=project_uuid,
        node_uuid=node_uuid,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_uuid: str,
    node_uuid: str,
) -> Optional[Union[OutputSpecsGet, StringDetailError]]:
    """Returns the output specs for the specified node."""

    return (
        await asyncio_detailed(
            client=client,
            project_uuid=project_uuid,
            node_uuid=node_uuid,
        )
    ).parsed
