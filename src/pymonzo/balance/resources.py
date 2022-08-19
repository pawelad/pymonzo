"""
Monzo API balance resource.
"""
from typing import Optional

from pymonzo.balance.schemas import MonzoBalance
from pymonzo.resources import BaseResource


class BalanceResource(BaseResource):
    """
    Monzo API balance resource.
    """

    def get(self, account_id: Optional[str] = None) -> MonzoBalance:
        """
        Return balance information for passed account.

        For ease of use, it allows not passing an account ID if the user has only
        one account.

        Docs:
            https://docs.monzo.com/#read-balance
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        endpoint = "/balance"
        params = {"account_id": account_id}
        response = self._get_response(method="get", endpoint=endpoint, params=params)

        balance = MonzoBalance(**response.json())

        return balance
