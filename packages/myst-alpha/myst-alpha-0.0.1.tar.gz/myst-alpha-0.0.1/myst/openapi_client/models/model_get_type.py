from enum import Enum


class ModelGetType(str, Enum):
    MODEL = "Model"

    def __str__(self) -> str:
        return str(self.value)
