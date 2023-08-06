from enum import Enum


class OperationRunResultGetType(str, Enum):
    OPERATIONRUNRESULT = "OperationRunResult"

    def __str__(self) -> str:
        return str(self.value)
