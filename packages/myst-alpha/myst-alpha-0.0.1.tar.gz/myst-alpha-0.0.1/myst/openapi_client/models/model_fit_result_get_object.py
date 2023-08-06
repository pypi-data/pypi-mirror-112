from enum import Enum


class ModelFitResultGetObject(str, Enum):
    RESULT = "Result"

    def __str__(self) -> str:
        return str(self.value)
