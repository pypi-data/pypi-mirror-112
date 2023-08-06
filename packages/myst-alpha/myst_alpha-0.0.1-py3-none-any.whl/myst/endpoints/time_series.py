"""Endpoints for the `time_series` API routes.

NOTE: This file is auto-generated and is not meant to be edited by hand. To update,
please run the `maint generate-endpoints` command (usually, after first running
the `maint generate-api-client` command)
"""

import myst.openapi_client.api.time_series.create_time_series
import myst.openapi_client.api.time_series.create_time_series_layer
import myst.openapi_client.api.time_series.create_time_series_run_policy
import myst.openapi_client.api.time_series.delete_time_series
import myst.openapi_client.api.time_series.get_time_series
import myst.openapi_client.api.time_series.get_time_series_layer
import myst.openapi_client.api.time_series.get_time_series_run_policy
import myst.openapi_client.api.time_series.get_time_series_run_result
import myst.openapi_client.api.time_series.insert_time_series_data
import myst.openapi_client.api.time_series.list_time_series
import myst.openapi_client.api.time_series.list_time_series_layers
import myst.openapi_client.api.time_series.list_time_series_run_policies
import myst.openapi_client.api.time_series.list_time_series_run_results
import myst.openapi_client.api.time_series.query_time_series_data
import myst.openapi_client.api.time_series.update_time_series
import myst.openapi_client.api.time_series.update_time_series_layer
import myst.openapi_client.api.time_series.update_time_series_run_policy
from myst.endpoints.base import EndpointsBase
from myst.openapi_client.models.layer_create import LayerCreate
from myst.openapi_client.models.layer_get import LayerGet
from myst.openapi_client.models.layer_update import LayerUpdate
from myst.openapi_client.models.resource_list_layer_get import ResourceListLayerGet
from myst.openapi_client.models.resource_list_time_series_get import (
    ResourceListTimeSeriesGet,
)
from myst.openapi_client.models.resource_list_time_series_run_policy_get import (
    ResourceListTimeSeriesRunPolicyGet,
)
from myst.openapi_client.models.resource_list_time_series_run_result_get import (
    ResourceListTimeSeriesRunResultGet,
)
from myst.openapi_client.models.time_series_create import TimeSeriesCreate
from myst.openapi_client.models.time_series_get import TimeSeriesGet
from myst.openapi_client.models.time_series_insert import TimeSeriesInsert
from myst.openapi_client.models.time_series_insert_result_get import (
    TimeSeriesInsertResultGet,
)
from myst.openapi_client.models.time_series_query_result_get import (
    TimeSeriesQueryResultGet,
)
from myst.openapi_client.models.time_series_run_policy_create import (
    TimeSeriesRunPolicyCreate,
)
from myst.openapi_client.models.time_series_run_policy_get import TimeSeriesRunPolicyGet
from myst.openapi_client.models.time_series_run_policy_update import (
    TimeSeriesRunPolicyUpdate,
)
from myst.openapi_client.models.time_series_run_result_get import TimeSeriesRunResultGet
from myst.openapi_client.models.time_series_update import TimeSeriesUpdate


class TimeSeries(EndpointsBase):
    """API methods for the `time_series` routes."""

    def get_time_series_run_result(self, time_series_uuid: str, uuid: str) -> TimeSeriesRunResultGet:
        """Calls the get_time_series_run_result endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.get_time_series_run_result.sync_detailed,
            time_series_uuid=time_series_uuid,
            uuid=uuid,
        )

    def create_time_series(self, json_body: TimeSeriesCreate) -> TimeSeriesGet:
        """Calls the create_time_series endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.create_time_series.sync_detailed, json_body=json_body
        )

    def list_time_series_run_policies(self, time_series_uuid: str) -> ResourceListTimeSeriesRunPolicyGet:
        """Calls the list_time_series_run_policies endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.list_time_series_run_policies.sync_detailed,
            time_series_uuid=time_series_uuid,
        )

    def list_time_series_run_results(self, time_series_uuid: str) -> ResourceListTimeSeriesRunResultGet:
        """Calls the list_time_series_run_results endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.list_time_series_run_results.sync_detailed,
            time_series_uuid=time_series_uuid,
        )

    def create_time_series_run_policy(
        self, time_series_uuid: str, json_body: TimeSeriesRunPolicyCreate
    ) -> TimeSeriesRunPolicyGet:
        """Calls the create_time_series_run_policy endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.create_time_series_run_policy.sync_detailed,
            time_series_uuid=time_series_uuid,
            json_body=json_body,
        )

    def get_time_series(self, uuid: str) -> TimeSeriesGet:
        """Calls the get_time_series endpoint"""
        return self.call_endpoint(myst.openapi_client.api.time_series.get_time_series.sync_detailed, uuid=uuid)

    def update_time_series_run_policy(
        self, time_series_uuid: str, uuid: str, json_body: TimeSeriesRunPolicyUpdate
    ) -> TimeSeriesRunPolicyGet:
        """Calls the update_time_series_run_policy endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.update_time_series_run_policy.sync_detailed,
            time_series_uuid=time_series_uuid,
            uuid=uuid,
            json_body=json_body,
        )

    def get_time_series_layer(self, uuid: str, time_series_uuid: str) -> LayerGet:
        """Calls the get_time_series_layer endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.get_time_series_layer.sync_detailed,
            uuid=uuid,
            time_series_uuid=time_series_uuid,
        )

    def list_time_series(
        self,
    ) -> ResourceListTimeSeriesGet:
        """Calls the list_time_series endpoint"""
        return self.call_endpoint(myst.openapi_client.api.time_series.list_time_series.sync_detailed)

    def insert_time_series_data(self, uuid: str, json_body: TimeSeriesInsert) -> TimeSeriesInsertResultGet:
        """Calls the insert_time_series_data endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.insert_time_series_data.sync_detailed, uuid=uuid, json_body=json_body
        )

    def update_time_series(self, uuid: str, json_body: TimeSeriesUpdate) -> TimeSeriesGet:
        """Calls the update_time_series endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.update_time_series.sync_detailed, uuid=uuid, json_body=json_body
        )

    def query_time_series_data(
        self, uuid: str, start_time: str, end_time: str, as_of_time: str
    ) -> TimeSeriesQueryResultGet:
        """Calls the query_time_series_data endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.query_time_series_data.sync_detailed,
            uuid=uuid,
            start_time=start_time,
            end_time=end_time,
            as_of_time=as_of_time,
        )

    def delete_time_series(self, uuid: str) -> TimeSeriesGet:
        """Calls the delete_time_series endpoint"""
        return self.call_endpoint(myst.openapi_client.api.time_series.delete_time_series.sync_detailed, uuid=uuid)

    def get_time_series_run_policy(self, time_series_uuid: str, uuid: str) -> TimeSeriesRunPolicyGet:
        """Calls the get_time_series_run_policy endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.get_time_series_run_policy.sync_detailed,
            time_series_uuid=time_series_uuid,
            uuid=uuid,
        )

    def update_time_series_layer(self, uuid: str, time_series_uuid: str, json_body: LayerUpdate) -> LayerGet:
        """Calls the update_time_series_layer endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.update_time_series_layer.sync_detailed,
            uuid=uuid,
            time_series_uuid=time_series_uuid,
            json_body=json_body,
        )

    def create_time_series_layer(self, time_series_uuid: str, json_body: LayerCreate) -> LayerGet:
        """Calls the create_time_series_layer endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.create_time_series_layer.sync_detailed,
            time_series_uuid=time_series_uuid,
            json_body=json_body,
        )

    def list_time_series_layers(self, time_series_uuid: str) -> ResourceListLayerGet:
        """Calls the list_time_series_layers endpoint"""
        return self.call_endpoint(
            myst.openapi_client.api.time_series.list_time_series_layers.sync_detailed, time_series_uuid=time_series_uuid
        )
