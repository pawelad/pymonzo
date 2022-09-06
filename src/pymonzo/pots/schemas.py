"""
Monzo API pots related schemas.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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

    # Undocumented in API docs
    goal_amount: int
    type: str
    product_id: str
    current_account_id: str
    cover_image_url: str
    isa_wrapper: str
    round_up: bool
    round_up_multiplier: Optional[int]
    is_tax_pot: bool
    locked: bool
    available_for_bills: bool
    has_virtual_cards: bool
