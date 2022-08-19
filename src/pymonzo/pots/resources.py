"""
Monzo API pots resource.
"""
from dataclasses import dataclass, field
from typing import List, Optional

from pymonzo.pots.schemas import MonzoPot
from pymonzo.resources import BaseResource


@dataclass
class PotsResource(BaseResource):
    """
    Monzo API pots resource.
    """

    _cached_pots: dict = field(default_factory=dict)

    def list(
        self,
        account_id: Optional[str] = None,
        refresh: bool = False,
    ) -> List[MonzoPot]:
        """
        Return a list of user pots.

        For ease of use, it allows not passing an account ID if the user has only
        one account.

        Docs:
            https://monzo.com/docs/#pots
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
