"""Test `pymonzo.whoami` module."""

import os

import pytest

from pymonzo import MonzoAPI
from pymonzo.whoami import MonzoWhoAmI, WhoAmIResource


@pytest.fixture(scope="module")
def whoami_resource(monzo_api: MonzoAPI) -> WhoAmIResource:
    """Initialize `WhoAmIResource` resource with `monzo_api` fixture."""
    return WhoAmIResource(client=monzo_api)


class TestWhoAmIResource:
    """Test `WhoAmIResource` class."""

    @pytest.mark.vcr()
    @pytest.mark.skipif(
        not bool(os.getenv("VCRPY_ENCRYPTION_KEY")),
        reason="`VCRPY_ENCRYPTION_KEY` is not available on GitHub PRs.",
    )
    def test_whoami_vcr(self, whoami_resource: WhoAmIResource) -> None:
        """API response is parsed into expected schema."""
        whoami = whoami_resource.whoami()

        assert isinstance(whoami, MonzoWhoAmI)
