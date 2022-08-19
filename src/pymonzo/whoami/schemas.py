"""
Monzo API whoami related schemas.
"""
from pydantic import BaseModel


class MonzoWhoAmI(BaseModel):
    """
    API schema for a 'whoami' object.
    """

    authenticated: bool
    client_id: str
    user_id: str
