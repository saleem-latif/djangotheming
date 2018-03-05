"""
Validate ThemingConfig
"""
import ddt
from six import assertRaisesRegex

from django.apps import apps
from django.conf import settings
from django.test import override_settings

from test_utils.testcases import TestCase
from theming.exceptions import ImproperlyConfigured


@ddt.ddt
class ThemingConfigTests(TestCase):
    """
    Validate ThemingConfig.
    """

    def setUp(self):
        """
        Instantiate ThemeConfig instance.
        """
        super(ThemingConfigTests, self).setUp()
        self.theming_config = apps.get_app_config('theming')

    @ddt.data(
        (
            {'THEMING': {}},
            ImproperlyConfigured,
            r'The THEMING\["DIRS"\] setting must be populated.',
        ),
        (
            {'THEMING': {'DIRS': []}},
            ImproperlyConfigured,
            r'The THEMING\["ENABLED"\] setting must be populated.',
        ),
        (
            {'THEMING': {'DIRS': None, 'ENABLED': True}},
            ImproperlyConfigured,
            r'The THEMING\["DIRS"\] setting is not a tuple or list. Perhaps you forgot a trailing comma\?',
        ),
        (
            {'THEMING': {'DIRS': [None], 'ENABLED': True}},
            ImproperlyConfigured,
            r'THEMING\["DIRS"\] must contain only string paths.',
        ),
        (
            {'THEMING': {'DIRS': ['../themes'], 'ENABLED': True}},
            ImproperlyConfigured,
            r'THEMING\["DIRS"\] must contain only absolute paths to themes dirs.',
        ),
        (
            {'THEMING': {'DIRS': ['/invalid/path'], 'ENABLED': True}},
            ImproperlyConfigured,
            r'THEMING\["DIRS"\] must contain valid paths.',
        ),
    )
    @ddt.unpack
    def test_ready(self, settings_override, exception, message_regex):
        """
        Verify ThemingConfig ready works as expected.
        """
        with override_settings(**settings_override):
            with assertRaisesRegex(self, exception, message_regex):
                self.theming_config.ready()

    @override_settings()
    def test_ready_with_missing_theme_settings(self):  # pylint: disable=invalid-name
        """
        Verify that ThemingConfig ready raises ImproperlyConfigured exception if THEMING setting is not set.
        """
        del settings.THEMING
        with assertRaisesRegex(
            self,
            ImproperlyConfigured,
            r'"THEMING" setting not set in django settings file. '
            r'If you are not using theming then remove it from INSTALLED_APPS.'
        ):
            self.theming_config.ready()
