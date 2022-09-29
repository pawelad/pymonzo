"""Monzo API 'transactions' related enums."""
from enum import Enum


class MonzoTransactionDeclineReason(str, Enum):
    """Monzo API 'transaction decline reason' enum.

    Docs: https://docs.monzo.com/#transactions
    """

    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    CARD_INACTIVE = "CARD_INACTIVE"
    CARD_BLOCKED = "CARD_BLOCKED"
    INVALID_CVC = "INVALID_CVC"
    OTHER = "OTHER"

    # Undocumented in Monzo API docs
    CARD_CLOSED = "CARD_CLOSED"
    INVALID_PIN = "INVALID_PIN"
    INVALID_EXPIRY_DATE = "INVALID_EXPIRY_DATE"
    STRONG_CUSTOMER_AUTHENTICATION_REQUIRED = "STRONG_CUSTOMER_AUTHENTICATION_REQUIRED"
    SCA_NOT_AUTHENTICATED_CARD_NOT_PRESENT = "SCA_NOT_AUTHENTICATED_CARD_NOT_PRESENT"


class MonzoTransactionCategory(str, Enum):
    """Monzo API 'transaction category' enum.

    Docs: https://docs.monzo.com/#transactions
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
