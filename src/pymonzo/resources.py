"""pymonzo base API resource related code."""

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import httpx
from httpx import codes

from pymonzo.exceptions import MonzoAccessDenied, MonzoAPIError

if TYPE_CHECKING:
    from pymonzo.client import MonzoAPI


@dataclass
class BaseResource:
    """Base Monzo API resource class.

    Attributes:
        client: Monzo API client instance.
    """

    client: "MonzoAPI"

    def _get_response(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
    ) -> httpx.Response:
        """Handle HTTP requests and catch API errors.

        Arguments:
            method: HTTP method.
            endpoint: HTTP endpoint.
            params: URL query parameters.
            data: form encoded data.

        Returns:
            HTTP response.

        Raises:
            MonzoAccessDenied: When access to Monzo API was denied.
            MonzoAPIError: When Monzo API returned an error.
        """
        httpx_kwargs = {"params": params}
        if method in ["post", "put", "patch"]:
            httpx_kwargs["data"] = data

        response = getattr(self.client.session, method)(endpoint, **httpx_kwargs)

        if response.status_code == codes.FORBIDDEN:
            raise MonzoAccessDenied(
                "Monzo API access denied (HTTP 403 Forbidden). "
                "Make sure to (re)authenticate the OAuth app on your mobile device."
            )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            try:
                content = response.json()
            except json.decoder.JSONDecodeError:
                content = {}

            error = content.get("message")
            code = content.get("code")

            if error and code:
                msg = f"{error} ({code})"
            else:
                msg = f"Something went wrong: {e}"

            raise MonzoAPIError(msg) from e

        return response
