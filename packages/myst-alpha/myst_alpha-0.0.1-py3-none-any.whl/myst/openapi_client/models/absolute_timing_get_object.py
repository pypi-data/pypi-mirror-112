from enum import Enum


class AbsoluteTimingGetObject(str, Enum):
    TIMING = "Timing"

    def __str__(self) -> str:
        return str(self.value)
