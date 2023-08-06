from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.input_update_object import InputUpdateObject
from ..models.input_update_type import InputUpdateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="InputUpdate")


@attr.s(auto_attribs=True)
class InputUpdate:
    """Input schema for update requests."""

    object_: Union[Unset, InputUpdateObject] = UNSET
    uuid: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    update_time: Union[Unset, str] = UNSET
    type: Union[Unset, InputUpdateType] = UNSET
    downstream_node: Union[Unset, str] = UNSET
    upstream_node: Union[Unset, str] = UNSET
    output_index: Union[Unset, int] = UNSET
    label_indexer: Union[List[None], List[Union[List[None], int, str]], None, Unset, int, str] = UNSET
    group_name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_: Union[Unset, str] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        update_time = self.update_time
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        downstream_node = self.downstream_node
        upstream_node = self.upstream_node
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

        group_name = self.group_name

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
        if type is not UNSET:
            field_dict["type"] = type
        if downstream_node is not UNSET:
            field_dict["downstream_node"] = downstream_node
        if upstream_node is not UNSET:
            field_dict["upstream_node"] = upstream_node
        if output_index is not UNSET:
            field_dict["output_index"] = output_index
        if label_indexer is not UNSET:
            field_dict["label_indexer"] = label_indexer
        if group_name is not UNSET:
            field_dict["group_name"] = group_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _object_ = d.pop("object", UNSET)
        object_: Union[Unset, InputUpdateObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = InputUpdateObject(_object_)

        uuid = d.pop("uuid", UNSET)

        create_time = d.pop("create_time", UNSET)

        update_time = d.pop("update_time", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, InputUpdateType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = InputUpdateType(_type)

        downstream_node = d.pop("downstream_node", UNSET)

        upstream_node = d.pop("upstream_node", UNSET)

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

        group_name = d.pop("group_name", UNSET)

        input_update = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            update_time=update_time,
            type=type,
            downstream_node=downstream_node,
            upstream_node=upstream_node,
            output_index=output_index,
            label_indexer=label_indexer,
            group_name=group_name,
        )

        return input_update
