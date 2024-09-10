"""Monzo API 'feed' resource."""

from typing import Optional

from pymonzo.feed.schemas import MonzoBasicFeedItem
from pymonzo.resources import BaseResource


class FeedResource(BaseResource):
    """Monzo API 'feed' resource.

    Note:
        Monzo API docs: https://docs.monzo.com/#feed-items
    """

    def create(
        self,
        feed_item: MonzoBasicFeedItem,
        account_id: Optional[str] = None,
        *,
        url: Optional[str] = None,
    ) -> dict:
        """Create a feed item.

        Note:
            Monzo API docs: https://docs.monzo.com/#create-feed-item

        Arguments:
            feed_item: Type of feed item. Currently only basic is supported.
            account_id: The account to create a feed item for. Can be omitted if
                user has only one active account.
            url: A URL to open when the feed item is tapped. If no URL is provided,
                the app will display a fallback view based on the title & body.

        Returns:
            API response.

        Raises:
            CannotDetermineDefaultAccount: If no account ID was passed and default
                account cannot be determined.
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        data = {
            "account_id": account_id,
            "type": "basic",
        }

        for key, value in feed_item.model_dump(exclude_none=True).items():
            data[f"params[{key}]"] = value

        if url:
            data["url"] = url

        endpoint = "/feed"
        response = self._get_response(method="post", endpoint=endpoint, data=data)

        return response.json()
