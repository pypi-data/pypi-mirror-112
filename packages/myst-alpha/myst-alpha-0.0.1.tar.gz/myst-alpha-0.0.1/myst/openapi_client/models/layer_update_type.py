from enum import Enum


class LayerUpdateType(str, Enum):
    LAYER = "Layer"

    def __str__(self) -> str:
        return str(self.value)
