from enum import Enum


class OperationConnectorGetType(str, Enum):
    OPERATIONCONNECTOR = "OperationConnector"

    def __str__(self) -> str:
        return str(self.value)
