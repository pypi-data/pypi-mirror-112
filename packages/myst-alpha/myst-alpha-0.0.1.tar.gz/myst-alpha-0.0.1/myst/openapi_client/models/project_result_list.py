from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.model_fit_result_get import ModelFitResultGet
from ..models.model_run_result_get import ModelRunResultGet
from ..models.operation_run_result_get import OperationRunResultGet
from ..models.source_run_result_get import SourceRunResultGet
from ..models.time_series_insert_result_get import TimeSeriesInsertResultGet
from ..models.time_series_run_result_get import TimeSeriesRunResultGet

T = TypeVar("T", bound="ProjectResultList")


@attr.s(auto_attribs=True)
class ProjectResultList:
    """Project result list schema."""

    data: List[
        Union[
            ModelFitResultGet,
            ModelRunResultGet,
            OperationRunResultGet,
            SourceRunResultGet,
            TimeSeriesInsertResultGet,
            TimeSeriesRunResultGet,
        ]
    ]
    has_more: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = []
        for data_item_data in self.data:
            if isinstance(data_item_data, SourceRunResultGet):
                data_item = data_item_data.to_dict()

            elif isinstance(data_item_data, ModelRunResultGet):
                data_item = data_item_data.to_dict()

            elif isinstance(data_item_data, OperationRunResultGet):
                data_item = data_item_data.to_dict()

            elif isinstance(data_item_data, TimeSeriesRunResultGet):
                data_item = data_item_data.to_dict()

            elif isinstance(data_item_data, TimeSeriesInsertResultGet):
                data_item = data_item_data.to_dict()

            else:
                data_item = data_item_data.to_dict()

            data.append(data_item)

        has_more = self.has_more

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "has_more": has_more,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = []
        _data = d.pop("data")
        for data_item_data in _data:

            def _parse_data_item(
                data: object,
            ) -> Union[
                ModelFitResultGet,
                ModelRunResultGet,
                OperationRunResultGet,
                SourceRunResultGet,
                TimeSeriesInsertResultGet,
                TimeSeriesRunResultGet,
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    data_item_type_0 = SourceRunResultGet.from_dict(data)

                    return data_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    data_item_type_1 = ModelRunResultGet.from_dict(data)

                    return data_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    data_item_type_2 = OperationRunResultGet.from_dict(data)

                    return data_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    data_item_type_3 = TimeSeriesRunResultGet.from_dict(data)

                    return data_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    data_item_type_4 = TimeSeriesInsertResultGet.from_dict(data)

                    return data_item_type_4
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                data_item_type_5 = ModelFitResultGet.from_dict(data)

                return data_item_type_5

            data_item = _parse_data_item(data_item_data)

            data.append(data_item)

        has_more = d.pop("has_more")

        project_result_list = cls(
            data=data,
            has_more=has_more,
        )

        project_result_list.additional_properties = d
        return project_result_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
