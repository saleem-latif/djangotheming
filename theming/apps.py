"""
App Config for theming.
"""
from __future__ import absolute_import

import os

from django.apps import AppConfig
from django.conf import settings

from theming.exceptions import ImproperlyConfigured


class ThemingConfig(AppConfig):
    """
    Basic config class for theming app.
    """

    name = 'theming'

    def ready(self):
        """
        Perform validations on theme settings.

        settings must contains the `THEMING` setting with the following format.
        ```
            THEMING = {
                'ENABLED': True,  # boolean indicating whether theming feature is enabled of disabled.
                'DIRS': [],  # List of absolute paths (str) to the directories that contain themes.
            }
        ```
        """
        if not hasattr(settings, 'THEMING'):
            raise ImproperlyConfigured(
                '"THEMING" setting not set in django settings file. '
                'If you are not using theming then remove it from INSTALLED_APPS.'
            )
        if 'DIRS' not in settings.THEMING:
            raise ImproperlyConfigured(
                'The THEMING["DIRS"] setting must be populated.',
            )
        if 'ENABLED' not in settings.THEMING:
            raise ImproperlyConfigured(
                'The THEMING["ENABLED"] setting must be populated.',
            )
        if not isinstance(settings.THEMING['DIRS'], (list, tuple)):
            raise ImproperlyConfigured(
                'The THEMING["DIRS"] setting is not a tuple or list. Perhaps you forgot a trailing comma?',
            )
        if not all(isinstance(theme_dir, str) for theme_dir in settings.THEMING['DIRS']):
            raise ImproperlyConfigured(
                'THEMING["DIRS"] must contain only string paths.',
            )
        if not all(theme_dir.startswith("/") for theme_dir in settings.THEMING['DIRS']):
            raise ImproperlyConfigured(
                'THEMING["DIRS"] must contain only absolute paths to themes dirs.',
            )
        if not all(os.path.isdir(theme_dir) for theme_dir in settings.THEMING['DIRS']):
            raise ImproperlyConfigured(
                'THEMING["DIRS"] must contain valid paths.',
            )
