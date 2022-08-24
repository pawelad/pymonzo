"""
pymonzo pytest configuration and utils.
"""
import pytest

from pymonzo import MonzoAPI


@pytest.fixture(scope="session")
def monzo_api() -> MonzoAPI:
    """
    Return a 'MonzoAPI' instance.
    """
    return MonzoAPI(
        client_id="TEST_CLIENT_ID",
        client_secret="TEST_CLIENT_SECRET",
        token={"access_token": "TEST_TOKEN"},
    )
