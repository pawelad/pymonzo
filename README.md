# pymonzo
[![PyPI version](https://img.shields.io/pypi/v/pymonzo.svg)][pypi]
[![Python versions](https://img.shields.io/pypi/pyversions/pymonzo.svg)][pypi]
[![License](https://img.shields.io/github/license/pawelad/pymonzo.svg)][license]

[![Build status](https://img.shields.io/travis/pawelad/pymonzo.svg)][travis]
[![Test coverage](https://img.shields.io/coveralls/pawelad/pymonzo.svg)][coveralls]

Python library that nicely wraps [Monzo][monzo] public API and allows you to use
it directly from your Python project.

## Installation
From PyPI:
```shell
$ pip install pymonzo
```

## Usage
To use the library you have to provide it with you Monzo access token. You can
either do that by exporting it as an environment variable
(`$ export MONZO_ACCESS_TOKEN="YOUR_ACTUAL_ACCESS_TOKEN"`) or by passing it
explicitly to `MonzoAPI()` class.

## Roadmap
The library currently does not implement feed items, webhooks and attachments
endpoints - I plan to add them in the future, but they were't essential to my
current needs and they could be completely different in the future - per
[docs][monzo docs inroduction]:
> The Monzo API is under active development. Breaking changes should be expected.

I want to implement all API functionality as soon as it comes out of beta and
stabilizes.

The major addition I do want to add before that is better authentication
support - currently access tokens can be taken only from the
[developer playground][monzo developer playground] and work for just a couple of
hours before expiring which is really annoying.
I chatted with Monzo devs in their Slack accout and currently there's no way to
get and regresh the access token for background only applications (without
OAuth authorization code grant and a website that is).

## API
There's no documentation as of now, but the code is commented and
*should* be pretty straightforward to use.

But feel free to ask me via [email](mailto:pawel.adamczak@sidnet.info) or 
[GitHub issues][github add issue] if anything is unclear.

## Tests
Package was tested with the help of `py.test` and `tox` on Python 2.7, 3.4
and 3.5 (see `tox.ini`).

To run tests yourself you need to set environment variables with access token
before running `tox` inside the repository:
```shell
$ export MONZO_ACCESS_TOKEN="YOUR_ACTUAL_ACCESS_TOKEN"
$ tox
```

## Contributions
Package source code is available at [GitHub][github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest enhancements,
add functionality and point out any mistakes.

## Authors
Developed and maintained by [Paweł Adamczak][pawelad].

Released under [MIT License][license].


[coveralls]: https://coveralls.io/github/pawelad/pymonzo
[github add issue]: https://github.com/pawelad/pymonzo/issues/new
[github]: https://github.com/pawelad/pymonzo
[license]: https://github.com/pawelad/pymonzo/blob/master/LICENSE
[monzo developer playground]: https://developers.getmondo.co.uk/api/playground
[monzo docs inroduction]: https://monzo.com/docs/#introduction
[monzo]: https://monzo.com/
[pawelad]: https://github.com/pawelad
[pypi]: https://pypi.python.org/pypi/pymonzo
[travis]: https://travis-ci.org/pawelad/pymonzo
