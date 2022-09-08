"""
Monzo API webhooks resource.
"""
from typing import List, Optional

from pymonzo.resources import BaseResource
from pymonzo.webhooks.schemas import MonzoWebhook


class WebhooksResource(BaseResource):
    """
    Monzo API webhooks resource.

    Docs:
        https://docs.monzo.com/#webhooks
    """

    def list(self, account_id: Optional[str] = None) -> List[MonzoWebhook]:
        """
        List all webhooks.

        Docs:
            https://docs.monzo.com/#list-webhooks
        """
        endpoint = "/webhooks"
        params = {"account_id": account_id}

        response = self._get_response(method="get", endpoint=endpoint, params=params)

        webhooks = [MonzoWebhook(**webhook) for webhook in response.json()["webhooks"]]

        return webhooks

    def register(
        self,
        url: str,
        account_id: Optional[str] = None,
    ) -> MonzoWebhook:
        """
        Register a webhook.

        Docs:
            https://docs.monzo.com/#registering-a-webhook
        """
        endpoint = "/webhooks"
        params = {
            "account_id": account_id,
            "url": url,
        }
        response = self._get_response(method="post", endpoint=endpoint, params=params)

        webhook = MonzoWebhook(**response.json()["attachment"])

        return webhook
