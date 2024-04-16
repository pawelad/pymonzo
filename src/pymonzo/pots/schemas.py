"""Monzo API 'pots' related schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# Optional `rich` support
try:
    from rich.table import Table

    # Optional `babel` support
    try:
        from babel.dates import format_datetime
        from babel.numbers import format_currency
    except ImportError:
        from pymonzo.utils import format_currency, format_datetime  # type: ignore

except ImportError:
    RICH_AVAILABLE = False
else:
    RICH_AVAILABLE = True


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

    if RICH_AVAILABLE:

        def __rich__(self) -> Table:
            """Pretty printing support for `rich`."""
            balance = format_currency(self.balance / 100, self.currency)

            grid = Table.grid(padding=(0, 5))
            grid.title = f"Pot '{self.name}' | {balance}"
            grid.title_style = "bold green"
            grid.add_column(style="bold cyan")
            grid.add_column(style="" if not self.deleted else "dim")
            grid.add_row("ID:", self.id)
            grid.add_row("Name:", self.name)
            grid.add_row("Balance:", balance)
            if self.goal_amount:
                goal_amount = format_currency(self.goal_amount / 100, self.currency)
                grid.add_row("Goal:", goal_amount)
            grid.add_row("Currency:", self.currency)
            grid.add_row("Type:", self.type)
            grid.add_row("Deleted:", "Yes" if self.deleted else "No")
            if self.round_up:
                grid.add_row("Round up:", "Yes" if self.round_up else "No")
            if self.round_up_multiplier:
                grid.add_row("Round up multiplier:", str(self.round_up_multiplier))
            if self.locked:
                grid.add_row("Locked:", "Yes" if self.locked else "No")
            grid.add_row("Created:", format_datetime(self.created))
            grid.add_row("Updated:", format_datetime(self.updated))

            return grid
