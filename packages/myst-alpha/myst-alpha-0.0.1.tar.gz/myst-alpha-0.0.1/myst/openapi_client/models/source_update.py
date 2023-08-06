from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.deploy_status import DeployStatus
from ..models.source_update_parameters import SourceUpdateParameters
from ..models.source_update_type import SourceUpdateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SourceUpdate")


@attr.s(auto_attribs=True)
class SourceUpdate:
    """Source schema for update requests."""

    object_: Union[Unset, None] = UNSET
    uuid: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    update_time: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    type: Union[Unset, SourceUpdateType] = UNSET
    project: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    deploy_status: Union[Unset, DeployStatus] = UNSET
    connector_uuid: Union[Unset, str] = UNSET
    parameters: Union[Unset, SourceUpdateParameters] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = None

        uuid = self.uuid
        create_time = self.create_time
        update_time = self.update_time
        organization = self.organization
        owner = self.owner
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        project = self.project
        title = self.title
        description = self.description
        deploy_status: Union[Unset, str] = UNSET
        if not isinstance(self.deploy_status, Unset):
            deploy_status = self.deploy_status.value

        connector_uuid = self.connector_uuid
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

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
        if organization is not UNSET:
            field_dict["organization"] = organization
        if owner is not UNSET:
            field_dict["owner"] = owner
        if type is not UNSET:
            field_dict["type"] = type
        if project is not UNSET:
            field_dict["project"] = project
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if deploy_status is not UNSET:
            field_dict["deploy_status"] = deploy_status
        if connector_uuid is not UNSET:
            field_dict["connector_uuid"] = connector_uuid
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = None

        uuid = d.pop("uuid", UNSET)

        create_time = d.pop("create_time", UNSET)

        update_time = d.pop("update_time", UNSET)

        organization = d.pop("organization", UNSET)

        owner = d.pop("owner", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, SourceUpdateType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = SourceUpdateType(_type)

        project = d.pop("project", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        _deploy_status = d.pop("deploy_status", UNSET)
        deploy_status: Union[Unset, DeployStatus]
        if isinstance(_deploy_status, Unset):
            deploy_status = UNSET
        else:
            deploy_status = DeployStatus(_deploy_status)

        connector_uuid = d.pop("connector_uuid", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, SourceUpdateParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = SourceUpdateParameters.from_dict(_parameters)

        source_update = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            update_time=update_time,
            organization=organization,
            owner=owner,
            type=type,
            project=project,
            title=title,
            description=description,
            deploy_status=deploy_status,
            connector_uuid=connector_uuid,
            parameters=parameters,
        )

        return source_update
