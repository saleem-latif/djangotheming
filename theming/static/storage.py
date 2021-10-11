"""
Theming support for Django's collectstatic functionality.
See https://docs.djangoproject.com/en/1.8/ref/contrib/staticfiles/
"""
from __future__ import absolute_import

import os.path

from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.utils._os import safe_join

import theming
from theming.thread_locals import get_current_theme


class ThemeStorage(StaticFilesStorage):
    """
    Comprehensive theme aware Static files storage.
    """
    # prefix for file path, this prefix is added at the beginning of file path before saving static files during
    # collectstatic command.
    # e.g. having "test-theme" as prefix will cause files to be saved as "test-theme/images/logo.png"
    # instead of "images/logo.png"
    prefix = None

    def __init__(self, location=None, base_url=None, file_permissions_mode=None,
                 directory_permissions_mode=None, prefix=None):

        self.prefix = prefix

        super().__init__(
            location=location,
            base_url=base_url,
            file_permissions_mode=file_permissions_mode,
            directory_permissions_mode=directory_permissions_mode,
        )

    def url(self, name):
        """
        Returns url of the asset, themed url will be returned if the asset is themed otherwise default
        asset url will be returned.

        Arguments:
            name: name of the asset, e.g. 'images/logo.png'

        Returns:
            url of the asset, e.g. '/static/red-theme/images/logo.png' if current theme is red-theme and logo
            is provided by red-theme otherwise '/static/images/logo.png'
        """
        prefix = ''
        theme = get_current_theme()

        # get theme prefix from site address if if asset is accessed via a url
        if theme:
            prefix = theme.name

        # get theme prefix from storage class, if asset is accessed during collectstatic run
        elif self.prefix:
            prefix = self.prefix

        # join theme prefix with asset name if theme is applied and themed asset exists
        if prefix and self.themed(name, prefix):
            name = os.path.join(prefix, name)

        return super().url(name)

    def themed(self, name, theme_name):
        """
        Returns True if given asset override is provided by the given theme otherwise returns False.

        Arguments:
            name: asset name e.g. 'images/logo.png'
            theme_name: theme name e.g. 'red-theme', 'test-theme'

        Returns:
            True if given asset override is provided by the given theme otherwise returns False
        """
        if not theming.is_enabled():
            return False

        # in debug mode check static asset from within the project directory
        if settings.DEBUG:
            themes_location = theming.get_base_dir(theme_name)
            # Nothing can be themed if we don't have a theme location or required params.
            if not all((themes_location, theme_name, name)):
                return False

            themed_path = "/".join([
                str(themes_location),
                theme_name,
                "static/"
            ])
            name = name[1:] if name.startswith("/") else name
            path = safe_join(themed_path, name)
            return os.path.exists(path)

        # in live mode check static asset in the static files dir defined by "STATIC_ROOT" setting
        return self.exists(os.path.join(theme_name, name))
