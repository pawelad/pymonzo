"""Monzo API 'attachments' related schemas."""

from datetime import datetime

from pydantic import BaseModel


class MonzoAttachment(BaseModel):
    """API schema for an 'attachment' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#attachments

    Attributes:
        id: The ID of the attachment.
        user_id: The ID of the user who owns this attachment.
        external_id: The ID of the transaction to associate the attachment with.
        file_url: The URL at which the attachment is available.
        file_type: The content type of the attachment.
        created: The timestamp in UTC when the attachment was created.
    """

    id: str
    user_id: str
    external_id: str
    file_url: str
    file_type: str
    created: datetime


class MonzoAttachmentResponse(BaseModel):
    """API schema for an 'attachment upload' API response.

    Note:
        Monzo API docs: https://docs.monzo.com/#upload-attachment

    Attributes:
        file_url: The URL of the file once it has been uploaded.
        upload_url: The URL to `POST` the file to when uploading.
    """

    file_url: str
    upload_url: str
