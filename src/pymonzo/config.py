# -*- coding: utf-8 -*-
"""
pymonzo config
"""
from __future__ import unicode_literals

import os


MONZO_ACCESS_TOKEN_ENV = 'MONZO_ACCESS_TOKEN'
MONZO_AUTH_CODE_ENV = 'MONZO_AUTH_CODE'
MONZO_CLIENT_ID_ENV = 'MONZO_CLIENT_ID'
MONZO_CLIENT_SECRET_ENV = 'MONZO_CLIENT_SECRET'

TOKEN_FILE_NAME = os.getenv(
    'PYMONZO_TOKEN_FILE_NAME',
    default='.pymonzo-token',
)
TOKEN_FILE_PATH = os.getenv(
    'PYMONZO_TOKEN_FILE_PATH',
    default=os.path.join(os.path.expanduser('~'), TOKEN_FILE_NAME),
)
