"""
Module to contain middleware defined by the theming app.
"""

from django.utils.deprecation import MiddlewareMixin

from theming.models import Theme
from theming.thread_locals import set_current_request, set_current_theme


class CurrentRequestMiddleware(MiddlewareMixin):
    """
    Middleware that sets `request` attribute in the local threading storage.
    """

    def process_request(self, request):  # pylint: disable=no-self-use
        """
        Save request object in local thread data.
        """
        set_current_request(request)


class CurrentThemeMiddleware(MiddlewareMixin):
    """
    Middleware that sets `theme` attribute to request object.

    Dependencies:
        This middleware is dependant on the following middleware,
        middleware must only be added after these two in the `MIDDLEWARE` setting.
            1. (django.contrib.sites.middleware.CurrentSiteMiddleware)
            2. (theming.middleware.CurrentRequestMiddleware)
    """

    def process_request(self, request):  # pylint: disable=no-self-use
        """
        Save theme object in local thread data.
        """
        set_current_theme(Theme.get_theme(request.site))
