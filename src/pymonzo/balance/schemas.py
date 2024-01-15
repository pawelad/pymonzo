"""Monzo API 'balance' related schemas."""
from pydantic import BaseModel


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
