from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.absolute_timing_create import AbsoluteTimingCreate
from ..models.model_fit_policy_update_object import ModelFitPolicyUpdateObject
from ..models.model_fit_policy_update_type import ModelFitPolicyUpdateType
from ..models.relative_timing_create import RelativeTimingCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelFitPolicyUpdate")


@attr.s(auto_attribs=True)
class ModelFitPolicyUpdate:
    """Model fit policy schema for update requests."""

    object_: Union[Unset, ModelFitPolicyUpdateObject] = UNSET
    uuid: Union[Unset, str] = UNSET
    create_time: Union[Unset, str] = UNSET
    update_time: Union[Unset, str] = UNSET
    type: Union[Unset, ModelFitPolicyUpdateType] = UNSET
    creator: Union[Unset, str] = UNSET
    schedule_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate, Unset] = UNSET
    active: Union[Unset, bool] = UNSET
    node: Union[Unset, str] = UNSET
    start_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate, Unset] = UNSET
    end_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate, Unset] = UNSET

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

        creator = self.creator
        schedule_timing: Union[Dict[str, Any], Unset]
        if isinstance(self.schedule_timing, Unset):
            schedule_timing = UNSET
        elif isinstance(self.schedule_timing, AbsoluteTimingCreate):
            schedule_timing = UNSET
            if not isinstance(self.schedule_timing, Unset):
                schedule_timing = self.schedule_timing.to_dict()

        else:
            schedule_timing = UNSET
            if not isinstance(self.schedule_timing, Unset):
                schedule_timing = self.schedule_timing.to_dict()

        active = self.active
        node = self.node
        start_timing: Union[Dict[str, Any], Unset]
        if isinstance(self.start_timing, Unset):
            start_timing = UNSET
        elif isinstance(self.start_timing, AbsoluteTimingCreate):
            start_timing = UNSET
            if not isinstance(self.start_timing, Unset):
                start_timing = self.start_timing.to_dict()

        else:
            start_timing = UNSET
            if not isinstance(self.start_timing, Unset):
                start_timing = self.start_timing.to_dict()

        end_timing: Union[Dict[str, Any], Unset]
        if isinstance(self.end_timing, Unset):
            end_timing = UNSET
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
        if creator is not UNSET:
            field_dict["creator"] = creator
        if schedule_timing is not UNSET:
            field_dict["schedule_timing"] = schedule_timing
        if active is not UNSET:
            field_dict["active"] = active
        if node is not UNSET:
            field_dict["node"] = node
        if start_timing is not UNSET:
            field_dict["start_timing"] = start_timing
        if end_timing is not UNSET:
            field_dict["end_timing"] = end_timing

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _object_ = d.pop("object", UNSET)
        object_: Union[Unset, ModelFitPolicyUpdateObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = ModelFitPolicyUpdateObject(_object_)

        uuid = d.pop("uuid", UNSET)

        create_time = d.pop("create_time", UNSET)

        update_time = d.pop("update_time", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, ModelFitPolicyUpdateType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ModelFitPolicyUpdateType(_type)

        creator = d.pop("creator", UNSET)

        def _parse_schedule_timing(data: object) -> Union[AbsoluteTimingCreate, RelativeTimingCreate, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _schedule_timing_type_0 = data
                schedule_timing_type_0: Union[Unset, AbsoluteTimingCreate]
                if isinstance(_schedule_timing_type_0, Unset):
                    schedule_timing_type_0 = UNSET
                else:
                    schedule_timing_type_0 = AbsoluteTimingCreate.from_dict(_schedule_timing_type_0)

                return schedule_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _schedule_timing_type_1 = data
            schedule_timing_type_1: Union[Unset, RelativeTimingCreate]
            if isinstance(_schedule_timing_type_1, Unset):
                schedule_timing_type_1 = UNSET
            else:
                schedule_timing_type_1 = RelativeTimingCreate.from_dict(_schedule_timing_type_1)

            return schedule_timing_type_1

        schedule_timing = _parse_schedule_timing(d.pop("schedule_timing", UNSET))

        active = d.pop("active", UNSET)

        node = d.pop("node", UNSET)

        def _parse_start_timing(data: object) -> Union[AbsoluteTimingCreate, RelativeTimingCreate, Unset]:
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

        def _parse_end_timing(data: object) -> Union[AbsoluteTimingCreate, RelativeTimingCreate, Unset]:
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

        model_fit_policy_update = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            update_time=update_time,
            type=type,
            creator=creator,
            schedule_timing=schedule_timing,
            active=active,
            node=node,
            start_timing=start_timing,
            end_timing=end_timing,
        )

        return model_fit_policy_update
