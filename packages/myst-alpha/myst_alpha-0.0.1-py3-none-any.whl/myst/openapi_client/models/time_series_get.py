from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..models.deploy_status import DeployStatus
from ..models.time_series_get_object import TimeSeriesGetObject
from ..models.time_series_get_type import TimeSeriesGetType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeSeriesGet")


@attr.s(auto_attribs=True)
class TimeSeriesGet:
    """Time series schema for get responses."""

    object_: TimeSeriesGetObject
    uuid: str
    create_time: str
    organization: str
    owner: str
    type: TimeSeriesGetType
    title: str
    project: str
    creator: str
    deploy_status: DeployStatus
    sample_period: str
    cell_shape: List[None]
    coordinate_labels: List[None]
    axis_labels: List[None]
    description: Optional[str]
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        organization = self.organization
        owner = self.owner
        type = self.type.value

        title = self.title
        project = self.project
        creator = self.creator
        deploy_status = self.deploy_status.value

        sample_period = self.sample_period
        cell_shape = []
        for cell_shape_item_data in self.cell_shape:
            cell_shape_item = None

            cell_shape.append(cell_shape_item)

        coordinate_labels = []
        for coordinate_labels_item_data in self.coordinate_labels:
            coordinate_labels_item = None

            coordinate_labels.append(coordinate_labels_item)

        axis_labels = []
        for axis_labels_item_data in self.axis_labels:
            axis_labels_item = None

            axis_labels.append(axis_labels_item)

        update_time = self.update_time
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "uuid": uuid,
                "create_time": create_time,
                "organization": organization,
                "owner": owner,
                "type": type,
                "title": title,
                "project": project,
                "creator": creator,
                "deploy_status": deploy_status,
                "sample_period": sample_period,
                "cell_shape": cell_shape,
                "coordinate_labels": coordinate_labels,
                "axis_labels": axis_labels,
                "description": description,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = TimeSeriesGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        organization = d.pop("organization")

        owner = d.pop("owner")

        type = TimeSeriesGetType(d.pop("type"))

        title = d.pop("title")

        project = d.pop("project")

        creator = d.pop("creator")

        deploy_status = DeployStatus(d.pop("deploy_status"))

        sample_period = d.pop("sample_period")

        cell_shape = []
        _cell_shape = d.pop("cell_shape")
        for cell_shape_item_data in _cell_shape:
            cell_shape_item = None

            cell_shape.append(cell_shape_item)

        coordinate_labels = []
        _coordinate_labels = d.pop("coordinate_labels")
        for coordinate_labels_item_data in _coordinate_labels:
            coordinate_labels_item = None

            coordinate_labels.append(coordinate_labels_item)

        axis_labels = []
        _axis_labels = d.pop("axis_labels")
        for axis_labels_item_data in _axis_labels:
            axis_labels_item = None

            axis_labels.append(axis_labels_item)

        update_time = d.pop("update_time", UNSET)

        description = d.pop("description")

        time_series_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            organization=organization,
            owner=owner,
            type=type,
            title=title,
            project=project,
            creator=creator,
            deploy_status=deploy_status,
            sample_period=sample_period,
            cell_shape=cell_shape,
            coordinate_labels=coordinate_labels,
            axis_labels=axis_labels,
            update_time=update_time,
            description=description,
        )

        return time_series_get
