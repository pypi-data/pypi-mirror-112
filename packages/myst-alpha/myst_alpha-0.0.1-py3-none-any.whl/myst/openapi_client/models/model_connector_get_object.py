from enum import Enum


class ModelConnectorGetObject(str, Enum):
    CONNECTOR = "Connector"

    def __str__(self) -> str:
        return str(self.value)
