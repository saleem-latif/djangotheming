# -*- coding: utf-8 -*-
"""
Thread scoped variables.
"""

from threading import local
from theming.exceptions import MiddlewareNotActivatedError
__thread_locals__ = local()


def set_thread_variable(key, val):
    setattr(__thread_locals__, key, val)


def get_thread_variable(key, default=None):
    return getattr(__thread_locals__, key, default)


def set_request_variable(key, value):
    request = get_current_request()
    if not request:
        raise MiddlewareNotActivatedError(
            "Unable to get request object. Make sure CurrentRequestMiddleware is installed",
        )

    return setattr(request, key, value)


def get_request_variable(key, default=None):
    request = get_current_request()
    if not request:
        raise MiddlewareNotActivatedError(
            "Unable to get request object. Make sure CurrentRequestMiddleware is installed",
        )

    return getattr(request, key, default)


def set_current_request(request):
    return set_thread_variable('request', request)


def get_current_request(default=None):
    return get_thread_variable('request', default)


def set_current_theme(theme):
    return set_request_variable('theme', theme)


def get_current_theme(default=None):
    return get_request_variable('theme', default)
