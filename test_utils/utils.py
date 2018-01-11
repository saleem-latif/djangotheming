"""
Utility functions for theming tests.
"""
from django.test import RequestFactory

from theming.thread_locals import get_current_request, set_current_request, set_current_theme


def setup_current_theme(theme, request=None):
    """
    Set current theme and request in thread locals.

    Arguments:
        theme (Theme): Theme instance to set.
        request (HttpRequest): Django request object for the current request.
    """
    request = request or get_current_request() or RequestFactory().get('/')
    set_current_request(request)
    set_current_theme(theme)


def cleanup_current_request_and_theme():  # pylint: disable=invalid-name
    """
    Remove current request and current theme.
    """
    set_current_request(request=None)
