from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.absolute_timing_create import AbsoluteTimingCreate
from ..models.model_fit_policy_create_object import ModelFitPolicyCreateObject
from ..models.model_fit_policy_create_type import ModelFitPolicyCreateType
from ..models.relative_timing_create import RelativeTimingCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelFitPolicyCreate")


@attr.s(auto_attribs=True)
class ModelFitPolicyCreate:
    """Model fit policy schema for create requests."""

    object_: ModelFitPolicyCreateObject
    type: ModelFitPolicyCreateType
    schedule_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    start_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    end_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    active: Union[Unset, bool] = True

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.value

        type = self.type.value

        if isinstance(self.schedule_timing, AbsoluteTimingCreate):
            schedule_timing = self.schedule_timing.to_dict()

        else:
            schedule_timing = self.schedule_timing.to_dict()

        if isinstance(self.start_timing, AbsoluteTimingCreate):
            start_timing = self.start_timing.to_dict()

        else:
            start_timing = self.start_timing.to_dict()

        if isinstance(self.end_timing, AbsoluteTimingCreate):
            end_timing = self.end_timing.to_dict()

        else:
            end_timing = self.end_timing.to_dict()

        active = self.active

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "object": object_,
                "type": type,
                "schedule_timing": schedule_timing,
                "start_timing": start_timing,
                "end_timing": end_timing,
            }
        )
        if active is not UNSET:
            field_dict["active"] = active

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        object_ = ModelFitPolicyCreateObject(d.pop("object"))

        type = ModelFitPolicyCreateType(d.pop("type"))

        def _parse_schedule_timing(data: object) -> Union[AbsoluteTimingCreate, RelativeTimingCreate]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                schedule_timing_type_0 = AbsoluteTimingCreate.from_dict(data)

                return schedule_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            schedule_timing_type_1 = RelativeTimingCreate.from_dict(data)

            return schedule_timing_type_1

        schedule_timing = _parse_schedule_timing(d.pop("schedule_timing"))

        def _parse_start_timing(data: object) -> Union[AbsoluteTimingCreate, RelativeTimingCreate]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                start_timing_type_0 = AbsoluteTimingCreate.from_dict(data)

                return start_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            start_timing_type_1 = RelativeTimingCreate.from_dict(data)

            return start_timing_type_1

        start_timing = _parse_start_timing(d.pop("start_timing"))

        def _parse_end_timing(data: object) -> Union[AbsoluteTimingCreate, RelativeTimingCreate]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                end_timing_type_0 = AbsoluteTimingCreate.from_dict(data)

                return end_timing_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            end_timing_type_1 = RelativeTimingCreate.from_dict(data)

            return end_timing_type_1

        end_timing = _parse_end_timing(d.pop("end_timing"))

        active = d.pop("active", UNSET)

        model_fit_policy_create = cls(
            object_=object_,
            type=type,
            schedule_timing=schedule_timing,
            start_timing=start_timing,
            end_timing=end_timing,
            active=active,
        )

        return model_fit_policy_create
