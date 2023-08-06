from typing import Any, Dict, Optional, Type, TypeVar

import attr

from ..models.relative_timing_get_object import RelativeTimingGetObject
from ..models.relative_timing_get_type import RelativeTimingGetType

T = TypeVar("T", bound="RelativeTimingGet")


@attr.s(auto_attribs=True)
class RelativeTimingGet:
    """Relative timing schema for get responses."""

    object_: RelativeTimingGetObject
    type: RelativeTimingGetType
    time_zone: str
    frequency: Optional[str]
    offset: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        type = self.type.value

        time_zone = self.time_zone
        frequency = self.frequency
        offset = self.offset

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "type": type,
                "time_zone": time_zone,
                "frequency": frequency,
                "offset": offset,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = RelativeTimingGetObject(d.pop("object"))

        type = RelativeTimingGetType(d.pop("type"))

        time_zone = d.pop("time_zone")

        frequency = d.pop("frequency")

        offset = d.pop("offset")

        relative_timing_get = cls(
            object_=object_,
            type=type,
            time_zone=time_zone,
            frequency=frequency,
            offset=offset,
        )

        return relative_timing_get
