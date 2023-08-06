from enum import Enum


class RelativeTimingCreateObject(str, Enum):
    TIMING = "Timing"

    def __str__(self) -> str:
        return str(self.value)
