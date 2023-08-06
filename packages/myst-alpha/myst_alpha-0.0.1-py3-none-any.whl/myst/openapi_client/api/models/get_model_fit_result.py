from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...models.model_fit_result_get import ModelFitResultGet
from ...models.string_detail_error import StringDetailError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    model_uuid: str,
    uuid: str,
) -> Dict[str, Any]:
    url = "{}/models/{model_uuid}/model_fit_results/{uuid}".format(client.base_url, model_uuid=model_uuid, uuid=uuid)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[HTTPValidationError, ModelFitResultGet, StringDetailError]]:
    if response.status_code == 200:
        response_200 = ModelFitResultGet.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ModelFitResultGet, StringDetailError]]:
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
    uuid: str,
) -> Response[Union[HTTPValidationError, ModelFitResultGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        model_uuid=model_uuid,
        uuid=uuid,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    model_uuid: str,
    uuid: str,
) -> Optional[Union[HTTPValidationError, ModelFitResultGet, StringDetailError]]:
    """Gets a model fit result by its unique identifier."""

    return sync_detailed(
        client=client,
        model_uuid=model_uuid,
        uuid=uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    model_uuid: str,
    uuid: str,
) -> Response[Union[HTTPValidationError, ModelFitResultGet, StringDetailError]]:
    kwargs = _get_kwargs(
        client=client,
        model_uuid=model_uuid,
        uuid=uuid,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    model_uuid: str,
    uuid: str,
) -> Optional[Union[HTTPValidationError, ModelFitResultGet, StringDetailError]]:
    """Gets a model fit result by its unique identifier."""

    return (
        await asyncio_detailed(
            client=client,
            model_uuid=model_uuid,
            uuid=uuid,
        )
    ).parsed
