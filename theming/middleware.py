"""
Middleware for theming app

Note:
    This middleware depends on "django_sites_extensions.middleware.CurrentSiteWithDefaultMiddleware" middleware
    So it must be added after this middleware in django settings files.
"""

from django.utils.deprecation import MiddlewareMixin

from theming.models import Theme
from theming.thread_locals import set_current_request, set_current_theme


class CurrentRequestMiddleware(MiddlewareMixin):
    """
    Middleware that sets `request` attribute in the local threading storage.
    """

    def process_request(self, request):
        set_current_request(request)


class CurrentThemeMiddleware(MiddlewareMixin):
    """
    Middleware that sets `theme` attribute to request object.
    """

    def process_request(self, request):
        set_current_theme(Theme.get_theme(request.site))
