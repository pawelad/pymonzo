"""Monzo API 'webhooks' related schemas."""

from pydantic import BaseModel

from pymonzo.transactions import MonzoTransactionMerchant


class MonzoWebhook(BaseModel):
    """API schema for a 'webhook' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#webhooks

    Attributes:
        id: The ID of the webhook.
        account_id: The account to receive notifications for.
        url: The URL we will send notifications to.
    """

    id: str
    account_id: str
    url: str


class MonzoWebhookTransactionEvent(BaseModel):
    """API schema for a 'webhook event' object.

    For some reason it seems slight different from
    [`pymonzo.transactions.MonzoTransaction`][].

    Note:
        Monzo API docs: https://docs.monzo.com/#transaction-created

    Attributes:
        account_id: The ID of the account.
        amount: The amount of the transaction in minor units of currency. For example
            pennies in the case of GBP. A negative amount indicates a debit (most
            card transactions will have a negative amount)
        created: Transaction creation date.
        currency: Transaction currency
        description: Transaction description.
        id: The ID of the transaction.
        category: The category can be set for each transaction by the user.
        is_load: Top-ups to an account are represented as transactions with a positive
            amount and `is_load = true`. Other transactions such as refunds, reversals
            or chargebacks may have a positive amount but `is_load = false`.
        settled: The timestamp at which the transaction settled. In most cases, this
            happens 24-48 hours after created. If this field is an empty string,
            the transaction is authorised but not yet "complete."
        merchant: Merchant information.
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

    Note:
        Monzo API docs: https://docs.monzo.com/#transaction-created

    Attributes:
        type: Webhook event type.
        data: Webhook event data.
    """

    type: str
    data: MonzoWebhookTransactionEvent
