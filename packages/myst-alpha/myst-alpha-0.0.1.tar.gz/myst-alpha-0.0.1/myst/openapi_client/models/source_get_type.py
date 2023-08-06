from enum import Enum


class SourceGetType(str, Enum):
    SOURCE = "Source"

    def __str__(self) -> str:
        return str(self.value)
