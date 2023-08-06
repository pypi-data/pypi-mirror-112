import pathlib
from datetime import datetime
from typing import Callable, Dict, Optional

from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials as GoogleCredentials
from google.oauth2.service_account import IDTokenCredentials
from google_auth_oauthlib.flow import InstalledAppFlow

from myst.settings import PROJECT_ROOT, Settings
from myst.user_credentials_cache import UserCredentialsCache


class Credentials:
    """Abstraction around various types of credentials which enable use of the Myst API."""

    @property
    def token(self) -> str:
        """Validated Bearer token using these credentials."""
        return "invalid-bearer-token"


class GoogleServiceAccountCredentials(Credentials):
    """Credentials that use a service account.

    Api docs are here:
    https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html
    """

    def __init__(self, key_file_path: Optional[pathlib.Path] = None):
        super().__init__()
        if key_file_path is None:
            key_file_path = Settings().MYST_APPLICATION_CREDENTIALS

        self.key_file_path = key_file_path

    @property
    def credentials(self) -> IDTokenCredentials:
        """The validated credential created from the specified key file."""
        if not hasattr(self, "_credential"):
            credentials = IDTokenCredentials.from_service_account_file(self.key_file_path, target_audience=None)
            self._credentials = credentials

        return self._credentials

    @property
    def token(self) -> str:
        """Validated Bearer token using these credentials"""
        expiry: Optional[datetime] = getattr(self.credentials, "expiry", None)

        # TODO: Check if expiry time is before `now()` and call `refresh()` again.
        if not expiry:
            self.credentials.refresh(GoogleRequest())

        return self.credentials.token


class GoogleConsoleCredentials(Credentials):
    """Credentials created by sending the user through a local OAuth flow.

    Api docs are here:
    https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html
    """

    CLIENT_SECRET_FILE = PROJECT_ROOT / "myst" / "data" / "google_oauth_client_not_so_secret.json"

    def __init__(self, use_console=False, use_cache=True):
        super().__init__()
        self.use_console = use_console
        self.use_cache = use_cache

    @property
    def flow(self) -> InstalledAppFlow:
        """Flow using correct client secrets and scopes."""
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file=self.CLIENT_SECRET_FILE,
            scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"],
        )

        return flow

    def get_credentials(self) -> GoogleCredentials:
        """Obtains credentials via cache or oauth flow."""
        user_credentials_cache = UserCredentialsCache()

        # Note that this will also return `None` if user credentials were not found or couldn't be loaded from cache.
        user_credentials = user_credentials_cache.load() if self.use_cache else None

        if user_credentials:
            return user_credentials

        # Couldn't find user credentials in cache or explicitly told not to use cache, so perform the OAuth2.0 dance.
        user_credentials = self.flow.run_console() if self.use_console else self.flow.run_local_server()

        # Write newly fetched user credentials to cache.
        if self.use_cache:
            user_credentials_cache.save(user_credentials=user_credentials)

        return user_credentials

    @property
    def credentials(self) -> GoogleCredentials:
        """Credentials using the account of the user invoking the program."""
        if not hasattr(self, "_credentials"):
            self._credentials = self.get_credentials()
        return self._credentials

    @property
    def token(self) -> str:
        """Validated Bearer token using these credentials."""
        if not self.credentials.valid:
            self.credentials.refresh(GoogleRequest())
        return self.credentials.id_token
