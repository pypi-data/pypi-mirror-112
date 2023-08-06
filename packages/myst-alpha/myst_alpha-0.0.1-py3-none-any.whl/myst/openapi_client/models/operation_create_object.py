from enum import Enum


class OperationCreateObject(str, Enum):
    NODE = "Node"

    def __str__(self) -> str:
        return str(self.value)
