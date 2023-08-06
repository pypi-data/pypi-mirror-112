from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

T = TypeVar("T", bound="TimeDatasetSpec")


@attr.s(auto_attribs=True)
class TimeDatasetSpec:
    """A custom schema that represents the `spec` of a `TimeDataset`."""

    sample_period: str
    cell_shape: List[int]
    coordinate_labels: List[List[Union[int, str]]]
    axis_labels: List[Union[int, str]]

    def to_dict(self) -> Dict[str, Any]:
        sample_period = self.sample_period
        cell_shape = self.cell_shape

        coordinate_labels = []
        for coordinate_labels_item_data in self.coordinate_labels:
            coordinate_labels_item = []
            for coordinate_labels_item_item_data in coordinate_labels_item_data:
                coordinate_labels_item_item = coordinate_labels_item_item_data

                coordinate_labels_item.append(coordinate_labels_item_item)

            coordinate_labels.append(coordinate_labels_item)

        axis_labels = []
        for axis_labels_item_data in self.axis_labels:
            axis_labels_item = axis_labels_item_data

            axis_labels.append(axis_labels_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "sample_period": sample_period,
                "cell_shape": cell_shape,
                "coordinate_labels": coordinate_labels,
                "axis_labels": axis_labels,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sample_period = d.pop("sample_period")

        cell_shape = cast(List[int], d.pop("cell_shape"))

        coordinate_labels = []
        _coordinate_labels = d.pop("coordinate_labels")
        for coordinate_labels_item_data in _coordinate_labels:
            coordinate_labels_item = []
            _coordinate_labels_item = coordinate_labels_item_data
            for coordinate_labels_item_item_data in _coordinate_labels_item:

                def _parse_coordinate_labels_item_item(data: object) -> Union[int, str]:
                    return cast(Union[int, str], data)

                coordinate_labels_item_item = _parse_coordinate_labels_item_item(coordinate_labels_item_item_data)

                coordinate_labels_item.append(coordinate_labels_item_item)

            coordinate_labels.append(coordinate_labels_item)

        axis_labels = []
        _axis_labels = d.pop("axis_labels")
        for axis_labels_item_data in _axis_labels:

            def _parse_axis_labels_item(data: object) -> Union[int, str]:
                return cast(Union[int, str], data)

            axis_labels_item = _parse_axis_labels_item(axis_labels_item_data)

            axis_labels.append(axis_labels_item)

        time_dataset_spec = cls(
            sample_period=sample_period,
            cell_shape=cell_shape,
            coordinate_labels=coordinate_labels,
            axis_labels=axis_labels,
        )

        return time_dataset_spec
