from typing import Any, Dict, Optional, Type, TypeVar, Union

import attr

from ..models.deploy_status import DeployStatus
from ..models.project_get_object import ProjectGetObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectGet")


@attr.s(auto_attribs=True)
class ProjectGet:
    """Schema for project get responses."""

    object_: ProjectGetObject
    uuid: str
    create_time: str
    organization: str
    owner: str
    title: str
    creator: str
    deploy_status: DeployStatus
    description: Optional[str]
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        organization = self.organization
        owner = self.owner
        title = self.title
        creator = self.creator
        deploy_status = self.deploy_status.value

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
                "title": title,
                "creator": creator,
                "deploy_status": deploy_status,
                "description": description,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = ProjectGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        organization = d.pop("organization")

        owner = d.pop("owner")

        title = d.pop("title")

        creator = d.pop("creator")

        deploy_status = DeployStatus(d.pop("deploy_status"))

        update_time = d.pop("update_time", UNSET)

        description = d.pop("description")

        project_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            organization=organization,
            owner=owner,
            title=title,
            creator=creator,
            deploy_status=deploy_status,
            update_time=update_time,
            description=description,
        )

        return project_get
