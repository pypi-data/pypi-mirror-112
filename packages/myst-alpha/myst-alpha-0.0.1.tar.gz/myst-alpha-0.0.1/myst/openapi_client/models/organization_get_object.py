from enum import Enum


class OrganizationGetObject(str, Enum):
    ORGANIZATION = "Organization"

    def __str__(self) -> str:
        return str(self.value)
