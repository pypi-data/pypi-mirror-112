from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.organization_update_object import OrganizationUpdateObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationUpdate")


@attr.s(auto_attribs=True)
class OrganizationUpdate:
    """Schema for organization update requests."""

    object_: Union[Unset, OrganizationUpdateObject] = UNSET
    uuid: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    update_time: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_: Union[Unset, str] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        update_time = self.update_time
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if object_ is not UNSET:
            field_dict["object"] = object_
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if create_time is not UNSET:
            field_dict["create_time"] = create_time
        if update_time is not UNSET:
            field_dict["update_time"] = update_time
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _object_ = d.pop("object", UNSET)
        object_: Union[Unset, OrganizationUpdateObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = OrganizationUpdateObject(_object_)

        uuid = d.pop("uuid", UNSET)

        create_time = d.pop("create_time", UNSET)

        update_time = d.pop("update_time", UNSET)

        name = d.pop("name", UNSET)

        organization_update = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            update_time=update_time,
            name=name,
        )

        return organization_update
