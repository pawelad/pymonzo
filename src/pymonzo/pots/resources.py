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

    Docs:
        https://monzo.com/docs/#pots
    """

    _cached_pots: dict = field(default_factory=dict)

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
