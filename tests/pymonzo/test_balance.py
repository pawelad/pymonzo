"""Test `pymonzo.balance` module."""
import json

import httpx
import pytest
import respx
from polyfactory.factories.pydantic_factory import ModelFactory
from pytest_mock import MockerFixture

from pymonzo import MonzoAPI
from pymonzo.balance import BalanceResource, MonzoBalance

from .test_accounts import MonzoAccountFactory


class MonzoBalanceFactory(ModelFactory[MonzoBalance]):
    """Factory for `MonzoBalance` schema."""

    # This is undocumented in Monzo API, and doesn't return anything for my account,
    # so I don't know its schema
    local_spend: list = []


@pytest.fixture(scope="module")
def balance_resource(monzo_api: MonzoAPI) -> BalanceResource:
    """Initialize `BalanceResource` resource with `monzo_api` fixture."""
    return BalanceResource(client=monzo_api)


class TestBalanceResource:
    """Test `BalanceResource` class."""

    @pytest.mark.respx(base_url=MonzoAPI.api_url)
    def test_list_respx(
        self,
        mocker: MockerFixture,
        respx_mock: respx.MockRouter,
        balance_resource: BalanceResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        balance = MonzoBalanceFactory.build()

        account = MonzoAccountFactory.build()
        mocked_get_default_account = mocker.patch.object(
            balance_resource.client.accounts,
            "get_default_account",
        )
        mocked_get_default_account.return_value = account

        mocked_route = respx_mock.get(
            "/balance", params={"account_id": account.id}
        ).mock(
            return_value=httpx.Response(
                200,
                # TODO: Change when updating to Pydantic 2
                #   `attachment.model_dump(mode='json')`
                json=json.loads(balance.json()),
            )
        )

        balance_get_response = balance_resource.get()

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        assert isinstance(balance_get_response, MonzoBalance)
        assert balance_get_response == balance
        assert mocked_route.called

        # Explicitly passed account ID
        account_id = "TEST_ACCOUNT_ID"

        mocked_route = respx_mock.get(
            "/balance", params={"account_id": account_id}
        ).mock(
            return_value=httpx.Response(
                200,
                # TODO: Change when updating to Pydantic 2
                #   `attachment.model_dump(mode='json')`
                json=json.loads(balance.json()),
            )
        )

        balance_get_response = balance_resource.get(account_id=account_id)

        mocked_get_default_account.assert_not_called()
        mocked_get_default_account.reset_mock()

        assert isinstance(balance_get_response, MonzoBalance)
        assert balance_get_response == balance
        assert mocked_route.called

    @pytest.mark.vcr()
    def test_list_vcr(self, balance_resource: BalanceResource) -> None:
        """API response is parsed into expected schema."""
        balance = balance_resource.get()

        assert isinstance(balance, MonzoBalance)
