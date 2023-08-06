"""Endpoints for the `organizations` API routes.

NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
please run the `maint generate-endpoints` command (usually, after first running
the `maint generate-api-client` command)
"""

import myst.openapi_client.api.organizations.create_organization
import myst.openapi_client.api.organizations.get_organization
import myst.openapi_client.api.organizations.list_organizations
import myst.openapi_client.api.organizations.update_organization
from myst.endpoints.base import EndpointsBase
from myst.openapi_client.models.organization_create import OrganizationCreate
from myst.openapi_client.models.organization_get import OrganizationGet
from myst.openapi_client.models.organization_update import OrganizationUpdate
from myst.openapi_client.models.resource_list_organization_get import (
    ResourceListOrganizationGet,
)


class Organizations(EndpointsBase):
    """API methods for the `organizations` routes."""

    def list_organizations(
        self,
    ) -> ResourceListOrganizationGet:
        """Calls the list_organizations endpoint"""
        return self.call_endpoint(myst.openapi_client.api.organizations.list_organizations.sync_detailed)

    def update_organization(self, uuid: str, json_body: OrganizationUpdate) -> OrganizationGet:
        """Calls the update_organization endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.organizations.update_organization.sync_detailed, uuid=uuid, json_body=json_body
        )

    def create_organization(self, json_body: OrganizationCreate) -> OrganizationGet:
        """Calls the create_organization endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.organizations.create_organization.sync_detailed, json_body=json_body
        )

    def get_organization(self, uuid: str) -> OrganizationGet:
        """Calls the get_organization endpoint"""
        return self.call_endpoint(myst.openapi_client.api.organizations.get_organization.sync_detailed, uuid=uuid)
