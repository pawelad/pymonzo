"""
Monzo API transactions related enums.
"""
from enum import Enum


class MonzoTransactionDeclineReason(str, Enum):
    """
    Monzo API transaction 'decline_reason' enum.

    Docs:
        https://docs.monzo.com/#transactions
    """

    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    CARD_INACTIVE = "CARD_INACTIVE"
    CARD_BLOCKED = "CARD_BLOCKED"
    INVALID_CVC = "INVALID_CVC"
    OTHER = "OTHER"


class MonzoTransactionCategory(str, Enum):
    """
    Monzo API transaction 'category' enum.

    Docs:
        https://docs.monzo.com/#transactions
    """

    GENERAL = "general"
    EATING_OUT = "eating_out"
    EXPENSES = "expenses"
    TRANSPORT = "transport"
    CASH = "cash"
    BILLS = "bills"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    HOLIDAYS = "holidays"
    GROCERIES = "groceries"
