from enum import Enum


class TimeSeriesRunPolicyCreateType(str, Enum):
    TIMESERIESRUNPOLICY = "TimeSeriesRunPolicy"

    def __str__(self) -> str:
        return str(self.value)
