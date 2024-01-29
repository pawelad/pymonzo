"""Test `pymonzo.pots` module."""

import pytest

from pymonzo import MonzoAPI
from pymonzo.pots import MonzoPot, PotsResource


@pytest.fixture(scope="module")
def pots_resource(monzo_api: MonzoAPI) -> PotsResource:
    """Initialize `PotsResource` resource with `monzo_api` fixture."""
    return PotsResource(client=monzo_api)


class TestPotsResource:
    """Test `PotsResource` class."""

    @pytest.mark.vcr()
    def test_list(self, pots_resource: PotsResource) -> None:
        """API response is parsed into expected schema."""
        pots_list = pots_resource.list()

        assert isinstance(pots_list, list)

        for pot in pots_list:
            assert isinstance(pot, MonzoPot)
