# pymonzo
[![Build status](https://img.shields.io/travis/pawelad/pymonzo.svg)][travis]
[![Test coverage](https://img.shields.io/coveralls/pawelad/pymonzo.svg)][coveralls]
[![PyPI version](https://img.shields.io/pypi/v/pymonzo.svg)][pypi]
[![Python versions](https://img.shields.io/pypi/pyversions/pymonzo.svg)][pypi]
[![License](https://img.shields.io/github/license/pawelad/pymonzo.svg)][license]

An - dare I say it - awesome Python [Monzo][monzo] public API wrapper.

It creates a layer of abstraction and returns Python objects instead of just
passing along the received JSONs. It also deals with authentication and allows
using either an access token or fully authenticate via OAuth 2 that's a
[PITA to set up](#oauth-2) but also automatically refreshes in the background.

## Installation
From PyPI:

```
$ pip install pymonzo
```

## Authentication

### Access token
If you want to just play around then you can simply get the access token taken
from [Monzo API Playground][monzo api playground], either pass it explicitly to
`MonzoAPI()` class or save it as an environment variable
(`$ export MONZO_ACCESS_TOKEN='...'`) and you're good to go. Everything works
as expected _but_ the token is valid only for couple of hours.

### OAuth 2
The second authentication option is to go through OAuth 2, which doesn't sound
bad (everyone is using it!) but from my experience is a PITA when setting up
for server side applications. So.

Some technical background: Monzo currently only allows OAuth 2 'authorization 
code' grant type and automatic token refreshing is only allowed for
'confidential' clients.

First, you need to create an OAuth client [here][monzo api client]. Name and
logo don't really matter but you need to set the redirect URL to this repo
(`https://github.com/pawelad/pymonzo`) and make it confidential.

Got it? Cool. You should be redirected to the overview of your new OAuth client
(`https://developers.monzo.com/apps/oauthclient_XXX`). You need two things from
that page, the 'Client ID' and 'Client secret'. The last required piece is the
auth code, which you can get by creating a link like the one below but with your
client ID:

```
https://auth.getmondo.co.uk/?response_type=code&redirect_uri=https://github.com/pawelad/pymonzo&client_id={{CLIENT_ID}}
```

You then go to the link and authorise the app. You should get an email with a
link back to the GitHub repo which contains the authorization code as an URL
parameter, something like:

```
https://github.com/pawelad/pymonzo?code={{AUTH_CODE}}&state=
```

You now have all three needed values - client ID, client secret and the auth
code. You can now either pass them directly to `MonzoAPI()` class:

```python
>> from pymonzo import MonzoAPI
>> monzo = MonzoAPI(
    client_id='...',
    client_secret='...',
    auth_code='...',
)
```

or save them as environment variables and initialize `MonzoAPI()` without any
arguments:

```shell
$ export MONZO_CLIENT_ID='...'
$ export MONZO_CLIENT_SECRET='...'
$ export MONZO_AUTH_CODE='...'
```

That's it! The token is then saved on the disk (`~/.pymonzo`) and is
automatically refreshed when needed, so all this (_should_) be one time only.

## API
There's no proper documentation as of now, but the code is commented and
*should* be pretty straightforward to use.

That said - feel free to open a [GitHub issues][github add issue] if anything
is unclear.

## Tests
Package was tested with the help of `py.test` and `tox` on Python 2.7, 3.4, 3.5
and 3.6 (see `tox.ini`).

Code coverage is available at [Coveralls][coveralls].

To run tests yourself you need to run `tox` inside the repository:

```shell
$ git clone
$ pip install tox
$ tox
```

## Contributions
Package source code is available at [GitHub][github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest enhancements,
add functionality and point out any mistakes. Thanks!

## Authors
Developed and maintained by [Paweł Adamczak][pawelad].

Released under [MIT License][license].


[coveralls]: https://coveralls.io/github/pawelad/pymonzo
[github add issue]: https://github.com/pawelad/pymonzo/issues/new
[github]: https://github.com/pawelad/pymonzo
[license]: https://github.com/pawelad/pymonzo/blob/master/LICENSE
[monz]: https://github.com/pawelad/monz
[monzo]: https://monzo.com/
[monzo api client]: https://developers.getmondo.co.uk/apps/home
[monzo api playground]: https://developers.getmondo.co.uk/api/playground
[monzo docs introduction]: https://monzo.com/docs/#introduction
[pawelad]: https://github.com/pawelad
[pypi]: https://pypi.python.org/pypi/pymonzo
[travis]: https://travis-ci.org/pawelad/pymonzo
