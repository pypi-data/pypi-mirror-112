from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeDatasetRow")


@attr.s(auto_attribs=True)
class TimeDatasetRow:
    """ """

    start_time: str
    end_time: str
    as_of_time: str
    values: List[float]
    mask: Union[Unset, List[float]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_time = self.start_time
        end_time = self.end_time
        as_of_time = self.as_of_time
        values = self.values

        mask: Union[Unset, List[float]] = UNSET
        if not isinstance(self.mask, Unset):
            mask = self.mask

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_time": start_time,
                "end_time": end_time,
                "as_of_time": as_of_time,
                "values": values,
            }
        )
        if mask is not UNSET:
            field_dict["mask"] = mask

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_time = d.pop("start_time")

        end_time = d.pop("end_time")

        as_of_time = d.pop("as_of_time")

        values = cast(List[float], d.pop("values"))

        mask = cast(List[float], d.pop("mask", UNSET))

        time_dataset_row = cls(
            start_time=start_time,
            end_time=end_time,
            as_of_time=as_of_time,
            values=values,
            mask=mask,
        )

        time_dataset_row.additional_properties = d
        return time_dataset_row

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
