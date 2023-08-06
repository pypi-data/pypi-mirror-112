from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.input_create_object import InputCreateObject
from ..models.input_create_type import InputCreateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="InputCreate")


@attr.s(auto_attribs=True)
class InputCreate:
    """Input schema for create requests."""

    object_: InputCreateObject
    type: InputCreateType
    upstream_node: str
    group_name: str
    output_index: Union[Unset, int] = 0
    label_indexer: Union[List[None], List[Union[List[None], int, str]], None, Unset, int, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        type = self.type.value

        upstream_node = self.upstream_node
        group_name = self.group_name
        output_index = self.output_index
        label_indexer: Union[List[None], List[Union[List[None], int, str]], None, Unset, int, str]
        if isinstance(self.label_indexer, Unset):
            label_indexer = UNSET
        elif self.label_indexer is None:
            label_indexer = None
        elif isinstance(self.label_indexer, list):
            label_indexer = UNSET
            if not isinstance(self.label_indexer, Unset):
                label_indexer = []
                for label_indexer_type_0_item_data in self.label_indexer:
                    if isinstance(label_indexer_type_0_item_data, list):
                        label_indexer_type_0_item = []
                        for label_indexer_type_0_item_type_2_item_data in label_indexer_type_0_item_data:
                            label_indexer_type_0_item_type_2_item = None

                            label_indexer_type_0_item.append(label_indexer_type_0_item_type_2_item)

                    else:
                        label_indexer_type_0_item = label_indexer_type_0_item_data

                    label_indexer.append(label_indexer_type_0_item)

        elif isinstance(self.label_indexer, list):
            label_indexer = UNSET
            if not isinstance(self.label_indexer, Unset):
                label_indexer = []
                for label_indexer_type_1_item_data in self.label_indexer:
                    label_indexer_type_1_item = None

                    label_indexer.append(label_indexer_type_1_item)

        else:
            label_indexer = self.label_indexer

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "type": type,
                "upstream_node": upstream_node,
                "group_name": group_name,
            }
        )
        if output_index is not UNSET:
            field_dict["output_index"] = output_index
        if label_indexer is not UNSET:
            field_dict["label_indexer"] = label_indexer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = InputCreateObject(d.pop("object"))

        type = InputCreateType(d.pop("type"))

        upstream_node = d.pop("upstream_node")

        group_name = d.pop("group_name")

        output_index = d.pop("output_index", UNSET)

        def _parse_label_indexer(
            data: object,
        ) -> Union[List[None], List[Union[List[None], int, str]], None, Unset, int, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                label_indexer_type_0 = UNSET
                _label_indexer_type_0 = data
                for label_indexer_type_0_item_data in _label_indexer_type_0 or []:

                    def _parse_label_indexer_type_0_item(data: object) -> Union[List[None], int, str]:
                        try:
                            if not isinstance(data, list):
                                raise TypeError()
                            label_indexer_type_0_item_type_2 = UNSET
                            _label_indexer_type_0_item_type_2 = data
                            for label_indexer_type_0_item_type_2_item_data in _label_indexer_type_0_item_type_2:
                                label_indexer_type_0_item_type_2_item = None

                                label_indexer_type_0_item_type_2.append(label_indexer_type_0_item_type_2_item)

                            return label_indexer_type_0_item_type_2
                        except:  # noqa: E722
                            pass
                        return cast(Union[List[None], int, str], data)

                    label_indexer_type_0_item = _parse_label_indexer_type_0_item(label_indexer_type_0_item_data)

                    label_indexer_type_0.append(label_indexer_type_0_item)

                return label_indexer_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                label_indexer_type_1 = UNSET
                _label_indexer_type_1 = data
                for label_indexer_type_1_item_data in _label_indexer_type_1 or []:
                    label_indexer_type_1_item = None

                    label_indexer_type_1.append(label_indexer_type_1_item)

                return label_indexer_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[None], List[Union[List[None], int, str]], None, Unset, int, str], data)

        label_indexer = _parse_label_indexer(d.pop("label_indexer", UNSET))

        input_create = cls(
            object_=object_,
            type=type,
            upstream_node=upstream_node,
            group_name=group_name,
            output_index=output_index,
            label_indexer=label_indexer,
        )

        return input_create
