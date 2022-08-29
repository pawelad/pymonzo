"""
Test 'pymonzo.balance' package.
"""
import pytest

from pymonzo import MonzoAPI
from pymonzo.balance import BalanceResource, MonzoBalance


@pytest.fixture(scope="module")
def balance_resource(monzo_api: MonzoAPI) -> BalanceResource:
    """
    Return a 'BalanceResource' instance.
    """
    return BalanceResource(client=monzo_api)


class TestBalanceResource:
    """
    Test 'balance.BalanceResource' class.
    """

    @pytest.mark.vcr
    def test_list(self, balance_resource: BalanceResource) -> None:
        """
        API response is parsed into expected schema.
        """
        balance = balance_resource.get()

        assert isinstance(balance, MonzoBalance)
