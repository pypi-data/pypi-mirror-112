from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.deployment_get import DeploymentGet

T = TypeVar("T", bound="ResourceListDeploymentGet")


@attr.s(auto_attribs=True)
class ResourceListDeploymentGet:
    """Generic resource list."""

    data: List[DeploymentGet]
    has_more: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()

            data.append(data_item)

        has_more = self.has_more

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "has_more": has_more,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = DeploymentGet.from_dict(data_item_data)

            data.append(data_item)

        has_more = d.pop("has_more")

        resource_list_deployment_get = cls(
            data=data,
            has_more=has_more,
        )

        resource_list_deployment_get.additional_properties = d
        return resource_list_deployment_get

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
