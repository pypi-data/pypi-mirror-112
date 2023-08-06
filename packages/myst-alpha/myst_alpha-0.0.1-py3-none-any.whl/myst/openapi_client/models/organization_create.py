from typing import Any, Dict, Type, TypeVar

import attr

from ..models.organization_create_object import OrganizationCreateObject

T = TypeVar("T", bound="OrganizationCreate")


@attr.s(auto_attribs=True)
class OrganizationCreate:
    """Schema for organization create requests."""

    object_: OrganizationCreateObject
    name: str

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = OrganizationCreateObject(d.pop("object"))

        name = d.pop("name")

        organization_create = cls(
            object_=object_,
            name=name,
        )

        return organization_create
