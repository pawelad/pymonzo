"""Monzo API 'accounts' related schemas."""

from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from pymonzo.accounts.enums import MonzoAccountCurrency, MonzoAccountType

# Optional `rich` support
try:
    from textwrap import wrap

    from rich.table import Table

    # Optional `babel` support
    try:
        from babel.dates import format_datetime
    except ImportError:
        from pymonzo.utils import format_datetime  # type: ignore

except ImportError:
    RICH_AVAILABLE = False
else:
    RICH_AVAILABLE = True


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
    type: Union[MonzoAccountType, str] = Field(union_mode="left_to_right")
    currency: Union[MonzoAccountCurrency, str] = Field(union_mode="left_to_right")
    country_code: str
    owners: List[MonzoAccountOwner]

    # Only present in retail (non-prepaid) accounts
    account_number: Optional[str] = None
    sort_code: Optional[str] = None
    payment_details: Optional[dict] = None

    if RICH_AVAILABLE:

        def __rich__(self) -> Table:
            """Pretty printing support for `rich`."""
            grid = Table.grid(padding=(0, 5))
            grid.title = f"Account '{self.id}' ({self.country_code})"
            grid.title_style = "bold green"
            grid.add_column(style="bold cyan")
            grid.add_column(style="" if not self.closed else "dim")
            grid.add_row("ID:", self.id)
            grid.add_row("Description:", self.description)
            grid.add_row("Currency:", self.currency)
            if self.account_number:
                grid.add_row("Account Number:", self.account_number)
            if self.sort_code:
                grid.add_row("Sort Code:", "-".join(wrap(self.sort_code, 2)))
            grid.add_row("Type:", self.type)
            grid.add_row("Closed:", "Yes" if self.closed else "No")
            grid.add_row("Created:", format_datetime(self.created))

            return grid
