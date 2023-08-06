from enum import Enum


class AbsoluteTimingCreateType(str, Enum):
    ABSOLUTETIMING = "AbsoluteTiming"

    def __str__(self) -> str:
        return str(self.value)
