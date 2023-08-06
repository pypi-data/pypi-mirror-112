from enum import Enum


class LayerCreateType(str, Enum):
    LAYER = "Layer"

    def __str__(self) -> str:
        return str(self.value)
