from enum import Enum


class RelativeTimingCreateType(str, Enum):
    RELATIVETIMING = "RelativeTiming"

    def __str__(self) -> str:
        return str(self.value)
