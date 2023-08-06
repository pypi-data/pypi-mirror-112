from enum import Enum


class SourceRunResultGetType(str, Enum):
    SOURCERUNRESULT = "SourceRunResult"

    def __str__(self) -> str:
        return str(self.value)
