from typing import Any, Dict, Type, TypeVar

import attr

from ..models.deployment_create_object import DeploymentCreateObject

T = TypeVar("T", bound="DeploymentCreate")


@attr.s(auto_attribs=True)
class DeploymentCreate:
    """Abstract base resource schema for create requests."""

    object_: DeploymentCreateObject
    title: str

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        title = self.title

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "title": title,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = DeploymentCreateObject(d.pop("object"))

        title = d.pop("title")

        deployment_create = cls(
            object_=object_,
            title=title,
        )

        return deployment_create
