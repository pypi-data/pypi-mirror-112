from enum import Enum


class ModelFitResultGetType(str, Enum):
    MODELFITRESULT = "ModelFitResult"

    def __str__(self) -> str:
        return str(self.value)
