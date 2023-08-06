from enum import Enum


class DeploymentGetObject(str, Enum):
    DEPLOYMENT = "Deployment"

    def __str__(self) -> str:
        return str(self.value)
