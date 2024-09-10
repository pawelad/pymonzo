"""Test `pymonzo.accounts` module."""

import os

import httpx
import pytest
import respx
from polyfactory.factories.pydantic_factory import ModelFactory
from pytest_mock import MockerFixture

from pymonzo import MonzoAPI
from pymonzo.accounts import (
    AccountsResource,
    MonzoAccount,
    MonzoAccountCurrency,
    MonzoAccountType,
)
from pymonzo.exceptions import CannotDetermineDefaultAccount


class MonzoAccountFactory(ModelFactory[MonzoAccount]):
    """Factory for `MonzoAccount` schema."""


# TODO: What should be resources fixture scope?
#   With `module`, `_cached_accounts` value persisted between functions / tests.
@pytest.fixture()
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

    def test_list_respx(
        self,
        mocker: MockerFixture,
        respx_mock: respx.MockRouter,
        accounts_resource: AccountsResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        account = MonzoAccountFactory.build(payment_details=None)
        # Account `type` and `currency` should be converted to en enum
        account2 = MonzoAccountFactory.build(
            payment_details=None,
            type=MonzoAccountType.UK_RETAIL,
            currency=MonzoAccountCurrency.GBP,
        )
        # Account `type` and `currency` should be taken as in as a string
        account3 = MonzoAccountFactory.build(
            payment_details=None,
            type="TEST_TYPE",
            currency="TEST_CURRENCY",
        )
        # Account `type` should be taken as in as a string, but `currency` should be
        # converted to en enum because of casting priority
        account4 = MonzoAccountFactory.build(
            payment_details=None,
            type="TEST_TYPE",
            currency="GBP",
        )

        mocked_route = respx_mock.get("/accounts").mock(
            return_value=httpx.Response(
                200,
                json={
                    "accounts": [
                        account.model_dump(mode="json"),
                        account2.model_dump(mode="json"),
                        account3.model_dump(mode="json"),
                        account4.model_dump(mode="json"),
                    ]
                },
            )
        )

        accounts_list_response = accounts_resource.list()

        assert isinstance(accounts_list_response, list)
        for item in accounts_list_response:
            assert isinstance(item, MonzoAccount)
        assert accounts_list_response == [account, account2, account3, account4]
        assert mocked_route.called

        assert accounts_list_response[1].type == MonzoAccountType.UK_RETAIL
        assert accounts_list_response[1].currency == MonzoAccountCurrency.GBP

        assert accounts_list_response[2].type == "TEST_TYPE"
        assert accounts_list_response[2].currency == "TEST_CURRENCY"

        assert accounts_list_response[3].type == "TEST_TYPE"
        assert accounts_list_response[3].currency == MonzoAccountCurrency.GBP

    @pytest.mark.vcr()
    @pytest.mark.skipif(
        os.getenv("VCRPY_ENCRYPTION_KEY") is None,
        reason="`VCRPY_ENCRYPTION_KEY` is not available on GitHub PRs.",
    )
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
