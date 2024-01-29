"""Monzo API 'balance' resource."""

from typing import Optional

from pymonzo.balance.schemas import MonzoBalance
from pymonzo.resources import BaseResource


class BalanceResource(BaseResource):
    """Monzo API 'balance' resource.

    Note:
        Monzo API docs: https://docs.monzo.com/#balance
    """

    def get(self, account_id: Optional[str] = None) -> MonzoBalance:
        """Return account balance information.

        Note:
            Monzo API docs: https://docs.monzo.com/#read-balance

        Arguments:
            account_id: The ID of the account. Can be omitted if user has only one
                active account.

        Returns:
             Monzo account balance information.

        Raises:
            CannotDetermineDefaultAccount: If no account ID was passed and default
                account cannot be determined.
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        endpoint = "/balance"
        params = {"account_id": account_id}
        response = self._get_response(method="get", endpoint=endpoint, params=params)

        balance = MonzoBalance(**response.json())

        return balance
