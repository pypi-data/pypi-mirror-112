from enum import Enum


class SourceGetObject(str, Enum):
    NODE = "Node"

    def __str__(self) -> str:
        return str(self.value)
