from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.deploy_status import DeployStatus
from ..models.project_update_object import ProjectUpdateObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectUpdate")


@attr.s(auto_attribs=True)
class ProjectUpdate:
    """Schema for project update requests."""

    object_: Union[Unset, ProjectUpdateObject] = UNSET
    uuid: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    update_time: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    creator: Union[Unset, str] = UNSET
    deploy_status: Union[Unset, DeployStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_: Union[Unset, str] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        update_time = self.update_time
        organization = self.organization
        owner = self.owner
        title = self.title
        description = self.description
        creator = self.creator
        deploy_status: Union[Unset, str] = UNSET
        if not isinstance(self.deploy_status, Unset):
            deploy_status = self.deploy_status.value

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
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if creator is not UNSET:
            field_dict["creator"] = creator
        if deploy_status is not UNSET:
            field_dict["deploy_status"] = deploy_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _object_ = d.pop("object", UNSET)
        object_: Union[Unset, ProjectUpdateObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = ProjectUpdateObject(_object_)

        uuid = d.pop("uuid", UNSET)

        create_time = d.pop("create_time", UNSET)

        update_time = d.pop("update_time", UNSET)

        organization = d.pop("organization", UNSET)

        owner = d.pop("owner", UNSET)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        creator = d.pop("creator", UNSET)

        _deploy_status = d.pop("deploy_status", UNSET)
        deploy_status: Union[Unset, DeployStatus]
        if isinstance(_deploy_status, Unset):
            deploy_status = UNSET
        else:
            deploy_status = DeployStatus(_deploy_status)

        project_update = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            update_time=update_time,
            organization=organization,
            owner=owner,
            title=title,
            description=description,
            creator=creator,
            deploy_status=deploy_status,
        )

        return project_update
