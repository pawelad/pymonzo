"""
pymonzo exceptions.
"""


class PyMonzoException(Exception):
    """Base pymonzo exception"""


class MonzoAPIError(PyMonzoException):
    """Monzo API error exception"""
