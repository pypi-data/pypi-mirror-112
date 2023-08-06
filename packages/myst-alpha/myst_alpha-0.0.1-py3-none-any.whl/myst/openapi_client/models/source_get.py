from typing import Any, Dict, Optional, Type, TypeVar, Union

import attr

from ..models.deploy_status import DeployStatus
from ..models.source_get_object import SourceGetObject
from ..models.source_get_parameters import SourceGetParameters
from ..models.source_get_type import SourceGetType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SourceGet")


@attr.s(auto_attribs=True)
class SourceGet:
    """Source schema for get responses."""

    object_: SourceGetObject
    uuid: str
    create_time: str
    organization: str
    owner: str
    type: SourceGetType
    title: str
    project: str
    creator: str
    deploy_status: DeployStatus
    connector_uuid: str
    parameters: SourceGetParameters
    description: Optional[str]
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        organization = self.organization
        owner = self.owner
        type = self.type.value

        title = self.title
        project = self.project
        creator = self.creator
        deploy_status = self.deploy_status.value

        connector_uuid = self.connector_uuid
        parameters = self.parameters.to_dict()

        update_time = self.update_time
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "uuid": uuid,
                "create_time": create_time,
                "organization": organization,
                "owner": owner,
                "type": type,
                "title": title,
                "project": project,
                "creator": creator,
                "deploy_status": deploy_status,
                "connector_uuid": connector_uuid,
                "parameters": parameters,
                "description": description,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = SourceGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        organization = d.pop("organization")

        owner = d.pop("owner")

        type = SourceGetType(d.pop("type"))

        title = d.pop("title")

        project = d.pop("project")

        creator = d.pop("creator")

        deploy_status = DeployStatus(d.pop("deploy_status"))

        connector_uuid = d.pop("connector_uuid")

        parameters = SourceGetParameters.from_dict(d.pop("parameters"))

        update_time = d.pop("update_time", UNSET)

        description = d.pop("description")

        source_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            organization=organization,
            owner=owner,
            type=type,
            title=title,
            project=project,
            creator=creator,
            deploy_status=deploy_status,
            connector_uuid=connector_uuid,
            parameters=parameters,
            update_time=update_time,
            description=description,
        )

        return source_get
