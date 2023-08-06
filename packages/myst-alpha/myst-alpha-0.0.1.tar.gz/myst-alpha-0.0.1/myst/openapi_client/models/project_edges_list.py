from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.input_get import InputGet
from ..models.layer_get import LayerGet

T = TypeVar("T", bound="ProjectEdgesList")


@attr.s(auto_attribs=True)
class ProjectEdgesList:
    """Project edges list schema."""

    data: List[Union[InputGet, LayerGet]]
    has_more: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            if isinstance(data_item_data, InputGet):
                data_item = data_item_data.to_dict()

            else:
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

            def _parse_data_item(data: object) -> Union[InputGet, LayerGet]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    data_item_type_0 = InputGet.from_dict(data)

                    return data_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                data_item_type_1 = LayerGet.from_dict(data)

                return data_item_type_1

            data_item = _parse_data_item(data_item_data)

            data.append(data_item)

        has_more = d.pop("has_more")

        project_edges_list = cls(
            data=data,
            has_more=has_more,
        )

        project_edges_list.additional_properties = d
        return project_edges_list

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
