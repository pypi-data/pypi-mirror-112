from enum import Enum


class OperationGetObject(str, Enum):
    NODE = "Node"

    def __str__(self) -> str:
        return str(self.value)
