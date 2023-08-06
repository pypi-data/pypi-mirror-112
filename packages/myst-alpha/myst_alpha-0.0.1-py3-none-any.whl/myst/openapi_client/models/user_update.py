from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.organization_role import OrganizationRole
from ..models.user_update_object import UserUpdateObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserUpdate")


@attr.s(auto_attribs=True)
class UserUpdate:
    """User schema for update requests."""

    object_: Union[Unset, UserUpdateObject] = UNSET
    uuid: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    update_time: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    organization_role: Union[Unset, OrganizationRole] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_: Union[Unset, str] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        update_time = self.update_time
        email = self.email
        organization = self.organization
        organization_role: Union[Unset, str] = UNSET
        if not isinstance(self.organization_role, Unset):
            organization_role = self.organization_role.value

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
        if email is not UNSET:
            field_dict["email"] = email
        if organization is not UNSET:
            field_dict["organization"] = organization
        if organization_role is not UNSET:
            field_dict["organization_role"] = organization_role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _object_ = d.pop("object", UNSET)
        object_: Union[Unset, UserUpdateObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = UserUpdateObject(_object_)

        uuid = d.pop("uuid", UNSET)

        create_time = d.pop("create_time", UNSET)

        update_time = d.pop("update_time", UNSET)

        email = d.pop("email", UNSET)

        organization = d.pop("organization", UNSET)

        _organization_role = d.pop("organization_role", UNSET)
        organization_role: Union[Unset, OrganizationRole]
        if isinstance(_organization_role, Unset):
            organization_role = UNSET
        else:
            organization_role = OrganizationRole(_organization_role)

        user_update = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            update_time=update_time,
            email=email,
            organization=organization,
            organization_role=organization_role,
        )

        return user_update
