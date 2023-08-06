from enum import Enum


class TimeSeriesGetType(str, Enum):
    TIMESERIES = "TimeSeries"

    def __str__(self) -> str:
        return str(self.value)
