"""Monzo API 'attachments' resource."""
from typing import Dict

from pymonzo.attachments.schemas import MonzoAttachment
from pymonzo.resources import BaseResource


class AttachmentsResource(BaseResource):
    """Monzo API 'attachments' resource.

    Note:
        Monzo API docs: https://docs.monzo.com/#attachments
    """

    def upload(
        self,
        *,
        file_name: str,
        file_type: str,
        content_length: int,
    ) -> Dict[str, str]:
        """Upload an attachment.

        The response will include a `file_url` which will be the URL of the resulting
        file, and an `upload_url` to which the file should be uploaded to.

        Note:
            Monzo API docs: https://docs.monzo.com/#upload-attachment

        Arguments:
            file_name: The name of the file to be uploaded.
            file_type: The content type of the file.
            content_length: The HTTP Content-Length of the upload request body,
                in bytes.

        Returns:
            Dictionary with `file_url` which will be the URL of the resulting file,
            and an `upload_url` to which the file should be uploaded to.
        """
        endpoint = "/attachment/upload"
        params = {
            "file_name": file_name,
            "file_type": file_type,
            "content_length": content_length,
        }
        response = self._get_response(method="post", endpoint=endpoint, params=params)

        return response.json()

    def register(
        self,
        transaction_id: str,
        *,
        file_url: str,
        file_type: str,
    ) -> MonzoAttachment:
        """Register uploaded image to an attachment.

        Note:
            Monzo API docs: https://docs.monzo.com/#register-attachment

        Arguments:
            transaction_id: The ID of the transaction to associate the attachment with.
            file_url: The URL of the uploaded attachment.
            file_type: The content type of the attachment.

        Returns:
            A Monzo attachment.
        """
        endpoint = "/attachment/register"
        params = {
            "external_id": transaction_id,
            "file_url": file_url,
            "file_type": file_type,
        }
        response = self._get_response(method="post", endpoint=endpoint, params=params)

        attachment = MonzoAttachment(**response.json()["attachment"])

        return attachment

    def deregister(self, attachment_id: str) -> dict:
        """Deregister an attachment.

        Note:
            Monzo API docs: https://docs.monzo.com/#deregister-attachment

        Arguments:
            attachment_id: The ID of the attachment to deregister.

        Returns:
            API response.
        """
        endpoint = "/attachment/deregister"
        params = {"id": attachment_id}
        response = self._get_response(method="post", endpoint=endpoint, params=params)

        return response.json()
