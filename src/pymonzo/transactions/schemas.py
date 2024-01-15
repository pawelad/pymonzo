"""Monzo API 'transactions' related schemas."""
from datetime import datetime
from typing import Dict, Optional, Union

from pydantic import BaseModel, field_validator

from pymonzo.transactions.enums import (
    MonzoTransactionCategory,
    MonzoTransactionDeclineReason,
)
from pymonzo.utils import empty_str_to_none


class MonzoTransactionMerchantAddress(BaseModel):
    """API schema for a 'transaction merchant address' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#transactions

    Attributes:
        address: Merchant address.
        city: Merchant city.
        country: Merchant country.
        latitude: Merchant latitude.
        longitude: Merchant longitude.
        postcode: Merchant postcode.
        region: Merchant region.
    """

    address: str
    city: str
    country: str
    latitude: float
    longitude: float
    postcode: str
    region: str


class MonzoTransactionMerchant(BaseModel):
    """API schema for a 'transaction merchant' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#transactions

    Attributes:
        address: Merchant address.
        created: Merchant creation date.
        group_id: Merchant group ID.
        id: The ID of the merchant.
        logo: Merchant logo URL.
        emoji: Merchant emoji.
        name: Merchant name.
        category: The category can be set for each transaction by the user. Over
            time we learn which merchant goes in which category and auto-assign
            the category of a transaction. If the user hasn't set a category, we'll
            return the default category of the merchant on this transactions. Top-ups
            have category mondo. Valid values are general, eating_out, expenses,
            transport, cash, bills, entertainment, shopping, holidays, groceries.
    """

    address: MonzoTransactionMerchantAddress
    created: datetime
    group_id: str
    id: str
    logo: str
    emoji: str
    name: str
    category: MonzoTransactionCategory


class MonzoTransaction(BaseModel):
    """API schema for a 'transaction' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#transactions

    Attributes:
        amount: The amount of the transaction in minor units of currency. For example
            pennies in the case of GBP. A negative amount indicates a debit (most
            card transactions will have a negative amount)
        created: Transaction creation date.
        currency: Transaction currency
        description: Transaction description.
        id: The ID of the transaction.
        merchant: This contains the `merchant_id of` the merchant that this transaction
            was made at. If you pass `?expand[]=merchant` in your request URL, it
            will contain lots of information about the merchant.
        metadata: Transaction metadata.
        notes: Transaction notes.
        is_load: Top-ups to an account are represented as transactions with a positive
            amount and `is_load = true`. Other transactions such as refunds, reversals
            or chargebacks may have a positive amount but `is_load = false`.
        settled: The timestamp at which the transaction settled. In most cases, this
            happens 24-48 hours after created. If this field is an empty string,
            the transaction is authorised but not yet "complete."
        category: The category can be set for each transaction by the user. Over
            time we learn which merchant goes in which category and auto-assign
            the category of a transaction. If the user hasn't set a category, we'll
            return the default category of the merchant on this transactions. Top-ups
            have category mondo. Valid values are general, eating_out, expenses,
            transport, cash, bills, entertainment, shopping, holidays, groceries.
        decline_reason: This is only present on declined transactions.
    """

    amount: int
    created: datetime
    currency: str
    description: str
    id: str
    merchant: Union[str, None, MonzoTransactionMerchant]
    metadata: Dict[str, str]
    notes: str
    is_load: bool
    settled: Optional[datetime]
    category: Optional[MonzoTransactionCategory] = None
    decline_reason: Optional[MonzoTransactionDeclineReason] = None

    @field_validator("settled")
    @classmethod
    def empty_str_to_none(cls, v: str) -> Optional[str]:
        """Convert empty strings to `None`."""
        return empty_str_to_none(v)
