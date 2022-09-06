"""
Monzo API attachments related schemas.
"""
from datetime import datetime

from pydantic import BaseModel


class MonzoAttachment(BaseModel):
    """
    API schema for an 'attachment' object.

    Docs:
        https://docs.monzo.com/#attachments
    """

    id: str
    user_id: str
    external_id: str
    file_url: str
    file_type: str
    created: datetime
