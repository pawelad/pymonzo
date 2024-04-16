# pymonzo
[![Package Version](https://img.shields.io/pypi/v/pymonzo)][pypi pymonzo]
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pymonzo)][pypi pymonzo]
[![Read the Docs](https://img.shields.io/readthedocs/pymonzo)][rtfd pymonzo]
[![Codecov](https://img.shields.io/codecov/c/github/pawelad/pymonzo)][codecov pymonzo]
[![License](https://img.shields.io/pypi/l/pymonzo)][license]
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]
[![py.typed](https://img.shields.io/badge/py-typed-FFD43B)][rickroll]

Modern Python API client for [Monzo] public [API][monzo api docs].

- Works on Python 3.8+
- Fully type annotated
- Explicitly defined and validated API schemas (via [pydantic])
- Easy authentication with automatic access token refreshing
- Sensible defaults - don't specify account / pot ID if you only have one active
- Optional [rich] support for pretty printing

This project is not officially affiliated with [Monzo].

## Installation
From [PyPI] (ideally, inside a [virtualenv]):

```console
$ python -m pip install pymonzo
```

## Quick start
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

## Authors
Developed and maintained by [Paweł Adamczak][pawelad].

Source code is available at [GitHub][github pymonzo].

If you'd like to contribute, please take a look at the
[contributing guide].

Released under [Mozilla Public License 2.0][license].


[black]: https://github.com/psf/black
[codecov pymonzo]: https://app.codecov.io/github/pawelad/pymonzo
[contributing guide]: ./CONTRIBUTING.md
[github pymonzo]: https://github.com/pawelad/pymonzo
[license]: ./LICENSE
[monzo api docs]: https://docs.monzo.com/
[monzo developer tools]: https://developers.monzo.com/
[monzo]: https://monzo.com/
[pawelad]: https://pawelad.me/
[pydantic]: https://github.com/pydantic/pydantic
[pypi pymonzo]: https://pypi.org/project/pymonzo/
[pypi]: https://pypi.org/
[rich]: https://github.com/Textualize/rich
[rickroll]: https://www.youtube.com/watch?v=I6OXjnBIW-4&t=15s
[rtfd pymonzo]: https://pymonzo.rtfd.io/
[virtualenv]: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
