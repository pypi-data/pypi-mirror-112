from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.time_dataset_spec import TimeDatasetSpec

T = TypeVar("T", bound="OutputSpecsGet")


@attr.s(auto_attribs=True)
class OutputSpecsGet:
    """Schema for node output spec responses."""

    output_specs: List[TimeDatasetSpec]

    def to_dict(self) -> Dict[str, Any]:
        output_specs = []
        for output_specs_item_data in self.output_specs:
            output_specs_item = output_specs_item_data.to_dict()

            output_specs.append(output_specs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "output_specs": output_specs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        output_specs = []
        _output_specs = d.pop("output_specs")
        for output_specs_item_data in _output_specs:
            output_specs_item = TimeDatasetSpec.from_dict(output_specs_item_data)

            output_specs.append(output_specs_item)

        output_specs_get = cls(
            output_specs=output_specs,
        )

        return output_specs_get
