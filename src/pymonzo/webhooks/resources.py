"""
Monzo API webhooks resource.
"""
from typing import Optional

from pymonzo.resources import BaseResource
from pymonzo.webhooks.schemas import MonzoWebhook


class WebhooksResource(BaseResource):
    """
    Monzo API webhooks resource.

    Docs:
        https://docs.monzo.com/#webhooks
    """

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
