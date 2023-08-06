from enum import Enum


class ModelUpdateType(str, Enum):
    MODEL = "Model"

    def __str__(self) -> str:
        return str(self.value)
