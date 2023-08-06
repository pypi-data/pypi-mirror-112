from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.absolute_timing_create import AbsoluteTimingCreate
from ..models.layer_update_object import LayerUpdateObject
from ..models.layer_update_type import LayerUpdateType
from ..models.relative_timing_create import RelativeTimingCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="LayerUpdate")


@attr.s(auto_attribs=True)
class LayerUpdate:
    """Layer schema for update requests."""

    object_: Union[Unset, LayerUpdateObject] = UNSET
    uuid: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    update_time: Union[Unset, str] = UNSET
    type: Union[Unset, LayerUpdateType] = UNSET
    downstream_node: Union[Unset, str] = UNSET
    upstream_node: Union[Unset, str] = UNSET
    output_index: Union[Unset, int] = UNSET
    label_indexer: Union[List[None], List[Union[List[None], int, str]], None, Unset, int, str] = UNSET
    order: Union[Unset, int] = UNSET
    start_timing: Union[AbsoluteTimingCreate, None, RelativeTimingCreate, Unset] = UNSET
    end_timing: Union[AbsoluteTimingCreate, None, RelativeTimingCreate, Unset] = UNSET

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

        order = self.order
        start_timing: Union[Dict[str, Any], None, Unset]
        if isinstance(self.start_timing, Unset):
            start_timing = UNSET
        elif self.start_timing is None:
            start_timing = None
        elif isinstance(self.start_timing, AbsoluteTimingCreate):
            start_timing = UNSET
            if not isinstance(self.start_timing, Unset):
                start_timing = self.start_timing.to_dict()

        else:
            start_timing = UNSET
            if not isinstance(self.start_timing, Unset):
                start_timing = self.start_timing.to_dict()

        end_timing: Union[Dict[str, Any], None, Unset]
        if isinstance(self.end_timing, Unset):
            end_timing = UNSET
        elif self.end_timing is None:
            end_timing = None
        elif isinstance(self.end_timing, AbsoluteTimingCreate):
            end_timing = UNSET
            if not isinstance(self.end_timing, Unset):
                end_timing = self.end_timing.to_dict()

        else:
            end_timing = UNSET
            if not isinstance(self.end_timing, Unset):
                end_timing = self.end_timing.to_dict()

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
        if order is not UNSET:
            field_dict["order"] = order
        if start_timing is not UNSET:
            field_dict["start_timing"] = start_timing
        if end_timing is not UNSET:
            field_dict["end_timing"] = end_timing

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _object_ = d.pop("object", UNSET)
        object_: Union[Unset, LayerUpdateObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = LayerUpdateObject(_object_)

        uuid = d.pop("uuid", UNSET)

        create_time = d.pop("create_time", UNSET)

        update_time = d.pop("update_time", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, LayerUpdateType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = LayerUpdateType(_type)

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

        order = d.pop("order", UNSET)

        def _parse_start_timing(data: object) -> Union[AbsoluteTimingCreate, None, RelativeTimingCreate, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _start_timing_type_0 = data
                start_timing_type_0: Union[Unset, AbsoluteTimingCreate]
                if isinstance(_start_timing_type_0, Unset):
                    start_timing_type_0 = UNSET
                else:
                    start_timing_type_0 = AbsoluteTimingCreate.from_dict(_start_timing_type_0)

                return start_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _start_timing_type_1 = data
            start_timing_type_1: Union[Unset, RelativeTimingCreate]
            if isinstance(_start_timing_type_1, Unset):
                start_timing_type_1 = UNSET
            else:
                start_timing_type_1 = RelativeTimingCreate.from_dict(_start_timing_type_1)

            return start_timing_type_1

        start_timing = _parse_start_timing(d.pop("start_timing", UNSET))

        def _parse_end_timing(data: object) -> Union[AbsoluteTimingCreate, None, RelativeTimingCreate, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _end_timing_type_0 = data
                end_timing_type_0: Union[Unset, AbsoluteTimingCreate]
                if isinstance(_end_timing_type_0, Unset):
                    end_timing_type_0 = UNSET
                else:
                    end_timing_type_0 = AbsoluteTimingCreate.from_dict(_end_timing_type_0)

                return end_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _end_timing_type_1 = data
            end_timing_type_1: Union[Unset, RelativeTimingCreate]
            if isinstance(_end_timing_type_1, Unset):
                end_timing_type_1 = UNSET
            else:
                end_timing_type_1 = RelativeTimingCreate.from_dict(_end_timing_type_1)

            return end_timing_type_1

        end_timing = _parse_end_timing(d.pop("end_timing", UNSET))

        layer_update = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            update_time=update_time,
            type=type,
            downstream_node=downstream_node,
            upstream_node=upstream_node,
            output_index=output_index,
            label_indexer=label_indexer,
            order=order,
            start_timing=start_timing,
            end_timing=end_timing,
        )

        return layer_update
