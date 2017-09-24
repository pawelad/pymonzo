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


class UnableToRefreshTokenException(MonzoAPIException):
    """Base Monzo API response exception"""
    pass
