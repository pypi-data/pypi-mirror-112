from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.model_run_result_get_object import ModelRunResultGetObject
from ..models.model_run_result_get_type import ModelRunResultGetType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelRunResultGet")


@attr.s(auto_attribs=True)
class ModelRunResultGet:
    """Model run result schema for get responses."""

    object_: ModelRunResultGetObject
    uuid: str
    create_time: str
    type: ModelRunResultGetType
    node: str
    start_time: str
    end_time: str
    as_of_time: str
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        type = self.type.value

        node = self.node
        start_time = self.start_time
        end_time = self.end_time
        as_of_time = self.as_of_time
        update_time = self.update_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "uuid": uuid,
                "create_time": create_time,
                "type": type,
                "node": node,
                "start_time": start_time,
                "end_time": end_time,
                "as_of_time": as_of_time,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = ModelRunResultGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        type = ModelRunResultGetType(d.pop("type"))

        node = d.pop("node")

        start_time = d.pop("start_time")

        end_time = d.pop("end_time")

        as_of_time = d.pop("as_of_time")

        update_time = d.pop("update_time", UNSET)

        model_run_result_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            type=type,
            node=node,
            start_time=start_time,
            end_time=end_time,
            as_of_time=as_of_time,
            update_time=update_time,
        )

        return model_run_result_get
