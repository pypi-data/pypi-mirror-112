from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.resource_list_user_get import ResourceListUserGet
from ...models.string_detail_error import StringDetailError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    organization_uuid: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/users/".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "organization_uuid": organization_uuid,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[HTTPValidationError, ResourceListUserGet, StringDetailError]]:
    if response.status_code == 200:
        response_200 = ResourceListUserGet.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = StringDetailError.from_dict(response.json())

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[HTTPValidationError, ResourceListUserGet, StringDetailError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    organization_uuid: Union[Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ResourceListUserGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        organization_uuid=organization_uuid,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    organization_uuid: Union[Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ResourceListUserGet, StringDetailError]]:
    """Lists users."""

    return sync_detailed(
        client=client,
        organization_uuid=organization_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    organization_uuid: Union[Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, ResourceListUserGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        organization_uuid=organization_uuid,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    organization_uuid: Union[Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, ResourceListUserGet, StringDetailError]]:
    """Lists users."""

    return (
        await asyncio_detailed(
            client=client,
            organization_uuid=organization_uuid,
        )
    ).parsed
