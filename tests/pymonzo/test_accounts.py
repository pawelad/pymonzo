"""
Test 'pymonzo.accounts' package.
"""
import pytest

from pymonzo import MonzoAPI
from pymonzo.accounts import AccountsResource, MonzoAccount
from pymonzo.exceptions import CannotDetermineDefaultAccount


@pytest.fixture(scope="module")
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
    def test_get_default_account(self, accounts_resource: AccountsResource) -> None:
        """
        Account is presented as default if there is only one (or one active) account.

        TODO: This probably needs a better (mocking?) testing approach
        """
        # Two accounts, one active
        default_account = accounts_resource.get_default_account()

        assert default_account.id == "acc_00009superSecretAccountID2"
        assert default_account.closed is False

        # Two accounts, none active
        for account in accounts_resource._cached_accounts:
            account.closed = True

        with pytest.raises(CannotDetermineDefaultAccount):
            accounts_resource.get_default_account()

        # One, non-active accounts
        accounts_resource._cached_accounts = accounts_resource._cached_accounts[:1]
        default_account = accounts_resource.get_default_account()

        assert default_account.id == "acc_00009superSecretAccountID1"
        assert default_account.closed is True

    @pytest.mark.vcr
    def test_list(self, accounts_resource: AccountsResource) -> None:
        """
        API response is parsed into expected schema.
        """
        accounts_list = accounts_resource.list()

        assert isinstance(accounts_list, list)

        for account in accounts_list:
            assert isinstance(account, MonzoAccount)
