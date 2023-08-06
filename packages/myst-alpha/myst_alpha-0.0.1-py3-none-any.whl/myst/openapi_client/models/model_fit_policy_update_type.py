from enum import Enum


class ModelFitPolicyUpdateType(str, Enum):
    MODELFITPOLICY = "ModelFitPolicy"

    def __str__(self) -> str:
        return str(self.value)
