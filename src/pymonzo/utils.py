"""pymonzo utils."""

import locale
from datetime import datetime, timedelta
from typing import Any, Callable, List, Tuple
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri


def n_days_ago(n: int) -> datetime:
    """Return datetime that was `n` days ago.

    Arguments:
        n: Number of days to go back.

    Returns:
        Datetime that was `n` days ago.
    """
    today = datetime.now()
    delta = timedelta(days=n)
    return today - delta


def empty_str_to_none(v: Any) -> Any:
    """Return `None` passed value is an empty string, otherwise do nothing.

    Arguments:
        v: Value to check.

    Returns:
        Passed value or `None` if it's an empty string.
    """
    if isinstance(v, str) and v == "":
        return None

    return v


def empty_dict_to_none(v: Any) -> Any:
    """Return `None` if the passed value is an empty dict, otherwise do nothing.

    Arguments:
        v: Value to check.

    Returns:
        Passed value or `None` if it's an empty dict.
    """
    if isinstance(v, dict) and not bool(v):
        return None

    return v


def format_datetime(dt: datetime) -> str:
    """Format passed `datetime` in user locale.

    Used as a fallback when `babel` isn't available.

    Arguments:
        dt: Datetime to format.

    Returns:
        Passed `datetime` formatted in user locale.
    """
    return dt.strftime(locale.nl_langinfo(locale.D_T_FMT))


def format_currency(amount: float, currency: str) -> str:
    """Format passed amount with two decimal places.

    Used as a fallback when `babel` isn't available.

    Arguments:
        amount: Amount of money.
        currency: Money currency. Unused here, but needed to match the signature
            with `babel.numbers.format_currency`.

    Returns:
        Passed amount with two decimal places.
    """
    return f"{amount:.2f}"


class WSGIApp:
    """Bare-bones WSGI app made for retrieving the OAuth callback."""

    last_request_uri = ""

    def __call__(
        self,
        environ: dict,
        start_response: Callable[[str, List[Tuple[str, str]]], None],
    ) -> List[bytes]:
        """Implement WSGI interface and save the URL of the callback."""
        start_response("200 OK", [("Content-type", "text/plain; charset=utf-8")])
        self.last_request_uri = request_uri(environ)
        msg = "Monzo OAuth authorization complete."
        return [msg.encode("utf-8")]


def get_authorization_response_url(host: str, port: int) -> str:
    """Get OAuth authorization response URL.

    It's done by creating a bare-bones HTTP server and retrieving a single request,
    the OAuth callback.

    Arguments:
        host: temporary HTTP server host name.
        port: temporary HTTP server port.

    Returns:
        URL of the OAuth authorization response.
    """
    wsgi_app = WSGIApp()
    with make_server(host, port, wsgi_app) as server:  # type: ignore
        server.handle_request()

    return wsgi_app.last_request_uri
