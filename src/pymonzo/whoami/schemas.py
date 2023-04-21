"""Monzo API 'whoami' related schemas."""
from pydantic import BaseModel


class MonzoWhoAmI(BaseModel):
    """API schema for a 'whoami' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#authenticating-requests

    Attributes:
        authenticated: Whether the user is authenticated.
        client_id: Client ID.
        user_id: User ID.
    """

    authenticated: bool
    client_id: str
    user_id: str
