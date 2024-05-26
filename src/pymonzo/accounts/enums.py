"""Monzo API 'accounts' related enums."""

from enum import Enum


class MonzoAccountType(str, Enum):
    """Monzo API 'account type' enum.

    Note:
        Currently undocumented in Monzo API docs.
    """

    UK_PREPAID = "uk_prepaid"
    UK_RETAIL = "uk_retail"
    UK_REWARDS = "uk_rewards"
    UK_BUSINESS = "uk_business"
    UK_LOAN = "uk_loan"
    UK_MONZO_FLEX = "uk_monzo_flex"
    UK_RETAIL_JOINT = "uk_retail_joint"


class MonzoAccountCurrency(str, Enum):
    """Monzo API 'account currency' enum.

    Note:
        Currently undocumented in Monzo API docs.
    """

    GBP = "GBP"
