from enum import Enum


class TimeSeriesRunPolicyGetObject(str, Enum):
    POLICY = "Policy"

    def __str__(self) -> str:
        return str(self.value)
