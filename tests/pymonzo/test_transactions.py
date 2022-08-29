"""
Test 'pymonzo.transactions' package.
"""
import pytest

from pymonzo import MonzoAPI
from pymonzo.transactions import MonzoTransaction, TransactionsResource


@pytest.fixture(scope="module")
def transactions_resource(monzo_api: MonzoAPI) -> TransactionsResource:
    """
    Return a 'TransactionsResource' instance.
    """
    return TransactionsResource(client=monzo_api)


@pytest.mark.skip
class TestTransactionsResource:
    """
    Test 'whoami.WhoAmIResource' class.
    """

    @pytest.mark.vcr
    def test_get(self, transactions_resource: TransactionsResource) -> None:
        """
        API response is parsed into expected schema.
        """
        transaction = transactions_resource.get("")

        assert isinstance(transaction, MonzoTransaction)

    @pytest.mark.vcr
    def test_list(self, transactions_resource: TransactionsResource) -> None:
        """
        API response is parsed into expected schema.
        """
        transactions_list = transactions_resource.list()

        assert isinstance(transactions_list, list)

        for transaction in transactions_list:
            assert isinstance(transaction, MonzoTransaction)
