from enum import Enum


class UserUpdateObject(str, Enum):
    USER = "User"

    def __str__(self) -> str:
        return str(self.value)
