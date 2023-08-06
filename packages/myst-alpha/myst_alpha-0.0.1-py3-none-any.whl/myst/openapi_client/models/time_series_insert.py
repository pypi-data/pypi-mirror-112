from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.time_dataset import TimeDataset

T = TypeVar("T", bound="TimeSeriesInsert")


@attr.s(auto_attribs=True)
class TimeSeriesInsert:
    """Schema for time series insert requests."""

    time_dataset: TimeDataset
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        time_dataset = self.time_dataset.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "time_dataset": time_dataset,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        time_dataset = TimeDataset.from_dict(d.pop("time_dataset"))

        time_series_insert = cls(
            time_dataset=time_dataset,
        )

        time_series_insert.additional_properties = d
        return time_series_insert

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
