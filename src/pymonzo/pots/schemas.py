"""
Monzo API pots related schemas.
"""
from datetime import datetime

from pydantic import BaseModel


class MonzoPot(BaseModel):
    """
    API schema for a 'pot' object.

    Docs:
        https://docs.monzo.com/#pots
    """

    id: str
    name: str
    style: str
    balance: int
    currency: str
    created: datetime
    updated: datetime
    deleted: bool
