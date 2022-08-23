"""
Test 'pymonzo.accounts' package.
"""
import pytest

from pymonzo import MonzoAPI
from pymonzo.accounts import AccountsResource, MonzoAccount


@pytest.fixture(scope="session")
def accounts_resource(monzo_api: MonzoAPI) -> AccountsResource:
    """
    Return a 'AccountsResource' instance.
    """
    return AccountsResource(client=monzo_api)


class TestAccountsResource:
    """
    Test 'accounts.AccountsResource' class.
    """

    @pytest.mark.vcr
    def test_get_default_account(self) -> None:
        pass

    @pytest.mark.vcr
    def test_list(self, accounts_resource: AccountsResource) -> None:
        """
        API response is parsed into expected schema.
        """
        accounts_list = accounts_resource.list()

        assert isinstance(accounts_list, list)

        for account in accounts_list:
            assert isinstance(account, MonzoAccount)
