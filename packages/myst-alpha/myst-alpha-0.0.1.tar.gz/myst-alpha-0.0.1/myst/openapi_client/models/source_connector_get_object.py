from enum import Enum


class SourceConnectorGetObject(str, Enum):
    CONNECTOR = "Connector"

    def __str__(self) -> str:
        return str(self.value)
