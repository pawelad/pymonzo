"""Test `pymonzo.transactions` module."""

from datetime import datetime

import httpx
import pytest
import respx
from polyfactory.factories.pydantic_factory import ModelFactory
from pytest_mock import MockerFixture

from pymonzo import MonzoAPI
from pymonzo.transactions import (
    MonzoTransaction,
    MonzoTransactionMerchant,
    MonzoTransactionCounterparty,
    TransactionsResource,
)

from .test_accounts import MonzoAccountFactory


class MonzoTransactionFactory(ModelFactory[MonzoTransaction]):
    """Factory for `MonzoTransaction` schema."""


class MonzoTransactionMerchantFactory(ModelFactory[MonzoTransactionMerchant]):
    """Factory for `MonzoTransactionMerchant` schema."""


class MonzoTransactionCounterpartyFactory(ModelFactory[MonzoTransactionCounterparty]):
    """Factory for `MonzoTransactionCounterparty` schema."""


@pytest.fixture(scope="module")
def transactions_resource(monzo_api: MonzoAPI) -> TransactionsResource:
    """Initialize `TransactionsResource` resource with `monzo_api` fixture."""
    return TransactionsResource(client=monzo_api)


class TestTransactionsResource:
    """Test `TransactionsResource` class."""

    def test_get_respx(
        self,
        respx_mock: respx.MockRouter,
        transactions_resource: TransactionsResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        transaction = MonzoTransactionFactory.build(merchant="TEST_MERCHANT", counterparty={})

        mocked_route = respx_mock.get(f"/transactions/{transaction.id}").mock(
            return_value=httpx.Response(
                200,
                json={"transaction": transaction.model_dump(mode="json")},
            )
        )

        transaction_response = transactions_resource.get(transaction.id)

        assert isinstance(transaction_response, MonzoTransaction)
        assert transaction_response == transaction
        assert mocked_route.called

        # Expand merchant
        merchant = MonzoTransactionMerchantFactory.build()
        counterparty = MonzoTransactionCounterpartyFactory.build()
        transaction = MonzoTransactionFactory.build(merchant=merchant, counterparty=counterparty)

        mocked_route = respx_mock.get(
            f"/transactions/{transaction.id}", params={"expand[]": "merchant"}
        ).mock(
            return_value=httpx.Response(
                200,
                json={"transaction": transaction.model_dump(mode="json")},
            )
        )

        transaction_response = transactions_resource.get(
            transaction.id,
            expand_merchant=True,
        )

        assert isinstance(transaction_response, MonzoTransaction)
        assert isinstance(transaction_response.merchant, MonzoTransactionMerchant)
        assert transaction_response.counterparty is None
        assert transaction_response == transaction
        assert mocked_route.called

    def test_annotate_respx(
        self,
        respx_mock: respx.MockRouter,
        transactions_resource: TransactionsResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        transaction = MonzoTransactionFactory.build(merchant="TEST_MERCHANT", counterparty={})
        metadata = {
            "foo": "TEST_FOO",
            "bar": "TEST_BAR",
        }

        mocked_route = respx_mock.patch(
            f"/transactions/{transaction.id}",
            params={
                "metadata[foo]": "TEST_FOO",
                "metadata[bar]": "TEST_BAR",
            },
        ).mock(
            return_value=httpx.Response(
                200,
                json={"transaction": transaction.model_dump(mode="json")},
            )
        )

        transaction_response = transactions_resource.annotate(transaction.id, metadata)

        assert isinstance(transaction_response, MonzoTransaction)
        assert transaction_response == transaction
        assert mocked_route.called

    def test_list_respx(
        self,
        mocker: MockerFixture,
        respx_mock: respx.MockRouter,
        transactions_resource: TransactionsResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        transaction = MonzoTransactionFactory.build(merchant="TEST_MERCHANT", counterparty={})
        transaction2 = MonzoTransactionFactory.build(merchant="TEST_MERCHANT", counterparty={})

        account = MonzoAccountFactory.build()
        mocked_get_default_account = mocker.patch.object(
            transactions_resource.client.accounts,
            "get_default_account",
        )
        mocked_get_default_account.return_value = account

        mocked_route = respx_mock.get(
            "/transactions", params={"account_id": account.id}
        ).mock(
            return_value=httpx.Response(
                200,
                json={
                    "transactions": [
                        transaction.model_dump(mode="json"),
                        transaction2.model_dump(mode="json"),
                    ]
                },
            )
        )

        transactions_list_response = transactions_resource.list()

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        assert isinstance(transactions_list_response, list)
        for item in transactions_list_response:
            assert isinstance(item, MonzoTransaction)
        assert transactions_list_response == [transaction, transaction2]
        assert mocked_route.called

        # Explicitly passed account ID and params
        account_id = "TEST_ACCOUNT_ID"
        since = datetime(2022, 1, 14)
        before = datetime(2022, 1, 14)
        limit = 42

        mocked_route = respx_mock.get(
            "/transactions",
            params={
                "account_id": account_id,
                "since": since.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "before": before.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "limit": "42",
            },
        ).mock(
            return_value=httpx.Response(
                200,
                json={"transactions": [transaction.model_dump(mode="json")]},
            )
        )

        transactions_list_response = transactions_resource.list(
            account_id=account_id,
            since=since,
            before=before,
            limit=limit,
        )

        mocked_get_default_account.assert_not_called()
        mocked_get_default_account.reset_mock()

        assert isinstance(transactions_list_response, list)
        for item in transactions_list_response:
            assert isinstance(item, MonzoTransaction)
        assert transactions_list_response == [transaction]
        assert mocked_route.called
