# Getting Started
Before starting, please take note of these warnings from [Monzo API docs]:

!!! warning "The Monzo Developer API is not suitable for building public applications"

    You may only connect to your own account or those of a small set of users you
    explicitly allow. Please read our [blog post](https://monzo.com/blog/2017/05/11/api-update/)
    for more detail.

!!! warning "Strong Customer Authentication"

    After a user has authenticated, your client can fetch all of their transactions,
    and after 5 minutes, it can only sync the last 90 days of transactions. If you
    need the user’s entire transaction history, you should consider fetching and
    storing it right after authentication.

## Installation
From [PyPI] (ideally, inside a [virtualenv]):

```console
$ python -m pip install pymonzo
```

## Authentication
Monzo API implements OAuth 2.0 authorization code grant type. To use it, you need
to first create an OAuth client in Monzo [developer tools][monzo developer tools].

You should set the "Redirect URLs" to `http://localhost:6600/pymonzo` and set the
client as confidential if you want the access token to be refreshed automatically
(name, description and logo don't really matter).

That should give you a client ID and client secret, which you need to pass to
[`pymonzo.MonzoAPI.authorize`][] function:

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
>>> from pymonzo import MonzoAPI
>>> monzo_api = MonzoAPI()
>>> monzo_api.whoami()
MonzoWhoAmI(authenticated=True, client_id='oauth2client_***', user_id='user_***')
```

## Usage
All implemented API endpoints are grouped into resources and 'mounted' to the
[`pymonzo.MonzoAPI`][] class:

```pycon
>>> from pymonzo import MonzoAPI
>>> monzo_api = MonzoAPI()
>>> accounts = monzo_api.accounts.list()
>>> # If you have only one active account, you don't need to pass account ID
>>> balance = monzo_api.balance.get(account_id=accounts[0].id)
>>> pots = monzo_api.pots.list()
>>> # Similarly, if you have only one active pot, you don't need to pass pot ID
>>> monzo_api.pots.deposit(amount=5, pot_id=pots[0].id)
>>> # Remember that you can fetch all transactions only within 5 minutes of being authenticated
>>> transactions = monzo_api.transactions.list()
```

You can find all mounted resources, implemented endpoints and their arguments by
looking at [`pymonzo.MonzoAPI`][] docs.


[monzo developer tools]: https://developers.monzo.com/
[monzo api docs]: https://docs.monzo.com/
[pypi]: https://pypi.org/
[virtualenv]: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
