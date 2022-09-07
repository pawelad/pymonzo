"""
Monzo API transactions resource.
"""
from datetime import datetime
from typing import Dict, List, Optional

from pymonzo.resources import BaseResource
from pymonzo.transactions.schemas import MonzoTransaction


class TransactionsResource(BaseResource):
    """
    Monzo API transactions resource.

    Docs:
        https://docs.monzo.com/#transactions
    """

    def get(
        self,
        transaction_id: str,
        *,
        expand_merchant: bool = False,
    ) -> MonzoTransaction:
        """
        Return single transaction.

        Docs:
            https://docs.monzo.com/#retrieve-transaction
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
        """
        Annotate transaction with extra metadata.

        Docs:
            https://docs.monzo.com/#annotate-transaction
        """
        endpoint = f"/transactions/{transaction_id}"
        params = {f"metadata[{key}]": value for key, value in metadata.items()}

        response = self._get_response(method="patch", endpoint=endpoint, params=params)

        transaction = MonzoTransaction(**response.json()["transaction"])

        return transaction

    def list(
        self,
        account_id: Optional[str] = None,
        *,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> List[MonzoTransaction]:
        """
        Return a list of passed account transactions.

        For ease of use, account ID is not required if user has only one active account.

        You can only fetch all transactions within 5 minutes of authentication.
        After that, you can query your last 90 days.

        Docs:
            https://docs.monzo.com/#list-transactions
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        endpoint = "/transactions"
        params = {"account_id": account_id}

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
