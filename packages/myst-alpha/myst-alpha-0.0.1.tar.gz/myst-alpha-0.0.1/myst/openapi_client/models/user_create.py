from typing import Any, Dict, Type, TypeVar

import attr

from ..models.organization_role import OrganizationRole
from ..models.user_create_object import UserCreateObject

T = TypeVar("T", bound="UserCreate")


@attr.s(auto_attribs=True)
class UserCreate:
    """User schema for create requests."""

    object_: UserCreateObject
    email: str
    organization: str
    organization_role: OrganizationRole

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        email = self.email
        organization = self.organization
        organization_role = self.organization_role.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "email": email,
                "organization": organization,
                "organization_role": organization_role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = UserCreateObject(d.pop("object"))

        email = d.pop("email")

        organization = d.pop("organization")

        organization_role = OrganizationRole(d.pop("organization_role"))

        user_create = cls(
            object_=object_,
            email=email,
            organization=organization,
            organization_role=organization_role,
        )

        return user_create
