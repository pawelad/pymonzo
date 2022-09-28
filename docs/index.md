# pymonzo
[![Package Version](https://img.shields.io/pypi/v/pymonzo)][pypi pymonzo]
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/pymonzo)][pypi pymonzo]
[![License](https://img.shields.io/pypi/l/pymonzo)][license]
[![py.typed](https://img.shields.io/badge/py-typed-green)][rickyroll]
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

Modern Python API client for [Monzo][monzo] public [API][monzo docs].

- Works on Python 3.7+
- Fully type annotated
- Explicitly defined and validated API schemas (via [pydantic])
- Easy authentication with automatic access token refreshing
- Nice defaults - don't specify account / pot ID if you only have one active


[black]: https://github.com/psf/black
[license]: license.md
[monzo]: https://monzo.com/
[monzo docs]: https://docs.monzo.com/
[pydantic]: https://github.com/pydantic/pydantic
[pypi pymonzo]: https://pypi.org/project/pymonzo/
[rickyroll]: https://www.youtube.com/watch?v=I6OXjnBIW-4&t=15s
