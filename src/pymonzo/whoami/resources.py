"""
Monzo API accounts resource.
"""
from pymonzo.resources import BaseResource
from pymonzo.whoami.schemas import MonzoWhoAmI


class WhoAmIResource(BaseResource):
    """
    Monzo API whoamI resource.
    """

    def whoami(self) -> MonzoWhoAmI:
        """
        Return information about the access token.

        Docs:
            https://docs.monzo.com/#authenticating-requests
        """
        endpoint = "/ping/whoami"
        response = self._get_response(method="get", endpoint=endpoint)

        who_am_i = MonzoWhoAmI(**response.json())

        return who_am_i
