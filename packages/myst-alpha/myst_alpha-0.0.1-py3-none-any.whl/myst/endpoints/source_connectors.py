"""Endpoints for the `source_connectors` API routes.

NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
please run the `maint generate-endpoints` command (usually, after first running
the `maint generate-api-client` command)
"""

import myst.openapi_client.api.source_connectors.get_source_connector
import myst.openapi_client.api.source_connectors.get_source_connector_parameters_schema
import myst.openapi_client.api.source_connectors.list_source_connectors
from myst.endpoints.base import EndpointsBase
from myst.openapi_client.models.get_source_connector_parameters_schema_response_get_source_connector_parameters_schema_source_connectors_uuid_get_parameters_schema_get import (
    GetSourceConnectorParametersSchemaResponseGetSourceConnectorParametersSchemaSourceConnectorsUuidGetParametersSchemaGet,
)
from myst.openapi_client.models.resource_list_source_connector_get import (
    ResourceListSourceConnectorGet,
)
from myst.openapi_client.models.source_connector_get import SourceConnectorGet


class SourceConnectors(EndpointsBase):
    """API methods for the `source_connectors` routes."""

    def get_source_connector(self, uuid: str) -> SourceConnectorGet:
        """Calls the get_source_connector endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.source_connectors.get_source_connector.sync_detailed, uuid=uuid
        )

    def list_source_connectors(
        self,
    ) -> ResourceListSourceConnectorGet:
        """Calls the list_source_connectors endpoint"""
        return self.call_endpoint(myst.openapi_client.api.source_connectors.list_source_connectors.sync_detailed)

    def get_source_connector_parameters_schema(
        self, uuid: str
    ) -> GetSourceConnectorParametersSchemaResponseGetSourceConnectorParametersSchemaSourceConnectorsUuidGetParametersSchemaGet:
        """Calls the get_source_connector_parameters_schema endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.source_connectors.get_source_connector_parameters_schema.sync_detailed, uuid=uuid
        )
