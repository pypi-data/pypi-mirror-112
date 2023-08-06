from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.time_dataset import TimeDataset
from ..models.time_series_query_result_get_object import TimeSeriesQueryResultGetObject
from ..models.time_series_query_result_get_type import TimeSeriesQueryResultGetType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeSeriesQueryResultGet")


@attr.s(auto_attribs=True)
class TimeSeriesQueryResultGet:
    """Time series query result schema for get responses."""

    object_: TimeSeriesQueryResultGetObject
    uuid: str
    create_time: str
    type: TimeSeriesQueryResultGetType
    node: str
    time_dataset: TimeDataset
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        type = self.type.value

        node = self.node
        time_dataset = self.time_dataset.to_dict()

        update_time = self.update_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "uuid": uuid,
                "create_time": create_time,
                "type": type,
                "node": node,
                "time_dataset": time_dataset,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = TimeSeriesQueryResultGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        type = TimeSeriesQueryResultGetType(d.pop("type"))

        node = d.pop("node")

        time_dataset = TimeDataset.from_dict(d.pop("time_dataset"))

        update_time = d.pop("update_time", UNSET)

        time_series_query_result_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            type=type,
            node=node,
            time_dataset=time_dataset,
            update_time=update_time,
        )

        return time_series_query_result_get
