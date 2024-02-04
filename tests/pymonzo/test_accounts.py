"""Test `pymonzo.accounts` module."""

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory
from pytest_mock import MockerFixture

from pymonzo import MonzoAPI
from pymonzo.accounts import AccountsResource, MonzoAccount
from pymonzo.exceptions import CannotDetermineDefaultAccount


class MonzoAccountFactory(ModelFactory[MonzoAccount]):
    """Factory for `MonzoAccount` schema."""


@pytest.fixture(scope="module")
def accounts_resource(monzo_api: MonzoAPI) -> AccountsResource:
    """Initialize `AccountsResource` resource with `monzo_api` fixture."""
    return AccountsResource(client=monzo_api)


class TestAccountsResource:
    """Test `AccountsResource` class."""

    def test_get_default_account(
        self,
        mocker: MockerFixture,
        accounts_resource: AccountsResource,
    ) -> None:
        """Account is presented as default if there is only one (active) account."""
        # Mock `.list()` method
        mocked_accounts_list = mocker.patch.object(accounts_resource, "list")

        active_account1 = MonzoAccountFactory.build(closed=False)
        active_account2 = MonzoAccountFactory.build(closed=False)

        closed_account1 = MonzoAccountFactory.build(closed=True)
        closed_account2 = MonzoAccountFactory.build(closed=True)

        # No accounts
        mocked_accounts_list.return_value = []

        with pytest.raises(CannotDetermineDefaultAccount):
            accounts_resource.get_default_account()

        mocked_accounts_list.assert_called_once_with()
        mocked_accounts_list.reset_mock()

        # One account, none active
        mocked_accounts_list.return_value = [closed_account1]

        default_account = accounts_resource.get_default_account()

        mocked_accounts_list.assert_called_once_with()
        mocked_accounts_list.reset_mock()

        assert default_account == closed_account1
        assert default_account.id == closed_account1.id
        assert default_account.closed is True

        # One account, one active
        mocked_accounts_list.return_value = [active_account1]

        default_account = accounts_resource.get_default_account()

        mocked_accounts_list.assert_called_once_with()
        mocked_accounts_list.reset_mock()

        assert default_account == active_account1
        assert default_account.id == active_account1.id
        assert default_account.closed is False

        # Two accounts, none active
        mocked_accounts_list.return_value = [closed_account1, closed_account2]

        with pytest.raises(CannotDetermineDefaultAccount):
            accounts_resource.get_default_account()

        mocked_accounts_list.assert_called_once_with()
        mocked_accounts_list.reset_mock()

        # Two accounts, one active
        mocked_accounts_list.return_value = [closed_account1, active_account1]

        default_account = accounts_resource.get_default_account()

        mocked_accounts_list.assert_called_once_with()
        mocked_accounts_list.reset_mock()

        assert default_account == active_account1
        assert default_account.id == active_account1.id
        assert default_account.closed is False

        # Two accounts, two active
        mocked_accounts_list.return_value = [active_account1, active_account2]

        with pytest.raises(CannotDetermineDefaultAccount):
            accounts_resource.get_default_account()

        mocked_accounts_list.assert_called_once_with()
        mocked_accounts_list.reset_mock()

    @pytest.mark.vcr()
    def test_list_vcr(
        self,
        mocker: MockerFixture,
        accounts_resource: AccountsResource,
    ) -> None:
        """API response is parsed into expected schema."""
        assert accounts_resource._cached_accounts == []
        _get_response_spy = mocker.spy(accounts_resource, "_get_response")

        accounts_list = accounts_resource.list()

        _get_response_spy.assert_called_once()
        _get_response_spy.reset_mock()

        assert isinstance(accounts_list, list)

        for account in accounts_list:
            assert isinstance(account, MonzoAccount)

        # Check that response was cached
        assert accounts_resource._cached_accounts == accounts_list

        accounts_list2 = accounts_resource.list()

        _get_response_spy.assert_not_called()
        _get_response_spy.reset_mock()

        assert accounts_list2 is accounts_list

        # Using `refresh` should force using cache reload
        accounts_list3 = accounts_resource.list(refresh=True)

        _get_response_spy.assert_called_once()
        _get_response_spy.reset_mock()

        assert accounts_list3 == accounts_list

        assert isinstance(accounts_list3, list)

        for account in accounts_list3:
            assert isinstance(account, MonzoAccount)
