"""Endpoints for the `sources` API routes.

NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
please run the `maint generate-endpoints` command (usually, after first running
the `maint generate-api-client` command)
"""

import myst.openapi_client.api.sources.create_source
import myst.openapi_client.api.sources.delete_source
import myst.openapi_client.api.sources.get_source
import myst.openapi_client.api.sources.get_source_run_result
import myst.openapi_client.api.sources.list_source_run_results
import myst.openapi_client.api.sources.list_sources
import myst.openapi_client.api.sources.update_source
from myst.endpoints.base import EndpointsBase
from myst.openapi_client.models.resource_list_source_get import ResourceListSourceGet
from myst.openapi_client.models.resource_list_source_run_result_get import (
    ResourceListSourceRunResultGet,
)
from myst.openapi_client.models.source_create import SourceCreate
from myst.openapi_client.models.source_get import SourceGet
from myst.openapi_client.models.source_run_result_get import SourceRunResultGet
from myst.openapi_client.models.source_update import SourceUpdate


class Sources(EndpointsBase):
    """API methods for the `sources` routes."""

    def get_source(self, uuid: str) -> SourceGet:
        """Calls the get_source endpoint"""
        return self.call_endpoint(myst.openapi_client.api.sources.get_source.sync_detailed, uuid=uuid)

    def create_source(self, json_body: SourceCreate) -> SourceGet:
        """Calls the create_source endpoint"""
        return self.call_endpoint(myst.openapi_client.api.sources.create_source.sync_detailed, json_body=json_body)

    def update_source(self, uuid: str, json_body: SourceUpdate) -> SourceGet:
        """Calls the update_source endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.sources.update_source.sync_detailed, uuid=uuid, json_body=json_body
        )

    def get_source_run_result(self, source_uuid: str, uuid: str) -> SourceRunResultGet:
        """Calls the get_source_run_result endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.sources.get_source_run_result.sync_detailed, source_uuid=source_uuid, uuid=uuid
        )

    def list_sources(
        self,
    ) -> ResourceListSourceGet:
        """Calls the list_sources endpoint"""
        return self.call_endpoint(myst.openapi_client.api.sources.list_sources.sync_detailed)

    def list_source_run_results(self, source_uuid: str) -> ResourceListSourceRunResultGet:
        """Calls the list_source_run_results endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.sources.list_source_run_results.sync_detailed, source_uuid=source_uuid
        )

    def delete_source(self, uuid: str) -> SourceGet:
        """Calls the delete_source endpoint"""
        return self.call_endpoint(myst.openapi_client.api.sources.delete_source.sync_detailed, uuid=uuid)
