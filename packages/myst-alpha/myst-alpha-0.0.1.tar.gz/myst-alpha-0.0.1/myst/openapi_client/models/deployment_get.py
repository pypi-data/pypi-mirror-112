from typing import Any, Dict, Optional, Type, TypeVar, Union

import attr

from ..models.deployment_get_object import DeploymentGetObject
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeploymentGet")


@attr.s(auto_attribs=True)
class DeploymentGet:
    """Abstract base resource schema for get responses."""

    object_: DeploymentGetObject
    uuid: str
    create_time: str
    title: str
    creator: str
    activate_time: Optional[str]
    deactivate_time: Optional[str]
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        title = self.title
        creator = self.creator
        update_time = self.update_time
        activate_time = self.activate_time
        deactivate_time = self.deactivate_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "uuid": uuid,
                "create_time": create_time,
                "title": title,
                "creator": creator,
                "activate_time": activate_time,
                "deactivate_time": deactivate_time,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = DeploymentGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        title = d.pop("title")

        creator = d.pop("creator")

        update_time = d.pop("update_time", UNSET)

        activate_time = d.pop("activate_time")

        deactivate_time = d.pop("deactivate_time")

        deployment_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            title=title,
            creator=creator,
            update_time=update_time,
            activate_time=activate_time,
            deactivate_time=deactivate_time,
        )

        return deployment_get
