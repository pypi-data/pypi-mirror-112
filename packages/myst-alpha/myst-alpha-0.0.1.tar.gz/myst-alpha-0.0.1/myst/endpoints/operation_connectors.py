"""Endpoints for the `operation_connectors` API routes.

NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
please run the `maint generate-endpoints` command (usually, after first running
the `maint generate-api-client` command)
"""

import myst.openapi_client.api.operation_connectors.get_operation_connector
import myst.openapi_client.api.operation_connectors.get_operation_connector_parameters_schema
import myst.openapi_client.api.operation_connectors.list_operation_connectors
from myst.endpoints.base import EndpointsBase
from myst.openapi_client.models.get_operation_connector_parameters_schema_response_get_operation_connector_parameters_schema_operation_connectors_uuid_get_parameters_schema_get import (
    GetOperationConnectorParametersSchemaResponseGetOperationConnectorParametersSchemaOperationConnectorsUuidGetParametersSchemaGet,
)
from myst.openapi_client.models.operation_connector_get import OperationConnectorGet
from myst.openapi_client.models.resource_list_operation_connector_get import (
    ResourceListOperationConnectorGet,
)


class OperationConnectors(EndpointsBase):
    """API methods for the `operation_connectors` routes."""

    def get_operation_connector(self, uuid: str) -> OperationConnectorGet:
        """Calls the get_operation_connector endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operation_connectors.get_operation_connector.sync_detailed, uuid=uuid
        )

    def get_operation_connector_parameters_schema(
        self, uuid: str
    ) -> GetOperationConnectorParametersSchemaResponseGetOperationConnectorParametersSchemaOperationConnectorsUuidGetParametersSchemaGet:
        """Calls the get_operation_connector_parameters_schema endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operation_connectors.get_operation_connector_parameters_schema.sync_detailed,
            uuid=uuid,
        )

    def list_operation_connectors(
        self,
    ) -> ResourceListOperationConnectorGet:
        """Calls the list_operation_connectors endpoint"""
        return self.call_endpoint(myst.openapi_client.api.operation_connectors.list_operation_connectors.sync_detailed)
