"""pymonzo pytest configuration and utils."""

import os

import pytest
from dotenv import load_dotenv
from vcr import VCR
from vcrpy_encrypt import BaseEncryptedPersister

from pymonzo import MonzoAPI

load_dotenv()

VCRPY_ENCRYPTION_KEY = os.getenv("VCRPY_ENCRYPTION_KEY", "").encode("UTF-8")


class PyMonzoEncryptedPersister(BaseEncryptedPersister):
    """Custom VCR persister that encrypts cassettes."""

    encryption_key: bytes = VCRPY_ENCRYPTION_KEY


def pytest_recording_configure(config: pytest.Config, vcr: VCR) -> None:
    """Register custom VCR persister that encrypts cassettes."""
    vcr.register_persister(PyMonzoEncryptedPersister)


@pytest.fixture(scope="module")
def monzo_api() -> MonzoAPI:
    """Return a `MonzoAPI` instance."""
    return MonzoAPI(
        client_id="TEST_CLIENT_ID",
        client_secret="TEST_CLIENT_SECRET",  # noqa
        token={"access_token": "TEST_TOKEN"},
    )
