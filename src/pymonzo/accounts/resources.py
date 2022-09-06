"""
Monzo API accounts resource.
"""
from typing import List, Optional

from pymonzo.accounts.schemas import MonzoAccount
from pymonzo.exceptions import CannotDetermineDefaultAccount
from pymonzo.resources import BaseResource


class AccountsResource(BaseResource):
    """
    Monzo API accounts resource.

    Docs:
        https://docs.monzo.com/#accounts
    """

    _cached_accounts = None

    def get_default_account(self) -> MonzoAccount:
        """
        If the user has only one active account, treat it as the default account.
        """
        accounts = self.list()

        # If there is only one account, return it
        if len(accounts) == 1:
            return accounts[0]

        # Otherwise check if there is only one active (non-closed) account
        active_accounts = [account for account in accounts if not account.closed]

        if len(active_accounts) == 1:
            return active_accounts[0]

        raise CannotDetermineDefaultAccount(
            "Cannot determine default account. "
            "You need to explicitly pass an 'account_id' argument."
        )

    def list(self, refresh: bool = False) -> List[MonzoAccount]:
        """
        Return a list of user accounts.

        It's often used when deciding whether to require explicit account ID
        or use the only available one, so we cache the response by default.

        Docs:
            https://docs.monzo.com/#list-accounts
        """
        if not refresh and self._cached_accounts:
            return self._cached_accounts

        endpoint = "/accounts"
        response = self._get_response(method="get", endpoint=endpoint)

        accounts = [MonzoAccount(**account) for account in response.json()["accounts"]]
        self._cached_accounts = accounts

        return accounts
