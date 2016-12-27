# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class PyMonzoException(Exception):
    """Base pymonzo exception"""
    pass


class MonzoAPIException(PyMonzoException):
    """Base Monzo API response exception"""
    pass
