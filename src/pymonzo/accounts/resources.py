"""Monzo API 'accounts' resource."""

from dataclasses import dataclass, field
from typing import List

from pymonzo.accounts.schemas import MonzoAccount
from pymonzo.exceptions import CannotDetermineDefaultAccount
from pymonzo.resources import BaseResource


@dataclass
class AccountsResource(BaseResource):
    """Monzo API 'accounts' resource.

    Note:
        Monzo API docs: https://docs.monzo.com/#accounts
    """

    _cached_accounts: List[MonzoAccount] = field(default_factory=list)

    def get_default_account(self) -> MonzoAccount:
        """If the user has only one active account, treat it as the default account.

        Returns:
            User's active account.

        Raises:
            CannotDetermineDefaultAccount: If user has more than one active account.
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

    def list(self, *, refresh: bool = False) -> List[MonzoAccount]:
        """Return a list of user's Monzo accounts.

        It's often used when deciding whether to require explicit account ID
        or use the only active one, so we cache the response by default.

        Note:
            Monzo API docs: https://docs.monzo.com/#list-accounts

        Arguments:
            refresh: Whether to refresh the cached list of accounts.

        Returns:
            A list of user's Monzo accounts.
        """
        if not refresh and self._cached_accounts:
            return self._cached_accounts

        endpoint = "/accounts"
        response = self._get_response(method="get", endpoint=endpoint)

        accounts = [MonzoAccount(**account) for account in response.json()["accounts"]]
        self._cached_accounts = accounts

        return accounts
