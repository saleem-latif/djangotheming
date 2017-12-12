"""
Module to contain all of the exceptions defined and used by the theming app.
"""


class ThemeException(Exception):
    """
    Base exception for all theming related exceptions.
    """

    pass


class MiddlewareNotActivatedError(ThemeException):
    """
    Exception raised when features being used depends on a theming middleware.
    """

    pass
