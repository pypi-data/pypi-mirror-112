from enum import Enum


class OperationConnectorGetObject(str, Enum):
    CONNECTOR = "Connector"

    def __str__(self) -> str:
        return str(self.value)
