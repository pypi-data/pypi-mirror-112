from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.absolute_timing_get import AbsoluteTimingGet
from ..models.layer_get_object import LayerGetObject
from ..models.layer_get_type import LayerGetType
from ..models.relative_timing_get import RelativeTimingGet
from ..types import UNSET, Unset

T = TypeVar("T", bound="LayerGet")


@attr.s(auto_attribs=True)
class LayerGet:
    """Layer schema for get responses."""

    object_: LayerGetObject
    uuid: str
    create_time: str
    type: LayerGetType
    downstream_node: str
    upstream_node: str
    output_index: int
    order: int
    label_indexer: Union[List[None], List[Union[List[None], int, str]], None, int, str]
    update_time: Union[Unset, str] = UNSET
    start_timing: Union[AbsoluteTimingGet, None, RelativeTimingGet, Unset] = UNSET
    end_timing: Union[AbsoluteTimingGet, None, RelativeTimingGet, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        type = self.type.value

        downstream_node = self.downstream_node
        upstream_node = self.upstream_node
        output_index = self.output_index
        order = self.order
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

        start_timing: Union[Dict[str, Any], None, Unset]
        if isinstance(self.start_timing, Unset):
            start_timing = UNSET
        elif self.start_timing is None:
            start_timing = None
        elif isinstance(self.start_timing, AbsoluteTimingGet):
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
        elif isinstance(self.end_timing, AbsoluteTimingGet):
            end_timing = UNSET
            if not isinstance(self.end_timing, Unset):
                end_timing = self.end_timing.to_dict()

        else:
            end_timing = UNSET
            if not isinstance(self.end_timing, Unset):
                end_timing = self.end_timing.to_dict()

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
                "order": order,
                "label_indexer": label_indexer,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time
        if start_timing is not UNSET:
            field_dict["start_timing"] = start_timing
        if end_timing is not UNSET:
            field_dict["end_timing"] = end_timing

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = LayerGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        type = LayerGetType(d.pop("type"))

        downstream_node = d.pop("downstream_node")

        upstream_node = d.pop("upstream_node")

        output_index = d.pop("output_index")

        order = d.pop("order")

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

        def _parse_start_timing(data: object) -> Union[AbsoluteTimingGet, None, RelativeTimingGet, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _start_timing_type_0 = data
                start_timing_type_0: Union[Unset, AbsoluteTimingGet]
                if isinstance(_start_timing_type_0, Unset):
                    start_timing_type_0 = UNSET
                else:
                    start_timing_type_0 = AbsoluteTimingGet.from_dict(_start_timing_type_0)

                return start_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _start_timing_type_1 = data
            start_timing_type_1: Union[Unset, RelativeTimingGet]
            if isinstance(_start_timing_type_1, Unset):
                start_timing_type_1 = UNSET
            else:
                start_timing_type_1 = RelativeTimingGet.from_dict(_start_timing_type_1)

            return start_timing_type_1

        start_timing = _parse_start_timing(d.pop("start_timing", UNSET))

        def _parse_end_timing(data: object) -> Union[AbsoluteTimingGet, None, RelativeTimingGet, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _end_timing_type_0 = data
                end_timing_type_0: Union[Unset, AbsoluteTimingGet]
                if isinstance(_end_timing_type_0, Unset):
                    end_timing_type_0 = UNSET
                else:
                    end_timing_type_0 = AbsoluteTimingGet.from_dict(_end_timing_type_0)

                return end_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _end_timing_type_1 = data
            end_timing_type_1: Union[Unset, RelativeTimingGet]
            if isinstance(_end_timing_type_1, Unset):
                end_timing_type_1 = UNSET
            else:
                end_timing_type_1 = RelativeTimingGet.from_dict(_end_timing_type_1)

            return end_timing_type_1

        end_timing = _parse_end_timing(d.pop("end_timing", UNSET))

        layer_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            type=type,
            downstream_node=downstream_node,
            upstream_node=upstream_node,
            output_index=output_index,
            order=order,
            update_time=update_time,
            label_indexer=label_indexer,
            start_timing=start_timing,
            end_timing=end_timing,
        )

        return layer_get
