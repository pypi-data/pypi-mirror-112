"""Endpoints for the `projects` API routes.

NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
please run the `maint generate-endpoints` command (usually, after first running
the `maint generate-api-client` command)
"""

import myst.openapi_client.api.projects.create_project
import myst.openapi_client.api.projects.create_project_deployment
import myst.openapi_client.api.projects.deactivate_project_deployment
import myst.openapi_client.api.projects.delete_project
import myst.openapi_client.api.projects.get_node_output_specs
import myst.openapi_client.api.projects.get_project
import myst.openapi_client.api.projects.list_project_deployments
import myst.openapi_client.api.projects.list_project_edges
import myst.openapi_client.api.projects.list_project_nodes
import myst.openapi_client.api.projects.list_project_policies
import myst.openapi_client.api.projects.list_project_results
import myst.openapi_client.api.projects.list_projects
import myst.openapi_client.api.projects.update_project
from myst.endpoints.base import EndpointsBase
from myst.openapi_client.models.deployment_create import DeploymentCreate
from myst.openapi_client.models.deployment_get import DeploymentGet
from myst.openapi_client.models.output_specs_get import OutputSpecsGet
from myst.openapi_client.models.project_create import ProjectCreate
from myst.openapi_client.models.project_edges_list import ProjectEdgesList
from myst.openapi_client.models.project_get import ProjectGet
from myst.openapi_client.models.project_nodes_list import ProjectNodesList
from myst.openapi_client.models.project_policies_list import ProjectPoliciesList
from myst.openapi_client.models.project_result_list import ProjectResultList
from myst.openapi_client.models.project_update import ProjectUpdate
from myst.openapi_client.models.resource_list_deployment_get import (
    ResourceListDeploymentGet,
)
from myst.openapi_client.models.resource_list_project_get import ResourceListProjectGet


class Projects(EndpointsBase):
    """API methods for the `projects` routes."""

    def list_project_edges(self, project_uuid: str) -> ProjectEdgesList:
        """Calls the list_project_edges endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.projects.list_project_edges.sync_detailed, project_uuid=project_uuid
        )

    def list_project_deployments(self, project_uuid: str) -> ResourceListDeploymentGet:
        """Calls the list_project_deployments endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.projects.list_project_deployments.sync_detailed, project_uuid=project_uuid
        )

    def deactivate_project_deployment(self, project_uuid: str, uuid: str) -> DeploymentGet:
        """Calls the deactivate_project_deployment endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.projects.deactivate_project_deployment.sync_detailed,
            project_uuid=project_uuid,
            uuid=uuid,
        )

    def get_project(self, uuid: str) -> ProjectGet:
        """Calls the get_project endpoint"""
        return self.call_endpoint(myst.openapi_client.api.projects.get_project.sync_detailed, uuid=uuid)

    def list_projects(
        self,
    ) -> ResourceListProjectGet:
        """Calls the list_projects endpoint"""
        return self.call_endpoint(myst.openapi_client.api.projects.list_projects.sync_detailed)

    def list_project_nodes(self, project_uuid: str) -> ProjectNodesList:
        """Calls the list_project_nodes endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.projects.list_project_nodes.sync_detailed, project_uuid=project_uuid
        )

    def list_project_policies(self, project_uuid: str) -> ProjectPoliciesList:
        """Calls the list_project_policies endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.projects.list_project_policies.sync_detailed, project_uuid=project_uuid
        )

    def create_project_deployment(self, project_uuid: str, json_body: DeploymentCreate) -> DeploymentGet:
        """Calls the create_project_deployment endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.projects.create_project_deployment.sync_detailed,
            project_uuid=project_uuid,
            json_body=json_body,
        )

    def get_node_output_specs(self, project_uuid: str, node_uuid: str) -> OutputSpecsGet:
        """Calls the get_node_output_specs endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.projects.get_node_output_specs.sync_detailed,
            project_uuid=project_uuid,
            node_uuid=node_uuid,
        )

    def list_project_results(self, project_uuid: str) -> ProjectResultList:
        """Calls the list_project_results endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.projects.list_project_results.sync_detailed, project_uuid=project_uuid
        )

    def update_project(self, uuid: str, json_body: ProjectUpdate) -> ProjectGet:
        """Calls the update_project endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.projects.update_project.sync_detailed, uuid=uuid, json_body=json_body
        )

    def create_project(self, json_body: ProjectCreate) -> ProjectGet:
        """Calls the create_project endpoint"""
        return self.call_endpoint(myst.openapi_client.api.projects.create_project.sync_detailed, json_body=json_body)

    def delete_project(self, uuid: str) -> ProjectGet:
        """Calls the delete_project endpoint"""
        return self.call_endpoint(myst.openapi_client.api.projects.delete_project.sync_detailed, uuid=uuid)
