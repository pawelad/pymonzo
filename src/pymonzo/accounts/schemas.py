"""Monzo API 'accounts' related schemas."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from pymonzo.accounts.enums import MonzoAccountCurrency, MonzoAccountType


class MonzoAccountOwner(BaseModel):
    """API schema for an 'account owner' object.

    Note:
        Currently undocumented in Monzo API docs.

    Attributes:
        user_id: The ID of the user.
        preferred_name: Name preferred by the user.
        preferred_first_name: First name preferred by the user.
    """

    # Undocumented in API docs
    user_id: str
    preferred_name: str
    preferred_first_name: str


class MonzoAccount(BaseModel):
    """API schema for an 'account' object.

    Most attributes are currently undocumented in Monzo API docs.

    Note:
        Monzo API docs: https://docs.monzo.com/#accounts

    Attributes:
        id: The ID of the account.
        description: Account description.
        created: Account creation date.
        closed: Whether account is closed.
        type: Account type.
        currency: Account currency.
        country_code: Account country code.
        owners: Account owners.
        account_number: Account number.
        sort_code: Account sort code.
        payment_details: Account payment details.
    """

    id: str
    description: str
    created: datetime

    # Undocumented in Monzo API docs
    closed: bool
    type: MonzoAccountType
    currency: MonzoAccountCurrency
    country_code: str
    owners: List[MonzoAccountOwner]

    # Only present in retail (non-prepaid) accounts
    account_number: Optional[str] = None
    sort_code: Optional[str] = None
    payment_details: Optional[dict] = None
