from enum import Enum


class InputGetObject(str, Enum):
    EDGE = "Edge"

    def __str__(self) -> str:
        return str(self.value)
