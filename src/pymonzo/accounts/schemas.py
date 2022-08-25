"""
Monzo API accounts related schemas.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from pymonzo.accounts.enums import MonzoAccountCurrency, MonzoAccountType


class MonzoAccountOwner(BaseModel):
    """
    API schema for an 'account owner' object.

    Currently undocumented in docs.
    """

    # Undocumented in API docs
    user_id: str
    preferred_name: str
    preferred_first_name: str


class MonzoAccount(BaseModel):
    """
    API schema for an 'account' object.

    Most attributes are currently undocumented in docs.

    Docs:
        https://docs.monzo.com/#accounts
    """

    id: str
    description: str
    created: datetime

    # Undocumented in API docs
    closed: bool
    type: MonzoAccountType
    currency: MonzoAccountCurrency
    country_code: str
    owners: List[MonzoAccountOwner]

    # Only present in retail (non-prepaid) accounts
    account_number: Optional[str] = None
    sort_code: Optional[str] = None
    payment_details: Optional[dict] = None
