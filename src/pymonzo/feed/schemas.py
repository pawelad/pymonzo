"""Monzo API 'feed' related schemas."""

from typing import Optional

from pydantic import BaseModel, HttpUrl


class MonzoBasicFeedItem(BaseModel):
    """API schema for a 'basic feed item' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#feed-items

    Attributes:
        title: The title to display.
        image_url: URL of the image to display. This will be displayed as an icon
            in the feed, and on the expanded page if no url has been provided.
        body: The body text of the feed item.
        background_color: Hex value for the background colour of the feed item in the
            format #RRGGBB. Defaults to standard app colours (ie. white background).
        title_color: Hex value for the colour of the title text in the format #RRGGBB.
            Defaults to standard app colours.
        body_color: Hex value for the colour of the body text in the format #RRGGBB.
            Defaults to standard app colours.
    """

    title: str
    image_url: HttpUrl
    body: str
    background_color: Optional[str] = None
    title_color: Optional[str] = None
    body_color: Optional[str] = None
