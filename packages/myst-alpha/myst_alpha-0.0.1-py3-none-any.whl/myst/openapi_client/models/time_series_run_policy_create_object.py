from enum import Enum


class TimeSeriesRunPolicyCreateObject(str, Enum):
    POLICY = "Policy"

    def __str__(self) -> str:
        return str(self.value)
