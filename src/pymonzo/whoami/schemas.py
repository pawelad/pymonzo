"""Monzo API 'whoami' related schemas."""
from pydantic import BaseModel


class MonzoWhoAmI(BaseModel):
    """API schema for a 'whoami' object.

    Docs: https://docs.monzo.com/#authenticating-requests
    """

    authenticated: bool
    client_id: str
    user_id: str
