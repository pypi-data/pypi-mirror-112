from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.deploy_status import DeployStatus
from ..models.time_series_update_type import TimeSeriesUpdateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeSeriesUpdate")


@attr.s(auto_attribs=True)
class TimeSeriesUpdate:
    """Time series schema for update requests."""

    object_: Union[Unset, None] = UNSET
    uuid: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    update_time: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    type: Union[Unset, TimeSeriesUpdateType] = UNSET
    project: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    deploy_status: Union[Unset, DeployStatus] = UNSET
    sample_period: Union[Unset, str] = UNSET
    cell_shape: Union[Unset, List[None]] = UNSET
    coordinate_labels: Union[Unset, List[None]] = UNSET
    axis_labels: Union[Unset, List[None]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = None

        uuid = self.uuid
        create_time = self.create_time
        update_time = self.update_time
        organization = self.organization
        owner = self.owner
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        project = self.project
        title = self.title
        description = self.description
        deploy_status: Union[Unset, str] = UNSET
        if not isinstance(self.deploy_status, Unset):
            deploy_status = self.deploy_status.value

        sample_period = self.sample_period
        cell_shape: Union[Unset, List[None]] = UNSET
        if not isinstance(self.cell_shape, Unset):
            cell_shape = []
            for cell_shape_item_data in self.cell_shape:
                cell_shape_item = None

                cell_shape.append(cell_shape_item)

        coordinate_labels: Union[Unset, List[None]] = UNSET
        if not isinstance(self.coordinate_labels, Unset):
            coordinate_labels = []
            for coordinate_labels_item_data in self.coordinate_labels:
                coordinate_labels_item = None

                coordinate_labels.append(coordinate_labels_item)

        axis_labels: Union[Unset, List[None]] = UNSET
        if not isinstance(self.axis_labels, Unset):
            axis_labels = []
            for axis_labels_item_data in self.axis_labels:
                axis_labels_item = None

                axis_labels.append(axis_labels_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if object_ is not UNSET:
            field_dict["object"] = object_
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if create_time is not UNSET:
            field_dict["create_time"] = create_time
        if update_time is not UNSET:
            field_dict["update_time"] = update_time
        if organization is not UNSET:
            field_dict["organization"] = organization
        if owner is not UNSET:
            field_dict["owner"] = owner
        if type is not UNSET:
            field_dict["type"] = type
        if project is not UNSET:
            field_dict["project"] = project
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if deploy_status is not UNSET:
            field_dict["deploy_status"] = deploy_status
        if sample_period is not UNSET:
            field_dict["sample_period"] = sample_period
        if cell_shape is not UNSET:
            field_dict["cell_shape"] = cell_shape
        if coordinate_labels is not UNSET:
            field_dict["coordinate_labels"] = coordinate_labels
        if axis_labels is not UNSET:
            field_dict["axis_labels"] = axis_labels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = None

        uuid = d.pop("uuid", UNSET)

        create_time = d.pop("create_time", UNSET)

        update_time = d.pop("update_time", UNSET)

        organization = d.pop("organization", UNSET)

        owner = d.pop("owner", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, TimeSeriesUpdateType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = TimeSeriesUpdateType(_type)

        project = d.pop("project", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        _deploy_status = d.pop("deploy_status", UNSET)
        deploy_status: Union[Unset, DeployStatus]
        if isinstance(_deploy_status, Unset):
            deploy_status = UNSET
        else:
            deploy_status = DeployStatus(_deploy_status)

        sample_period = d.pop("sample_period", UNSET)

        cell_shape = []
        _cell_shape = d.pop("cell_shape", UNSET)
        for cell_shape_item_data in _cell_shape or []:
            cell_shape_item = None

            cell_shape.append(cell_shape_item)

        coordinate_labels = []
        _coordinate_labels = d.pop("coordinate_labels", UNSET)
        for coordinate_labels_item_data in _coordinate_labels or []:
            coordinate_labels_item = None

            coordinate_labels.append(coordinate_labels_item)

        axis_labels = []
        _axis_labels = d.pop("axis_labels", UNSET)
        for axis_labels_item_data in _axis_labels or []:
            axis_labels_item = None

            axis_labels.append(axis_labels_item)

        time_series_update = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            update_time=update_time,
            organization=organization,
            owner=owner,
            type=type,
            project=project,
            title=title,
            description=description,
            deploy_status=deploy_status,
            sample_period=sample_period,
            cell_shape=cell_shape,
            coordinate_labels=coordinate_labels,
            axis_labels=axis_labels,
        )

        return time_series_update
