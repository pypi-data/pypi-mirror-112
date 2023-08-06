from enum import Enum


class AbsoluteTimingCreateObject(str, Enum):
    TIMING = "Timing"

    def __str__(self) -> str:
        return str(self.value)
