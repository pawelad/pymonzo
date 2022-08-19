"""
pymonzo resources.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pymonzo.client import MonzoAPI

from dataclasses import dataclass
from typing import Optional

import httpx

from pymonzo.exceptions import MonzoAPIError


@dataclass
class BaseResource:
    """
    Base Monzo API resource class.
    """

    client: MonzoAPI

    def _get_response(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
    ) -> httpx.Response:
        """
        Helper method to handle HTTP requests and catch API errors.
        """
        response = getattr(self.client.session, method)(endpoint, params=params)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise MonzoAPIError(f"Something went wrong: {e}")

        return response
