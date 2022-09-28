"""
Test 'pymonzo.whoami' package.
"""
import pytest

from pymonzo import MonzoAPI
from pymonzo.whoami import MonzoWhoAmI, WhoAmIResource


@pytest.fixture(scope="module")
def whoami_resource(monzo_api: MonzoAPI) -> WhoAmIResource:
    """
    Return a 'WhoAmIResource' instance.
    """
    return WhoAmIResource(client=monzo_api)


class TestWhoAmIResource:
    """
    Test 'whoami.WhoAmIResource' class.
    """

    @pytest.mark.vcr()
    def test_whoami(self, whoami_resource: WhoAmIResource) -> None:
        """
        API response is parsed into expected schema.
        """
        whoami = whoami_resource.whoami()

        assert isinstance(whoami, MonzoWhoAmI)
