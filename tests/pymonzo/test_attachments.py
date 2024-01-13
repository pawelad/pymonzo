"""Test `pymonzo.attachments` module."""
import httpx
import pytest
import respx
from polyfactory.factories.pydantic_factory import ModelFactory

from pymonzo import MonzoAPI
from pymonzo.attachments import AttachmentsResource, MonzoAttachmentResponse


class MonzoAttachmentResponseFactory(ModelFactory[MonzoAttachmentResponse]):
    """Factory for `MonzoAttachmentResponse` schema."""


@pytest.fixture(scope="module")
def attachments_resource(monzo_api: MonzoAPI) -> AttachmentsResource:
    """Initialize `AttachmentsResource` resource with `monzo_api` fixture."""
    return AttachmentsResource(client=monzo_api)


class TestAttachmentsResource:
    """Test `AttachmentsResource` class."""

    @pytest.mark.respx(base_url=MonzoAPI.api_url)
    def test_upload_respx(
        self,
        respx_mock: respx.MockRouter,
        attachments_resource: AttachmentsResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        file_name = "TEST_FILE_NAME"
        file_type = "TEST_FILE_TYPE"
        content_length = 1
        attachment_response = MonzoAttachmentResponseFactory.build()

        mocked_route = respx_mock.post(
            "/attachment/upload",
            params={
                "file_name": file_name,
                "file_type": file_type,
                "content_length": content_length,
            },
        ).mock(return_value=httpx.Response(200, json=attachment_response.dict()))

        attachment_upload_response = attachments_resource.upload(
            file_name=file_name,
            file_type=file_type,
            content_length=content_length,
        )

        assert attachment_upload_response == attachment_response
        assert mocked_route.called
