from enum import Enum


class TimeSeriesUpdateType(str, Enum):
    TIMESERIES = "TimeSeries"

    def __str__(self) -> str:
        return str(self.value)
