from enum import Enum


class OperationCreateType(str, Enum):
    OPERATION = "Operation"

    def __str__(self) -> str:
        return str(self.value)
