from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.get_model_connector_parameters_schema_response_get_model_connector_parameters_schema_model_connectors_uuid_get_parameters_schema_get import (
    GetModelConnectorParametersSchemaResponseGetModelConnectorParametersSchemaModelConnectorsUuidGetParametersSchemaGet,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.string_detail_error import StringDetailError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Dict[str, Any]:
    url = "{}/model_connectors/{uuid}:get_parameters_schema".format(client.base_url, uuid=uuid)

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
) -> Optional[
    Union[
        GetModelConnectorParametersSchemaResponseGetModelConnectorParametersSchemaModelConnectorsUuidGetParametersSchemaGet,
        HTTPValidationError,
        StringDetailError,
    ]
]:
    if response.status_code == 200:
        response_200 = GetModelConnectorParametersSchemaResponseGetModelConnectorParametersSchemaModelConnectorsUuidGetParametersSchemaGet.from_dict(
            response.json()
        )

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
) -> Response[
    Union[
        GetModelConnectorParametersSchemaResponseGetModelConnectorParametersSchemaModelConnectorsUuidGetParametersSchemaGet,
        HTTPValidationError,
        StringDetailError,
    ]
]:
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
) -> Response[
    Union[
        GetModelConnectorParametersSchemaResponseGetModelConnectorParametersSchemaModelConnectorsUuidGetParametersSchemaGet,
        HTTPValidationError,
        StringDetailError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Optional[
    Union[
        GetModelConnectorParametersSchemaResponseGetModelConnectorParametersSchemaModelConnectorsUuidGetParametersSchemaGet,
        HTTPValidationError,
        StringDetailError,
    ]
]:
    """Gets a model connector's parameters schema."""

    return sync_detailed(
        client=client,
        uuid=uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Response[
    Union[
        GetModelConnectorParametersSchemaResponseGetModelConnectorParametersSchemaModelConnectorsUuidGetParametersSchemaGet,
        HTTPValidationError,
        StringDetailError,
    ]
]:
    kwargs = _get_kwargs(
        client=client,
        uuid=uuid,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    uuid: str,
) -> Optional[
    Union[
        GetModelConnectorParametersSchemaResponseGetModelConnectorParametersSchemaModelConnectorsUuidGetParametersSchemaGet,
        HTTPValidationError,
        StringDetailError,
    ]
]:
    """Gets a model connector's parameters schema."""

    return (
        await asyncio_detailed(
            client=client,
            uuid=uuid,
        )
    ).parsed
