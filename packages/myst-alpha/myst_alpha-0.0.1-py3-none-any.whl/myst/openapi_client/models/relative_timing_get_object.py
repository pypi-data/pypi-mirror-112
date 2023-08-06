from enum import Enum


class RelativeTimingGetObject(str, Enum):
    TIMING = "Timing"

    def __str__(self) -> str:
        return str(self.value)
