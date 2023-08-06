from enum import Enum


class InputCreateType(str, Enum):
    INPUT = "Input"

    def __str__(self) -> str:
        return str(self.value)
