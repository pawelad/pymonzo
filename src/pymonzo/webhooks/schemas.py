"""
Monzo API webhooks related schemas.
"""
from pydantic import BaseModel


class MonzoWebhook(BaseModel):
    """
    API schema for a 'webhook' object.

    Docs:
        https://docs.monzo.com/#webhooks
    """

    id: str
    account_id: str
    url: str
