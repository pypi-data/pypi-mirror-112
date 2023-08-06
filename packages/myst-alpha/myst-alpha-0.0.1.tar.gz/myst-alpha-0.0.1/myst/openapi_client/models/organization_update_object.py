from enum import Enum


class OrganizationUpdateObject(str, Enum):
    ORGANIZATION = "Organization"

    def __str__(self) -> str:
        return str(self.value)
