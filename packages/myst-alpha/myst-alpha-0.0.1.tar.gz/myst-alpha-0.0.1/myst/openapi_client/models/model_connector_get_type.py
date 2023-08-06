from enum import Enum


class ModelConnectorGetType(str, Enum):
    MODELCONNECTOR = "ModelConnector"

    def __str__(self) -> str:
        return str(self.value)
