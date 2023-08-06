from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.source_create_object import SourceCreateObject
from ..models.source_create_parameters import SourceCreateParameters
from ..models.source_create_type import SourceCreateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SourceCreate")


@attr.s(auto_attribs=True)
class SourceCreate:
    """Source schema for create requests."""

    object_: SourceCreateObject
    type: SourceCreateType
    title: str
    project: str
    connector_uuid: str
    description: Union[Unset, None, str] = UNSET
    parameters: Union[Unset, SourceCreateParameters] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        type = self.type.value

        title = self.title
        project = self.project
        connector_uuid = self.connector_uuid
        description = self.description
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "type": type,
                "title": title,
                "project": project,
                "connector_uuid": connector_uuid,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = SourceCreateObject(d.pop("object"))

        type = SourceCreateType(d.pop("type"))

        title = d.pop("title")

        project = d.pop("project")

        connector_uuid = d.pop("connector_uuid")

        description = d.pop("description", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, SourceCreateParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = SourceCreateParameters.from_dict(_parameters)

        source_create = cls(
            object_=object_,
            type=type,
            title=title,
            project=project,
            connector_uuid=connector_uuid,
            description=description,
            parameters=parameters,
        )

        return source_create
