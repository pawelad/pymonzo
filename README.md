# pymonzo
[![Build Status](https://img.shields.io/travis/pawelad/pymonzo.svg)][travis]
[![PyPI Version](https://img.shields.io/pypi/v/pymonzo.svg)][pypi]
[![Python Versions](https://img.shields.io/pypi/pyversions/pymonzo.svg)][pypi]
[![License](https://img.shields.io/github/license/pawelad/pymonzo.svg)][license]

Python library that nicely wraps [Monzo][monzo] public API and allows you to use
it directly from your Python project.

To use the library you have to provide it with you Monzo access token. You can
either do that by exporting it as an environment variable
(`$ export MONZO_ACCESS_TOKEN="YOUR_ACTUAL_ACCESS_TOKEN"`) or by passing it
explicitly to `MonzoAPI()`.

The library currently does not implement feed items, webhooks and attachments
endpoints - I plan to add them in the future, but they were't essential to my
current needs and they could be completely different in the future - per
[docs][monzo docs inroduction]:
> The Monzo API is under active development. Breaking changes should be expected.

The major addition I do want to add is better authentication support - currently
access tokens can be taken directly from the developer playground and only last
a couple of hours which is really annoying.

## Installation
From PyPI:
```shell
$ pip install pymonzo
```

## API
There's no documentation as of now, but the code is commented and
*should* be pretty straightforward to use.

But feel free to ask me via [mail](mailto:pawel.adamczak@sidnet.info) or 
[GitHub issues][github add issue] if anything is unclear.

## Tests
Package was tested with `pytest` and `tox` on Python 2.7, 3.4 and 3.5
(see `tox.ini`).

To run tests yourself you need to set environment variables with access token
before running `tox` inside the repository:
```shell
$ export MONZO_ACCESS_TOKEN="YOUR_ACTUAL_ACCESS_TOKEN"
$ tox
```

## Contributions
Package source code is available at [GitHub][github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest enhancements
and point out any mistakes.

## Authors
Developed and maintained by [Paweł Adamczak][pawelad].

Released under [MIT License][[license]].


[travis]: https://travis-ci.org/pawelad/pymonzo
[pypi]: https://pypi.python.org/pypi/pymonzo
[license]: https://github.com/pawelad/pymonzo/blob/master/LICENSE
[monzo]: https://monzo.com/
[monzo docs inroduction]: https://monzo.com/docs/#introduction
[github add issue]: https://github.com/pawelad/pymonzo
[github]: https://github.com/pawelad/pymonzo
[pawelad]: https://github.com/pawelad
