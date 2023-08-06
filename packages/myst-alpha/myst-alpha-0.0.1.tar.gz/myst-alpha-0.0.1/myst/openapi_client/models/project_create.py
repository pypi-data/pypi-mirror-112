from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.project_create_object import ProjectCreateObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectCreate")


@attr.s(auto_attribs=True)
class ProjectCreate:
    """Schema for project create requests."""

    object_: ProjectCreateObject
    title: str
    description: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        title = self.title
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "title": title,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = ProjectCreateObject(d.pop("object"))

        title = d.pop("title")

        description = d.pop("description", UNSET)

        project_create = cls(
            object_=object_,
            title=title,
            description=description,
        )

        return project_create
