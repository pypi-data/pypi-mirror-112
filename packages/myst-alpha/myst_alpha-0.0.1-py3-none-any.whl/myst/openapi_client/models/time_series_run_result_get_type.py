from enum import Enum


class TimeSeriesRunResultGetType(str, Enum):
    TIMESERIESRUNRESULT = "TimeSeriesRunResult"

    def __str__(self) -> str:
        return str(self.value)
