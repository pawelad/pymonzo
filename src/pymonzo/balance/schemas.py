"""Monzo API 'balance' related schemas."""

from pydantic import BaseModel

# Optional `rich` support
try:
    from rich.table import Table

    # Optional `babel` support
    try:
        from babel.numbers import format_currency
    except ImportError:
        from pymonzo.utils import format_currency  # type: ignore

except ImportError:
    RICH_AVAILABLE = False
else:
    RICH_AVAILABLE = True


class MonzoBalance(BaseModel):
    """API schema for a 'balance' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#balance

    Attributes:
        balance: The currently available balance of the account, as a 64bit integer in
            minor units of the currency, eg. pennies for GBP, or cents for EUR and USD.
        total_balance: The sum of the currently available balance of the account
            and the combined total of all the user's pots.
        currency: The ISO 4217 currency code.
        spend_today: The amount spent from this account today (considered from approx
            4am onwards), as a 64bit integer in minor units of the currency.
        balance_including_flexible_savings: Whether balance includes flexible
            savings pots.
        local_currency: Local currency.
        local_exchange_rate: Local exchange rate.
        local_spend: Local spend.
    """

    balance: int
    total_balance: int
    currency: str
    spend_today: int

    # Undocumented in Monzo API docs
    balance_including_flexible_savings: int
    local_currency: str
    local_exchange_rate: float
    local_spend: list

    if RICH_AVAILABLE:

        def __rich__(self) -> Table:
            """Pretty printing support for `rich`."""
            balance = format_currency(self.balance / 100, self.currency)
            total_balance = format_currency(self.total_balance / 100, self.currency)
            spend_today = format_currency(self.spend_today / 100, self.currency)

            grid = Table.grid(padding=(0, 5))
            grid.add_column(style="bold magenta")
            grid.add_column()
            grid.add_row("Balance:", balance)
            grid.add_row("Total balance:", total_balance)
            grid.add_row("Currency:", self.currency)
            grid.add_row("Spend today:", spend_today)
            grid.add_row("Local currency:", self.local_currency)
            grid.add_row("Local exchange rate:", str(self.local_exchange_rate))

            return grid
