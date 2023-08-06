"""AL-KO: Exceptions"""


class AlkoException(Exception):
    """Raise this when something is off."""


class AlkoAuthenticationException(AlkoException):
    """Raise this when there is an authentication issue."""
