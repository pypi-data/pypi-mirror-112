from typing import Any, Dict, Type, TypeVar

import attr

from ..models.absolute_timing_get_object import AbsoluteTimingGetObject
from ..models.absolute_timing_get_type import AbsoluteTimingGetType

T = TypeVar("T", bound="AbsoluteTimingGet")


@attr.s(auto_attribs=True)
class AbsoluteTimingGet:
    """Absolute timing schema for get responses."""

    object_: AbsoluteTimingGetObject
    type: AbsoluteTimingGetType
    time: str
    time_zone: str

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
                "time_zone": time_zone,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = AbsoluteTimingGetObject(d.pop("object"))

        type = AbsoluteTimingGetType(d.pop("type"))

        time = d.pop("time")

        time_zone = d.pop("time_zone")

        absolute_timing_get = cls(
            object_=object_,
            type=type,
            time=time,
            time_zone=time_zone,
        )

        return absolute_timing_get
