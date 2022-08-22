"""
pymonzo resources related code.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import httpx
from httpx import codes

from pymonzo.exceptions import MonzoAccessDenied, MonzoAPIError

if TYPE_CHECKING:
    from pymonzo.client import MonzoAPI


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

        if response.status_code == codes.FORBIDDEN:
            raise MonzoAccessDenied(
                "Monzo API access denied (HTTP 403 Forbidden). "
                "Make sure to authenticate the OAuth app on your mobile device."
            )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            content = response.json()
            error = content.get("message")
            code = content.get("code")

            if error and code:
                msg = f"{error} ({code})."
            else:
                msg = f"Something went wrong: {e}"

            raise MonzoAPIError(msg)

        return response
