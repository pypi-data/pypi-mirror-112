from enum import Enum


class ModelCreateType(str, Enum):
    MODEL = "Model"

    def __str__(self) -> str:
        return str(self.value)
