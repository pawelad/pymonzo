"""
Monzo API pots resource.
"""
from dataclasses import dataclass, field
from secrets import token_urlsafe
from typing import List, Optional, Union

from pymonzo.exceptions import CannotDetermineDefaultPot
from pymonzo.pots.schemas import MonzoPot
from pymonzo.resources import BaseResource


@dataclass
class PotsResource(BaseResource):
    """
    Monzo API pots resource.

    Docs:
        https://monzo.com/docs/#pots
    """

    _cached_pots: dict = field(default_factory=dict)

    def get_default_pot(self, account_id: Optional[str] = None) -> MonzoPot:
        """
        If the user has only one active pot, treat it as the default account.
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
        """
        Return a list of user pots.

        For ease of use, account ID is not required if user has only one active account.

        It's often used when deciding whether to require explicit pot ID
        or use the only active one, so we cache the response by default.

        Docs:
            https://docs.monzo.com/#list-pots
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
    ):
        """
        Move money from an account to a pot.

        For ease of use, pot ID and/or account ID is not required if user has only
        one active pot/account.

        Docs:
            https://docs.monzo.com/#deposit-into-a-pot
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        if not pot_id:
            pot_id = self.get_default_pot(account_id)

        if not dedupe_id:
            dedupe_id = token_urlsafe(16)

        endpoint = f"/pots/{pot_id}/deposit"
        params = {
            "source_account_id": account_id,
            "amount": amount,
            "dedupe_id": dedupe_id,
        }
        response = self._get_response(method="put", endpoint=endpoint, params=params)

        pot = MonzoPot(**response.json())

        return pot

    def withdraw(
        self,
        amount: Union[int, float],
        pot_id: Optional[str] = None,
        *,
        account_id: Optional[str] = None,
        dedupe_id: Optional[str] = None,
    ):
        """
        Withdraw money from a pot to an account.

        For ease of use, pot ID and/or account ID is not required if user has only
        one active pot/account.

        Docs:
            https://docs.monzo.com/#withdraw-from-a-pot
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        if not pot_id:
            pot_id = self.get_default_pot(account_id)

        if not dedupe_id:
            dedupe_id = token_urlsafe(16)

        endpoint = f"/pots/{pot_id}/withdraw"
        params = {
            "destination_account_id": account_id,
            "amount": amount,
            "dedupe_id": dedupe_id,
        }
        response = self._get_response(method="put", endpoint=endpoint, params=params)

        pot = MonzoPot(**response.json())

        return pot
