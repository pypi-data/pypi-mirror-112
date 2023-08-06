from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.input_get_object import InputGetObject
from ..models.input_get_type import InputGetType
from ..types import UNSET, Unset

T = TypeVar("T", bound="InputGet")


@attr.s(auto_attribs=True)
class InputGet:
    """Input schema for get responses."""

    object_: InputGetObject
    uuid: str
    create_time: str
    type: InputGetType
    downstream_node: str
    upstream_node: str
    output_index: int
    group_name: str
    label_indexer: Union[List[None], List[Union[List[None], int, str]], None, int, str]
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        type = self.type.value

        downstream_node = self.downstream_node
        upstream_node = self.upstream_node
        output_index = self.output_index
        group_name = self.group_name
        update_time = self.update_time
        label_indexer: Union[List[None], List[Union[List[None], int, str]], None, int, str]
        if self.label_indexer is None:
            label_indexer = None
        elif isinstance(self.label_indexer, list):
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
                "uuid": uuid,
                "create_time": create_time,
                "type": type,
                "downstream_node": downstream_node,
                "upstream_node": upstream_node,
                "output_index": output_index,
                "group_name": group_name,
                "label_indexer": label_indexer,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = InputGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        type = InputGetType(d.pop("type"))

        downstream_node = d.pop("downstream_node")

        upstream_node = d.pop("upstream_node")

        output_index = d.pop("output_index")

        group_name = d.pop("group_name")

        update_time = d.pop("update_time", UNSET)

        def _parse_label_indexer(data: object) -> Union[List[None], List[Union[List[None], int, str]], None, int, str]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                label_indexer_type_0 = UNSET
                _label_indexer_type_0 = data
                for label_indexer_type_0_item_data in _label_indexer_type_0:

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
                for label_indexer_type_1_item_data in _label_indexer_type_1:
                    label_indexer_type_1_item = None

                    label_indexer_type_1.append(label_indexer_type_1_item)

                return label_indexer_type_1
            except:  # noqa: E722
                pass
            return cast(Union[List[None], List[Union[List[None], int, str]], None, int, str], data)

        label_indexer = _parse_label_indexer(d.pop("label_indexer"))

        input_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            type=type,
            downstream_node=downstream_node,
            upstream_node=upstream_node,
            output_index=output_index,
            group_name=group_name,
            update_time=update_time,
            label_indexer=label_indexer,
        )

        return input_get
