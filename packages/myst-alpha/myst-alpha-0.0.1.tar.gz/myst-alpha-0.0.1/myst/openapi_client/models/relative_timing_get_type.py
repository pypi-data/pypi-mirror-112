from enum import Enum


class RelativeTimingGetType(str, Enum):
    RELATIVETIMING = "RelativeTiming"

    def __str__(self) -> str:
        return str(self.value)
