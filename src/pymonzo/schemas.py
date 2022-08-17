"""
Monzo API schemas.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from pymonzo.enums import MonzoTransactionCategory, MonzoTransactionDeclineReason


class MonzoWhoAmi(BaseModel):
    """
    API schema for a 'Who Am I' object.
    """

    authenticated: bool
    client_id: str
    user_id: str


class MonzoAccount(BaseModel):
    """
    API schema for an 'account' object.

    Docs:
        https://docs.monzo.com/#accounts
    """

    id: str
    description: str
    created: datetime


class MonzoBalance(BaseModel):
    """
    API schema for a 'balance' object.

    Docs:
        https://docs.monzo.com/#balance
    """

    balance: int
    total_balance: int
    currency: str
    spend_today: int


class MonzoPot(BaseModel):
    """
    API schema for a 'pot' object.

    Docs:
        https://docs.monzo.com/#pots
    """

    id: str
    name: str
    style: str
    balance: int
    currency: str
    created: datetime
    updated: datetime
    deleted: bool


class MonzoTransactionMerchantAddress(BaseModel):
    """
    API schema for a 'transaction merchant adress' object.

    Docs:
        https://docs.monzo.com/#transactions
    """

    address: str
    city: str
    country: str
    latitude: float
    longitude: float
    postcode: str
    region: str


class MonzoTransactionMerchant(BaseModel):
    """
    API schema for a 'transaction merchant' object.

    Docs:
        https://docs.monzo.com/#transactions
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
    """
    API schema for a 'transaction' object.

    Docs:
        https://docs.monzo.com/#transactions
    """

    amount: int
    created: datetime
    currency: str
    description: str
    id: str
    merchant: MonzoTransactionMerchant
    metadata: dict
    notes: str
    is_load: bool
    settled: datetime
    decline_reason: Optional[MonzoTransactionDeclineReason] = None
