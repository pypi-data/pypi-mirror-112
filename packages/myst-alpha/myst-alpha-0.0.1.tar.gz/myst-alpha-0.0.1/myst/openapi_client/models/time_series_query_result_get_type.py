from enum import Enum


class TimeSeriesQueryResultGetType(str, Enum):
    TIMESERIESQUERYRESULT = "TimeSeriesQueryResult"

    def __str__(self) -> str:
        return str(self.value)
