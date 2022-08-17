"""
pymonzo related exceptions
"""


class PyMonzoException(Exception):
    """Base pymonzo exception"""

    pass


class MonzoAPIError(PyMonzoException):
    """Monzo API response exception"""

    pass


class CantRefreshTokenError(MonzoAPIError):
    """Base Monzo API response exception"""

    pass
