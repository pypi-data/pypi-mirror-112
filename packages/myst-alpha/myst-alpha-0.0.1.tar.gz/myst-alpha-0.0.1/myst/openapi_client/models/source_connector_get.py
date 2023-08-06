from typing import Any, Dict, Type, TypeVar

import attr

from ..models.source_connector_get_object import SourceConnectorGetObject
from ..models.source_connector_get_type import SourceConnectorGetType

T = TypeVar("T", bound="SourceConnectorGet")


@attr.s(auto_attribs=True)
class SourceConnectorGet:
    """Source connector schema for get responses."""

    object_: SourceConnectorGetObject
    type: SourceConnectorGetType
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
        object_ = SourceConnectorGetObject(d.pop("object"))

        type = SourceConnectorGetType(d.pop("type"))

        uuid = d.pop("uuid")

        name = d.pop("name")

        entity = d.pop("entity")

        source_connector_get = cls(
            object_=object_,
            type=type,
            uuid=uuid,
            name=name,
            entity=entity,
        )

        return source_connector_get
