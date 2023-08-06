from typing import Any, Dict, Type, TypeVar

import attr

from ..models.input_specs_schema_get_input_specs_schema import InputSpecsSchemaGetInputSpecsSchema

T = TypeVar("T", bound="InputSpecsSchemaGet")


@attr.s(auto_attribs=True)
class InputSpecsSchemaGet:
    """Schema for node input spec schema responses."""

    input_specs_schema: InputSpecsSchemaGetInputSpecsSchema

    def to_dict(self) -> Dict[str, Any]:
        input_specs_schema = self.input_specs_schema.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "input_specs_schema": input_specs_schema,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        input_specs_schema = InputSpecsSchemaGetInputSpecsSchema.from_dict(d.pop("input_specs_schema"))

        input_specs_schema_get = cls(
            input_specs_schema=input_specs_schema,
        )

        return input_specs_schema_get
