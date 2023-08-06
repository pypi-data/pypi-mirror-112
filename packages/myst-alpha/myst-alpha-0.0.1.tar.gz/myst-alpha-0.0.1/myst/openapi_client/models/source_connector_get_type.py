from enum import Enum


class SourceConnectorGetType(str, Enum):
    SOURCECONNECTOR = "SourceConnector"

    def __str__(self) -> str:
        return str(self.value)
