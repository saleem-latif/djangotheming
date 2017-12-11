"""
App Config for theming.
"""

from django.apps import AppConfig


class ThemingConfig(AppConfig):
    """
    Basic config class for theming app.
    """
    name = 'theming'

    def ready(self):
        # TODO: Add all theme validations here.
        pass
