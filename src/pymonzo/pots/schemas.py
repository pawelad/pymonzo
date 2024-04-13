"""Monzo API 'pots' related schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MonzoPot(BaseModel):
    """API schema for a 'pot' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#pots

    Attributes:
        id: The ID of the pot.
        name: Pot name.
        style: The pot background image.
        balance: Pot balance.
        currency: Pot currency.
        created: When this pot was created.
        updated: When this pot was last updated.
        deleted: Whether this pot is deleted. The API will be updated soon to not
            return deleted pots.
        goal_amount: Pot goal account.
        type: Pot type.
        product_id: Product ID
        current_account_id: Current account ID.
        cover_image_url: Cover image URL.
        isa_wrapper: ISA wrapper.
        round_up: Whether to use transfer money from rounding up transactions to
            the pot. You can only switch on round ups for one pot at a time.
        round_up_multiplier: Rounding up multiplier.
        is_tax_pot: Whether the pot is taxed.
        locked: Whether the pot is locked.
        available_for_bills: Whether the pot is available for bills.
        has_virtual_cards: Whether the pot has linked virtual cards.
    """

    id: str
    name: str
    style: str
    balance: int
    currency: str
    created: datetime
    updated: datetime
    deleted: bool

    # Undocumented in Monzo API docs
    goal_amount: Optional[int] = None
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
