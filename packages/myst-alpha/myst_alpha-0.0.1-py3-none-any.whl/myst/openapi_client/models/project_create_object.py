from enum import Enum


class ProjectCreateObject(str, Enum):
    PROJECT = "Project"

    def __str__(self) -> str:
        return str(self.value)
