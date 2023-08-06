from typing import Any, Dict, Type, TypeVar

import attr

from ..models.operation_connector_get_object import OperationConnectorGetObject
from ..models.operation_connector_get_type import OperationConnectorGetType

T = TypeVar("T", bound="OperationConnectorGet")


@attr.s(auto_attribs=True)
class OperationConnectorGet:
    """Operation connector schema for get responses."""

    object_: OperationConnectorGetObject
    type: OperationConnectorGetType
    uuid: str
    name: str
    entity: str

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        type = self.type.value

        uuid = self.uuid
        name = self.name
        entity = self.entity

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "type": type,
                "uuid": uuid,
                "name": name,
                "entity": entity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = OperationConnectorGetObject(d.pop("object"))

        type = OperationConnectorGetType(d.pop("type"))

        uuid = d.pop("uuid")

        name = d.pop("name")

        entity = d.pop("entity")

        operation_connector_get = cls(
            object_=object_,
            type=type,
            uuid=uuid,
            name=name,
            entity=entity,
        )

        return operation_connector_get
