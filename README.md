# pymonzo
[![Package Version](https://img.shields.io/pypi/v/pymonzo)][pypi pymonzo]
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pymonzo)][pypi pymonzo]
[![License](https://img.shields.io/pypi/l/pymonzo)](./LICENSE)
[![py.typed](https://img.shields.io/badge/py-typed-green)][rickyroll]
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

Modern Python API client for [Monzo][monzo] public [API][monzo docs].

- Works on Python 3.7+
- Fully type annotated
- Explicitly defined and validated API schemas (via [pydantic])
- Easy [authentication](#authentication) with automatic access token refreshing
- Nice defaults - don't specify account / pot ID if you only have one active

## Installation
From [PyPI][pypi] (ideally, inside a [virtualenv]):

```console
$ python -m pip install pymonzo
```

## Usage
Here's an example of what `pymonzo` can do:

```pycon
>>> from pymonzo import MonzoAPI
>>> monzo_api = MonzoAPI()
>>> accounts = monzo_api.accounts.list()
>>> len(accounts)
2
>>> # Only one active account, so we don't need to pass it explicitly
>>> monzo_api.balance.get()
MonzoBalance(balance=75000, total_balance=95012, currency='GBP', spend_today=0, balance_including_flexible_savings=95012, local_currency='', local_exchange_rate=0, local_spend=[])
>>> from pymonzo.utils import n_days_ago
>>> transactions = monzo_api.transactions.list(since=n_days_ago(5))
>>> len(transactions)
8
```

### Authentication
Monzo API implements OAuth 2.0 authorization code grant type. To use it, you need
to first create an OAuth client in Monzo [developer tools][monzo developer tools].
You should set the "Redirect URLs" to `http://localhost:6600/pymonzo` and set the
client as confidential if you want the access token to be refreshed automatically
(name, description and logo don't really matter).

That should give you a client ID and client secret, which you need to pass to
`MonzoAPI.authorize()` function:

```pycon
>>> from pymonzo import MonzoAPI
>>> MonzoAPI.authorize(
    client_id="oauth2client_***",
    client_secret="mnzconf.***",
)
2022-09-15 20:21.37 [info     ] Please visit this URL to authorize: https://auth.monzo.com/?response_type=code&client_id=oauth2client_***&redirect_uri=http%3A%2F%2Flocalhost%3A6600%2Fpymonzo&state=PY5VAKZwwrdOz8qyzzEojb90vFp78S
```

This should open a new web browser tab (if it didn't, go to the link from the
log message) that will let you authorize the OAuth client you just created. If
everything goes well, you should be redirected to `http://localhost:6600/pymonzo`
and greeted with `Monzo OAuth authorization complete.` message.

Note that you might need to open your mobile app to allow full access to your account.

That's it! The access token is saved locally at `~/.pymonzo` and - as long as you set
the OAuth client as confidential - should be refreshed automatically when it expires.

```pycon
>>> monzo_api = MonzoAPI()
>>> monzo_api.whoami()
MonzoWhoAmI(authenticated=True, client_id='oauth2client_***', user_id='user_***')
```

## Implemented endpoints
Currently, only transaction receipts endpoints are not implemented:

- [x] GET `/ping/whoami`
- [x] GET `/accounts`
- [x] GET `/balance`
- [x] GET `/pots`
- [x] PUT `/pots/$pot_id/deposit`
- [x] PUT `/pots/$pot_id/withdraw`
- [x] GET `/transactions`
- [x] GET `/transactions/$transaction_id`
- [x] PATCH `/transactions/$transaction_id`
- [x] POST `/feed`
- [x] POST `/attachment/upload`
- [x] POST `/attachment/register`
- [x] POST `/attachment/deregister`
- [ ] GET `/transaction-receipts`
- [ ] PUT `/transaction-receipts`
- [ ] DELETE `/transaction-receipts`
- [x] GET `/webhooks`
- [x] POST `/webhooks`
- [x] DELETE `/webhooks/$webhook_id`

## Authors
Developed and maintained by [Paweł Adamczak][pawelad].

If you'd like to contribute, please take a look at [CONTRIBUTING.md](CONTRIBUTING.md).

Released under [Mozilla Public License 2.0](./LICENSE).


[black]: https://github.com/psf/black
[github pymonzo]: https://github.com/pawelad/pymonzo
[monzo]: https://monzo.com/
[monzo developer tools]: https://developers.monzo.com/
[monzo docs]: https://docs.monzo.com/
[pawelad]: https://pawelad.me/
[pydantic]: https://github.com/pydantic/pydantic
[pypi]: https://pypi.org/
[pypi pymonzo]: https://pypi.org/project/pymonzo/
[rickyroll]: https://www.youtube.com/watch?v=I6OXjnBIW-4&t=15s
[virtualenv]: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
