"""
Middleware for theming app

Note:
    This middleware depends on "django_sites_extensions.middleware.CurrentSiteWithDefaultMiddleware" middleware
    So it must be added after this middleware in django settings files.
"""

from theming.models import Theme

from theming.thread_locals import set_current_request, set_current_theme
from django.utils.deprecation import MiddlewareMixin


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


# class ThemePreviewMiddleware(object):
#     """
#     Middleware for previewing themes. This middleware should be added after
#     CurrentSiteThemeMiddleware and SessionMiddleware.
#     """
#
#     def process_request(self, request):
#
#         if 'clear-theme' in request.GET and 'preview-theme' in request.session:
#             del request.session['preview-theme']
#
#         preview_theme = request.GET.get('preview-theme') or request.session.get('preview-theme')
#
#         if request.user.is_staff and preview_theme:
#             request.session['preview-theme'] = preview_theme
#
#             request.site_theme = SiteTheme(
#                 site=getattr(request, 'site', None),
#                 theme_dir_name=preview_theme,
#             )
