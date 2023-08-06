import uuid
from typing import Optional

import httpx
import pytest
from pytest_httpx import HTTPXMock

from myst.client import Client
from myst.credentials import Credentials
from myst.endpoints.users import UserGet
from myst.exceptions import MystAPIError, MystClientError, UnAuthenticatedError
from myst.openapi_client.models.organization_role import OrganizationRole
from myst.openapi_client.models.user_get_object import UserGetObject


@pytest.fixture()
def client(credentials: Optional[Credentials]) -> Client:
    """Client instance used in these tests."""
    return Client(credentials=credentials)


@pytest.fixture()
def endpoint(client: Client):
    """Endpoint we use for testing, picked somewhat-arbitrarily."""
    return client.endpoints.users.get_me


def describe_call_endpoint():
    """Tests for the `call_endpoint` function -- the main dispatcher for all API requests."""

    @pytest.fixture
    def credentials():
        return None

    def raises_unauthenticated_error(endpoint):
        with pytest.raises(UnAuthenticatedError):
            endpoint()

    def describe_with_authenticated_client():
        """Tests a client that's authenticated."""

        @pytest.fixture
        def credentials():
            return Credentials()

        def token_is_used_in_headers(httpx_mock, endpoint):
            # If we don't get a request matching given headers, pytest_httpx
            # will raise an error at teardown RE: not all added responses being
            # returned
            httpx_mock.add_response(
                match_headers={"Authorization": "Bearer invalid-bearer-token"},
            )

            # We expect this test to fail because `expected_request` does not return valid JSON.
            with pytest.raises(MystClientError):
                endpoint()

        def describe_with_valid_json_response():
            @pytest.fixture
            def valid_user() -> UserGet:
                return UserGet(
                    object_=UserGetObject.USER,
                    uuid=str(uuid.uuid4()),
                    create_time="2021-01-01T00:00:00Z",
                    email="test@example.com",
                    organization=str(uuid.uuid4()),
                    organization_role=OrganizationRole.MEMBER,
                )

            def returns_the_user(endpoint, httpx_mock: HTTPXMock, valid_user: UserGet):
                httpx_mock.add_response(json=valid_user.to_dict())

                response = endpoint()
                assert response == valid_user

            def describe_with_error_code_response():
                def returns_api_error(endpoint, httpx_mock: HTTPXMock, valid_user: UserGet):
                    httpx_mock.add_response(json=valid_user.to_dict(), status_code=400)

                    with pytest.raises(MystAPIError):
                        endpoint()
