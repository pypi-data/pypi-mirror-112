from enum import Enum


class OperationGetType(str, Enum):
    OPERATION = "Operation"

    def __str__(self) -> str:
        return str(self.value)
