from enum import Enum


class UserGetObject(str, Enum):
    USER = "User"

    def __str__(self) -> str:
        return str(self.value)
