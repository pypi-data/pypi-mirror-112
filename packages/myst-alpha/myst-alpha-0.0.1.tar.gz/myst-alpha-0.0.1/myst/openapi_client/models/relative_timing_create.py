from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.relative_timing_create_object import RelativeTimingCreateObject
from ..models.relative_timing_create_type import RelativeTimingCreateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RelativeTimingCreate")


@attr.s(auto_attribs=True)
class RelativeTimingCreate:
    """Relative timing schema for create requests."""

    object_: RelativeTimingCreateObject
    type: RelativeTimingCreateType
    frequency: Union[Unset, None, str] = UNSET
    offset: Union[Unset, None, str] = UNSET
    time_zone: Union[Unset, str] = "UTC"

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        type = self.type.value

        frequency = self.frequency
        offset = self.offset
        time_zone = self.time_zone

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "type": type,
            }
        )
        if frequency is not UNSET:
            field_dict["frequency"] = frequency
        if offset is not UNSET:
            field_dict["offset"] = offset
        if time_zone is not UNSET:
            field_dict["time_zone"] = time_zone

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = RelativeTimingCreateObject(d.pop("object"))

        type = RelativeTimingCreateType(d.pop("type"))

        frequency = d.pop("frequency", UNSET)

        offset = d.pop("offset", UNSET)

        time_zone = d.pop("time_zone", UNSET)

        relative_timing_create = cls(
            object_=object_,
            type=type,
            frequency=frequency,
            offset=offset,
            time_zone=time_zone,
        )

        return relative_timing_create
