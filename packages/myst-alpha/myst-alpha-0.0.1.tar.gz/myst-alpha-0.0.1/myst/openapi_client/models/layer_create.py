from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.absolute_timing_create import AbsoluteTimingCreate
from ..models.layer_create_object import LayerCreateObject
from ..models.layer_create_type import LayerCreateType
from ..models.relative_timing_create import RelativeTimingCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="LayerCreate")


@attr.s(auto_attribs=True)
class LayerCreate:
    """Layer schema for create requests."""

    object_: LayerCreateObject
    type: LayerCreateType
    upstream_node: str
    order: int
    output_index: Union[Unset, int] = 0
    label_indexer: Union[List[None], List[Union[List[None], int, str]], None, Unset, int, str] = UNSET
    start_timing: Union[AbsoluteTimingCreate, None, RelativeTimingCreate, Unset] = UNSET
    end_timing: Union[AbsoluteTimingCreate, None, RelativeTimingCreate, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        type = self.type.value

        upstream_node = self.upstream_node
        order = self.order
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
        field_dict.update(
            {
                "object": object_,
                "type": type,
                "upstream_node": upstream_node,
                "order": order,
            }
        )
        if output_index is not UNSET:
            field_dict["output_index"] = output_index
        if label_indexer is not UNSET:
            field_dict["label_indexer"] = label_indexer
        if start_timing is not UNSET:
            field_dict["start_timing"] = start_timing
        if end_timing is not UNSET:
            field_dict["end_timing"] = end_timing

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = LayerCreateObject(d.pop("object"))

        type = LayerCreateType(d.pop("type"))

        upstream_node = d.pop("upstream_node")

        order = d.pop("order")

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

        layer_create = cls(
            object_=object_,
            type=type,
            upstream_node=upstream_node,
            order=order,
            output_index=output_index,
            label_indexer=label_indexer,
            start_timing=start_timing,
            end_timing=end_timing,
        )

        return layer_create
