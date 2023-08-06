import json
import os
import pathlib
import tempfile
import unittest
from typing import Generator
from unittest import mock

import google.oauth2.credentials
import pytest

from myst.user_credentials_cache import UserCredentialsCache


@pytest.fixture
def credentials_cache() -> Generator[UserCredentialsCache, None, None]:
    with tempfile.TemporaryDirectory() as tempdir:
        with mock.patch.object(UserCredentialsCache, "cache_file_dir", new_callable=mock.PropertyMock) as mock_path:
            mock_path.return_value = pathlib.Path(tempdir)

            cache = UserCredentialsCache()
            yield cache


def test_credentials_cache_load(credentials_cache: UserCredentialsCache):
    # Write a mock user credentials to load.
    credentials_cache.cache_file_path.parent.mkdir()
    with credentials_cache.cache_file_path.open("w+") as temp_user_credentials_file:
        mock_user_credentials_json = {
            "refresh_token": "mock_refresh_token",
            "id_token": "mock_id_token",
            "token_uri": "mock_token_uri",
            "client_id": "mock_client_id",
            "client_secret": "mock_client_secret",
            "scopes": ["mock_scope"],
        }
        json.dump(mock_user_credentials_json, temp_user_credentials_file)

    user_credentials = credentials_cache.load()

    # Test that the user credentials was loaded as expected.
    assert isinstance(user_credentials, google.oauth2.credentials.Credentials)
    assert user_credentials.refresh_token == "mock_refresh_token"
    assert user_credentials.id_token == "mock_id_token"
    assert user_credentials.token_uri == "mock_token_uri"
    assert user_credentials.client_id == "mock_client_id"
    assert user_credentials.client_secret == "mock_client_secret"
    assert user_credentials.scopes == ["mock_scope"]


def test_credentials_cache_save(credentials_cache: UserCredentialsCache):
    """make sure saving google credentials works"""
    # Create a mock user credentials object to test with.
    user_credentials = google.oauth2.credentials.Credentials(
        token=None,
        refresh_token="mock_refresh_token",
        id_token="mock_id_token",
        token_uri="mock_token_uri",
        client_id="mock_client_id",
        client_secret="mock_client_secret",
        scopes=["mock_scope"],
    )

    # file should not exist
    assert credentials_cache.cache_file_path.exists() is False

    credentials_cache.save(user_credentials=user_credentials)

    # saving created the file
    assert credentials_cache.cache_file_path.exists()

    # Test that the contents of the user credentials were written as expected.
    with credentials_cache.cache_file_path.open("r") as creds_file:
        user_credentials_json = json.load(creds_file)
        assert user_credentials_json == {
            "refresh_token": "mock_refresh_token",
            "id_token": "mock_id_token",
            "token_uri": "mock_token_uri",
            "client_id": "mock_client_id",
            "client_secret": "mock_client_secret",
            "scopes": ["mock_scope"],
        }
