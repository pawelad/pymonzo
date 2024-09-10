"""Monzo API 'webhooks' resource."""

from typing import List, Optional

from pymonzo.resources import BaseResource
from pymonzo.webhooks.schemas import MonzoWebhook


class WebhooksResource(BaseResource):
    """Monzo API 'webhooks' resource.

    Note:
        Monzo API docs: https://docs.monzo.com/#webhooks
    """

    def list(self, account_id: Optional[str] = None) -> List[MonzoWebhook]:
        """List all webhooks.

        Note:
            Monzo API docs: https://docs.monzo.com/#list-webhooks

        Arguments:
            account_id: The account to list registered webhooks for. Can be omitted
                if user has only one active account.

        Returns:
            List of Monzo webhooks.

        Raises:
            CannotDetermineDefaultAccount: If no account ID was passed and default
                account cannot be determined.
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

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
        """Register a webhook.

        Note:
            Monzo API docs: https://docs.monzo.com/#registering-a-webhook

        Arguments:
            account_id: The account to receive notifications for. Can be omitted
                if user has only one active account.
            url: The URL we will send notifications to.

        Returns:
            Registered Monzo webhook.

        Raises:
            CannotDetermineDefaultAccount: If no account ID was passed and default
                account cannot be determined.
        """
        if not account_id:
            account_id = self.client.accounts.get_default_account().id

        endpoint = "/webhooks"
        data = {
            "account_id": account_id,
            "url": url,
        }
        response = self._get_response(method="post", endpoint=endpoint, data=data)

        webhook = MonzoWebhook(**response.json()["webhook"])

        return webhook

    def delete(self, webhook_id: str) -> dict:
        """Delete a webhook.

        Note:
            Monzo API docs: https://docs.monzo.com/#deleting-a-webhook

        Arguments:
            webhook_id: The ID of the webhook.

        Returns:
            API response.
        """
        endpoint = f"/webhooks/{webhook_id}"

        response = self._get_response(method="delete", endpoint=endpoint)

        return response.json()
