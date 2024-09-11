"""Test `pymonzo.pots` module."""

import os

import httpx
import pytest
import respx
from polyfactory.factories.pydantic_factory import ModelFactory
from pytest_mock import MockerFixture

from pymonzo import MonzoAPI
from pymonzo.exceptions import CannotDetermineDefaultPot
from pymonzo.pots import MonzoPot, PotsResource

from .test_accounts import MonzoAccountFactory


class MonzoPotFactory(ModelFactory[MonzoPot]):
    """Factory for `MonzoPot` schema."""


@pytest.fixture(scope="module")
def pots_resource(monzo_api: MonzoAPI) -> PotsResource:
    """Initialize `PotsResource` resource with `monzo_api` fixture."""
    return PotsResource(client=monzo_api)


class TestPotsResource:
    """Test `PotsResource` class."""

    def test_get_default_pot(
        self,
        mocker: MockerFixture,
        pots_resource: PotsResource,
    ) -> None:
        """Pot is presented as default if there is only one (active) pot."""
        # Set up a default account
        account = MonzoAccountFactory.build()

        mocked_get_default_account = mocker.patch.object(
            pots_resource.client.accounts,
            "get_default_account",
        )
        mocked_get_default_account.return_value = account

        # Mock `.list()` method
        mocked_pots_list = mocker.patch.object(pots_resource, "list")

        active_pot = MonzoPotFactory.build(deleted=False)
        active_pot2 = MonzoPotFactory.build(deleted=False)
        deleted_pot = MonzoPotFactory.build(deleted=True)
        deleted_pot2 = MonzoPotFactory.build(deleted=True)

        # No pots
        mocked_pots_list.return_value = []

        with pytest.raises(CannotDetermineDefaultPot):
            pots_resource.get_default_pot()

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        mocked_pots_list.assert_called_once_with(account.id)
        mocked_pots_list.reset_mock()

        # One account, none active
        mocked_pots_list.return_value = [deleted_pot]

        default_pot = pots_resource.get_default_pot()

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        mocked_pots_list.assert_called_once_with(account.id)
        mocked_pots_list.reset_mock()

        assert default_pot == deleted_pot
        assert default_pot.id == deleted_pot.id
        assert default_pot.deleted is True

        # One account, one active
        mocked_pots_list.return_value = [active_pot]

        default_pot = pots_resource.get_default_pot()

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        mocked_pots_list.assert_called_once_with(account.id)
        mocked_pots_list.reset_mock()

        assert default_pot == active_pot
        assert default_pot.id == active_pot.id
        assert default_pot.deleted is False

        # Two accounts, none active
        mocked_pots_list.return_value = [deleted_pot, deleted_pot2]

        with pytest.raises(CannotDetermineDefaultPot):
            pots_resource.get_default_pot()

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        mocked_pots_list.assert_called_once_with(account.id)
        mocked_pots_list.reset_mock()

        # Two accounts, one active
        mocked_pots_list.return_value = [deleted_pot, active_pot]

        default_pot = pots_resource.get_default_pot()

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        mocked_pots_list.assert_called_once_with(account.id)
        mocked_pots_list.reset_mock()

        assert default_pot == active_pot
        assert default_pot.id == active_pot.id
        assert default_pot.deleted is False

        # Two accounts, two active
        mocked_pots_list.return_value = [active_pot, active_pot2]

        with pytest.raises(CannotDetermineDefaultPot):
            pots_resource.get_default_pot()

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        mocked_pots_list.assert_called_once_with(account.id)
        mocked_pots_list.reset_mock()

    @pytest.mark.vcr()
    @pytest.mark.skipif(
        not bool(os.getenv("VCRPY_ENCRYPTION_KEY")),
        reason="`VCRPY_ENCRYPTION_KEY` is not available on GitHub PRs.",
    )
    def test_list_vcr(self, pots_resource: PotsResource) -> None:
        """API response is parsed into expected schema."""
        pots_list = pots_resource.list()

        assert isinstance(pots_list, list)
        for pot in pots_list:
            assert isinstance(pot, MonzoPot)

    @pytest.mark.respx(base_url=MonzoAPI.api_url)
    def test_deposit_respx(
        self,
        mocker: MockerFixture,
        respx_mock: respx.MockRouter,
        pots_resource: PotsResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        # Mock `get_default_account()`
        account = MonzoAccountFactory.build()
        mocked_get_default_account = mocker.patch.object(
            pots_resource.client.accounts,
            "get_default_account",
        )
        mocked_get_default_account.return_value = account

        # Mock `get_default_pot()`
        pot = MonzoPotFactory.build()
        mocked_get_default_pot = mocker.patch.object(
            pots_resource,
            "get_default_pot",
        )
        mocked_get_default_pot.return_value = pot

        # Mock `token_urlsafe`
        token = "TEST_TOKEN"  # noqa
        mocked_token_urlsafe = mocker.patch(
            "pymonzo.pots.resources.token_urlsafe",
            autospec=True,
        )
        mocked_token_urlsafe.return_value = token

        # Mock `httpx`
        amount = 42
        endpoint = f"/pots/{pot.id}/deposit"
        data = {
            "source_account_id": account.id,
            "amount": amount,
            "dedupe_id": token,
        }
        mocked_route = respx_mock.put(endpoint, data=data).mock(
            return_value=httpx.Response(
                200,
                json=pot.model_dump(mode="json"),
            )
        )

        pots_deposit_response = pots_resource.deposit(amount)

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        mocked_get_default_pot.assert_called_once_with(account.id)
        mocked_get_default_pot.reset_mock()

        mocked_token_urlsafe.assert_called_once_with(16)
        mocked_token_urlsafe.reset_mock()

        assert pots_deposit_response == pot
        assert mocked_route.called

        # Explicitly passed account ID, pot ID and dedupe ID
        account_id = "TEST_ACCOUNT_ID"
        pot_id = "TEST_POT_ID"
        dedupe_id = "TEST_DEDUPE_ID"

        amount = 42
        endpoint = f"/pots/{pot_id}/deposit"
        data = {
            "source_account_id": account_id,
            "amount": amount,
            "dedupe_id": dedupe_id,
        }
        mocked_route = respx_mock.put(endpoint, data=data).mock(
            return_value=httpx.Response(
                200,
                json=pot.model_dump(mode="json"),
            )
        )

        pots_deposit_response = pots_resource.deposit(
            amount=amount,
            pot_id=pot_id,
            account_id=account_id,
            dedupe_id=dedupe_id,
        )

        mocked_get_default_account.assert_not_called()
        mocked_get_default_account.reset_mock()

        mocked_get_default_pot.assert_not_called()
        mocked_token_urlsafe.reset_mock()

        mocked_token_urlsafe.assert_not_called()
        mocked_token_urlsafe.reset_mock()

        assert pots_deposit_response == pot
        assert mocked_route.called

    @pytest.mark.respx(base_url=MonzoAPI.api_url)
    def test_withdraw_respx(
        self,
        mocker: MockerFixture,
        respx_mock: respx.MockRouter,
        pots_resource: PotsResource,
    ) -> None:
        """Correct API response is sent, API response is parsed into expected schema."""
        # Mock `get_default_account()`
        account = MonzoAccountFactory.build()
        mocked_get_default_account = mocker.patch.object(
            pots_resource.client.accounts,
            "get_default_account",
        )
        mocked_get_default_account.return_value = account

        # Mock `get_default_pot()`
        pot = MonzoPotFactory.build()
        mocked_get_default_pot = mocker.patch.object(
            pots_resource,
            "get_default_pot",
        )
        mocked_get_default_pot.return_value = pot

        # Mock `token_urlsafe`
        token = "TEST_TOKEN"  # noqa
        mocked_token_urlsafe = mocker.patch(
            "pymonzo.pots.resources.token_urlsafe",
            autospec=True,
        )
        mocked_token_urlsafe.return_value = token

        # Mock `httpx`
        amount = 42
        endpoint = f"/pots/{pot.id}/withdraw"
        data = {
            "destination_account_id": account.id,
            "amount": amount,
            "dedupe_id": token,
        }
        mocked_route = respx_mock.put(endpoint, data=data).mock(
            return_value=httpx.Response(
                200,
                json=pot.model_dump(mode="json"),
            )
        )

        pots_deposit_response = pots_resource.withdraw(amount)

        mocked_get_default_account.assert_called_once_with()
        mocked_get_default_account.reset_mock()

        mocked_get_default_pot.assert_called_once_with(account.id)
        mocked_get_default_pot.reset_mock()

        mocked_token_urlsafe.assert_called_once_with(16)
        mocked_token_urlsafe.reset_mock()

        assert pots_deposit_response == pot
        assert mocked_route.called

        # Explicitly passed account ID, pot ID and dedupe ID
        account_id = "TEST_ACCOUNT_ID"
        pot_id = "TEST_POT_ID"
        dedupe_id = "TEST_DEDUPE_ID"

        amount = 42
        endpoint = f"/pots/{pot_id}/withdraw"
        data = {
            "destination_account_id": account_id,
            "amount": amount,
            "dedupe_id": dedupe_id,
        }
        mocked_route = respx_mock.put(endpoint, data=data).mock(
            return_value=httpx.Response(
                200,
                json=pot.model_dump(mode="json"),
            )
        )

        pots_deposit_response = pots_resource.withdraw(
            amount=amount,
            pot_id=pot_id,
            account_id=account_id,
            dedupe_id=dedupe_id,
        )

        mocked_get_default_account.assert_not_called()
        mocked_get_default_account.reset_mock()

        mocked_get_default_pot.assert_not_called()
        mocked_token_urlsafe.reset_mock()

        mocked_token_urlsafe.assert_not_called()
        mocked_token_urlsafe.reset_mock()

        assert pots_deposit_response == pot
        assert mocked_route.called
