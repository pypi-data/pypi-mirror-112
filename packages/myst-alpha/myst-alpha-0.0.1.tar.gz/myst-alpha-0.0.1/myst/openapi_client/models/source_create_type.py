from enum import Enum


class SourceCreateType(str, Enum):
    SOURCE = "Source"

    def __str__(self) -> str:
        return str(self.value)
