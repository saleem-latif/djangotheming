# -*- coding: utf-8 -*-
"""
Thread scoped variables.
"""

from threading import local

from theming.exceptions import MiddlewareNotActivated

__thread_locals__ = local()


def set_thread_variable(key, value):
    """
    Set thread variable with the given key, value pair.

    Arguments:
        key (str): Name of the thread variable.
        value (object): Value of the thread variable.

    Example:
        >>> set_thread_variable('current_theme_name', "test-theme")
    """
    setattr(__thread_locals__, key, value)


def get_thread_variable(key, default=None):
    """
    Get thread variable with the given key. Return `default` if key not found in thread data.

    Arguments:
        key (str): Name of the thread variable.
        default (object): Value to return if variable with given key is not present in thread data.

    Example:
        >>> get_thread_variable('current_theme_name', "default-theme")
        "default-theme"
        >>> set_thread_variable('current_theme_name', "test-theme")
        >>> get_thread_variable('current_theme_name', "default-theme")
        "test-theme"
    """
    return getattr(__thread_locals__, key, default)


def set_request_variable(key, value):
    """
    Set request variable with the given key, value pair.

    Arguments:
        key (str): Name of the request variable.
        value (object): Value of the request variable.

    Example:
        >>> set_request_variable('current_theme_name', "test-theme")
    """
    request = get_current_request()
    if not request:
        raise MiddlewareNotActivated(
            "Unable to get request object. Make sure CurrentRequestMiddleware is installed",
        )

    return setattr(request, key, value)


def get_request_variable(key, default=None):
    """
    Get request variable with the given key. Return `default` if key not found in thread data.

    Arguments:
        key (str): Name of the request variable.
        default (object): Value to return if variable with given key is not present in request data.

    Example:
        >>> get_request_variable('current_theme_name', "default-theme")
        "default-theme"
        >>> set_request_variable('current_theme_name', "test-theme")
        >>> get_request_variable('current_theme_name', "default-theme")
        "test-theme"
    """
    request = get_current_request()
    if not request:
        raise MiddlewareNotActivated(
            "Unable to get request object. Make sure CurrentRequestMiddleware is installed",
        )

    return getattr(request, key, default)


def set_current_request(request):
    """
    Save request object in the thread data.

    Arguments:
        request (HttpRequest): Django request object.
    """
    return set_thread_variable('request', request)


def get_current_request(default=None):
    """
    Get request object from the thread data associated with the current django request.

    Arguments:
        default (object): Default value to return in case there is no current request being processed.
    """
    return get_thread_variable('request', default)


def set_current_theme(theme):
    """
    Save theme object in the request data.

    Arguments:
        theme (theming.models.Theme): Theme object
    """
    return set_request_variable('theme', theme)


def get_current_theme(default=None):
    """
    Get theme object from the thread data associated with the current django request.

    Arguments:
        default (object):  Default value to return in case there is no current request being processed.
    """
    return get_request_variable('theme', default)
