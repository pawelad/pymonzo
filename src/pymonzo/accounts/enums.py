"""
Monzo API accounts related enums.
"""
from enum import Enum


class MonzoAccountType(str, Enum):
    """
    Monzo API account 'type' enum.

    Currently undocumented in docs.
    """

    UK_PREPAID = "uk_prepaid"
    UK_RETAIL = "uk_retail"


class MonzoAccountCurrency(str, Enum):
    """
    Monzo API account 'currency' enum.

    Currently undocumented in docs.
    """

    GBP = "GBP"
