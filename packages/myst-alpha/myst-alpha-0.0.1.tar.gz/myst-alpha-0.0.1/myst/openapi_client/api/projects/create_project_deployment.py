from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.deployment_create import DeploymentCreate
from ...models.deployment_get import DeploymentGet
from ...models.http_validation_error import HTTPValidationError
from ...models.string_detail_error import StringDetailError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    project_uuid: str,
    json_body: DeploymentCreate,
) -> Dict[str, Any]:
    url = "{}/projects/{project_uuid}/deployments/".format(client.base_url, project_uuid=project_uuid)

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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[DeploymentGet, HTTPValidationError, StringDetailError]]:
    if response.status_code == 201:
        response_201 = DeploymentGet.from_dict(response.json())

        return response_201
    if response.status_code == 404:
        response_404 = StringDetailError.from_dict(response.json())

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[DeploymentGet, HTTPValidationError, StringDetailError]]:
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
    json_body: DeploymentCreate,
) -> Response[Union[DeploymentGet, HTTPValidationError, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        project_uuid=project_uuid,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    project_uuid: str,
    json_body: DeploymentCreate,
) -> Optional[Union[DeploymentGet, HTTPValidationError, StringDetailError]]:
    """Creates a deployment for a given project, deactivating any currently active deployment."""

    return sync_detailed(
        client=client,
        project_uuid=project_uuid,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_uuid: str,
    json_body: DeploymentCreate,
) -> Response[Union[DeploymentGet, HTTPValidationError, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        project_uuid=project_uuid,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    project_uuid: str,
    json_body: DeploymentCreate,
) -> Optional[Union[DeploymentGet, HTTPValidationError, StringDetailError]]:
    """Creates a deployment for a given project, deactivating any currently active deployment."""

    return (
        await asyncio_detailed(
            client=client,
            project_uuid=project_uuid,
            json_body=json_body,
        )
    ).parsed
