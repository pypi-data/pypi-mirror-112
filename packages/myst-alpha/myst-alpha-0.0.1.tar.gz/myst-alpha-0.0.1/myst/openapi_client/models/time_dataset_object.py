from enum import Enum


class TimeDatasetObject(str, Enum):
    TIMEDATASET = "TimeDataset"

    def __str__(self) -> str:
        return str(self.value)
