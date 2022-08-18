"""
pymonzo utils
"""
from typing import Callable, List, Tuple
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri


class WSGIApp:
    """
    Bare-bones WSGI app made for retrieving the OAuth callback.
    """

    last_request_uri = ""

    def __call__(
        self,
        environ: dict,
        start_response: Callable[[str, List[Tuple[str, str]]], None],
    ) -> List[bytes]:
        """
        Implement WSGI interface and save the URL of the callback.
        """
        start_response("200 OK", [("Content-type", "text/plain; charset=utf-8")])
        self.last_request_uri = request_uri(environ)
        msg = "Monzo OAuth authorization complete."
        return [msg.encode("utf-8")]


def get_authorization_response(host: str, port: int) -> str:
    """
    Get OAuth authorization response by creating a bare-bones HTTP server and
    retrieving the OAuth callback.
    """
    wsgi_app = WSGIApp()
    with make_server(host, port, wsgi_app) as server:  # type: ignore
        server.handle_request()

    return wsgi_app.last_request_uri
