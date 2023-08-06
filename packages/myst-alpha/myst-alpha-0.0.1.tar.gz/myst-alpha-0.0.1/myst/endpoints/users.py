"""Endpoints for the `users` API routes.

NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
please run the `maint generate-endpoints` command (usually, after first running
the `maint generate-api-client` command)
"""

import myst.openapi_client.api.users.create_user
import myst.openapi_client.api.users.get_me
import myst.openapi_client.api.users.get_user
import myst.openapi_client.api.users.list_users
import myst.openapi_client.api.users.update_user
from myst.endpoints.base import EndpointsBase
from myst.openapi_client.models.resource_list_user_get import ResourceListUserGet
from myst.openapi_client.models.user_create import UserCreate
from myst.openapi_client.models.user_get import UserGet
from myst.openapi_client.models.user_update import UserUpdate


class Users(EndpointsBase):
    """API methods for the `users` routes."""

    def create_user(self, json_body: UserCreate) -> UserGet:
        """Calls the create_user endpoint"""
        return self.call_endpoint(myst.openapi_client.api.users.create_user.sync_detailed, json_body=json_body)

    def get_user(self, uuid: str) -> UserGet:
        """Calls the get_user endpoint"""
        return self.call_endpoint(myst.openapi_client.api.users.get_user.sync_detailed, uuid=uuid)

    def update_user(self, uuid: str, json_body: UserUpdate) -> UserGet:
        """Calls the update_user endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.users.update_user.sync_detailed, uuid=uuid, json_body=json_body
        )

    def get_me(
        self,
    ) -> UserGet:
        """Calls the get_me endpoint"""
        return self.call_endpoint(myst.openapi_client.api.users.get_me.sync_detailed)

    def list_users(self, organization_uuid: str) -> ResourceListUserGet:
        """Calls the list_users endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.users.list_users.sync_detailed, organization_uuid=organization_uuid
        )
