from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.model_create_object import ModelCreateObject
from ..models.model_create_parameters import ModelCreateParameters
from ..models.model_create_type import ModelCreateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelCreate")


@attr.s(auto_attribs=True)
class ModelCreate:
    """Model schema for create requests."""

    object_: ModelCreateObject
    type: ModelCreateType
    title: str
    project: str
    connector_uuid: str
    description: Union[Unset, None, str] = UNSET
    parameters: Union[Unset, ModelCreateParameters] = UNSET

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
        object_ = ModelCreateObject(d.pop("object"))

        type = ModelCreateType(d.pop("type"))

        title = d.pop("title")

        project = d.pop("project")

        connector_uuid = d.pop("connector_uuid")

        description = d.pop("description", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, ModelCreateParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = ModelCreateParameters.from_dict(_parameters)

        model_create = cls(
            object_=object_,
            type=type,
            title=title,
            project=project,
            connector_uuid=connector_uuid,
            description=description,
            parameters=parameters,
        )

        return model_create
