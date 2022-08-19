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
    return MonzoAPI()
