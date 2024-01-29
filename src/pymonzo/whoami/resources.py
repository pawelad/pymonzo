"""Monzo API 'whoami' resource."""

from pymonzo.resources import BaseResource
from pymonzo.whoami.schemas import MonzoWhoAmI


class WhoAmIResource(BaseResource):
    """Monzo API 'whoami' resource.

    Note:
        Monzo API docs: https://docs.monzo.com/#authenticating-requests
    """

    def whoami(self) -> MonzoWhoAmI:
        """Return information about the access token.

        Note:
            Monzo API docs: https://docs.monzo.com/#authenticating-requests

        Returns:
            Information about the access token.
        """
        endpoint = "/ping/whoami"
        response = self._get_response(method="get", endpoint=endpoint)

        who_am_i = MonzoWhoAmI(**response.json())

        return who_am_i
