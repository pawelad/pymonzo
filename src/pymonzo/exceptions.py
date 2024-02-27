"""pymonzo exceptions."""


class PyMonzoError(Exception):
    """Base pymonzo exception."""


class NoSettingsFile(PyMonzoError):
    """No settings file found."""


class CannotDetermineDefaultAccount(PyMonzoError):
    """Cannot determine default account."""


class CannotDetermineDefaultPot(PyMonzoError):
    """Cannot determine default pot."""


class MonzoAPIError(PyMonzoError):
    """Catch all Monzo API error."""


class MonzoAccessDenied(MonzoAPIError):
    """Access to Monzo API has been denied."""
