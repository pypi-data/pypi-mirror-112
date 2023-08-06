from enum import Enum


class SourceUpdateType(str, Enum):
    SOURCE = "Source"

    def __str__(self) -> str:
        return str(self.value)
