from enum import Enum


class TimeSeriesRunPolicyUpdateType(str, Enum):
    TIMESERIESRUNPOLICY = "TimeSeriesRunPolicy"

    def __str__(self) -> str:
        return str(self.value)
