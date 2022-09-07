"""
Monzo API feed resource.
"""
from typing import Optional

from pymonzo.feed.schemas import MonzoBasicFeedItem
from pymonzo.resources import BaseResource


class FeedResource(BaseResource):
    """
    Monzo API feed resource.

    Docs:
        https://docs.monzo.com/#feed-items
    """

    def create(
        self,
        feed_item: MonzoBasicFeedItem,
        account_id: Optional[str] = None,
        *,
        url: Optional[str] = None,
    ) -> dict:
        """
        Create a feed item.

        For ease of use, account ID is not required if user has only one active account.

        Docs:
            https://docs.monzo.com/#create-feed-item
        """
        params = {
            "account_id": account_id,
            "type": "basic",
        }

        for key, value in feed_item.dict(exclude_none=True).items():
            params[f"params[{key}]"] = value

        if url:
            params["url"] = url

        endpoint = "/feed"
        response = self._get_response(method="post", endpoint=endpoint, params=params)

        return response.json()
