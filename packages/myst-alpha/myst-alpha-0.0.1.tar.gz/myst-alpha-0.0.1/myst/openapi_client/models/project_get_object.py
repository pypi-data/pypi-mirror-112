from enum import Enum


class ProjectGetObject(str, Enum):
    PROJECT = "Project"

    def __str__(self) -> str:
        return str(self.value)
