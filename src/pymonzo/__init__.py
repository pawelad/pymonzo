"""Modern Python API client for [Monzo] public [API][Monzo API].

It exposes a [`pymonzo.MonzoAPI`][] class that can be used to access implemented
endpoints. HTTP requests are made with [httpx], data parsing and validation is done
with [pydantic].

[Monzo API]: https://docs.monzo.com/
[Monzo]: https://monzo.com/
[httpx]: https://github.com/encode/httpx
[pydantic]: https://github.com/pydantic/pydantic
"""

from pymonzo.client import MonzoAPI  # noqa

__title__ = "pymonzo"
__description__ = "Modern Python API client for Monzo public API."
__version__ = "2.2.0"
__url__ = "https://github.com/pawelad/pymonzo"
__author__ = "Paweł Adamczak"
__email__ = "pawel.ad@gmail.com"
__license__ = "MPL-2.0"
