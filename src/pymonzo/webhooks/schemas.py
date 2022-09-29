"""Monzo API 'webhooks' related schemas."""
from pydantic import BaseModel

from pymonzo.transactions import MonzoTransactionMerchant


class MonzoWebhook(BaseModel):
    """API schema for a 'webhook' object.

    Docs: https://docs.monzo.com/#webhooks
    """

    id: str
    account_id: str
    url: str


class MonzoWebhookTransactionEvent(BaseModel):
    """API schema for a 'webhook event' object.

    For some reason it seems slight different from 'MonzoTransaction'.

    Docs: https://docs.monzo.com/#transaction-created
    """

    account_id: str
    amount: int
    created: str
    currency: str
    description: str
    id: str
    category: str
    is_load: bool
    settled: str
    merchant: MonzoTransactionMerchant


class MonzoWebhookEvent(BaseModel):
    """API schema for a 'webhook event' object.

    Docs: https://docs.monzo.com/#transaction-created
    """

    type: str
    data: MonzoWebhookTransactionEvent
