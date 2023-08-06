"""Endpoints for the `operations` API routes.

NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
please run the `maint generate-endpoints` command (usually, after first running
the `maint generate-api-client` command)
"""

import myst.openapi_client.api.operations.create_operation
import myst.openapi_client.api.operations.create_operation_input
import myst.openapi_client.api.operations.delete_operation
import myst.openapi_client.api.operations.get_operation
import myst.openapi_client.api.operations.get_operation_input
import myst.openapi_client.api.operations.get_operation_input_specs_schema
import myst.openapi_client.api.operations.get_operation_run_result
import myst.openapi_client.api.operations.list_operation_inputs
import myst.openapi_client.api.operations.list_operation_run_results
import myst.openapi_client.api.operations.list_operations
import myst.openapi_client.api.operations.update_operation
import myst.openapi_client.api.operations.update_operation_input
from myst.endpoints.base import EndpointsBase
from myst.openapi_client.models.input_create import InputCreate
from myst.openapi_client.models.input_get import InputGet
from myst.openapi_client.models.input_specs_schema_get import InputSpecsSchemaGet
from myst.openapi_client.models.input_update import InputUpdate
from myst.openapi_client.models.operation_create import OperationCreate
from myst.openapi_client.models.operation_get import OperationGet
from myst.openapi_client.models.operation_run_result_get import OperationRunResultGet
from myst.openapi_client.models.operation_update import OperationUpdate
from myst.openapi_client.models.resource_list_input_get import ResourceListInputGet
from myst.openapi_client.models.resource_list_operation_get import (
    ResourceListOperationGet,
)
from myst.openapi_client.models.resource_list_operation_run_result_get import (
    ResourceListOperationRunResultGet,
)


class Operations(EndpointsBase):
    """API methods for the `operations` routes."""

    def list_operation_run_results(self, operation_uuid: str) -> ResourceListOperationRunResultGet:
        """Calls the list_operation_run_results endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operations.list_operation_run_results.sync_detailed, operation_uuid=operation_uuid
        )

    def list_operations(
        self,
    ) -> ResourceListOperationGet:
        """Calls the list_operations endpoint"""
        return self.call_endpoint(myst.openapi_client.api.operations.list_operations.sync_detailed)

    def update_operation_input(self, uuid: str, operation_uuid: str, json_body: InputUpdate) -> InputGet:
        """Calls the update_operation_input endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operations.update_operation_input.sync_detailed,
            uuid=uuid,
            operation_uuid=operation_uuid,
            json_body=json_body,
        )

    def get_operation_input(self, uuid: str, operation_uuid: str) -> InputGet:
        """Calls the get_operation_input endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operations.get_operation_input.sync_detailed,
            uuid=uuid,
            operation_uuid=operation_uuid,
        )

    def update_operation(self, uuid: str, json_body: OperationUpdate) -> OperationGet:
        """Calls the update_operation endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operations.update_operation.sync_detailed, uuid=uuid, json_body=json_body
        )

    def list_operation_inputs(self, operation_uuid: str) -> ResourceListInputGet:
        """Calls the list_operation_inputs endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operations.list_operation_inputs.sync_detailed, operation_uuid=operation_uuid
        )

    def get_operation_input_specs_schema(self, uuid: str) -> InputSpecsSchemaGet:
        """Calls the get_operation_input_specs_schema endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operations.get_operation_input_specs_schema.sync_detailed, uuid=uuid
        )

    def create_operation(self, json_body: OperationCreate) -> OperationGet:
        """Calls the create_operation endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operations.create_operation.sync_detailed, json_body=json_body
        )

    def get_operation_run_result(self, operation_uuid: str, uuid: str) -> OperationRunResultGet:
        """Calls the get_operation_run_result endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operations.get_operation_run_result.sync_detailed,
            operation_uuid=operation_uuid,
            uuid=uuid,
        )

    def get_operation(self, uuid: str) -> OperationGet:
        """Calls the get_operation endpoint"""
        return self.call_endpoint(myst.openapi_client.api.operations.get_operation.sync_detailed, uuid=uuid)

    def create_operation_input(self, operation_uuid: str, json_body: InputCreate) -> InputGet:
        """Calls the create_operation_input endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.operations.create_operation_input.sync_detailed,
            operation_uuid=operation_uuid,
            json_body=json_body,
        )

    def delete_operation(self, uuid: str) -> OperationGet:
        """Calls the delete_operation endpoint"""
        return self.call_endpoint(myst.openapi_client.api.operations.delete_operation.sync_detailed, uuid=uuid)
