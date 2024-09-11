"""Monzo API 'transactions' resource."""

from datetime import datetime
from typing import Dict, List, Optional

from pymonzo.resources import BaseResource
from pymonzo.transactions.schemas import MonzoTransaction


class TransactionsResource(BaseResource):
    """Monzo API 'transactions' resource.

    Note:
        Monzo API docs: https://docs.monzo.com/#transactions
    """

    def get(
        self,
        transaction_id: str,
        *,
        expand_merchant: bool = False,
    ) -> MonzoTransaction:
        """Return single transaction.

        Note:
            Monzo API docs: https://docs.monzo.com/#retrieve-transaction

        Arguments:
            transaction_id: The ID of the transaction.
            expand_merchant: Whether to return expanded merchant information.

        Returns:
            A Monzo transaction.
        """
        endpoint = f"/transactions/{transaction_id}"
        params = {}
        if expand_merchant:
            params["expand[]"] = "merchant"

        response = self._get_response(method="get", endpoint=endpoint, params=params)

        transaction = MonzoTransaction(**response.json()["transaction"])

        return transaction

    def annotate(
        self,
        transaction_id: str,
        metadata: Dict[str, str],
    ) -> MonzoTransaction:
        """Annotate transaction with extra metadata.

        Note:
            Monzo API docs: https://docs.monzo.com/#annotate-transaction

        Arguments:
            transaction_id: The ID of the transaction.
            metadata: Include each key you would like to modify. To delete a key,
                set its value to an empty string.

        Returns:
            Annotated Monzo transaction.
        """
        endpoint = f"/transactions/{transaction_id}"
        data = {f"metadata[{key}]": value for key, value in metadata.items()}

        response = self._get_response(method="patch", endpoint=endpoint, data=data)

        transaction = MonzoTransaction(**response.json()["transaction"])

        return transaction

    def list(
        self,
        account_id: Optional[str] = None,
        *,
        expand_merchant: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> List[MonzoTransaction]:
        """Return a list of account transactions.

        You can only fetch all transactions within 5 minutes of authentication.
        After that, you can query your last 90 days.

        Note:
            Monzo API docs: https://docs.monzo.com/#list-transactions

        Arguments:
            account_id: The ID of the account. Can be omitted if user has only one
                active account.
            expand_merchant: Whether to return expanded merchant information.
            since: Filter transactions by start time.
            before: Filter transactions by end time.
            limit: Limits the number of results per-page. Maximum: 100.

        Returns:
            List of Monzo transactions.

        Raises:
            CannotDetermineDefaultAccount: If no account ID was passed and default
                account cannot be determined.
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        endpoint = "/transactions"
        params = {"account_id": account_id}

        if expand_merchant:
            params["expand[]"] = "merchant"

        if since:
            params["since"] = since.strftime("%Y-%m-%dT%H:%M:%SZ")

        if before:
            params["before"] = before.strftime("%Y-%m-%dT%H:%M:%SZ")

        if limit:
            params["limit"] = str(limit)

        response = self._get_response(method="get", endpoint=endpoint, params=params)

        transactions = [
            MonzoTransaction(**transaction)
            for transaction in response.json()["transactions"]
        ]

        return transactions
