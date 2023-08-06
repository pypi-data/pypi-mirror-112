from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.organization_get_object import OrganizationGetObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationGet")


@attr.s(auto_attribs=True)
class OrganizationGet:
    """Schema for organization get responses."""

    object_: OrganizationGetObject
    uuid: str
    create_time: str
    name: str
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        name = self.name
        update_time = self.update_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "uuid": uuid,
                "create_time": create_time,
                "name": name,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = OrganizationGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        name = d.pop("name")

        update_time = d.pop("update_time", UNSET)

        organization_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            name=name,
            update_time=update_time,
        )

        return organization_get
