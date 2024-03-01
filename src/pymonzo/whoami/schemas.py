"""Monzo API 'whoami' related schemas."""

from pydantic import BaseModel

# Optional `rich` support
try:
    from rich.table import Table
except ImportError:
    RICH_AVAILABLE = False
else:
    RICH_AVAILABLE = True


class MonzoWhoAmI(BaseModel):
    """API schema for a 'whoami' object.

    Note:
        Monzo API docs: https://docs.monzo.com/#authenticating-requests

    Attributes:
        authenticated: Whether the user is authenticated.
        client_id: Client ID.
        user_id: User ID.
    """

    authenticated: bool
    client_id: str
    user_id: str

    if RICH_AVAILABLE:

        def __rich__(self) -> Table:
            """Pretty printing support for `rich`."""
            grid = Table.grid(padding=(0, 5))
            grid.add_column(style="bold yellow")
            grid.add_column()
            grid.add_row("Authenticated:", "Yes" if self.authenticated else "No")
            grid.add_row("Client ID:", self.client_id)
            grid.add_row("User ID:", self.user_id)

            return grid
