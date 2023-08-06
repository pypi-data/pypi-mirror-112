from enum import Enum


class TimeSeriesQueryResultGetObject(str, Enum):
    RESULT = "Result"

    def __str__(self) -> str:
        return str(self.value)
