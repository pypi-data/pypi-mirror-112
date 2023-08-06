"""Endpoints for the `models` API routes.

NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
please run the `maint generate-endpoints` command (usually, after first running
the `maint generate-api-client` command)
"""

import myst.openapi_client.api.models.create_model
import myst.openapi_client.api.models.create_model_fit_policy
import myst.openapi_client.api.models.create_model_input
import myst.openapi_client.api.models.delete_model
import myst.openapi_client.api.models.get_model
import myst.openapi_client.api.models.get_model_fit_policy
import myst.openapi_client.api.models.get_model_fit_result
import myst.openapi_client.api.models.get_model_input
import myst.openapi_client.api.models.get_model_input_specs_schema
import myst.openapi_client.api.models.get_model_run_result
import myst.openapi_client.api.models.list_model_fit_policies
import myst.openapi_client.api.models.list_model_fit_results
import myst.openapi_client.api.models.list_model_inputs
import myst.openapi_client.api.models.list_model_run_results
import myst.openapi_client.api.models.list_models
import myst.openapi_client.api.models.update_model
import myst.openapi_client.api.models.update_model_fit_policy
import myst.openapi_client.api.models.update_model_input
from myst.endpoints.base import EndpointsBase
from myst.openapi_client.models.input_create import InputCreate
from myst.openapi_client.models.input_get import InputGet
from myst.openapi_client.models.input_specs_schema_get import InputSpecsSchemaGet
from myst.openapi_client.models.input_update import InputUpdate
from myst.openapi_client.models.model_create import ModelCreate
from myst.openapi_client.models.model_fit_policy_create import ModelFitPolicyCreate
from myst.openapi_client.models.model_fit_policy_get import ModelFitPolicyGet
from myst.openapi_client.models.model_fit_policy_update import ModelFitPolicyUpdate
from myst.openapi_client.models.model_fit_result_get import ModelFitResultGet
from myst.openapi_client.models.model_get import ModelGet
from myst.openapi_client.models.model_run_result_get import ModelRunResultGet
from myst.openapi_client.models.model_update import ModelUpdate
from myst.openapi_client.models.resource_list_input_get import ResourceListInputGet
from myst.openapi_client.models.resource_list_model_fit_policy_get import (
    ResourceListModelFitPolicyGet,
)
from myst.openapi_client.models.resource_list_model_fit_result_get import (
    ResourceListModelFitResultGet,
)
from myst.openapi_client.models.resource_list_model_get import ResourceListModelGet
from myst.openapi_client.models.resource_list_model_run_result_get import (
    ResourceListModelRunResultGet,
)


class Models(EndpointsBase):
    """API methods for the `models` routes."""

    def get_model_input_specs_schema(self, uuid: str) -> InputSpecsSchemaGet:
        """Calls the get_model_input_specs_schema endpoint"""
        return self.call_endpoint(myst.openapi_client.api.models.get_model_input_specs_schema.sync_detailed, uuid=uuid)

    def get_model_input(self, uuid: str, model_uuid: str) -> InputGet:
        """Calls the get_model_input endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.get_model_input.sync_detailed, uuid=uuid, model_uuid=model_uuid
        )

    def list_model_fit_results(self, model_uuid: str) -> ResourceListModelFitResultGet:
        """Calls the list_model_fit_results endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.list_model_fit_results.sync_detailed, model_uuid=model_uuid
        )

    def create_model_input(self, model_uuid: str, json_body: InputCreate) -> InputGet:
        """Calls the create_model_input endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.create_model_input.sync_detailed, model_uuid=model_uuid, json_body=json_body
        )

    def list_model_inputs(self, model_uuid: str) -> ResourceListInputGet:
        """Calls the list_model_inputs endpoint"""
        return self.call_endpoint(myst.openapi_client.api.models.list_model_inputs.sync_detailed, model_uuid=model_uuid)

    def get_model_run_result(self, model_uuid: str, uuid: str) -> ModelRunResultGet:
        """Calls the get_model_run_result endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.get_model_run_result.sync_detailed, model_uuid=model_uuid, uuid=uuid
        )

    def get_model_fit_result(self, model_uuid: str, uuid: str) -> ModelFitResultGet:
        """Calls the get_model_fit_result endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.get_model_fit_result.sync_detailed, model_uuid=model_uuid, uuid=uuid
        )

    def list_model_fit_policies(self, model_uuid: str) -> ResourceListModelFitPolicyGet:
        """Calls the list_model_fit_policies endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.list_model_fit_policies.sync_detailed, model_uuid=model_uuid
        )

    def list_models(
        self,
    ) -> ResourceListModelGet:
        """Calls the list_models endpoint"""
        return self.call_endpoint(myst.openapi_client.api.models.list_models.sync_detailed)

    def update_model_input(self, uuid: str, model_uuid: str, json_body: InputUpdate) -> InputGet:
        """Calls the update_model_input endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.update_model_input.sync_detailed,
            uuid=uuid,
            model_uuid=model_uuid,
            json_body=json_body,
        )

    def get_model_fit_policy(self, model_uuid: str, uuid: str) -> ModelFitPolicyGet:
        """Calls the get_model_fit_policy endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.get_model_fit_policy.sync_detailed, model_uuid=model_uuid, uuid=uuid
        )

    def update_model(self, uuid: str, json_body: ModelUpdate) -> ModelGet:
        """Calls the update_model endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.update_model.sync_detailed, uuid=uuid, json_body=json_body
        )

    def get_model(self, uuid: str) -> ModelGet:
        """Calls the get_model endpoint"""
        return self.call_endpoint(myst.openapi_client.api.models.get_model.sync_detailed, uuid=uuid)

    def list_model_run_results(self, model_uuid: str) -> ResourceListModelRunResultGet:
        """Calls the list_model_run_results endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.list_model_run_results.sync_detailed, model_uuid=model_uuid
        )

    def update_model_fit_policy(self, model_uuid: str, uuid: str, json_body: ModelFitPolicyUpdate) -> ModelFitPolicyGet:
        """Calls the update_model_fit_policy endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.update_model_fit_policy.sync_detailed,
            model_uuid=model_uuid,
            uuid=uuid,
            json_body=json_body,
        )

    def delete_model(self, uuid: str) -> ModelGet:
        """Calls the delete_model endpoint"""
        return self.call_endpoint(myst.openapi_client.api.models.delete_model.sync_detailed, uuid=uuid)

    def create_model(self, json_body: ModelCreate) -> ModelGet:
        """Calls the create_model endpoint"""
        return self.call_endpoint(myst.openapi_client.api.models.create_model.sync_detailed, json_body=json_body)

    def create_model_fit_policy(self, model_uuid: str, json_body: ModelFitPolicyCreate) -> ModelFitPolicyGet:
        """Calls the create_model_fit_policy endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.models.create_model_fit_policy.sync_detailed,
            model_uuid=model_uuid,
            json_body=json_body,
        )
