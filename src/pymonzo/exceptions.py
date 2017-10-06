# -*- coding: utf-8 -*-
"""
pymonzo related exceptions
"""
from __future__ import unicode_literals


class PyMonzoException(Exception):
    """Base pymonzo exception"""
    pass


class MonzoAPIError(PyMonzoException):
    """Monzo API response exception"""
    pass


class CantRefreshTokenError(MonzoAPIError):
    """Base Monzo API response exception"""
    pass
