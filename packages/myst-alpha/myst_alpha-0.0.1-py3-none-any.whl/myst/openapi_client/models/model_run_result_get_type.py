from enum import Enum


class ModelRunResultGetType(str, Enum):
    MODELRUNRESULT = "ModelRunResult"

    def __str__(self) -> str:
        return str(self.value)
