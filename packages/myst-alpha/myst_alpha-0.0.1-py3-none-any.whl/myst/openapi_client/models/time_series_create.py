from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.time_series_create_object import TimeSeriesCreateObject
from ..models.time_series_create_type import TimeSeriesCreateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeSeriesCreate")


@attr.s(auto_attribs=True)
class TimeSeriesCreate:
    """Time series schema for create requests."""

    object_: TimeSeriesCreateObject
    title: str
    project: str
    sample_period: str
    cell_shape: List[None]
    coordinate_labels: List[None]
    axis_labels: List[None]
    type: Union[Unset, TimeSeriesCreateType] = UNSET
    description: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        title = self.title
        project = self.project
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

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "title": title,
                "project": project,
                "sample_period": sample_period,
                "cell_shape": cell_shape,
                "coordinate_labels": coordinate_labels,
                "axis_labels": axis_labels,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = TimeSeriesCreateObject(d.pop("object"))

        title = d.pop("title")

        project = d.pop("project")

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

        _type = d.pop("type", UNSET)
        type: Union[Unset, TimeSeriesCreateType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = TimeSeriesCreateType(_type)

        description = d.pop("description", UNSET)

        time_series_create = cls(
            object_=object_,
            title=title,
            project=project,
            sample_period=sample_period,
            cell_shape=cell_shape,
            coordinate_labels=coordinate_labels,
            axis_labels=axis_labels,
            type=type,
            description=description,
        )

        return time_series_create
