from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.resource_list_model_fit_policy_get import ResourceListModelFitPolicyGet
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    model_uuid: str,
) -> Dict[str, Any]:
    url = "{}/models/{model_uuid}/model_fit_policies/".format(client.base_url, model_uuid=model_uuid)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, ResourceListModelFitPolicyGet]]:
    if response.status_code == 200:
        response_200 = ResourceListModelFitPolicyGet.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, ResourceListModelFitPolicyGet]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    model_uuid: str,
) -> Response[Union[HTTPValidationError, ResourceListModelFitPolicyGet]]:
    kwargs = _get_kwargs(
        client=client,
        model_uuid=model_uuid,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    model_uuid: str,
) -> Optional[Union[HTTPValidationError, ResourceListModelFitPolicyGet]]:
    """Lists fit policies for a model."""

    return sync_detailed(
        client=client,
        model_uuid=model_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    model_uuid: str,
) -> Response[Union[HTTPValidationError, ResourceListModelFitPolicyGet]]:
    kwargs = _get_kwargs(
        client=client,
        model_uuid=model_uuid,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    model_uuid: str,
) -> Optional[Union[HTTPValidationError, ResourceListModelFitPolicyGet]]:
    """Lists fit policies for a model."""

    return (
        await asyncio_detailed(
            client=client,
            model_uuid=model_uuid,
        )
    ).parsed
