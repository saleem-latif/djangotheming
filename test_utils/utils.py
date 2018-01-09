"""
Utility functions for theming tests.
"""
from django.test import RequestFactory
from theming.thread_locals import get_current_request, set_current_request, set_current_theme


def setup_current_theme(theme, request=None):
    """
    Setup current theme and request.

    Arguments:
        theme (Theme): Theme instance to set.
        request (HttpRequest): Django request object for the current request.
    """
    request = request or get_current_request() or RequestFactory().get('/')
    set_current_request(request)
    set_current_theme(theme)
