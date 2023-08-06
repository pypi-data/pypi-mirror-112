from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.absolute_timing_create_object import AbsoluteTimingCreateObject
from ..models.absolute_timing_create_type import AbsoluteTimingCreateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AbsoluteTimingCreate")


@attr.s(auto_attribs=True)
class AbsoluteTimingCreate:
    """Absolute timing schema for create requests."""

    object_: AbsoluteTimingCreateObject
    type: AbsoluteTimingCreateType
    time: str
    time_zone: Union[Unset, str] = "UTC"

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        type = self.type.value

        time = self.time
        time_zone = self.time_zone

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "type": type,
                "time": time,
            }
        )
        if time_zone is not UNSET:
            field_dict["time_zone"] = time_zone

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = AbsoluteTimingCreateObject(d.pop("object"))

        type = AbsoluteTimingCreateType(d.pop("type"))

        time = d.pop("time")

        time_zone = d.pop("time_zone", UNSET)

        absolute_timing_create = cls(
            object_=object_,
            type=type,
            time=time,
            time_zone=time_zone,
        )

        return absolute_timing_create
