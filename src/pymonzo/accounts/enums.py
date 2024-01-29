"""Monzo API 'accounts' related enums."""

from enum import Enum


class MonzoAccountType(str, Enum):
    """Monzo API 'account type' enum.

    Note:
        Currently undocumented in Monzo API docs.
    """

    UK_PREPAID = "uk_prepaid"
    UK_RETAIL = "uk_retail"


class MonzoAccountCurrency(str, Enum):
    """Monzo API 'account currency' enum.

    Note:
        Currently undocumented in Monzo API docs.
    """

    GBP = "GBP"
