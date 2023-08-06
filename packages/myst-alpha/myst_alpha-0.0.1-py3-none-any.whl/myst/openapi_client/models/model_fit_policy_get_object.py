from enum import Enum


class ModelFitPolicyGetObject(str, Enum):
    POLICY = "Policy"

    def __str__(self) -> str:
        return str(self.value)
