# -*- coding: utf-8 -*-
"""
pymonzo related exceptions
"""
from __future__ import unicode_literals


class PyMonzoException(Exception):
    """Base pymonzo exception"""
    pass


class MonzoAPIException(PyMonzoException):
    """Monzo API response exception"""
    pass


class UnableToGetToken(PyMonzoException):
    """Unable to get a token generic"""
    pass


class UnableToRefreshTokenException(MonzoAPIException):
    """Base Monzo API response exception"""
    pass
