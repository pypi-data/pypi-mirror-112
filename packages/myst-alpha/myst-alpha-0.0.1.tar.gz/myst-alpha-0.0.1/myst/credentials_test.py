from unittest import mock

import pytest
from google.oauth2.service_account import IDTokenCredentials
from google_auth_oauthlib.flow import InstalledAppFlow

from myst.credentials import (
    Credentials,
    GoogleConsoleCredentials,
    GoogleServiceAccountCredentials,
)
from myst.settings import PROJECT_ROOT
from myst.user_credentials_cache import UserCredentialsCache

TEST_SERVICE_ACCOUNT_KEY = PROJECT_ROOT / "myst" / "data" / "test_service_account_key.json"


def test_credentials():
    assert isinstance(Credentials().token, str)


def test_service_account_credentials():
    cred = GoogleServiceAccountCredentials(key_file_path=TEST_SERVICE_ACCOUNT_KEY)
    assert isinstance(cred.credentials, IDTokenCredentials)

    with mock.patch.object(
        GoogleServiceAccountCredentials, "credentials", new_callable=mock.PropertyMock
    ) as mock_cred_getter:
        mock_cred_getter.return_value = mock.MagicMock(spec=IDTokenCredentials, autospec=True)

        # Manually set the `.token` property -- it's created by the call to `refresh`.
        mock_cred = cred.credentials
        mock_cred.token = mock.Mock()

        # Try to grab the token.
        cred.token

        # We should have refreshed to get the token.
        mock_cred.refresh.assert_called_once()


@pytest.fixture
def creds_cache():
    """Mock credentials cache.

    We return the instance mock for convenience"""
    with mock.patch("myst.credentials.UserCredentialsCache", autospec=True) as mock_cache:
        yield mock_cache()


def test_console_flow():
    """Make sure we correctly use the InstalledAppsFlow."""
    cred = GoogleConsoleCredentials(use_console=False, use_cache=False)
    assert isinstance(cred.flow, InstalledAppFlow)


def test_flow_options(creds_cache: mock.MagicMock):
    """Make sure we invoke the correct flow method."""

    with mock.patch.object(GoogleConsoleCredentials, "flow", new_callable=mock.PropertyMock) as mock_cred_getter:
        flow = mock.MagicMock(spec=InstalledAppFlow, autospec=True)
        mock_cred_getter.return_value = flow

        # Without console.
        GoogleConsoleCredentials(use_console=False, use_cache=False).get_credentials()

        flow.run_console.assert_not_called()
        flow.run_local_server.assert_called_once()
        flow.reset_mock()

        # With console.
        GoogleConsoleCredentials(use_console=True, use_cache=False).get_credentials()

        flow.run_console.assert_called_once()
        flow.run_local_server.assert_not_called()
        flow.reset_mock()

        creds_cache.save.assert_not_called()
        creds_cache.reset_mock()

        # With console, trying to use cache, but cache is not set.
        creds_cache.load.return_value = False
        GoogleConsoleCredentials(use_console=True, use_cache=True).get_credentials()

        flow.run_console.assert_called_once()
        flow.run_local_server.assert_not_called()
        flow.reset_mock()

        creds_cache.save.assert_called_once()
        creds_cache.reset_mock()

        # With console, trying to use cache, but cache is set correctly.
        creds_cache.load.return_value = True
        GoogleConsoleCredentials(use_console=True, use_cache=True).get_credentials()

        flow.run_console.assert_not_called()
        flow.run_local_server.assert_not_called()
        flow.reset_mock()

        creds_cache.save.assert_not_called()
        creds_cache.reset_mock()
