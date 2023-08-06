"""Endpoints for the `model_connectors` API routes.

NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
please run the `maint generate-endpoints` command (usually, after first running
the `maint generate-api-client` command)
"""

import myst.openapi_client.api.model_connectors.get_model_connector
import myst.openapi_client.api.model_connectors.get_model_connector_parameters_schema
import myst.openapi_client.api.model_connectors.list_model_connectors
from myst.endpoints.base import EndpointsBase
from myst.openapi_client.models.get_model_connector_parameters_schema_response_get_model_connector_parameters_schema_model_connectors_uuid_get_parameters_schema_get import (
    GetModelConnectorParametersSchemaResponseGetModelConnectorParametersSchemaModelConnectorsUuidGetParametersSchemaGet,
)
from myst.openapi_client.models.model_connector_get import ModelConnectorGet
from myst.openapi_client.models.resource_list_model_connector_get import (
    ResourceListModelConnectorGet,
)


class ModelConnectors(EndpointsBase):
    """API methods for the `model_connectors` routes."""

    def get_model_connector_parameters_schema(
        self, uuid: str
    ) -> GetModelConnectorParametersSchemaResponseGetModelConnectorParametersSchemaModelConnectorsUuidGetParametersSchemaGet:
        """Calls the get_model_connector_parameters_schema endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.model_connectors.get_model_connector_parameters_schema.sync_detailed, uuid=uuid
        )

    def list_model_connectors(
        self,
    ) -> ResourceListModelConnectorGet:
        """Calls the list_model_connectors endpoint"""
        return self.call_endpoint(myst.openapi_client.api.model_connectors.list_model_connectors.sync_detailed)

    def get_model_connector(self, uuid: str) -> ModelConnectorGet:
        """Calls the get_model_connector endpoint"""
        return self.call_endpoint(myst.openapi_client.api.model_connectors.get_model_connector.sync_detailed, uuid=uuid)
