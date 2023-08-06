from enum import Enum


class AbsoluteTimingGetType(str, Enum):
    ABSOLUTETIMING = "AbsoluteTiming"

    def __str__(self) -> str:
        return str(self.value)
