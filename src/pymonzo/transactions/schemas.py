"""Monzo API 'transactions' related schemas."""
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator

from pymonzo.transactions.enums import (
    MonzoTransactionCategory,
    MonzoTransactionDeclineReason,
)
from pymonzo.utils import empty_str_to_none


class MonzoTransactionMerchantAddress(BaseModel):
    """API schema for a 'transaction merchant address' object.

    Docs: https://docs.monzo.com/#transactions
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

    Docs: https://docs.monzo.com/#transactions
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

    Docs: https://docs.monzo.com/#transactions
    """

    amount: int
    created: datetime
    currency: str
    description: str
    id: str
    merchant: Union[str, None, MonzoTransactionMerchant]
    metadata: dict
    notes: str
    is_load: bool
    settled: Optional[datetime]
    decline_reason: Optional[MonzoTransactionDeclineReason] = None

    # Validators
    _settled_empty_str_to_none = validator("settled", pre=True, allow_reuse=True)(
        empty_str_to_none
    )
