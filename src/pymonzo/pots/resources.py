"""Monzo API 'pots' resource."""

from dataclasses import dataclass, field
from secrets import token_urlsafe
from typing import Dict, List, Optional, Union

from pymonzo.exceptions import CannotDetermineDefaultPot
from pymonzo.pots.schemas import MonzoPot
from pymonzo.resources import BaseResource


@dataclass
class PotsResource(BaseResource):
    """Monzo API 'pots' resource.

    Note:
        Monzo API docs: https://monzo.com/docs/#pots
    """

    _cached_pots: Dict[str, List[MonzoPot]] = field(default_factory=dict)

    def get_default_pot(self, account_id: Optional[str] = None) -> MonzoPot:
        """If the user has only one (active) pot, treat it as the default pot.

        Arguments:
            account_id: The ID of the account. Can be omitted if user has only one
                active account.

        Returns:
            User's active pot.

        Raises:
            CannotDetermineDefaultPot: If user has more than one active pot.
            CannotDetermineDefaultAccount: If no account ID was passed and default
                account cannot be determined.
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        pots = self.list(account_id)

        # If there is only one pot, return it
        if len(pots) == 1:
            return pots[0]

        # Otherwise check if there is only one active (non-deleted) pot
        active_pots = [pot for pot in pots if not pot.deleted]

        if len(active_pots) == 1:
            return active_pots[0]

        raise CannotDetermineDefaultPot(
            "Cannot determine default pot. "
            "You need to explicitly pass an 'pot_id' argument."
        )

    def list(
        self,
        account_id: Optional[str] = None,
        *,
        refresh: bool = False,
    ) -> List[MonzoPot]:
        """Return a list of user's pots.

        It's often used when deciding whether to require explicit pot ID
        or use the only active one, so we cache the response by default.

        Note:
            Monzo API docs: https://docs.monzo.com/#list-pots

        Arguments:
            account_id: The ID of the account. Can be omitted if user has only one
                active account.
            refresh: Whether to refresh the cached list of pots.

        Returns:
            A list of user's pots.

        Raises:
            CannotDetermineDefaultAccount: If no account ID was passed and default
                account cannot be determined.
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        if not refresh and self._cached_pots.get(account_id):
            return self._cached_pots[account_id]

        endpoint = "/pots"
        params = {"current_account_id": account_id}
        response = self._get_response(method="get", endpoint=endpoint, params=params)

        pots = [MonzoPot(**pot) for pot in response.json()["pots"]]
        self._cached_pots[account_id] = pots

        return pots

    def deposit(
        self,
        amount: Union[int, float],
        pot_id: Optional[str] = None,
        *,
        account_id: Optional[str] = None,
        dedupe_id: Optional[str] = None,
    ) -> MonzoPot:
        """Move money from an account to a pot.

        Note:
            Monzo API docs: https://docs.monzo.com/#deposit-into-a-pot

        Arguments:
            amount: The amount to deposit, as a 64bit integer in minor units of
                the currency, eg. pennies for GBP, or cents for EUR and USD.
            pot_id: The ID of the pot to deposit into.
            account_id: The ID of the account to withdraw from. Can be omitted if
                user has only one active account.
            dedupe_id: A unique string used to de-duplicate deposits. Ensure this
                remains static between retries to ensure only one deposit is created.
                If omitted, a random 16 character string will be generated.

        Returns:
            A Monzo pot.

        Raises:
            CannotDetermineDefaultPot: If user has more than one active pot.
            CannotDetermineDefaultAccount: If no account ID was passed and default
                account cannot be determined.
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        if not pot_id:
            pot_id = self.get_default_pot(account_id).id

        if not dedupe_id:
            dedupe_id = token_urlsafe(16)

        endpoint = f"/pots/{pot_id}/deposit"
        data = {
            "source_account_id": account_id,
            "amount": amount,
            "dedupe_id": dedupe_id,
        }
        response = self._get_response(method="put", endpoint=endpoint, data=data)

        pot = MonzoPot(**response.json())

        return pot

    def withdraw(
        self,
        amount: Union[int, float],
        pot_id: Optional[str] = None,
        *,
        account_id: Optional[str] = None,
        dedupe_id: Optional[str] = None,
    ) -> MonzoPot:
        """Withdraw money from a pot to an account.

        Note:
            Monzo API docs: https://docs.monzo.com/#withdraw-from-a-pot

        Arguments:
            amount: The amount to deposit, as a 64bit integer in minor units of
                the currency, eg. pennies for GBP, or cents for EUR and USD.
            pot_id: The ID of the pot to withdraw from.
            account_id: The ID of the account to deposit into. Can be omitted if
                user has only one active account.
            dedupe_id: A unique string used to de-duplicate deposits. Ensure this
                remains static between retries to ensure only one deposit is created.
                If omitted, a random 16 character string will be generated.

        Returns:
            A Monzo pot.

        Raises:
            CannotDetermineDefaultPot: If user has more than one active pot.
            CannotDetermineDefaultAccount: If no account ID was passed and default
                account cannot be determined.
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        if not pot_id:
            pot_id = self.get_default_pot(account_id).id

        if not dedupe_id:
            dedupe_id = token_urlsafe(16)

        endpoint = f"/pots/{pot_id}/withdraw"
        data = {
            "destination_account_id": account_id,
            "amount": amount,
            "dedupe_id": dedupe_id,
        }
        response = self._get_response(method="put", endpoint=endpoint, data=data)

        pot = MonzoPot(**response.json())

        return pot
