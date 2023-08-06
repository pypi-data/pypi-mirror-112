from enum import Enum


class LayerUpdateObject(str, Enum):
    EDGE = "Edge"

    def __str__(self) -> str:
        return str(self.value)
