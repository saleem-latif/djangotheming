

class ThemeException(Exception):
    pass


class MiddlewareNotActivatedError(ThemeException):
    """
    Exception raised when features being used depend on a middleware.
    """
    pass
