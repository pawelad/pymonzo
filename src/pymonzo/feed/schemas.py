"""Monzo API 'feed' related schemas."""
from typing import Optional

from pydantic import BaseModel, HttpUrl
from pydantic.color import Color


class MonzoBasicFeedItem(BaseModel):
    """API schema for a 'basic feed item' object.

    Docs: https://docs.monzo.com/#feed-items
    """

    title: str
    image_url: HttpUrl
    body: str
    background_color: Optional[Color] = None
    title_color: Optional[Color] = None
    body_color: Optional[Color] = None
