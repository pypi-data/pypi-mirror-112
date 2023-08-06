from enum import Enum


class OperationUpdateType(str, Enum):
    OPERATION = "Operation"

    def __str__(self) -> str:
        return str(self.value)
