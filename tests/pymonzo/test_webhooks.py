"""Test `pymonzo.webhooks` module."""

import httpx
import pytest
import respx
from polyfactory.factories.pydantic_factory import ModelFactory
from pytest_mock import MockerFixture

from pymonzo import MonzoAPI
from pymonzo.webhooks import MonzoWebhook, WebhooksResource

from .test_accounts import MonzoAccountFactory


class MonzoWebhookFactory(ModelFactory[MonzoWebhook]):
    """Factory for `MonzoWebhook` schema."""


@pytest.fixture(scope="module")
def webhooks_resource(monzo_api: MonzoAPI) -> WebhooksResource:
    """Initialize `WebhooksResource` resource with `monzo_api` fixture."""
    return WebhooksResource(client=monzo_api)


class TestWebhooksResource:
    """Test `WebhooksResource` class."""

    @pytest.mark.respx(base_url=MonzoAPI.api_url)
    def test_list_respx(
        self,
        mocker: MockerFixture,
        respx_mock: respx.MockRouter,
        webhooks_resource: WebhooksResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        webhook = MonzoWebhookFactory.build()
        webhook2 = MonzoWebhookFactory.build()

        account = MonzoAccountFactory.build()
        mocked_get_default_account = mocker.patch.object(
            webhooks_resource.client.accounts,
            "get_default_account",
        )
        mocked_get_default_account.return_value = account

        mocked_route = respx_mock.get(
            "/webhooks",
            params={"account_id": account.id},
        ).mock(
            return_value=httpx.Response(
                200,
                json={
                    "webhooks": [
                        webhook.model_dump(mode="json"),
                        webhook2.model_dump(mode="json"),
                    ]
                },
            )
        )

        webhooks_list_response = webhooks_resource.list()

        mocked_get_default_account.assert_called_once_with()

        assert isinstance(webhooks_list_response, list)
        for item in webhooks_list_response:
            assert isinstance(item, MonzoWebhook)

        assert webhooks_list_response == [webhook, webhook2]
        assert mocked_route.called

        # Explicitly passed account ID
        account_id = "TEST_ACCOUNT_ID"

        mocked_route = respx_mock.get(
            "/webhooks",
            params={"account_id": account_id},
        ).mock(
            return_value=httpx.Response(
                200,
                json={"webhooks": [webhook.model_dump(mode="json")]},
            )
        )

        webhooks_list_response = webhooks_resource.list(account_id=account_id)

        assert isinstance(webhooks_list_response, list)
        for item in webhooks_list_response:
            assert isinstance(item, MonzoWebhook)

        assert webhooks_list_response == [webhook]
        assert mocked_route.called

    @pytest.mark.respx(base_url=MonzoAPI.api_url)
    def test_register_respx(
        self,
        mocker: MockerFixture,
        respx_mock: respx.MockRouter,
        webhooks_resource: WebhooksResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        webhook = MonzoWebhookFactory.build()
        url = "TEST_URL"

        account = MonzoAccountFactory.build()
        mocked_get_default_account = mocker.patch.object(
            webhooks_resource.client.accounts,
            "get_default_account",
        )
        mocked_get_default_account.return_value = account

        mocked_route = respx_mock.post(
            "/webhooks",
            params={
                "account_id": account.id,
                "url": url,
            },
        ).mock(
            return_value=httpx.Response(
                200,
                json={"webhook": webhook.model_dump(mode="json")},
            )
        )

        webhooks_register_response = webhooks_resource.register(url=url)

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        assert webhooks_register_response == webhook
        assert mocked_route.called

        # Explicitly passed account ID
        account_id = "TEST_ACCOUNT_ID"

        mocked_route = respx_mock.post(
            "/webhooks",
            params={
                "account_id": account_id,
                "url": url,
            },
        ).mock(
            return_value=httpx.Response(
                200,
                json={"webhook": webhook.model_dump(mode="json")},
            )
        )

        webhooks_register_response = webhooks_resource.register(
            url=url, account_id=account_id
        )

        mocked_get_default_account.assert_not_called()
        mocked_get_default_account.reset_mock()

        assert webhooks_register_response == webhook
        assert mocked_route.called

    @pytest.mark.respx(base_url=MonzoAPI.api_url)
    def test_delete_respx(
        self,
        respx_mock: respx.MockRouter,
        webhooks_resource: WebhooksResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        webhook_id = "TEST_WEBHOOK_ID"

        mocked_route = respx_mock.delete(f"/webhooks/{webhook_id}").mock(
            return_value=httpx.Response(200, json={})
        )

        webhooks_delete_response = webhooks_resource.delete(webhook_id)

        assert webhooks_delete_response == {}
        assert mocked_route.called
