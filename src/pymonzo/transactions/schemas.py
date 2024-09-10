"""Monzo API 'transactions' related schemas."""

from datetime import datetime
from typing import Dict, Optional, Union

from pydantic import BaseModel, Field, field_validator

from pymonzo.transactions.enums import (
    MonzoTransactionCategory,
    MonzoTransactionDeclineReason,
)
from pymonzo.utils import empty_dict_to_none, empty_str_to_none

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

    # Undocumented in API docs
    formatted: str
    short_formatted: str
    zoom_level: int
    approximate: bool


class MonzoTransactionMerchant(BaseModel):
    """API schema for a 'transaction merchant' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#transactions

    Attributes:
        id: The ID of the merchant.
        group_id: Merchant group ID.
        name: Merchant name.
        logo: Merchant logo URL.
        address: Merchant address.
        emoji: Merchant emoji.
        category: The category can be set for each transaction by the user. Over
            time we learn which merchant goes in which category and auto-assign
            the category of a transaction. If the user hasn't set a category, we'll
            return the default category of the merchant on this transactions. Top-ups
            have category mondo. Valid values are general, eating_out, expenses,
            transport, cash, bills, entertainment, shopping, holidays, groceries.
        address: Merchant address
        created: Merchant creation date.
    """

    id: str
    group_id: str
    name: str
    logo: str
    emoji: str
    category: Union[MonzoTransactionCategory, str] = Field(union_mode="left_to_right")
    address: MonzoTransactionMerchantAddress

    # Undocumented in API docs
    online: bool
    atm: bool
    disable_feedback: bool
    metadata: Dict[str, str]
    suggested_tags: Optional[str] = None

    # Visible in API docs, not present in the API
    created: Optional[datetime] = None

    if RICH_AVAILABLE:

        def __rich__(self) -> Table:
            """Pretty printing support for `rich`."""
            grid = Table.grid(padding=(0, 5))
            grid.title = f"{self.emoji} | {self.name}"
            grid.title_style = "bold yellow"
            grid.add_column(style="bold cyan")
            grid.add_column()
            grid.add_row("ID:", self.id)
            grid.add_row("Group ID:", self.group_id)
            grid.add_row("Name:", self.name)
            grid.add_row("Address:", self.address.short_formatted)
            grid.add_row("Category:", self.category)
            if self.online:
                grid.add_row("Online:", "Yes")
            if self.atm:
                grid.add_row("ATM:", "Yes")

            return grid


class MonzoTransactionCounterparty(BaseModel):
    """API schema for a 'transaction counterparty' object.

    Note:
        This is undocumented in the Monzo API docs: https://docs.monzo.com/#transactions

    Attributes:
        user_id: Monzo internal User ID of the other party.
        name: The name of the other party.
        sort_code: The sort code of the other party.
        account_number: The account number of the other party.
    """

    user_id: str
    name: str
    sort_code: str
    account_number: str

    if RICH_AVAILABLE:

        def __rich__(self) -> Table:
            """Pretty printing support for `rich`."""
            grid = Table.grid(padding=(0, 5))
            grid.title = f"{self.name}"
            grid.title_style = "bold yellow"
            grid.add_column(style="bold cyan")
            grid.add_column()
            grid.add_row("ID:", self.user_id)
            grid.add_row("Name:", self.name)
            grid.add_row("Sort Code:", self.sort_code)
            grid.add_row("Account Number:", self.account_number)

            return grid


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
    merchant: Union[MonzoTransactionMerchant, str, None]
    metadata: Dict[str, str]
    notes: str
    is_load: bool
    settled: Optional[datetime]
    category: Union[MonzoTransactionCategory, str, None] = Field(
        default=None,
        union_mode="left_to_right",
    )
    decline_reason: Union[MonzoTransactionDeclineReason, str, None] = Field(
        default=None,
        union_mode="left_to_right",
    )

    # Undocumented in the API Documentation
    counterparty: Optional[MonzoTransactionCounterparty] = None

    @field_validator("settled", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: str) -> Optional[str]:
        """Convert empty strings to `None`."""
        return empty_str_to_none(v)

    @field_validator("counterparty", mode="before")
    @classmethod
    def empty_dict_to_none(cls, v: dict) -> Optional[dict]:
        """Convert empty dict to `None`."""
        return empty_dict_to_none(v)

    if RICH_AVAILABLE:

        def __rich__(self) -> Table:
            """Pretty printing support for `rich`."""
            amount = format_currency(self.amount / 100, self.currency)
            amount_color = "green" if self.amount > 0 else "red"

            grid = Table.grid(padding=(0, 5))
            grid.title = f"{amount} | {self.description}"
            grid.title_style = (
                f"bold {amount_color}"
                if not self.decline_reason
                else f"bold {amount_color} dim"
            )
            grid.add_column(style="bold cyan")
            grid.add_column(
                style="" if not self.decline_reason else "dim",
                max_width=50,
            )
            grid.add_row("ID:", self.id)
            grid.add_row("Description:", self.description)
            grid.add_row("Amount:", amount)
            grid.add_row("Currency:", self.currency)
            grid.add_row("Category:", self.category)
            if self.notes:
                grid.add_row("Notes:", self.notes)
            if self.decline_reason:
                grid.add_row("Decline reason:", self.decline_reason)
            grid.add_row("Created:", format_datetime(self.created))
            grid.add_row("Settled:", format_datetime(self.settled))
            if isinstance(self.merchant, MonzoTransactionMerchant):
                grid.add_row("Merchant:", self.merchant)

            return grid
