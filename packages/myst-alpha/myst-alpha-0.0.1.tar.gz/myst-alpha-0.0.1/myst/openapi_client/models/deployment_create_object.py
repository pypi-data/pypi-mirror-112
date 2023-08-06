from enum import Enum


class DeploymentCreateObject(str, Enum):
    DEPLOYMENT = "Deployment"

    def __str__(self) -> str:
        return str(self.value)
