"""Monzo API 'balance' related schemas."""
from pydantic import BaseModel


class MonzoBalance(BaseModel):
    """API schema for a 'balance' object.

    Docs: https://docs.monzo.com/#balance
    """

    balance: int
    total_balance: int
    currency: str
    spend_today: int

    # Undocumented in Monzo API docs
    balance_including_flexible_savings: int
    local_currency: str
    local_exchange_rate: int
    local_spend: list
