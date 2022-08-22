"""
pymonzo exceptions.
"""


class PyMonzoException(Exception):
    """Base pymonzo exception"""


class MonzoAPIError(PyMonzoException):
    """Catch all Monzo API error."""


class MonzoAccessDenied(MonzoAPIError):
    """Access to Monzo API has been denied."""
