from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.organization_role import OrganizationRole
from ..models.user_get_object import UserGetObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserGet")


@attr.s(auto_attribs=True)
class UserGet:
    """User schema for get responses."""

    object_: UserGetObject
    uuid: str
    create_time: str
    email: str
    organization: str
    organization_role: OrganizationRole
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        email = self.email
        organization = self.organization
        organization_role = self.organization_role.value

        update_time = self.update_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "uuid": uuid,
                "create_time": create_time,
                "email": email,
                "organization": organization,
                "organization_role": organization_role,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = UserGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        email = d.pop("email")

        organization = d.pop("organization")

        organization_role = OrganizationRole(d.pop("organization_role"))

        update_time = d.pop("update_time", UNSET)

        user_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            email=email,
            organization=organization,
            organization_role=organization_role,
            update_time=update_time,
        )

        return user_get
