from enum import Enum


class TimeSeriesRunResultGetObject(str, Enum):
    RESULT = "Result"

    def __str__(self) -> str:
        return str(self.value)
