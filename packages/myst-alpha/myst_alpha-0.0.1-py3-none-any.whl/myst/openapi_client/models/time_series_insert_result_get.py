from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.time_series_insert_result_get_object import TimeSeriesInsertResultGetObject
from ..models.time_series_insert_result_get_type import TimeSeriesInsertResultGetType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeSeriesInsertResultGet")


@attr.s(auto_attribs=True)
class TimeSeriesInsertResultGet:
    """Time series insert result schema for get responses."""

    object_: TimeSeriesInsertResultGetObject
    uuid: str
    create_time: str
    type: TimeSeriesInsertResultGetType
    node: str
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        type = self.type.value

        node = self.node
        update_time = self.update_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "uuid": uuid,
                "create_time": create_time,
                "type": type,
                "node": node,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = TimeSeriesInsertResultGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        type = TimeSeriesInsertResultGetType(d.pop("type"))

        node = d.pop("node")

        update_time = d.pop("update_time", UNSET)

        time_series_insert_result_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            type=type,
            node=node,
            update_time=update_time,
        )

        return time_series_insert_result_get
