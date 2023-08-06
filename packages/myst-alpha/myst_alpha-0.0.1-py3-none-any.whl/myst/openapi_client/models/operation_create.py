from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.operation_create_object import OperationCreateObject
from ..models.operation_create_parameters import OperationCreateParameters
from ..models.operation_create_type import OperationCreateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="OperationCreate")


@attr.s(auto_attribs=True)
class OperationCreate:
    """Operation schema for create requests."""

    object_: OperationCreateObject
    type: OperationCreateType
    title: str
    project: str
    connector_uuid: str
    description: Union[Unset, None, str] = UNSET
    parameters: Union[Unset, OperationCreateParameters] = UNSET

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
        object_ = OperationCreateObject(d.pop("object"))

        type = OperationCreateType(d.pop("type"))

        title = d.pop("title")

        project = d.pop("project")

        connector_uuid = d.pop("connector_uuid")

        description = d.pop("description", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, OperationCreateParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = OperationCreateParameters.from_dict(_parameters)

        operation_create = cls(
            object_=object_,
            type=type,
            title=title,
            project=project,
            connector_uuid=connector_uuid,
            description=description,
            parameters=parameters,
        )

        return operation_create
