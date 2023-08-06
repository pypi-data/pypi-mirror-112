from unittest import mock

import pytest

from myst.client import Client
from myst.credentials import Credentials


def test_client():
    client = Client()
    assert client.openapi_client.headers["User-Agent"] == client.user_agent
    assert client.openapi_client.timeout == client.API_TIMEOUT_SEC
    assert not hasattr(client.openapi_client, "token")


def test_auth_client():
    creds = Credentials()
    client = Client(credentials=creds)
    assert client.openapi_client.token == creds.token
