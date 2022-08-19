"""
Monzo API accounts related schemas.
"""
from datetime import datetime

from pydantic import BaseModel


class MonzoAccount(BaseModel):
    """
    API schema for an 'account' object.

    Docs:
        https://docs.monzo.com/#accounts
    """

    id: str
    description: str
    created: datetime
