from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.absolute_timing_get import AbsoluteTimingGet
from ..models.model_fit_policy_get_object import ModelFitPolicyGetObject
from ..models.model_fit_policy_get_type import ModelFitPolicyGetType
from ..models.relative_timing_get import RelativeTimingGet
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelFitPolicyGet")


@attr.s(auto_attribs=True)
class ModelFitPolicyGet:
    """Model fit policy schema for get responses."""

    object_: ModelFitPolicyGetObject
    uuid: str
    create_time: str
    type: ModelFitPolicyGetType
    creator: str
    schedule_timing: Union[AbsoluteTimingGet, RelativeTimingGet]
    active: bool
    node: str
    start_timing: Union[AbsoluteTimingGet, RelativeTimingGet]
    end_timing: Union[AbsoluteTimingGet, RelativeTimingGet]
    update_time: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        uuid = self.uuid
        create_time = self.create_time
        type = self.type.value

        creator = self.creator
        if isinstance(self.schedule_timing, AbsoluteTimingGet):
            schedule_timing = self.schedule_timing.to_dict()

        else:
            schedule_timing = self.schedule_timing.to_dict()

        active = self.active
        node = self.node
        if isinstance(self.start_timing, AbsoluteTimingGet):
            start_timing = self.start_timing.to_dict()

        else:
            start_timing = self.start_timing.to_dict()

        if isinstance(self.end_timing, AbsoluteTimingGet):
            end_timing = self.end_timing.to_dict()

        else:
            end_timing = self.end_timing.to_dict()

        update_time = self.update_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "uuid": uuid,
                "create_time": create_time,
                "type": type,
                "creator": creator,
                "schedule_timing": schedule_timing,
                "active": active,
                "node": node,
                "start_timing": start_timing,
                "end_timing": end_timing,
            }
        )
        if update_time is not UNSET:
            field_dict["update_time"] = update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = ModelFitPolicyGetObject(d.pop("object"))

        uuid = d.pop("uuid")

        create_time = d.pop("create_time")

        type = ModelFitPolicyGetType(d.pop("type"))

        creator = d.pop("creator")

        def _parse_schedule_timing(data: object) -> Union[AbsoluteTimingGet, RelativeTimingGet]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                schedule_timing_type_0 = AbsoluteTimingGet.from_dict(data)

                return schedule_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            schedule_timing_type_1 = RelativeTimingGet.from_dict(data)

            return schedule_timing_type_1

        schedule_timing = _parse_schedule_timing(d.pop("schedule_timing"))

        active = d.pop("active")

        node = d.pop("node")

        def _parse_start_timing(data: object) -> Union[AbsoluteTimingGet, RelativeTimingGet]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                start_timing_type_0 = AbsoluteTimingGet.from_dict(data)

                return start_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            start_timing_type_1 = RelativeTimingGet.from_dict(data)

            return start_timing_type_1

        start_timing = _parse_start_timing(d.pop("start_timing"))

        def _parse_end_timing(data: object) -> Union[AbsoluteTimingGet, RelativeTimingGet]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                end_timing_type_0 = AbsoluteTimingGet.from_dict(data)

                return end_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            end_timing_type_1 = RelativeTimingGet.from_dict(data)

            return end_timing_type_1

        end_timing = _parse_end_timing(d.pop("end_timing"))

        update_time = d.pop("update_time", UNSET)

        model_fit_policy_get = cls(
            object_=object_,
            uuid=uuid,
            create_time=create_time,
            type=type,
            creator=creator,
            schedule_timing=schedule_timing,
            active=active,
            node=node,
            start_timing=start_timing,
            end_timing=end_timing,
            update_time=update_time,
        )

        return model_fit_policy_get
