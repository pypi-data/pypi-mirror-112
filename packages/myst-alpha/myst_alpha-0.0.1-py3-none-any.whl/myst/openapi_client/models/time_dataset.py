from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.time_dataset_metadata import TimeDatasetMetadata
from ..models.time_dataset_object import TimeDatasetObject
from ..models.time_dataset_row import TimeDatasetRow
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeDataset")


@attr.s(auto_attribs=True)
class TimeDataset:
    """ """

    object_: TimeDatasetObject
    cell_shape: List[int]
    sample_period: str
    data: List[TimeDatasetRow]
    coordinate_labels: Union[Unset, List[List[Union[int, str]]]] = UNSET
    axis_labels: Union[Unset, List[Union[int, str]]] = UNSET
    metadata: Union[Unset, TimeDatasetMetadata] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        cell_shape = self.cell_shape

        sample_period = self.sample_period
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()

            data.append(data_item)

        coordinate_labels: Union[Unset, List[List[Union[int, str]]]] = UNSET
        if not isinstance(self.coordinate_labels, Unset):
            coordinate_labels = []
            for coordinate_labels_item_data in self.coordinate_labels:
                coordinate_labels_item = []
                for coordinate_labels_item_item_data in coordinate_labels_item_data:
                    coordinate_labels_item_item = coordinate_labels_item_item_data

                    coordinate_labels_item.append(coordinate_labels_item_item)

                coordinate_labels.append(coordinate_labels_item)

        axis_labels: Union[Unset, List[Union[int, str]]] = UNSET
        if not isinstance(self.axis_labels, Unset):
            axis_labels = []
            for axis_labels_item_data in self.axis_labels:
                axis_labels_item = axis_labels_item_data

                axis_labels.append(axis_labels_item)

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
                "cell_shape": cell_shape,
                "sample_period": sample_period,
                "data": data,
            }
        )
        if coordinate_labels is not UNSET:
            field_dict["coordinate_labels"] = coordinate_labels
        if axis_labels is not UNSET:
            field_dict["axis_labels"] = axis_labels
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = TimeDatasetObject(d.pop("object"))

        cell_shape = cast(List[int], d.pop("cell_shape"))

        sample_period = d.pop("sample_period")

        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = TimeDatasetRow.from_dict(data_item_data)

            data.append(data_item)

        coordinate_labels = []
        _coordinate_labels = d.pop("coordinate_labels", UNSET)
        for coordinate_labels_item_data in _coordinate_labels or []:
            coordinate_labels_item = []
            _coordinate_labels_item = coordinate_labels_item_data
            for coordinate_labels_item_item_data in _coordinate_labels_item:

                def _parse_coordinate_labels_item_item(data: object) -> Union[int, str]:
                    return cast(Union[int, str], data)

                coordinate_labels_item_item = _parse_coordinate_labels_item_item(coordinate_labels_item_item_data)

                coordinate_labels_item.append(coordinate_labels_item_item)

            coordinate_labels.append(coordinate_labels_item)

        axis_labels = []
        _axis_labels = d.pop("axis_labels", UNSET)
        for axis_labels_item_data in _axis_labels or []:

            def _parse_axis_labels_item(data: object) -> Union[int, str]:
                return cast(Union[int, str], data)

            axis_labels_item = _parse_axis_labels_item(axis_labels_item_data)

            axis_labels.append(axis_labels_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, TimeDatasetMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = TimeDatasetMetadata.from_dict(_metadata)

        time_dataset = cls(
            object_=object_,
            cell_shape=cell_shape,
            sample_period=sample_period,
            data=data,
            coordinate_labels=coordinate_labels,
            axis_labels=axis_labels,
            metadata=metadata,
        )

        time_dataset.additional_properties = d
        return time_dataset

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
