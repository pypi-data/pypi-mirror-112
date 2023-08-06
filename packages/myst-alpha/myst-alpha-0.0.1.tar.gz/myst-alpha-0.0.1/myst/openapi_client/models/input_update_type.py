from enum import Enum


class InputUpdateType(str, Enum):
    INPUT = "Input"

    def __str__(self) -> str:
        return str(self.value)
