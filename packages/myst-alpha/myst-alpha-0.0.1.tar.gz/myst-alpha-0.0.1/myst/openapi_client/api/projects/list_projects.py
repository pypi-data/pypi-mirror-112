from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.resource_list_project_get import ResourceListProjectGet
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/projects/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[ResourceListProjectGet]:
    if response.status_code == 200:
        response_200 = ResourceListProjectGet.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ResourceListProjectGet]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ResourceListProjectGet]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[ResourceListProjectGet]:
    """Lists projects."""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[ResourceListProjectGet]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[ResourceListProjectGet]:
    """Lists projects."""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
