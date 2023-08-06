from enum import Enum


class TimeSeriesInsertResultGetType(str, Enum):
    TIMESERIESINSERTRESULT = "TimeSeriesInsertResult"

    def __str__(self) -> str:
        return str(self.value)
